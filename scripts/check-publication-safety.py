#!/usr/bin/env python3
"""Mechanical enforcement for the Publication Safety department.

Scans every text file in this public repository for violations of the
synthetic-only boundary:

  1. External resource loads in HTML (script/link/img/iframe/media src, srcset
     or poster, CSS url()/@import to another host) — including tags split
     across lines, unquoted attributes, and protocol-relative //host URLs.
     Outbound <a href> navigation is allowed; outbound *loads* are not — public
     pages are self-contained.
  2. Network APIs in page JavaScript (fetch, XHR, WebSocket, EventSource,
     sendBeacon, service-worker registration).
  3. Credential-shaped strings (cloud keys, tokens, private key blocks).
  4. Private-fabric identifiers (RFC1918 and CGNAT/tailnet addresses,
     cluster-internal hostnames).
  5. Staleness of the generated org chart (delegates to build-org-chart.py --check).
  6. A page (.html, .htm, .xhtml) without a Content-Security-Policy that a
     browser will actually enforce, or with one that re-opens anything. The
     policy must be a <meta http-equiv="Content-Security-Policy"> in <head>,
     ahead of any script, style, link or base element, and must start from
     default-src 'none'. Sources are limited to 'none', 'self', 'unsafe-inline',
     'unsafe-hashes', hashes and nonces, plus data: for images, fonts and
     media: no host, no other scheme, no 'unsafe-eval', 'wasm-unsafe-eval' or
     'strict-dynamic', and connect-src stays 'none'.
  7. Email addresses other than documented placeholders — also when written
     with HTML character references or percent-encoded in a mailto: link.

A blocking finding here is a Publication Safety finding: it is fixed, or the
Operator overrides it in the decision ledger. Exit code is non-zero on findings.

Findings never reproduce what they caught. This checker runs in CI on a public
repository, where logs are public, so a gate that printed its matches would
publish them. A finding names the file, line, column, category and match
length, which is enough to find it locally, and never the matched text, a
digest of it, or the source line around it: a digest of a low-entropy value
such as a private address can be reversed by brute force in seconds.

Every file is scanned in several decodings, so that how it was saved does not
decide what the gate can see: UTF-8; UTF-16 or UTF-32 when a byte-order mark
or the NUL pattern says so; the bytes with NULs removed, which makes ASCII
text inside UTF-16 or UTF-32 of either byte order readable even in mixed or
padded files; and, for pages, the text with character references decoded.
Text that is non-ASCII and encoded in an unmarked UTF-16 can still escape the
credential and address rules, which only look for ASCII shapes anyway.

Per the negative-controls doctrine, a checker must prove it can fail:

  python3 scripts/check-publication-safety.py --self-test

seeds known-bad fixtures and asserts every category and every guard is caught,
that clean fixtures yield nothing, that no finding echoes a seeded value, and
that a long line is scanned in linear time. A scanner that has never caught
anything is indistinguishable from a scanner that cannot.
"""

