#!/usr/bin/env python3
"""Mechanical enforcement for the Publication Safety department.

Scans every text file in this public repository for violations of the
synthetic-only boundary:

  1. External resource loads in HTML (script/link/img/iframe/media src or href,
     CSS url()/@import to another host) — including tags split across lines,
     unquoted attributes, and protocol-relative //host URLs. Outbound <a href>
     navigation is allowed; outbound *loads* are not — public pages are
     self-contained.
  2. Network APIs in page JavaScript (fetch, XHR, WebSocket, EventSource,
     sendBeacon, service-worker registration).
  3. Credential-shaped strings (cloud keys, tokens, private key blocks).
  4. Private-fabric identifiers (RFC1918 and CGNAT/tailnet addresses,
     cluster-internal hostnames).
  5. Staleness of the generated org chart (delegates to build-org-chart.py --check).
  6. A missing or weak Content-Security-Policy on any HTML page: every page
     declares one in a <meta> tag, starting from default-src 'none', with no
     wildcard, scheme-wide, or remote-host sources and no 'unsafe-eval'.
  7. Email addresses other than documented placeholders.

A blocking finding here is a Publication Safety finding: it is fixed, or the
Operator overrides it in the decision ledger. Exit code is non-zero on findings.

Findings about credentials, addresses, hostnames and emails never echo the
matched value: this checker also runs in CI on a public repository, where logs
are public, so a gate that prints what it caught would publish it. Those
findings report the location, the length and a short digest instead. Files are
decoded as UTF-16 when they carry a BOM or look like BOM-less UTF-16, so an
editor or shell that saved in that encoding cannot hide a finding.

Per the negative-controls doctrine, a checker must prove it can fail:

  python3 scripts/check-publication-safety.py --self-test

seeds a known-bad fixture and asserts every category is caught, and that a clean
fixture yields nothing. A scanner that has never caught anything is
indistinguishable from a scanner that cannot.
"""

import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEXT_EXT = {".html", ".js", ".css", ".json", ".md", ".webmanifest", ".svg",
            ".py", ".yml", ".yaml", ".txt", ".xml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

# --- rule sets -------------------------------------------------------------

# 1. External resource loads (HTML only). href counts only on <link>. Matched
#    against the whole file, not per line: a tag broken across lines, an
#    unquoted attribute, or a protocol-relative //host URL is the same load.
#    ([^>] spans newlines, so a multi-line tag cannot hide its src.)
RE_EXT_SRC = re.compile(
    r"<(script|img|iframe|video|audio|source|embed|object)\b[^>]*?"
    r"\bsrc\s*=\s*[\"']?\s*(?:https?:)?//", re.I)
RE_EXT_LINK = re.compile(r"<link\b[^>]*?\bhref\s*=\s*[\"']?\s*(?:https?:)?//", re.I)
RE_CSS_URL = re.compile(r"(@import\s+[\"'(]|url\(\s*[\"']?)\s*(?:https?:)?//", re.I)

# 2. Network APIs (HTML + JS).
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
    ("LLM provider API key", re.compile(r"\bsk-" + r"(?:proj-|ant-)?[A-Za-z0-9_-]{20,}")),
    ("Telegram bot token", re.compile(r"\b\d{8,10}:" + r"AA[A-Za-z0-9_-]{33}")),
    ("Discord bot token", re.compile(r"\b[MNO][A-Za-z\d]{23,25}\." + r"[\w-]{6}\.[\w-]{27,38}")),
    ("JSON Web Token", re.compile("eyJ" + r"[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("Tailscale key", re.compile("tskey-" + r"[A-Za-z0-9-]{16,}")),
    ("Bearer token literal", re.compile(r"\bBearer\s+" + r"[A-Za-z0-9._~+/=-]{20,}")),
]

# 4. Private-fabric identifiers (all text files): RFC1918 plus the CGNAT block
#    (100.64/10), which mesh/tailnet peers use — every bit as identifying.
RE_PRIVATE_IP = re.compile(
    r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01])"
    r"|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))" + r"\.\d{1,3}\.\d{1,3}\b")
RE_CLUSTER_HOST = re.compile(r"[a-z0-9.-]+\.svc\.cluster" + r"\.local\b", re.I)

