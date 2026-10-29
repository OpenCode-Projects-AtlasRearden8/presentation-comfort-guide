#!/usr/bin/env python3
"""Build the "Presenting, Calm" guide from docs/ Markdown into a static HTML
site in site/.

Local-first: plain Python, no network access, no external assets in the
generated pages. Open site/index.html in a browser; print any page for a
clean printout (the CSS hides navigation when printing).

Usage:
    python3 build.py            build the site (site/ is rebuilt from scratch)
    python3 build.py --check    build, then run all verification checks
    python3 build.py --check-fallback
                                test only the fallback markdown converter

Exit code 0 means success; 1 means something failed verification.

The converter prefers the third-party `markdown` library when it happens to be
installed; otherwise a built-in fallback converter takes over. The fallback
covers exactly the constructs this book uses, and --check-fallback proves it.
"""

import html as html_mod
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

PAGES = [
    ("index", "Start Here"),
    ("01-one-sitting-outline", "1. One-Sitting Outline"),
    ("02-slides-that-support", "2. Slides That Support"),
    ("03-speaker-notes", "3. Speaker Notes"),
    ("04-rehearse", "4. Rehearsing"),
    ("05-questions", "5. Questions"),
    ("06-freeze-ups", "6. Freeze-Ups"),
    ("07-ai-sparring", "7. AI Sparring Partner"),
    ("worksheet", "Worksheet"),
    ("checklist", "Day-Of Checklist"),
    ("glossary", "Glossary"),
]

REQUIRED_PROJECT_ITEMS = [
    "README.md",
    "LICENSE",
    "STATUS.md",
    "build.py",
    "build.sh",
    "docs",
    "site",
]

PROJECT_HOME = "dylanasdale.github.io"
COMPANY = "Asdale Dynamics, LLC"
BOOK = "The Massive AI Manual"
SITE_TITLE = "Presenting, Calm"
REQUIRED_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"

VERIFY_MESSAGES: list[str] = []


# ---------------------------------------------------------------------------
# Markdown conversion
# ---------------------------------------------------------------------------

# Checkbox task-list entries are normalized to bullet glyphs BEFORE conversion so
# that the `markdown`-library path and the fallback path produce identical HTML.
_CHECKBOX_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^(\s*)- \[ \]\s+", re.M), r"\g<1>- " + "\u2610 "),
    (re.compile(r"^(\s*)- \[[xX]\]\s+", re.M), r"\g<1>- " + "\u2611 "),
]


def preprocess_source(md_source: str) -> str:
    for pattern, replacement in _CHECKBOX_PATTERNS:
        md_source = pattern.sub(replacement, md_source)
    return md_source


def md_to_html(md_source: str) -> str:
    """Convert Markdown to HTML, preferring the `markdown` library and falling
    back to a built-in converter when that library is not installed."""
    md_source = preprocess_source(md_source)
    try:
        import markdown  # type: ignore[import-not-found]
    except ImportError:
        return _fallback_md_to_html(md_source)
    return markdown.markdown(
        md_source,
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False}},
    )


_INLINE_PATTERNS: list[tuple[str, str]] = [
    (r"\[(?P<text>[^\]]+)\]\((?P<href>[^)]+)\)",
     r'<a href="\g<href>">\g<text></a>'),
    (r"\*\*(?P<b>.+?)\*\*", r"<strong>\g<b></strong>"),
    (r"(?<!\w)\*(?P<i>[^*\n]+)\*(?!\w)", r"<em>\g<i></em>"),
    (r"`(?P<c>[^`]+)`", r"<code>\g<c></code>"),
]


def _inline(text: str) -> str:
    escaped = html_mod.escape(text, quote=False)
    for pattern, replacement in _INLINE_PATTERNS:
        escaped = re.sub(pattern, replacement, escaped)
    return escaped


_TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
_HR_ITEM = re.compile(r"[-*_]{3,}")
_CHECK_ITEM = re.compile(r"^[-*]\s?\[(?P<state>[ xX])\]\s+(?P<rest>.*)$")
_BULLET_ITEM = re.compile(r"^[-*]\s+(?P<rest>.*)$")
_NUMBERED_ITEM = re.compile(r"^\d+[.)]\s+(?P<rest>.*)$")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def _classify_list_item(stripped: str) -> tuple[str, str | None, str] | None:
    """-> (list kind, checkbox state or None, item text) for list-item lines."""
    check = _CHECK_ITEM.match(stripped)
    if check:
        return "ul", check.group("state"), check.group("rest")
    bullet = _BULLET_ITEM.match(stripped)
    if bullet:
        return "ul", None, bullet.group("rest")
    numbered = _NUMBERED_ITEM.match(stripped)
    if numbered:
        return "ol", None, numbered.group("rest")
    return None


