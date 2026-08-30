#!/usr/bin/env python3
"""Generate org/index.html — the Asgardr operations org chart — from the repository tree.

Reads departments/org-manifest.json plus every departments/*/skills/*/SKILL.md
frontmatter, and emits a single self-contained static page. No external resources,
no network calls, no state: the page is derived entirely from the repo tree, which
is what makes it publishable under the synthetic-only boundary.

Usage:
  python3 scripts/build-org-chart.py            # (re)generate org/index.html
  python3 scripts/build-org-chart.py --check    # exit 1 if org/index.html is stale

Pattern after cbrock84/headcount (MIT): departments that install independently,
a reviewer class that reports to the top, a chart generated from the tree.
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "departments" / "org-manifest.json"
OUT = ROOT / "org" / "index.html"


def fail(msg: str) -> None:
    print(f"[build-org-chart] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_frontmatter(path: Path) -> dict:
    """Parse the simple key: value frontmatter between the first two --- fences."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{path}: missing frontmatter fence")
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("'\"")
    fail(f"{path}: unterminated frontmatter")


def load_org() -> dict:
    org = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seen = set()
    for dept in org["departments"]:
        ddir = ROOT / "departments" / dept["id"]
        if not ddir.is_dir():
            fail(f"manifest names department '{dept['id']}' but {ddir} does not exist")
        skills = []
        for sdir in sorted((ddir / "skills").iterdir()):
            skill_md = sdir / "SKILL.md"
            if not sdir.is_dir() or not skill_md.is_file():
                continue
            meta = parse_frontmatter(skill_md)
            name, desc = meta.get("name", ""), meta.get("description", "")
            if not name or not desc:
                fail(f"{skill_md}: frontmatter needs both name and description")
            if name != sdir.name:
                fail(f"{skill_md}: frontmatter name '{name}' != directory '{sdir.name}'")
            if name in seen:
                fail(f"duplicate skill name across departments: '{name}'")
            seen.add(name)
            skills.append({"name": name, "description": desc})
        if not skills:
            fail(f"department '{dept['id']}' has no skills")
        dept["skills"] = skills
    return org


def e(s: str) -> str:
    return html.escape(s, quote=True)


def render_skill(s: dict) -> str:
    return (
        f'      <li class="skill" data-search="{e(s["name"].lower())} '
        f'{e(s["description"].lower())}">\n'
        f'        <code>{e(s["name"])}</code>\n'
        f'        <p>{e(s["description"])}</p>\n'
        f"      </li>"
    )


def render_dept(d: dict, install_example: str, open_by_default: bool) -> str:
    skills = "\n".join(render_skill(s) for s in d["skills"])
    n = len(d["skills"])
    cls = "dept reviewer" if d["class"] == "reviewer" else "dept"
    badge = '<span class="badge">reviewer</span>' if d["class"] == "reviewer" else ""
    return f"""  <details class="{cls}" id="{e(d["id"])}"{" open" if open_by_default else ""}>
    <summary>
      <span class="rune" aria-hidden="true">{e(d["rune"])}</span>
      <span class="dtitle">{e(d["title"])} {badge}</span>
      <span class="dmeta">{e(d["steward"])} · {n} skill{"s" if n != 1 else ""}</span>
      <a class="anchor" href="#{e(d["id"])}" aria-label="Link to {e(d["title"])}">§</a>
    </summary>
    <p class="charter">{e(d["charter"])}</p>
    <p class="install"><code>/plugin install {e(d["id"])}@asgardr</code></p>
    <ul class="skills">
{skills}
    </ul>
  </details>"""