# 6. Content-Security-Policy (HTML only). A self-contained static page needs no
#    remote source of any kind, so the policy must start from default-src 'none'
#    and must not re-open the network anywhere else in the policy.
RE_CSP_META = re.compile(
    r"<meta\b[^>]*?\bhttp-equiv\s*=\s*[\"']?Content-Security-Policy[\"']?[^>]*>", re.I)
RE_CSP_CONTENT = re.compile(r"\bcontent\s*=\s*\"([^\"]*)\"", re.I)
RE_CSP_DEFAULT_NONE = re.compile(r"(?:^|;)\s*default-src\s+'none'\s*(?:;|$)", re.I)
RE_CSP_CONNECT = re.compile(r"(?:^|;)\s*connect-src\s+([^;]*)", re.I)


def csp_problem(policy: str):
    """Return why a CSP is too weak for a self-contained page, or None if it is fine."""
    if not RE_CSP_DEFAULT_NONE.search(policy):
        return "policy does not start from default-src 'none'"
    for token in re.split(r"[\s;]+", policy):
        low = token.lower()
        if low in {"*", "http:", "https:", "ws:", "wss:", "'unsafe-eval'"}:
            return f"policy allows {low}"
        if "://" in low or low.startswith("*."):
            return "policy allows a remote host source"
    connect = RE_CSP_CONNECT.search(policy)
    if connect and connect.group(1).strip().lower() != "'none'":
        return "connect-src is not 'none'"
    return None


# 7. Email addresses (all text files). Personal contact details do not belong
#    on a public surface; documentation placeholders and no-reply addresses do.
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
RE_EMAIL_ALLOWED = re.compile(
    r"@(?:[a-z0-9-]+\.)*example\.(?:com|org|net)$|@users\.noreply\.github\.com$"
    r"|^noreply@|^no-reply@", re.I)


def redact(value: str) -> str:
    """Describe a sensitive match without reproducing it."""
    digest = hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()[:12]
    return f"<redacted: {len(value)} chars, sha256:{digest}>"


def read_text(path: Path) -> str:
    """Decode a file for scanning; UTF-16 must not make content invisible."""
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    sample = raw[:4096]
    if len(sample) >= 4 and sample.count(b"\x00") * 4 > len(sample):
        encoding = "utf-16-be" if sample[0] == 0 else "utf-16-le"
        return raw.decode(encoding, errors="replace")
    return raw.decode("utf-8", errors="replace")


