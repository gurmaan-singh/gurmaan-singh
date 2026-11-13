"""Writes card-activity.svg: the latest commits across my public repos, in the same style as the other cards.
Run by .github/workflows/activity.yml once a day. Needs GITHUB_TOKEN (any token that can read public repos)."""
import json, os, html, urllib.request
from datetime import datetime, timezone

USER = "gurmaan-singh"; N = 8
MONO = "Consolas, 'Courier New', monospace"; RED = "#E0122B"
tok = os.environ.get("GITHUB_TOKEN", "")

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {tok}"} if tok else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

commits = []
for repo in get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed"):
    if repo["fork"] or repo["name"] == USER:
        continue
    try:
        for c in get(f"https://api.github.com/repos/{USER}/{repo['name']}/commits?per_page=3"):
            if c.get("author") and c["author"].get("login") not in (USER, None) and "actions" in c["author"]["login"]:
                continue  # skip bot commits
            when = datetime.fromisoformat(c["commit"]["committer"]["date"].replace("Z", "+00:00"))
            commits.append((when, repo["name"], c["sha"][:7], c["commit"]["message"].splitlines()[0]))
    except Exception:
        pass  # empty repo
commits.sort(reverse=True)
commits = commits[:N]
now = datetime.now(timezone.utc)

def ago(t):
    s = int((now - t).total_seconds())
    for unit, div in (("min", 60), ("h", 3600), ("d", 86400), ("w", 604800)):
        if s < div * (60 if unit == "min" else 24 if unit == "h" else 7 if unit == "d" else 1000):
            return f"{max(1, s // div)} {unit} ago"
    return f"{s // 604800} w ago"

W = 948; H = 92 + 24 * max(len(commits), 1)
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Recent work: the latest commits across my repositories">',
     f'<rect width="{W}" height="{H}" rx="12" fill="#000"/><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#fff" stroke-opacity="0.14"/>',
     f'<g fill="none" stroke="{RED}" stroke-width="2"><path d="M10 28V10H28"/><path d="M920 10H938V28"/><path d="M10 {H-28}V{H-10}H28"/><path d="M920 {H-10}H938V{H-28}"/></g>',
     f'<g transform="translate(24,20)"><text x="0" y="22" fill="{RED}" font-family="{MONO}" font-size="20" letter-spacing="3">// RECENT WORK</text>',
     f'<line x1="0" y1="36" x2="900" y2="36" stroke="#fff" stroke-opacity="0.18"/><rect x="0" y="35" width="90" height="2" fill="{RED}"><animate attributeName="x" from="-90" to="900" dur="4s" repeatCount="indefinite"/></rect>',
     f'<text x="900" y="22" text-anchor="end" fill="#fff" fill-opacity="0.45" font-family="{MONO}" font-size="11" letter-spacing="2">UPDATED {now.strftime("%Y-%m-%d")}</text>',
     f'<text x="6" y="60" fill="#fff" fill-opacity="0.7" font-family="{MONO}" font-size="13">$ git log --all --oneline --author=me | head -{N}</text>']
for i, (when, repo, sha, msg) in enumerate(commits):
    y = 84 + 24 * i
    msg = html.escape(msg if len(msg) <= 66 else msg[:63] + "...")
    s.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.25 + 0.18 * i:.2f}s" dur="0.25s" fill="freeze"/>'
             f'<text x="6" y="{y}" fill="{RED}" font-family="{MONO}" font-size="13">{sha}</text>'
             f'<text x="78" y="{y}" fill="#fff" font-family="{MONO}" font-size="13" font-weight="bold">{html.escape(repo)}</text>'
             f'<text x="200" y="{y}" fill="#fff" fill-opacity="0.8" font-family="{MONO}" font-size="13">{msg}</text>'
             f'<text x="896" y="{y}" text-anchor="end" fill="#fff" fill-opacity="0.45" font-family="{MONO}" font-size="12">{ago(when)}</text></g>')
if not commits:
    s.append('<text x="6" y="84" fill="#fff" fill-opacity="0.6" font-family="Consolas" font-size="13">nothing yet</text>')
s.append("</g></svg>")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "card-activity.svg")
open(os.path.normpath(out), "w", encoding="utf-8", newline="\n").write("".join(s))
print(f"{len(commits)} commits written")