def build_page(org: dict) -> str:
    depts = org["departments"]
    reviewers = [d for d in depts if d["class"] == "reviewer"]
    line = [d for d in depts if d["class"] != "reviewer"]
    total = sum(len(d["skills"]) for d in depts)
    reviewer_html = "\n".join(render_dept(d, org["install"]["example"], True) for d in reviewers)
    line_html = "\n".join(render_dept(d, org["install"]["example"], False) for d in line)
    op = org["operator"]

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="The Asgardr operations org chart — {len(depts)} departments of evidence-led skills for a ten-computer, local-first fabric, {len(reviewers)} of them reviewer-class. Generated from the repository tree; no live cluster access.">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; img-src data:; base-uri 'none'; form-action 'none'">
<title>{e(org["org"])}</title>
<style>
  :root{{color-scheme:dark;--bg:#0c1710;--panel:#111f17;--panel2:#0f1b13;--ink:#f4efe2;
        --muted:#a9b4ac;--gold:#e2aa45;--gold-soft:rgba(226,170,69,.12);--line:#ffffff26;
        --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
        --sans:"Avenir Next","Segoe UI",Helvetica,Arial,sans-serif}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}}
  .wrap{{max-width:960px;margin:0 auto;padding:0 20px 80px}}
  header{{padding:64px 0 30px;border-bottom:1px solid var(--line)}}
  .eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;
           color:var(--gold);margin:0 0 14px}}
  h1{{margin:0 0 14px;font:400 clamp(40px,7vw,64px)/1 Georgia,serif;letter-spacing:-.03em}}
  .lede{{color:var(--muted);max-width:66ch;margin:0}}
  .stats{{display:flex;flex-wrap:wrap;gap:26px;margin:26px 0 0}}
  .stat b{{display:block;font:700 26px/1 var(--mono)}}
  .stat span{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
  .tools{{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 8px}}
  #q{{flex:1 1 260px;min-width:0;padding:12px 14px;border:1px solid var(--line);border-radius:8px;
      background:var(--panel);color:var(--ink);font:inherit}}
  #q:focus{{outline:2px solid var(--gold);outline-offset:1px}}
  button{{padding:12px 16px;border:1px solid var(--line);border-radius:8px;background:var(--panel);
         color:var(--muted);font:inherit;cursor:pointer;min-height:44px}}
  button:focus{{outline:2px solid var(--gold);outline-offset:1px}}
  #count{{font-family:var(--mono);font-size:12.5px;color:var(--muted);align-self:center}}
  .operator{{margin:38px auto 0;width:fit-content;text-align:center}}
  .mark{{width:58px;height:58px;margin:0 auto;display:grid;place-items:center;border:2px solid var(--gold);
        border-radius:50%;color:var(--gold);font:italic 25px Georgia,serif}}
  .operator b{{display:block;margin-top:10px;font-size:17px}}
  .operator span{{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
  .stem{{width:1px;height:26px;background:var(--line);margin:0 auto}}
  .band{{border:1px dashed var(--gold);border-radius:12px;background:var(--gold-soft);padding:18px;margin:0 0 26px}}
  .band>p.blabel{{font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
                 color:var(--gold);text-align:center;margin:0 0 8px}}
  .band>p.bnote{{color:var(--muted);font-size:14.5px;text-align:center;max-width:62ch;margin:0 auto 16px}}
  details.dept{{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin:0 0 14px;overflow:hidden}}
  details.dept.reviewer{{border-color:var(--gold)}}
  summary{{display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:16px 18px;cursor:pointer;min-height:44px}}
  summary:focus-visible{{outline:2px solid var(--gold);outline-offset:-2px}}
  .rune{{width:38px;height:38px;flex:none;display:grid;place-items:center;border:1px solid var(--line);
        border-radius:9px;color:var(--gold);font:20px/1 Georgia,serif;background:var(--panel2)}}
  .dtitle{{font-weight:600;font-size:16.5px}}
  .badge{{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);
         border:1px solid var(--gold);border-radius:20px;padding:2px 9px;margin-left:6px;vertical-align:2px}}
  .dmeta{{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--muted)}}
  .anchor{{color:var(--muted);text-decoration:none;font-size:15px;padding:4px 8px;border-radius:6px}}
  .anchor:hover,.anchor:focus-visible{{color:var(--gold)}}
  .charter{{margin:0;padding:0 18px 4px;color:var(--muted);max-width:74ch}}
  .install{{margin:10px 0 4px;padding:0 18px}}
  code{{font-family:var(--mono);font-size:13px;color:var(--gold);background:var(--gold-soft);
       border-radius:6px;padding:2px 7px}}
  ul.skills{{list-style:none;margin:8px 0 0;padding:6px 18px 16px}}
  li.skill{{padding:12px 0;border-top:1px solid var(--line)}}
  li.skill p{{margin:6px 0 0;color:var(--muted);font-size:14.5px;max-width:76ch}}
  .grid{{display:grid;gap:0;grid-template-columns:1fr}}
  footer{{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}}
  footer a{{color:var(--gold)}}
  [hidden]{{display:none!important}}
  @media (prefers-reduced-motion:no-preference){{details.dept{{transition:border-color .15s}}}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <p class="eyebrow">Asgardr / Operations Org</p>
  <h1>{e(org["org"])}</h1>
  <p class="lede">{e(org["tagline"])}</p>
  <div class="stats">
    <div class="stat"><b>{len(depts)}</b><span>departments</span></div>
    <div class="stat"><b>{total}</b><span>skills</span></div>
    <div class="stat"><b>{len(reviewers)}</b><span>reviewer-class</span></div>
    <div class="stat"><b>10</b><span>machines served</span></div>
  </div>
  <div class="tools">
    <input id="q" type="search" placeholder="Search {total} skills — try “restore”, “rotation”, “refusal”…"
           aria-label="Search skills" title="Press / to search">
    <button id="expand" type="button">Expand all</button>
    <span id="count">{total} skills in {len(depts)} departments</span>
  </div>
</header>

<div class="operator">
  <div class="mark" aria-hidden="true">Á</div>
  <b>{e(op["title"])}</b>
  <span>{e(op["subtitle"])}</span>
</div>
<div class="stem" aria-hidden="true"></div>

<section class="band" aria-label="Reviewer-class departments">
  <p class="blabel">Reviewer-class — reports to the Operator</p>
  <p class="bnote">{e(op["note"])}</p>
{reviewer_html}
</section>

<section class="grid" aria-label="Line departments">
{line_html}
</section>

<footer>
  <p>Install a department on the machine whose role needs it:
  <code>{e(org["install"]["marketplace"])}</code> then <code>{e(org["install"]["example"])}</code>.
  Every value on this page is derived from the repository tree — no live cluster
  access, telemetry, or operator controls.</p>
  <p>Generated from the repository tree — <code>scripts/build-org-chart.py</code>.
  {e(org["credits"])}
  · <a href="https://github.com/itpro2792-beep/asgardr">Repository</a>
  · <a href="https://asgardr-public-garden.itpro27.chatgpt.site/">The Asgardr garden</a></p>
</footer>

</div>
<script>
(function () {{
  var q = document.getElementById('q');
  var count = document.getElementById('count');
  var expand = document.getElementById('expand');
  var depts = Array.prototype.slice.call(document.querySelectorAll('details.dept'));
  var total = document.querySelectorAll('li.skill').length;
  var allOpen = false;

  function filter() {{
    var term = q.value.trim().toLowerCase();
    var shown = 0;
    depts.forEach(function (d) {{
      var hits = 0;
      d.querySelectorAll('li.skill').forEach(function (li) {{
        var hit = !term || li.getAttribute('data-search').indexOf(term) !== -1;
        li.hidden = !hit;
        if (hit) hits++;
      }});
      d.hidden = term ? hits === 0 : false;
      if (term && hits > 0) d.open = true;
      shown += hits;
    }});
    count.textContent = term
      ? shown + ' of ' + total + ' skills match'
      : total + ' skills in ' + depts.length + ' departments';
  }}
  q.addEventListener('input', filter);

  expand.addEventListener('click', function () {{
    allOpen = !allOpen;
    depts.forEach(function (d) {{ d.open = allOpen; }});
    expand.textContent = allOpen ? 'Collapse all' : 'Expand all';
  }});

  // Deep links: /org/#retrieval opens and scrolls to that department.
  function openFromHash() {{
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var d = document.getElementById(id);
    if (d && d.tagName === 'DETAILS') {{
      d.open = true;
      d.scrollIntoView({{ block: 'start' }});
    }}
  }}
  addEventListener('hashchange', openFromHash);
  openFromHash();

  // The § link sets a shareable URL without toggling the card shut.
  document.querySelectorAll('details.dept summary .anchor').forEach(function (a) {{
    a.addEventListener('click', function (ev) {{
      ev.preventDefault(); ev.stopPropagation();
      a.closest('details').open = true;
      history.replaceState(null, '', a.getAttribute('href'));
    }});
  }});

  // Press / anywhere to jump to search.
  addEventListener('keydown', function (ev) {{
    if (ev.key === '/' && document.activeElement !== q &&
        !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {{
      ev.preventDefault(); q.focus();
    }}
  }});
}})();
</script>
</body>
</html>
"""


def main() -> None:
    org = load_org()
    page = build_page(org)
    if "--check" in sys.argv:
        if not OUT.is_file():
            fail("org/index.html does not exist — run scripts/build-org-chart.py")
        if OUT.read_text(encoding="utf-8") != page:
            fail("org/index.html is stale — run scripts/build-org-chart.py and commit the result")
        print("[build-org-chart] org/index.html is current")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    total = sum(len(d["skills"]) for d in org["departments"])
    print(f"[build-org-chart] wrote {OUT.relative_to(ROOT)} — "
          f"{len(org['departments'])} departments, {total} skills")


if __name__ == "__main__":
    main()