def iter_files(base: Path):
    for path in sorted(base.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXT:
            yield path


def scan_tree(base: Path) -> list:
    findings = []

    def hit(path, lineno, category, snippet):
        findings.append((path.relative_to(base), lineno, category, snippet.strip()[:120]))

    for path in iter_files(base):
        text = read_text(path)
        suffix = path.suffix.lower()
        is_html = suffix == ".html"
        is_js = suffix == ".js"
        is_css = suffix in {".css", ".html"}

        def line_of(pos):
            return text.count("\n", 0, pos) + 1

        def snippet_at(pos):
            start = text.rfind("\n", 0, pos) + 1
            end = text.find("\n", pos)
            return text[start:end if end != -1 else len(text)]

        # Whole-text rules: a tag split across lines is still one tag, so these
        # must never be evadable by a line break.
        whole_rules = []
        if is_html:
            whole_rules += [(RE_EXT_SRC, "external resource load"),
                            (RE_EXT_LINK, "external <link> load")]
        if is_css:
            whole_rules.append((RE_CSS_URL, "external CSS load"))
        if is_html or is_js:
            whole_rules.append((RE_NET, "network API in page code"))
        for pattern, category in whole_rules:
            for m in pattern.finditer(text):
                hit(path, line_of(m.start()), category, snippet_at(m.start()))

        if is_html:
            meta = RE_CSP_META.search(text)
            if not meta:
                hit(path, 1, "missing Content-Security-Policy",
                    "no <meta http-equiv=\"Content-Security-Policy\"> on this page")
            else:
                content = RE_CSP_CONTENT.search(meta.group(0))
                problem = csp_problem(content.group(1)) if content else \
                    "policy has no double-quoted content attribute"
                if problem:
                    hit(path, line_of(meta.start()), "weak Content-Security-Policy", problem)

        # Line-shaped rules (tokens and addresses never span lines). The matched
        # value is never echoed: see redact().
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pattern in SECRET_PATTERNS:
                m = pattern.search(line)
                if m:
                    hit(path, lineno, f"credential shape: {label}", redact(m.group(0)))
            m = RE_PRIVATE_IP.search(line)
            if m:
                hit(path, lineno, "private address", redact(m.group(0)))
            m = RE_CLUSTER_HOST.search(line)
            if m:
                hit(path, lineno, "cluster-internal hostname", redact(m.group(0)))
            for m in RE_EMAIL.finditer(line):
                if not RE_EMAIL_ALLOWED.search(m.group(0)):
                    hit(path, lineno, "email address", redact(m.group(0)))
    return findings


def check_chart_freshness() -> list:
    """The generated org chart is a public claim; a stale one is a false claim."""
    script = ROOT / "scripts" / "build-org-chart.py"
    if not script.is_file():
        return []
    proc = subprocess.run([sys.executable, str(script), "--check"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip().splitlines()
        return [(Path("org/index.html"), 0, "stale generated page",
                 detail[-1] if detail else "build-org-chart.py --check failed")]
    return []


def self_test() -> int:
    """Seed a known-bad fixture and prove every rule fires; prove clean stays clean."""
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        bad_lines = [
            "<html><head>",
            '<link rel="stylesheet" href="https://cdn.example.com/style.css">',
            "<style>body{background:url(https://cdn.example.com/bg.png)}</style>",
            '</head><body><script src="https://evil.example/x.js"></script>',
            "<script>fetch('/api/telemetry');</script>",
            "key = '" + "AKIA" + "B" * 16 + "'",
            "token = '" + "ghp_" + "a" * 36 + "'",
            "host = '" + "192.168." + "7.42" + "'",
            "peer = '" + "100.64." + "23.7" + "'",
            "svc = 'qdrant.default" + ".svc.cluster" + ".local'",
            "llm = '" + "sk-" + "proj-" + "c" * 24 + "'",
            "bot = '" + "123456789:" + "AA" + "d" * 33 + "'",
            "chat = '" + "M" + "e" * 24 + "." + "f" * 6 + "." + "g" * 30 + "'",
            "jwt = '" + "eyJ" + "h" * 12 + "." + "eyJ" + "i" * 12 + "." + "j" * 8 + "'",
            "mesh = '" + "tskey-" + "auth-" + "k" * 16 + "'",
            "auth = '" + "Bearer " + "m" * 24 + "'",
            "mail = '" + "someone.real" + "@" + "corp-mail.test" + "'",
            "</body></html>",
        ]
        (base / "bad.html").write_text("\n".join(bad_lines), encoding="utf-8")
        # Every sensitive value seeded above, so the test can prove that no
        # finding echoes one back (CI logs on a public repository are public).
        seeded_sensitive = [
            "AKIA" + "B" * 16, "ghp_" + "a" * 36, "192.168." + "7.42", "100.64." + "23.7",
            "qdrant.default" + ".svc.cluster" + ".local", "sk-" + "proj-" + "c" * 24,
            "123456789:" + "AA" + "d" * 33, "eyJ" + "h" * 12, "tskey-" + "auth-" + "k" * 16,
            "Bearer " + "m" * 24, "someone.real" + "@" + "corp-mail.test",
            "172.16." + "9.9",
        ]
        # Evasions a line-by-line scanner provably missed: a tag broken across
        # lines, an unquoted attribute, a protocol-relative URL.
        evasion_lines = [
            "<html><head>",
            "<link rel=stylesheet",
            "      href=https://cdn.example.com/a.css>",
            "<style>body{background:url('//cdn.example.com/bg.png')}</style>",
            "</head><body>",
            "<script",
            '  src="//evil.example/x.js"></script>',
            "</body></html>",
        ]
        (base / "bad2.html").write_text("\n".join(evasion_lines), encoding="utf-8")
        # Weak policies: each one re-opens what default-src 'none' closes.
        strict = "default-src 'none'; style-src 'unsafe-inline'"
        weak_policies = {
            "weak-default.html": "default-src 'self'; style-src 'unsafe-inline'",
            "weak-wildcard.html": strict + "; img-src *",
            "weak-scheme.html": strict + "; script-src https:",
            "weak-host.html": strict + "; script-src https://cdn.example.com",
            "weak-eval.html": strict + "; script-src 'unsafe-inline' 'unsafe-eval'",
            "weak-connect.html": strict + "; connect-src 'self'",
        }
        for name, policy in weak_policies.items():
            (base / name).write_text(
                '<html><head><meta http-equiv="Content-Security-Policy" '
                f'content="{policy}"></head><body>x</body></html>', encoding="utf-8")
        # A UTF-16 file must be decoded, not skipped: with a BOM and without one.
        utf16_line = "host = '" + "172.16." + "9.9" + "'\n"
        (base / "bad16-bom.txt").write_bytes(utf16_line.encode("utf-16"))
        (base / "bad16-nobom.txt").write_bytes(utf16_line.encode("utf-16-le"))
        (base / "clean.html").write_text(
            '<html><head><meta http-equiv="Content-Security-Policy" '
            "content=\"default-src 'none'; style-src 'unsafe-inline'; "
            "base-uri 'none'; form-action 'none'\">"
            "<style>body{color:#111}</style></head>"
            '<body><a href="https://example.org">a navigation link is fine</a>'
            "<p>Write to user@example.com or noreply@anthropic.com; the task-list "
            "desk-reference and risk-adjusted-return-on-investment are just words."
            "</p></body></html>", encoding="utf-8")

        findings = scan_tree(base)
        cats = {c for (_, _, c, _) in findings}
        expected = {"external resource load", "external <link> load",
                    "external CSS load", "network API in page code",
                    "credential shape: AWS access key",
                    "credential shape: GitHub token",
                    "credential shape: LLM provider API key",
                    "credential shape: Telegram bot token",
                    "credential shape: Discord bot token",
                    "credential shape: JSON Web Token",
                    "credential shape: Tailscale key",
                    "credential shape: Bearer token literal",
                    "private address", "cluster-internal hostname",
                    "missing Content-Security-Policy",
                    "weak Content-Security-Policy", "email address"}
        missed = expected - cats
        clean_hits = [f for f in findings if str(f[0]) == "clean.html"]
        if missed:
            print(f"[self-test] FAIL — rules did not fire: {sorted(missed)}")
            return 1
        private_hits = sum(1 for (_, _, c, _) in findings if c == "private address")
        if private_hits < 2:
            print("[self-test] FAIL — private-address rule missed a range "
                  f"(caught {private_hits} of 2: RFC1918 + CGNAT)")
            return 1
        evasion_cats = {c for (p, _, c, _) in findings if str(p) == "bad2.html"}
        evasion_expected = {"external resource load", "external <link> load",
                            "external CSS load"}
        evasion_missed = evasion_expected - evasion_cats
        if evasion_missed:
            print("[self-test] FAIL — evasion fixture (multi-line / unquoted / "
                  f"protocol-relative) slipped past: {sorted(evasion_missed)}")
            return 1
        if clean_hits:
            print(f"[self-test] FAIL — clean fixture drew findings: {clean_hits}")
            return 1
        weak_missed = sorted(
            name for name in weak_policies
            if not any(str(p) == name and c == "weak Content-Security-Policy"
                       for (p, _, c, _) in findings))
        if weak_missed:
            print(f"[self-test] FAIL — weak CSP fixtures passed as strong: {weak_missed}")
            return 1
        utf16_missed = sorted(
            name for name in ("bad16-bom.txt", "bad16-nobom.txt")
            if not any(str(p) == name and c == "private address"
                       for (p, _, c, _) in findings))
        if utf16_missed:
            print(f"[self-test] FAIL — UTF-16 content was not scanned: {utf16_missed}")
            return 1
        echoed = sorted({value[:6] + "…" for value in seeded_sensitive
                         for (_, _, _, snippet) in findings if value in snippet})
        if echoed:
            print("[self-test] FAIL — a finding echoed the sensitive value it caught "
                  f"(prefixes: {echoed})")
            return 1
        print(f"[self-test] PASS — {len(findings)} findings on the bad fixture, "
              "0 on the clean one. The checker can fail, so its passes mean something.")
        return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    findings = scan_tree(ROOT)
    if "--no-chart" not in sys.argv:
        findings += check_chart_freshness()
    if findings:
        print(f"[publication-safety] {len(findings)} finding(s):\n")
        for path, lineno, category, line in findings:
            where = f"{path}:{lineno}" if lineno else str(path)
            print(f"  BLOCKING  {where}  [{category}]\n            {line}")
        print("\nFix the findings, or record an Operator override in the decision ledger.")
        return 1
    print("[publication-safety] clean — no external loads, network APIs, "
          "credential shapes, private identifiers, or email addresses; every page "
          "carries a strict CSP; generated pages current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
