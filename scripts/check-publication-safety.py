#!/usr/bin/env python3
"""Mechanical enforcement for the Publication Safety department.

Scans every text file in this public repository for violations of the
synthetic-only boundary:

  1. External resource loads in HTML (script/link/img/iframe/media src or href,
     CSS url()/@import to another host). Outbound <a href> navigation is allowed;
     outbound *loads* are not — public pages are self-contained.
  2. Network APIs in page JavaScript (fetch, XHR, WebSocket, EventSource,
     sendBeacon, service-worker registration).
  3. Credential-shaped strings (cloud keys, tokens, private key blocks).
  4. Private-fabric identifiers (RFC1918 addresses, cluster-internal hostnames).
  5. Staleness of the generated org chart (delegates to build-org-chart.py --check).

A blocking finding here is a Publication Safety finding: it is fixed, or the
Operator overrides it in the decision ledger. Exit code is non-zero on findings.

Per the negative-controls doctrine, a checker must prove it can fail:

  python3 scripts/check-publication-safety.py --self-test

seeds a known-bad fixture and asserts every category is caught, and that a clean
fixture yields nothing. A scanner that has never caught anything is
indistinguishable from a scanner that cannot.
"""

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

# 1. External resource loads (HTML only). href counts only on <link>.
RE_EXT_SRC = re.compile(r"<(script|img|iframe|video|audio|source|embed|object)\b[^>]*\bsrc\s*=\s*[\"']https?://", re.I)
RE_EXT_LINK = re.compile(r"<link\b[^>]*\bhref\s*=\s*[\"']https?://", re.I)
RE_CSS_URL = re.compile(r"(@import\s+[\"'(]|url\(\s*[\"']?)\s*https?://", re.I)

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
]

# 4. Private-fabric identifiers (all text files).
RE_RFC1918 = re.compile(
    r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))" + r"\.\d{1,3}\.\d{1,3}\b")
RE_CLUSTER_HOST = re.compile(r"[a-z0-9.-]+\.svc\.cluster" + r"\.local\b", re.I)


def iter_files(base: Path):
    for path in sorted(base.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXT:
            yield path


def scan_tree(base: Path) -> list:
    findings = []

    def hit(path, lineno, category, line):
        findings.append((path.relative_to(base), lineno, category, line.strip()[:120]))

    for path in iter_files(base):
        text = path.read_text(encoding="utf-8", errors="replace")
        is_html = path.suffix.lower() == ".html"
        is_js = path.suffix.lower() == ".js"
        is_css = path.suffix.lower() in {".css", ".html"}
        for lineno, line in enumerate(text.splitlines(), 1):
            if is_html:
                if RE_EXT_SRC.search(line):
                    hit(path, lineno, "external resource load", line)
                if RE_EXT_LINK.search(line):
                    hit(path, lineno, "external <link> load", line)
            if is_css and RE_CSS_URL.search(line):
                hit(path, lineno, "external CSS load", line)
            if (is_html or is_js) and RE_NET.search(line):
                hit(path, lineno, "network API in page code", line)
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    hit(path, lineno, f"credential shape: {label}", line)
            if RE_RFC1918.search(line):
                hit(path, lineno, "private address", line)
            if RE_CLUSTER_HOST.search(line):
                hit(path, lineno, "cluster-internal hostname", line)
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
            "svc = 'qdrant.default" + ".svc.cluster" + ".local'",
            "</body></html>",
        ]
        (base / "bad.html").write_text("\n".join(bad_lines), encoding="utf-8")
        (base / "clean.html").write_text(
            "<html><head><style>body{color:#111}</style></head>"
            '<body><a href="https://example.org">a navigation link is fine</a>'
            "</body></html>", encoding="utf-8")

        findings = scan_tree(base)
        cats = {c for (_, _, c, _) in findings}
        expected = {"external resource load", "external <link> load",
                    "external CSS load", "network API in page code",
                    "credential shape: AWS access key",
                    "credential shape: GitHub token",
                    "private address", "cluster-internal hostname"}
        missed = expected - cats
        clean_hits = [f for f in findings if str(f[0]) == "clean.html"]
        if missed:
            print(f"[self-test] FAIL — rules did not fire: {sorted(missed)}")
            return 1
        if clean_hits:
            print(f"[self-test] FAIL — clean fixture drew findings: {clean_hits}")
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
          "credential shapes, or private identifiers; generated pages current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