import hashlib
import html
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGE_EXT = {".html", ".htm", ".xhtml"}
SCRIPT_EXT = {".js", ".mjs"}
TEXT_EXT = PAGE_EXT | SCRIPT_EXT | {".css", ".json", ".md", ".webmanifest", ".svg",
                                    ".py", ".yml", ".yaml", ".txt", ".xml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

# --- rule sets -------------------------------------------------------------

# 1. External resource loads (pages only). href counts only on <link>. Matched
#    against the whole text, not per line: a tag broken across lines, an
#    unquoted attribute, or a protocol-relative //host URL is the same load.
#    ([^>] spans newlines, so a multi-line tag cannot hide its src.)
RE_EXT_SRC = re.compile(
    r"<(script|img|iframe|video|audio|source|embed|object|track)\b[^>]*?"
    r"\b(?:src|srcset|poster)\s*=\s*[\"']?\s*(?:https?:)?//", re.I)
RE_EXT_LINK = re.compile(r"<link\b[^>]*?\bhref\s*=\s*[\"']?\s*(?:https?:)?//", re.I)
RE_CSS_URL = re.compile(r"(@import\s+[\"'(]|url\(\s*[\"']?)\s*(?:https?:)?//", re.I)

# 2. Network APIs (pages and scripts).
RE_NET = re.compile(
    r"\bfetch\s*\(|new\s+XMLHttpRequest|new\s+WebSocket|new\s+EventSource"
    r"|\bsendBeacon\b|serviceWorker\s*\.\s*register|\bimportScripts\s*\(")

# 3. Credential shapes (all text files). Built by concatenation so this file's
#    own source can never satisfy its own patterns.
SECRET_PATTERNS = [
    ("AWS access key", re.compile("AKIA" + r"[0-9A-Z]{16}")),
    ("GitHub token", re.compile(r"gh[pousr]_" + r"[A-Za-z0-9]{36}")),
    ("GitHub fine-grained token", re.compile("github_pat_" + r"[A-Za-z0-9_]{22,}")),
    ("Slack token", re.compile(r"xox[abprs]-" + r"[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile("AIza" + r"[0-9A-Za-z_-]{35}")),
    ("GitLab token", re.compile("glpat-" + r"[A-Za-z0-9_-]{20}")),
    ("Private key block", re.compile("-----BEGIN " + r"[A-Z ]*PRIVATE KEY-----")),
    # Provider keys are random, so they contain a digit; CSS classes and slugs
    # that happen to start with "sk-" do not. A key may follow a JSON or JS
    # escape (\n, \r, \t), an underscore or a digit, but not a letter.
    ("LLM provider API key", re.compile(
        r"(?:(?<![A-Za-z])|(?<=\\[nrt]))sk-" + r"(?:proj-|ant-)?(?=[A-Za-z0-9_-]{0,200}\d)[A-Za-z0-9_-]{20,}")),
    # The bot id is digits, so it may directly follow letters, as in the Bot API
    # URL form .../bot<token>/sendMessage.
    ("Telegram bot token", re.compile(r"(?<!\d)\d{8,10}:" + r"AA[A-Za-z0-9_-]{33}")),
    ("Discord bot token", re.compile(r"\b[MNO][A-Za-z\d]{23,25}\." + r"[\w-]{6}\.[\w-]{27,38}")),
    ("JSON Web Token", re.compile("eyJ" + r"[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("Tailscale key", re.compile("tskey-" + r"[A-Za-z0-9-]{16,}")),
    # A real token is random, so it holds at least one character that
    # lower-case hyphenated prose after the word "Bearer" never does.
    ("Bearer token literal", re.compile(
        r"(?i:\bbearer)(?:[ \t]+|[ \t]*[:=][ \t]*)" + r"(?=[a-z-]{0,200}[A-Z0-9._~+/=])[A-Za-z0-9._~+/=-]{20,}")),
]

# 4. Private-fabric identifiers (all text files): RFC1918 plus the CGNAT block
#    (100.64/10), which mesh/tailnet peers use — every bit as identifying.
RE_PRIVATE_IP = re.compile(
    r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01])"
    r"|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))" + r"\.\d{1,3}\.\d{1,3}\b")
# Bounded, and only tried when the suffix is present, so a long run of
# hostname characters cannot make the scan quadratic.
RE_CLUSTER_HINT = re.compile(r"\.svc\.cluster" + r"\.local", re.I)
RE_CLUSTER_HOST = re.compile(r"[a-z0-9.-]{1,253}\.svc\.cluster" + r"\.local\b", re.I)

# 7. Email addresses (all text files). Every quantifier is bounded so a long
#    line is scanned in linear time.
RE_EMAIL = re.compile(
    r"[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63}){0,8}"
    r"\.[A-Za-z]{2,24}(?![A-Za-z0-9-])")
# Documentation placeholders, no-reply senders, and the SSH user of public
# forges (git@github.com:owner/repo.git) are not personal addresses.
RE_EMAIL_PLACEHOLDER = re.compile(
    r"@(?:[a-z0-9-]+\.)*example\.(?:com|org|net)$|@users\.noreply\.github\.com$"
    r"|^no-?reply@|^git@(?:github\.com|gitlab\.com|bitbucket\.org|codeberg\.org)$", re.I)
# An asset name with a density suffix (hero@2x.png) is not an address either:
# its last label is a file extension that is not a top-level domain.
ASSET_SUFFIXES = {"png", "jpg", "jpeg", "gif", "svg", "webp", "avif", "ico", "bmp",
                  "css", "js", "mjs", "woff", "woff2", "ttf", "otf"}
RE_MAILTO = re.compile(r"mailto:([^\s\"'<>]{1,320})", re.I)


def is_placeholder_email(address: str) -> bool:
    if RE_EMAIL_PLACEHOLDER.search(address):
        return True
    return address.rsplit(".", 1)[-1].lower() in ASSET_SUFFIXES


# 6. Content-Security-Policy (pages only).
FETCH_DIRECTIVES = {
    "default-src", "script-src", "script-src-elem", "script-src-attr", "style-src",
    "style-src-elem", "style-src-attr", "img-src", "font-src", "media-src",
    "object-src", "frame-src", "child-src", "worker-src", "manifest-src",
    "connect-src", "prefetch-src"}
OTHER_SOURCE_DIRECTIVES = {"base-uri", "form-action"}
VALUELESS_DIRECTIVES = {"upgrade-insecure-requests", "block-all-mixed-content"}
DATA_SCHEME_DIRECTIVES = {"img-src", "font-src", "media-src"}
SAFE_KEYWORDS = {"'none'", "'self'", "'unsafe-inline'", "'unsafe-hashes'"}
RE_HASH_OR_NONCE = re.compile(
    r"^'(?:sha256|sha384|sha512|nonce)-[A-Za-z0-9+/_-]+={0,2}'$", re.I)
RE_ASCII_WS = re.compile(r"[\t\n\f\r ]+")
ASCII_WS = "\t\n\f\r "


def parse_policy(serialized: str):
    """Parse a policy the way CSP3 does: split on ';', ASCII whitespace only,
    drop non-ASCII directives, keep the first directive of each name."""
    directives, repeated = {}, False
    for token in serialized.split(";"):
        token = token.strip(ASCII_WS)
        if not token or not token.isascii():
            continue
        parts = RE_ASCII_WS.split(token)
        name = parts[0].lower()
        if name in directives:
            repeated = True
            continue
        directives[name] = parts[1:]
    return directives, repeated


def policy_problem(serialized: str):
    """Return why a policy is too weak for a self-contained page, or None.

    Every reason is a fixed string or names a directive from the allow-list:
    nothing from the page itself is ever printed."""
    directives, repeated = parse_policy(serialized)
    if repeated:
        return "a directive is repeated; browsers ignore the repeat"
    if [v.lower() for v in directives.get("default-src", [])] != ["'none'"]:
        return "default-src is not exactly 'none'"
    for name, values in directives.items():
        if name in VALUELESS_DIRECTIVES:
            continue  # browsers ignore any value these carry
        if name not in FETCH_DIRECTIVES and name not in OTHER_SOURCE_DIRECTIVES:
            return "the policy has a directive that is not on the allow-list"
        lowered = [v.lower() for v in values]
        if "'none'" in lowered and len(values) > 1:
            return f"{name} combines 'none' with other sources"
        for value, low in zip(values, lowered):
            if low in SAFE_KEYWORDS or RE_HASH_OR_NONCE.match(value):
                continue
            if low == "data:" and name in DATA_SCHEME_DIRECTIVES:
                continue
            return f"{name} allows a source that is not on the allow-list"
        if name == "connect-src" and lowered != ["'none'"]:
            return "connect-src is not 'none'"
    return None


class _PolicyFinder(HTMLParser):
    """Find the policy <meta> elements a browser would enforce."""

    HEAD_CONTENT = {"html", "head", "meta", "title", "base", "link", "style",
                    "script", "noscript", "template"}
    INERT = {"template", "noscript", "title", "textarea", "iframe", "noembed",
             "noframes", "xmp"}
    GOVERNED = {"script", "style", "link", "base"}
    RAW_TEXT = {"script", "style"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inert = []
        self.raw_text = None
        self.head_open = True
        self.governed_seen = False
        self.policies = []   # (line, col, content or None)
        self.ignored = []    # (line, col, reason)
        self.elements = 0    # start tags seen anywhere

    def _where(self):
        line, offset = self.getpos()
        return line, offset + 1

    def handle_starttag(self, tag, attrs):
        self.elements += 1
        if self.inert:
            if tag in self.INERT:
                self.inert.append(tag)
            return
        if tag not in self.HEAD_CONTENT:
            self.head_open = False
        if tag == "meta":
            first = {}
            for key, value in attrs:
                first.setdefault(key, value)  # browsers keep the first duplicate
            equiv = first.get("http-equiv") or ""
            kind = equiv.lower() if equiv.isascii() else ""
            if kind == "content-security-policy":
                line, col = self._where()
                if not self.head_open:
                    self.ignored.append((line, col, "the policy <meta> is outside <head>; "
                                                    "browsers ignore it"))
                elif self.governed_seen:
                    self.ignored.append((line, col, "the policy <meta> comes after a script, "
                                                    "style, link or base it cannot govern"))
                else:
                    self.policies.append((line, col, first.get("content")))
            elif kind == "content-security-policy-report-only":
                line, col = self._where()
                self.ignored.append((line, col, "a Report-Only policy cannot be delivered "
                                                "by a <meta>; browsers ignore it"))
        if tag in self.GOVERNED:
            self.governed_seen = True
        if tag in self.INERT:
            self.inert.append(tag)
        elif tag in self.RAW_TEXT:
            self.raw_text = tag

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.inert and self.inert[-1] == tag:
            self.inert.pop()
        if self.raw_text == tag:
            self.raw_text = None

    def handle_endtag(self, tag):
        if self.inert:
            if self.inert[-1] == tag:
                self.inert.pop()
            return
        if self.raw_text == tag:
            self.raw_text = None
        if tag == "head":
            self.head_open = False

    def handle_data(self, data):
        # Text that is not whitespace ends <head>, as it does in a browser.
        if not self.inert and self.raw_text is None and data.strip(ASCII_WS):
            self.head_open = False


def page_policy_problem(text: str):
    """(line, col, category, reason) if the page lacks an enforced strict policy."""
    finder = _PolicyFinder()
    try:
        finder.feed(text)
        finder.close()
    except Exception:  # html.parser is lenient; anything it rejects is not a page we vouch for
        return (1, 1, "missing Content-Security-Policy", "the page could not be parsed")
    if not finder.elements:
        # No element at all (a search-engine verification file, say): nothing
        # in it can load or run, so there is nothing for a policy to govern.
        return None
    if not finder.policies:
        if finder.ignored:
            line, col, reason = finder.ignored[0]
            return (line, col, "missing Content-Security-Policy", reason)
        return (1, 1, "missing Content-Security-Policy",
                "no Content-Security-Policy <meta> that a browser would enforce")
    line, col, content = finder.policies[0]
    if content is None:
        return (line, col, "weak Content-Security-Policy", "the policy <meta> has no content")
    problem = policy_problem(content)
    return (line, col, "weak Content-Security-Policy", problem) if problem else None


# --- decoding --------------------------------------------------------------

_BOMS = ((b"\xff\xfe\x00\x00", "utf-32-le"), (b"\x00\x00\xfe\xff", "utf-32-be"),
         (b"\xff\xfe", "utf-16-le"), (b"\xfe\xff", "utf-16-be"), (b"\xef\xbb\xbf", "utf-8"))


def browser_view(raw: bytes) -> str:
    """The text a browser builds from a page served as UTF-8: a byte-order
    mark wins, otherwise UTF-8."""
    for bom, encoding in _BOMS:
        if raw.startswith(bom):
            return raw[len(bom):].decode(encoding, errors="replace")
    return raw.decode("utf-8", errors="replace")


def decode_views(raw: bytes) -> list:
    """Every decoding worth scanning, most faithful first."""
    views = []
    for bom, encoding in _BOMS:
        if raw.startswith(bom):
            views.append(raw[len(bom):].decode(encoding, errors="replace"))
            break
    else:
        sample = raw[:4096]
        if len(sample) >= 4 and sample.count(b"\x00") * 4 > len(sample):
            # ASCII text in UTF-16 has its NUL in the high byte: odd offsets
            # for little-endian, even offsets for big-endian.
            big = sample[0::2].count(0) > sample[1::2].count(0)
            views.append(raw.decode("utf-16-be" if big else "utf-16-le", errors="replace"))
    for extra in (raw.decode("utf-8", errors="replace"),
                  raw.replace(b"\x00", b"").decode("utf-8", errors="replace")
                  if b"\x00" in raw else None):
        if extra is not None and extra not in views:
            views.append(extra)
    return views


def page_view(text: str) -> str:
    """A page as its reader sees it: character references decoded, and the
    address in each mailto: link percent-decoded."""
    decoded = html.unescape(text)
    return RE_MAILTO.sub(lambda m: "mailto:" + urllib.parse.unquote(m.group(1)), decoded)


# --- scanning --------------------------------------------------------------

def iter_files(base: Path):
    for path in sorted(base.rglob("*")):
        if any(part in SKIP_DIRS for part in path.relative_to(base).parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXT:
            yield path


def _load_detail(match) -> str:
    """Describe an external load without repeating its URL."""
    head = match.group(0)
    if head[:1] == "<":
        tag = re.match(r"<([a-zA-Z]+)", head).group(1).lower()
        attr = "href" if tag == "link" else "src"
        return f"<{tag} {attr}=//…>"
    return "@import //…" if head.lstrip()[:1] == "@" else "url(//…)"


def scan_file(path: Path, rel: Path) -> list:
    raw = path.read_bytes()
    suffix = path.suffix.lower()
    is_page = suffix in PAGE_EXT
    is_script = suffix in SCRIPT_EXT
    is_css = suffix == ".css" or is_page

    findings, seen = [], set()

    def add(text, pos, category, detail, value):
        line = text.count("\n", 0, pos) + 1
        col = pos - (text.rfind("\n", 0, pos) + 1) + 1
        key = (category, line, hashlib.sha256(value.encode("utf-8", "replace")).digest())
        if key not in seen:
            seen.add(key)
            findings.append((rel, line, col, category, detail))

    views = decode_views(raw)
    if is_page:
        primary = browser_view(raw)
        problem = page_policy_problem(primary)
        if problem:
            line, col, category, reason = problem
            findings.append((rel, line, col, category, reason))
        reader = page_view(primary)
        if reader not in views:
            views.append(reader)

    for text in views:
        whole_rules = []
        if is_page:
            whole_rules += [(RE_EXT_SRC, "external resource load"),
                            (RE_EXT_LINK, "external <link> load")]
        if is_css:
            whole_rules.append((RE_CSS_URL, "external CSS load"))
        for pattern, category in whole_rules:
            for m in pattern.finditer(text):
                add(text, m.start(), category, _load_detail(m), m.group(0))
        if is_page or is_script:
            for m in RE_NET.finditer(text):
                add(text, m.start(), "network API in page code",
                    RE_ASCII_WS.sub(" ", m.group(0)), m.group(0))

        for label, pattern in SECRET_PATTERNS:
            for m in pattern.finditer(text):
                add(text, m.start(), f"credential shape: {label}", f"len={len(m.group(0))}", m.group(0))
        for m in RE_PRIVATE_IP.finditer(text):
            add(text, m.start(), "private address", f"len={len(m.group(0))}", m.group(0))
        if RE_CLUSTER_HINT.search(text):
            for m in RE_CLUSTER_HOST.finditer(text):
                add(text, m.start(), "cluster-internal hostname", f"len={len(m.group(0))}", m.group(0))
        if "@" in text:
            for m in RE_EMAIL.finditer(text):
                if not is_placeholder_email(m.group(0)):
                    add(text, m.start(), "email address", f"len={len(m.group(0))}", m.group(0))
    return findings


def scan_tree(base: Path) -> list:
    findings = []
    for path in iter_files(base):
        findings += scan_file(path, path.relative_to(base))
    return findings


def format_findings(findings: list) -> str:
    """The only place findings become text. Details are fixed strings or
    lengths, never page content."""
    lines = [f"[publication-safety] {len(findings)} finding(s):", ""]
    for path, line, col, category, detail in findings:
        where = f"{path}:{line}:{col}" if line else str(path)
        lines.append(f"  BLOCKING  {where}  [{category}]  {detail}")
    lines += ["", "Fix the findings, or record an Operator override in the decision ledger."]
    return "\n".join(lines)


def check_chart_freshness() -> list:
    """The generated org chart is a public claim; a stale one is a false claim."""
    script = ROOT / "scripts" / "build-org-chart.py"
    if not script.is_file():
        return []
    proc = subprocess.run([sys.executable, str(script), "--check"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return [(Path("org/index.html"), 0, 0, "stale generated page",
                 "build-org-chart.py --check failed; regenerate org/index.html")]
    return []


# --- self-test ---------------------------------------------------------------

def _csp_page(policy: str, before: str = "", after: str = "", body: str = "x") -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8">{before}'
            f'<meta http-equiv="Content-Security-Policy" content="{policy}">{after}'
            f"<title>t</title></head><body>{body}</body></html>")


STRICT = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"


def self_test() -> int:
    """Seed known-bad fixtures and prove every rule and guard fires; prove the
    clean fixtures stay clean, that nothing seeded is echoed, and that a long
    line is scanned in linear time."""
    failures = []

    def expect(condition, message):
        if not condition:
            failures.append(message)

    # Sensitive values, assembled at run time so this file never contains them.
    ip_rfc = "192.168." + "7.42"
    ip_cgnat = "100.64." + "23.7"
    ip_utf16 = "172.16." + "9.9"
    aws = "AKIA" + "B" * 16
    gh = "ghp_" + "a" * 36
    svc = "qdrantx7.zone9" + ".svc.cluster" + ".local"
    sk_proj = "sk-" + "proj-" + "c3" * 12
    sk_plain = "sk-" + "Q7" * 12
    sk_escaped = "sk-" + "proj-" + "e5" * 12
    tg = "123456789" + ":" + "AA" + "d" * 33
    tg_url = "987654321" + ":" + "AA" + "k" * 33
    discord = "M" + "e" * 24 + "." + "f" * 6 + "." + "g" * 30
    jwt = "eyJ" + "h" * 12 + "." + "eyJ" + "i" * 12 + "." + "j" * 8
    tskey = "tskey-" + "auth-" + "k" * 16
    bearer_token = "m7" * 12
    lower_bearer_token = "n4" * 13
    colon_bearer_token = "p9" * 11
    nodigit_bearer_token = "Qx" * 12
    mail_test = "someone.real" + "@" + "corp-mail.test"
    mail_com = "jane.roe" + "@" + "corp-mail" + ".com"
    mail_entity_local, mail_entity_domain = "pat.doe", "corp-mail" + ".org"
    mail_pct_local, mail_pct_domain = "lee.kim", "corp-mail" + ".net"
    url_key = "AIza" + "S" * 35
    url_ip = "10.20." + "30.40"
    # The cluster suffix is the rule's own marker and appears in its category name,
    # so only the host part of that value counts as secret.
    seeded = [ip_rfc, ip_cgnat, ip_utf16, aws, gh, "qdrantx7.zone9", sk_proj, sk_plain, sk_escaped,
              tg, tg_url, discord, jwt, tskey, bearer_token, lower_bearer_token, colon_bearer_token, nodigit_bearer_token,
              mail_test, mail_com, mail_entity_local + "@" + mail_entity_domain,
              mail_pct_local + "@" + mail_pct_domain, url_key, url_ip]

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)

        def write(name, text, encoding="utf-8"):
            target = base / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(text if isinstance(text, bytes) else text.encode(encoding))

        # Every rule on one page, plus sensitive values on lines that also trip a
        # whole-text rule, so the echo check covers those findings too.
        write("bad.html", "\n".join([
            "<html><head>",
            '<link rel="stylesheet" href="https://cdn.example.com/style.css">',
            "<style>body{background:url(https://cdn.example.com/bg.png)}</style>",
            '</head><body><script src="https://evil.example/x.js"></script>',
            "<script>fetch('/api/telemetry');</script>",
            '<img srcset="//cdn.example.com/a.png 2x">',
            f'<img src="http://{ip_rfc}/cam.jpg">',
            f'<script src="https://maps.example.com/js?key={url_key}"></script>',
            f"<script>fetch('http://{url_ip}/api')</script>",
            f"key = '{aws}'", f"token = '{gh}'", f"peer = '{ip_cgnat}'", f"svc = '{svc}'",
            f"llm = '{sk_proj}'", f"plain = '{sk_plain}'", f"bot = '{tg}'",
            f"chat = '{discord}'", f"jwt = '{jwt}'", f"mesh = '{tskey}'",
            f"auth = 'Bearer {bearer_token}'", f"mail = '{mail_test}'",
            "</body></html>"]))
        # Shapes that word-boundary guards used to miss.
        write("shapes.md", "\n".join([
            f"POST https://api.telegram.org/bot{tg_url}/sendMessage 200 OK",
            '{"stdout": "exported key\\n' + sk_escaped + '"}',
            f"authorization: bearer {lower_bearer_token}",
            '{"Authorization":"Bearer:' + colon_bearer_token + '"}',
            "Authorization: Bearer " + nodigit_bearer_token,
            "key_" + sk_plain + " and 7" + sk_proj,
            f"contact user@example.com or {mail_com} for access"]))
        # Entity-encoded and percent-encoded addresses on a page with a strict policy.
        write("encoded.html", _csp_page(STRICT, body=(
            f'<a href="mailto:{mail_entity_local}&#64;{mail_entity_domain}">mail</a> '
            f'<a href="mailto:{mail_pct_local}%40{mail_pct_domain}">mail</a>')))
        # Evasions a line-by-line scanner provably missed.
        write("bad2.html", "\n".join([
            "<html><head>", "<link rel=stylesheet",
            "      href=https://cdn.example.com/a.css>",
            "<style>body{background:url('//cdn.example.com/bg.png')}</style>",
            "</head><body>", "<script", '  src="//evil.example/x.js"></script>',
            "</body></html>"]))

        # Policies that re-open what default-src 'none' closes.
        weak = {
            "w-default-self": "default-src 'self'; style-src 'unsafe-inline'",
            "w-default-plus": "default-src 'none' 'self'",
            "w-wildcard": STRICT + "; img-src *",
            "w-port-wildcard": STRICT + "; script-src *:*",
            "w-scheme": STRICT + "; script-src https:",
            "w-scheme-upper": STRICT + "; script-src HTTPS:",
            "w-http": STRICT + "; img-src http:",
            "w-ws": STRICT + "; connect-src ws:",
            "w-wss": STRICT + "; connect-src wss:",
            "w-host-scheme": STRICT + "; script-src https://cdn.example.com",
            "w-host-bare": STRICT + "; script-src 'self' cdn.example.com",
            "w-host-port": STRICT + "; img-src tracker.example.net:443",
            "w-subdomains": STRICT + "; img-src *.example.com",
            "w-entity": STRICT + "; script-src &#42;",
            "w-eval": STRICT + "; script-src 'unsafe-inline' 'unsafe-eval'",
            "w-wasm": STRICT + "; script-src 'wasm-unsafe-eval'",
            "w-dynamic": STRICT + "; script-src 'nonce-abc' 'strict-dynamic'",
            "w-data-script": STRICT + "; script-src data:",
            "w-blob": STRICT + "; img-src blob:",
            "w-connect": STRICT + "; connect-src 'self'",
            "w-shadowed": "default-src 'self' cdn.example.net; default-src 'none'",
            "w-nbsp": "default-src\u00a0'none'; style-src 'unsafe-inline'",
            "w-vtab": "default-src\x0b'none'; style-src 'unsafe-inline'",
            "w-repeat": STRICT + "; style-src 'self'",
            "w-none-combined": STRICT + "; img-src 'none' data:",
            "w-unknown": STRICT + "; navigate-to https://x.example",
            "w-form": STRICT.replace("form-action 'none'", "form-action collect.example.net"),
        }
        for name, policy in weak.items():
            write(f"{name}.html", _csp_page(policy))
        write("w-no-content.html", '<html><head><meta http-equiv="Content-Security-Policy">'
                                   "<title>t</title></head><body>x</body></html>")
        # Browsers use the first of two content attributes; a strict decoy after a
        # weak real one must not pass.
        write("w-dup-content.html", "<html><head><meta http-equiv=\"Content-Security-Policy\" "
                                    "content='default-src *' content=\"" + STRICT + "\">"
                                    "<title>t</title></head><body>x</body></html>")

        # Declarations a browser never enforces.
        ignored = {
            "i-report-only.html": _csp_page(STRICT).replace(
                "Content-Security-Policy", "Content-Security-Policy-Report-Only"),
            "i-in-body.html": ("<html><head><title>t</title></head><body>"
                               f'<meta http-equiv="Content-Security-Policy" content="{STRICT}">'
                               "</body></html>"),
            "i-in-comment.html": _csp_page(STRICT).replace('<meta http-equiv', '<!-- <meta http-equiv')
                                                  .replace('none\'">', 'none\'"> -->', 1),
            "i-after-script.html": _csp_page(STRICT, before="<script>var a=1</script>"),
            "i-in-template.html": ("<html><head><template>"
                                   f'<meta http-equiv="Content-Security-Policy" content="{STRICT}">'
                                   "</template><title>t</title></head><body>x</body></html>"),
            "i-look-alike.html": _csp_page(STRICT).replace("http-equiv", "data-http-equiv"),
            "i-after-text.html": ("<html><head>hello"
                                  f'<meta http-equiv="Content-Security-Policy" content="{STRICT}">'
                                  "<title>t</title></head><body>x</body></html>"),
            "i-no-policy.htm": "<html><head><title>t</title></head><body>x</body></html>",
        }
        for name, text in ignored.items():
            write(name, text)

        # Encodings: each one must still reveal the address it hides.
        line16 = f"host = '{ip_utf16}'\n"
        cjk = "\u5730\u5740\u8bb0\u5f55" * 600 + "\n"   # non-ASCII, so no NULs
        write("e-16le-bom.txt", b"\xff\xfe" + line16.encode("utf-16-le"))
        write("e-16be-bom.txt", b"\xfe\xff" + (cjk + line16).encode("utf-16-be"))
        write("e-16le-nobom.txt", line16.encode("utf-16-le"))
        write("e-16be-nobom.txt", line16.encode("utf-16-be"))
        write("e-32le-bom.txt", b"\xff\xfe\x00\x00" + line16.encode("utf-32-le"))
        write("e-mixed.txt", "notes\n".encode("utf-16") + line16.encode("utf-8"))
        write("e-padded.txt", b"log header" + bytes(2000) + line16.encode("utf-8"))
        write("e-appended.txt", ("plain prose line\n" * 300).encode("utf-8") + line16.encode("utf-16-le"))

        # Clean fixtures: none of these may draw a finding.
        write("clean.html", _csp_page(
            STRICT,
            body=('<a href="https://example.org">a navigation link is fine</a>'
                  "<p>Write to user@example.com, no-reply@example.net or noreply@github.com; "
                  "the task-list desk-reference and risk-adjusted-return-on-investment are "
                  'just words.</p><label class="sk-toggleable__label-arrow">x</label>'
                  '<img src="hero@2x.png" alt=""><p>Bearer tokens are described in RFC 6750.</p>'
                  "<p>Send it as a Bearer token-based-authentication header.</p>")))
        write("clean-verification.html", "google-site-verification: " + "google" + "0123abcd.html\n")
        write("clean-comment-first.html", (
            "<html><head><!-- the policy <meta http-equiv=\"Content-Security-Policy\"> follows -->"
            f'<meta http-equiv="Content-Security-Policy" content="{STRICT}"><title>t</title>'
            "</head><body>x</body></html>"))
        write("clean-single-quoted.html", (
            "<html><head><meta http-equiv='Content-Security-Policy' "
            "content=\"default-src 'none'; img-src data:\"><title>t</title></head>"
            "<body>x</body></html>"))
        write("clean-hash.html", _csp_page(
            "default-src 'none'; style-src 'sha256-xWG4J7IID87qWgff5wD106naR0YqLJ/r9AuAL+a26v4='"))
        write("clean-self.html", _csp_page(
            "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'none'; manifest-src 'self'; form-action 'none'; base-uri 'none'",
            after='<link rel="stylesheet" href="./styles.css">'))
        write("clean.md", "Clone with git clone git@github.com:owner/repo.git; mail the "
                          "list at user@users.noreply.github.com. Version 1.2.3.4 is not an address.")
        write("clean.css", ".hero{background-image:url(hero@2x.jpg)}")
        write("git-remote.md", "remote: git@" + "build-box.corp-mail" + ".test:team/repo.git")
        write("lookalike.md", "reach " + "example.user" + "@" + "corp-mail" + ".com today")

        start = time.process_time()
        findings = scan_tree(base)
        elapsed = time.process_time() - start

        def cats(name):
            return {c for (p, _, _, c, _) in findings if str(p) == name}

        expected_bad = {
            "external resource load", "external <link> load", "external CSS load",
            "network API in page code", "private address", "cluster-internal hostname",
            "email address", "credential shape: AWS access key", "credential shape: GitHub token",
            "credential shape: LLM provider API key", "credential shape: Telegram bot token",
            "credential shape: Discord bot token", "credential shape: JSON Web Token",
            "credential shape: Tailscale key", "credential shape: Bearer token literal",
            "missing Content-Security-Policy"}
        expect(not expected_bad - cats("bad.html"),
               f"rules did not fire on bad.html: {sorted(expected_bad - cats('bad.html'))}")
        expect(sum(1 for (p, _, _, c, _) in findings
                   if str(p) == "bad.html" and c == "credential shape: LLM provider API key") >= 2,
               "the provider-key rule missed a key without the proj-/ant- prefix")
        expect(sum(1 for (p, _, _, c, _) in findings
                   if str(p) == "bad.html" and c == "private address") >= 3,
               "the private-address rule missed a range or an address inside a load")
        expect(sum(1 for (p, _, _, c, _) in findings
                   if str(p) == "bad.html" and c == "external resource load") >= 4,
               "an external load (src, srcset, or a load carrying a value) slipped past")
        for category in ("credential shape: Telegram bot token", "credential shape: LLM provider API key",
                         "credential shape: Bearer token literal", "email address"):
            expect(category in cats("shapes.md"), f"shapes.md: [{category}] missed its shape")
        expect(sum(1 for (p, _, _, c, _) in findings
                   if str(p) == "shapes.md" and c == "credential shape: Bearer token literal") >= 3,
               "the colon form, or a token without a digit, slipped past the Bearer rule")
        expect(sum(1 for (p, _, _, c, _) in findings
                   if str(p) == "shapes.md" and c == "credential shape: LLM provider API key") >= 3,
               "a provider key after an underscore or a digit slipped past")
        expect(sum(1 for (p, _, _, c, _) in findings
                   if str(p) == "encoded.html" and c == "email address") >= 2,
               "an entity- or percent-encoded address on a page slipped past")
        expect({"external resource load", "external <link> load", "external CSS load"} <= cats("bad2.html"),
               "a multi-line, unquoted or protocol-relative load slipped past")
        for name in weak:
            expect("weak Content-Security-Policy" in cats(f"{name}.html"),
                   f"{name}: a weak policy passed as strict")
        expect("weak Content-Security-Policy" in cats("w-no-content.html"),
               "a policy <meta> without content passed")
        expect("weak Content-Security-Policy" in cats("w-dup-content.html"),
               "a strict decoy content attribute hid the weak one browsers use")
        expect("email address" in cats("git-remote.md"),
               "an SSH remote on a host that is not a public forge passed as a placeholder")
        expect("email address" in cats("lookalike.md"),
               "an address that merely contains 'example' passed as a placeholder")
        for name in ignored:
            expect("missing Content-Security-Policy" in cats(name),
                   f"{name}: a policy no browser enforces was accepted")
        for name in ("e-16le-bom.txt", "e-16be-bom.txt", "e-16le-nobom.txt", "e-16be-nobom.txt",
                     "e-32le-bom.txt", "e-mixed.txt", "e-padded.txt", "e-appended.txt"):
            expect("private address" in cats(name), f"{name}: encoded content was not scanned")
        for name in ("clean.html", "clean-comment-first.html", "clean-single-quoted.html",
                     "clean-hash.html", "clean-self.html", "clean.md", "clean.css",
                     "clean-verification.html"):
            expect(not cats(name), f"{name}: clean fixture drew {sorted(cats(name))}")

        # Decoding, unit by unit: each branch must produce the exact text.
        probe = "probe " + "172.16." + "0.1\n"
        for raw, label in ((b"\xff\xfe" + probe.encode("utf-16-le"), "UTF-16LE BOM"),
                           (b"\xfe\xff" + probe.encode("utf-16-be"), "UTF-16BE BOM"),
                           (b"\xff\xfe\x00\x00" + probe.encode("utf-32-le"), "UTF-32LE BOM"),
                           (b"\x00\x00\xfe\xff" + probe.encode("utf-32-be"), "UTF-32BE BOM"),
                           (probe.encode("utf-16-le"), "unmarked UTF-16LE"),
                           (probe.encode("utf-16-be"), "unmarked UTF-16BE")):
            expect(decode_views(raw)[0] == probe, f"decode_views: {label} not decoded first")
        expect(browser_view(b"\xef\xbb\xbf" + b"<p>") == "<p>", "browser_view kept a UTF-8 BOM")

        # Nothing printed may contain six or more characters of a seeded value.
        report = format_findings(findings)
        leaked = sorted({v[:4] + "…" for v in seeded for i in range(len(v) - 5)
                         if v[i:i + 6] in report})
        expect(not leaked, f"the report echoed part of a seeded value (prefixes: {leaked})")

        # Long lines must be linear: a 200 KB percent-encoded run and a 200 KB
        # hostname-character run, the shapes that made earlier patterns quadratic.
        # An at-sign and the cluster suffix are present, so both bounded patterns
        # really run over the long runs.
        write("long/a.css", ".i{background:url(\"data:image/svg+xml," + "%2B" * 70000 + "@x\")}")
        write("long/b.txt", "a1b2c3d4" * 25000 + "\nnode-x" + ".svc.cluster" + ".local\n")
        start = time.process_time()
        long_findings = scan_tree(base / "long")
        long_elapsed = time.process_time() - start
        expect([c for (_, _, _, c, _) in long_findings] == ["cluster-internal hostname"],
               f"long-line fixtures drew {[c for (_, _, _, c, _) in long_findings]}, "
               "expected one cluster-internal hostname")
        expect(long_elapsed < 5.0, f"long lines took {long_elapsed:.1f}s of CPU; a pattern is not linear")

    if failures:
        for message in failures:
            print(f"[self-test] FAIL — {message}")
        return 1
    print(f"[self-test] PASS — {len(findings)} findings on the bad fixtures, 0 on the clean ones, "
          f"nothing echoed, long lines linear ({elapsed:.2f}s + {long_elapsed:.2f}s CPU). "
          "The checker can fail, so its passes mean something.")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    findings = scan_tree(ROOT)
    if "--no-chart" not in sys.argv:
        findings += check_chart_freshness()
    if findings:
        print(format_findings(findings))
        return 1
    print("[publication-safety] clean — no external loads, network APIs, credential "
          "shapes, private identifiers, or email addresses; every page carries an "
          "enforced strict CSP; generated pages current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