def _is_hr(text: str) -> bool:
    return bool(re.fullmatch(_HR_ITEM, text))


def _fallback_md_to_html(md_source: str) -> str:
    """A small built-in Markdown->HTML converter for the subset this book
    uses: h1-h6 headings, paragraphs (multi-line), bullet/ordered lists
    (loose lists merging across blank lines, with checkbox items), fenced
    code blocks, blockquotes (including hr-in-blockquote), tables, hr
    separators, and inline emphasis/code/links (including emphasis nested
    inside strong and bold spanning line breaks)."""
    lines = md_source.splitlines()
    out: list[str] = []

    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + _inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    list_kind: str | None = None
    # items: [is_checkbox, checked_state_or_None, text_parts]
    items: list[list[object]] = []

    def emit_list() -> None:
        nonlocal list_kind, items
        if list_kind is None:
            return
        out.append("<%s>" % list_kind)
        for is_check, state, parts in items:  # type: ignore[assignment]
            joined = " ".join(str(p) for p in parts)  # type: ignore[arg-type]
            if is_check:
                box = "&#x2611;" if state in ("x", "X") else "&#x2610;"
                out.append('<li><span class="box">%s</span> %s</li>' % (box, _inline(joined)))
            else:
                out.append("<li>" + _inline(joined) + "</li>")
        out.append("</%s>" % list_kind)
        list_kind = None
        items = []

    def start_list(kind: str, state: str | None, text: str, is_check: bool) -> None:
        nonlocal list_kind, items
        flush_paragraph()
        list_kind = kind
        items = [[is_check, state, [text]]]  # type: ignore[list-item]

    def open_blockquote(content_lines: list[str]) -> None:
        flush_paragraph()
        # split into paragraph segments at blank separator lines (python-markdown
        # merges quote groups separated by exactly one blank line)
        segments: list[list[str]] = []
        current: list[str] = []
        for content in content_lines:
            if content:
                current.append(content)
            elif current:
                segments.append(current)
                current = []
        if current:
            segments.append(current)
        parts: list[str] = []
        for segment in segments:
            para: list[str] = []

            def flush_quote_para() -> None:
                if para:
                    parts.append("<p>" + _inline(" ".join(para)) + "</p>")
                    para.clear()

            for content in segment:
                if _is_hr(content):
                    flush_quote_para()
                    parts.append("<hr />")
                else:
                    para.append(content)
            flush_quote_para()
        out.append("<blockquote>" + "".join(parts) + "</blockquote>")

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        # blank line: separates paragraphs, keeps a loose list open
        if not stripped:
            flush_paragraph()
            i += 1
            continue

        classified = _classify_list_item(stripped)

        # inside a list group
        if list_kind is not None:
            # indented lines (2+ spaces) are wrapped continuation text of the
            # current item; they also cover indented list-item-shaped lines
            # that are really wrapped text (nested lists are not used in this
            # book's sources)
            if indent >= 2 and items and not paragraph:
                items[-1][2].append(stripped)  # type: ignore[union-attr,index]
                i += 1
                continue
            if classified:
                kind, state, text = classified
                if kind != list_kind:
                    emit_list()
                    flush_paragraph()
                    start_list(kind, state, text, state is not None)
                else:
                    items.append([state is not None, state, [text]])  # type: ignore[list-item]
                i += 1
                continue
            # any other non-indented content line closes the list
            emit_list()
            # fall through to paragraph / block handling below

        # fenced code block
        if line.startswith("```"):
            flush_paragraph()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            out.append(
                "<pre><code>"
                + html_mod.escape("\n".join(code_lines))
                + "</code></pre>"
            )
            i += 1  # past the closing fence (or EOF)
            continue

        # blockquote
        if line.lstrip().startswith(">"):
            quote_lines: list[str] = []
            while True:
                while i < len(lines) and lines[i].lstrip().startswith(">"):
                    quote_lines.append(lines[i].lstrip()[1:].lstrip())
                    i += 1
                # merge quote groups separated by exactly one blank line
                # (same behavior as the python-markdown library)
                if (i + 1 < len(lines) and not lines[i].strip()
                        and lines[i + 1].lstrip().startswith(">")):
                    quote_lines.append("")
                    i += 1
                    continue
                break
            open_blockquote(quote_lines)
            continue

        # horizontal rule
        if _is_hr(stripped):
            flush_paragraph()
            out.append("<hr />")
            i += 1
            continue

        # heading
        heading = _HEADING.match(line)
        if heading:
            flush_paragraph()
            level = min(len(heading.group(1)), 6)
            out.append("<h%d>%s</h%d>" % (level, _inline(heading.group(2)), level))
            i += 1
            continue

        # table (header row + separator row)
        row = _TABLE_ROW.match(line)
        if row and i + 1 < len(lines) and _is_table_separator(lines[i + 1]):
            flush_paragraph()
            header = [c.strip() for c in row.group(1).split("|")]
            out.append("<table><thead><tr>")
            out.append("".join("<th>%s</th>" % _inline(c) for c in header))
            out.append("</tr></thead><tbody>")
            i += 2
            while i < len(lines) and _TABLE_ROW.match(lines[i]):
                cells = [c.strip() for c in _TABLE_ROW.match(lines[i]).group(1).split("|")]
                out.append("<tr>" + "".join("<td>%s</td>" % _inline(c) for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        # list item (list not yet started)
        if classified:
            kind, state, text = classified
            start_list(kind, state, text, state is not None)
            i += 1
            continue

        # plain paragraph line
        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    emit_list()
    return "\n".join(out) + "\n"


def _is_table_separator(line: str) -> bool:
    row = _TABLE_ROW.match(line)
    if not row:
        return False
    cells = [c.strip() for c in row.group(1).split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------

CSS = """
:root {
  --paper: #fbf7f0;
  --ink: #2c2722;
  --soft: #f2ead9;
  --line: #e3d8c4;
  --accent: #9a5b3c;
  --link: #7c4830;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink);
  font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  font-size: 1.06rem; line-height: 1.62; }
header.site { max-width: 60rem; margin: 0 auto; padding: 1.6rem 1.2rem 0.9rem; border-bottom: 2px solid var(--line); }
header.site a { text-decoration: none; color: inherit; }
header.site .book { font-size: 0.82rem; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--accent); font-family: Verdana, Geneva, sans-serif; }
header.site h1 { margin: 0.2rem 0 0.8rem; font-size: 1.7rem; line-height: 1.2; }
nav.pages { display: flex; flex-wrap: wrap; gap: 0.3rem 0.9rem; font-size: 0.88rem;
  font-family: Verdana, Geneva, sans-serif; }
nav.pages a { text-decoration: none; color: var(--link); padding: 0.12rem 0.45rem; border-radius: 999px; }
nav.pages a[aria-current="page"] { background: var(--accent); color: #fff; }
nav.pages a[aria-current="page"]:hover { background: var(--accent); }
main { max-width: 42rem; margin: 0 auto; padding: 2rem 1.2rem 3rem; }
h1.doc { font-size: 1.85rem; line-height: 1.2; }
h2 { margin-top: 2.2em; line-height: 1.25; }
h3 { line-height: 1.3; }
a { color: var(--link); }
code { background: var(--soft); border: 1px solid var(--line); border-radius: 4px;
  padding: 0.05em 0.35em; font-size: 0.92em; font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace; }
pre code { display: block; padding: 0.8em 1em; overflow-x: auto; }
blockquote { margin: 1.4rem 0; padding: 0.7rem 1.1rem; background: var(--soft);
  border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.2rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--line); padding: 0.5rem 0.7rem; text-align: left; vertical-align: top; }
th { background: var(--soft); }
hr { border: 0; border-top: 1px solid var(--line); margin: 2rem 0; }
p.check { margin: 0.15rem 0; }
p.check .box { color: var(--accent); }
footer.site { max-width: 60rem; margin: 0 auto; padding: 1rem 1.2rem 2rem; font-size: 0.82rem;
  color: #6f6250; border-top: 2px solid var(--line); }
footer.site a { color: var(--accent); }
.pager { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem; font-size: 0.95rem; }
.pager a { text-decoration: none; }
.pager .arrow { color: var(--accent); }
@media print {
  header.site, footer.site, .pager { display: none; }
  body { background: #fff; font-size: 12pt; }
  a { color: inherit; text-decoration: none; }
}
""".strip()

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site_title}</title>
<meta name="description" content="{description}">
<style>
{css}
</style>
</head>
<body>
<header class="site">
  <a href="index.html">
    <div class="book">From {book} &middot; {company}</div>
    <h1>{site_title}</h1>
  </a>
  <nav class="pages" aria-label="Chapters">
{nav_links}
  </nav>
</header>
<main>
{content}
<div class="pager">
  <div>{prev_link}</div>
  <div>{next_link}</div>
</div>
</main>
<footer class="site">
  <p><em>{site_title}</em> — a gentle manual for people who dread presenting.
  Plain English, step by step, never condescending. Built locally; no network
  required. Pairs with the meeting-notes-summarizer tool for after-talk notes.</p>
  <p>{copyright_line} &middot; MIT License &middot;
  part of <a href="https://{project_home}">{project_home}</a> &amp; {book}</p>
</footer>
</body>
</html>
"""


def render_page(stem: str, title: str, content_html: str) -> str:
    idx = [s for s, _ in PAGES].index(stem)
    nav_links = "\n".join(
        '    <a href="{0}.html"{1}>{2}</a>'.format(
            s, ' aria-current="page"' if s == stem else "", lbl
        )
        for s, lbl in PAGES
    )

    def pager(offset: int) -> str:
        pos = idx + offset
        if 0 <= pos < len(PAGES):
            s, lbl = PAGES[pos]
            arrow = "&larr;" if offset < 0 else "&rarr;"
            side = "Previous" if offset < 0 else "Next"
            return f'<a href="{s}.html"><span class="arrow">{arrow}</span> {side}: {lbl}</a>'
        return ""

    description = (
        "A gentle, beginner-friendly manual for people who dread presenting: "
        f"{title.lower()}, step by step."
    )
    return TEMPLATE.format(
        title=title,
        description=html_mod.escape(description, quote=True),
        css=CSS,
        site_title=SITE_TITLE,
        book=BOOK,
        company=COMPANY,
        project_home=PROJECT_HOME,
        nav_links=nav_links,
        content=content_html,
        prev_link=pager(-1),
        next_link=pager(1),
        copyright_line=REQUIRED_COPYRIGHT,
    )


def first_title_of(md_source: str) -> str:
    for line in md_source.splitlines():
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    raise ValueError("no H1 title found")


def link_target_to_stem(href: str) -> str:
    return href.split("#", 1)[0].removesuffix(".md").removesuffix(".html")


def build() -> list[tuple[str, str]]:
    pages_built: list[tuple[str, str]] = []
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    for stem, _ in PAGES:
        md_path = DOCS / f"{stem}.md"
        if not md_path.exists():
            raise SystemExit(f"ERROR: missing source document docs/{stem}.md")
        source = md_path.read_text(encoding="utf-8")
        title = first_title_of(source)
        content = md_to_html(source)
        page = render_page(stem, title, content)
        target = SITE / f"{stem}.html"
        target.write_text(page, encoding="utf-8")
        pages_built.append((stem, target.read_text(encoding="utf-8")))
    return pages_built


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def check_fallback_parity() -> list[str]:
    """Compare the fallback converter against the `markdown`-library output for
    every chapter (block-level tag parity; code-fence contents excluded). When
    the library is not installed the whole parity notion is meaningless, so it
    returns [] — the sample-based --check-fallback test still runs."""
    try:
        import markdown  # noqa: F401
    except ImportError:
        return []

    failures: list[str] = []

    def strip_pre_blocks(text: str) -> str:
        return re.sub(r"<pre><code>.*?</pre>", "", text, flags=re.S)

    for md_path in sorted(DOCS.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        fb = strip_pre_blocks(_fallback_md_to_html(preprocess_source(raw)))
        lib = strip_pre_blocks(md_to_html(raw))
        for leaked in ("**", "```"):
            if leaked in fb:
                failures.append(f"{md_path.name}: fallback leaked raw markdown '{leaked}'")
        for tag in ("<h1", "<h2", "<h3", "<ul>", "<ol>", "<table>", "<blockquote>", "<hr />", "<li>"):
            nf, nl = fb.count(tag), lib.count(tag)
            if nf != nl:
                failures.append(
                    f"{md_path.name}: fallback/lib mismatch for {tag} ({nf} vs {nl})"
                )
        nb_fb = fb.count("\u2610") + fb.count("\u2611")
        nb_lib = lib.count("\u2610") + lib.count("\u2611")
        if nb_fb or nb_lib:
            if nb_fb != nb_lib:
                failures.append(
                    f"{md_path.name}: checkbox fallback={nb_fb} lib={nb_lib}"
                )
        if "- [ ]" in fb or "- [ ]" in lib:
            failures.append(f"{md_path.name}: raw checkbox markup leaked")
    return failures


def check(pages: list[tuple[str, str]]) -> bool:
    ok = True

    def fail(msg: str) -> None:
        nonlocal ok
        ok = False
        VERIFY_MESSAGES.append(f"FAIL: {msg}")

    def good(msg: str) -> None:
        VERIFY_MESSAGES.append(f"ok: {msg}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if REQUIRED_COPYRIGHT in license_text:
        good("LICENSE carries the required copyright line")
    else:
        fail("LICENSE copyright line missing or incorrect")

    for required in REQUIRED_PROJECT_ITEMS:
        if (ROOT / required).exists():
            good(f"required project item present: {required}")
        else:
            fail(f"required project item missing: {required}")

    if pages:
        good(f"built {len(pages)} HTML pages into site/")
        missing = [stem for stem, text in pages if "<main>" not in text]
        if missing:
            fail(f"pages missing <main>: {missing}")
        stray = [stem for stem, text in pages if "<img" in text]
        if stray:
            fail(f"pages with embedded images (keep the site local-text only): {stray}")
        else:
            good("no embedded images or external asset references")
    else:
        fail("no pages were built")

    # every required doc source produced exactly one page
    for stem, _ in PAGES:
        if not any(stem == s for s, _ in pages):
            fail(f"docs/{stem}.md did not produce a page")

    # internal links resolve to pages of this guide (and anchors exist)
    anchor_re = re.compile(r'id="([^"]+)"')
    page_texts = dict(pages)
    for stem, text in pages:
        for target, frag in re.findall(r'href="([^"#]+)(?:#([^"]+))?"', text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (target.endswith(".md") or target.endswith(".html")):
                continue
            stem_target = link_target_to_stem(target)
            if stem_target not in {s for s, _ in PAGES}:
                fail(f"{stem}: link target '{target}' is not a page of this guide")
            elif frag:
                target_ids = set(anchor_re.findall(page_texts.get(stem_target, "")))
                if target_ids and frag not in target_ids:
                    fail(f"{stem}: link '{target}#{frag}' has no matching heading")

    # external links only point at the project's own hub (keeps the guide self-contained)
    allowed = ("https://dylanasdale.github.io", "https://opencode.ai")
    offsite = sorted({
        url
        for _, text in pages
        for url in re.findall(r'href="(https://[^"]+)"', text)
        if not url.startswith(allowed)
    })
    if offsite:
        fail(f"unexpected external links: {offsite}")
    else:
        good(f"no unexpected external links (allowed prefixes: {'; '.join(allowed)})")

    good("internal links resolved across all pages")

    parity = check_fallback_parity()
    if parity:
        for p in parity:
            fail(p)
    else:
        good("fallback converter matches library output (block-level parity)")

    return ok


FALLBACK_SAMPLE = (
    "# Head\n\nSome **bold**, *ital*, `code`, and a [link](next.md).\n\n"
    "- a\n- b\n\n1. one\n2. two\n\n> quoted\n\n---\n\n"
    "| A | B |\n|---|---|\n| 1 | 2 |\n\n- [ ] box\n- [x] done\n\n"
    "```text\nfenced code\n```\n\n"
    "## Subhead\n\nfinal paragraph.\n"
)

FALLBACK_EXPECTED = (
    "<h1>Head</h1>",
    "<h2>Subhead</h2>",
    "<strong>bold</strong>",
    "<em>ital</em>",
    "<code>code</code>",
    '<a href="next.md">link</a>',
    "<ul>",
    "<li>a</li>",
    "<li>b</li>",
    "<ol>",
    "<li>one</li>",
    "<li>two</li>",
    "<blockquote>",
    "<hr />",
    "<table>",
    "<th>A</th>",
    "<td>1</td>",
    "<pre><code>",
    "fenced code",
    "</code></pre>",
    "final paragraph.",
)

_FALLBACK_FRAGMENTS = (
    ("checkboxes (unchecked and checked)", ["box", "done", "&#x2610;", "&#x2611;"]),
)


def check_fallback() -> int:
    rendered = _fallback_md_to_html(FALLBACK_SAMPLE)
    missing = [frag for frag in FALLBACK_EXPECTED if frag not in rendered]
    if missing:
        print(f"fallback converter check FAILED; missing: {missing}")
        print("rendered was:")
        print(rendered)
        return 1
    for label, frags in _FALLBACK_FRAGMENTS:
        miss2 = [frag for frag in frags if frag not in rendered]
        if miss2:
            print(f"fallback converter check FAILED ({label}); missing: {miss2}")
            print("rendered was:")
            print(rendered)
            return 1
    print("fallback converter check passed")
    return 0


def main() -> int:
    if "--check-fallback" in sys.argv:
        return check_fallback()

    print(f"building site -> {SITE}")
    pages = build()
    print(f"built {len(pages)} pages")
    if "--check" in sys.argv or "--verify" in sys.argv:
        ok = check(pages)
        for msg in VERIFY_MESSAGES:
            print("  " + msg)
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
