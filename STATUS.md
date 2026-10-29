# STATUS

**Repo:** presentation-comfort-guide
**Date:** 2026-10-29
**Author of work:** Asdale Dynamics, LLC — committed under the existing git
identity only; no co-authored-by trailers; never pushed; no remote created;
nothing published.

## What was built

"Presenting, Calm" — a gentle manual for people who dread presenting.
Markdown sources in `docs/`, rendered into a fully static, local-first HTML
site in `site/` by a small Python build script.

- **Chapters (`docs/`, 11 files):**
  - `index.md` — who this is for, the promise (structured / supported /
    rehearsed just enough), three ways to use the guide, house context
  - `01-one-sitting-outline.md` — structure a talk in one sitting: the five
    questions, the three moves, three route options (staircase / trailhead /
    problem-board), the landing sentence, the tell-a-friend test, a 90-minute
    recap table, and a talk-sizing sanity table
  - `02-slides-that-support.md` — slides as furniture: the slide ladder,
    five-word title test, one idea per slide, data slides (one big number /
    before-after / labeled trend), template strategy, when no slides is the
    right answer, rescuing an inherited bad deck
  - `03-speaker-notes.md` — notes format for stress: six-word bullets, the
    four cue words ([PAUSE] [SLIDE] [SLOW DOWN] [LOOK UP]), podium layout,
    presenter view in the common apps, the overnight rule
  - `04-rehearse.md` — the three-pass method (structure / full / front-door),
    one recording with a kind-limited review, over-rehearsal flags,
    "remember the route, not the road"
  - `05-questions.md` — handling questions you can't answer: Release / Bridge
    / Handoff-or-follow-up, five question types with matching moves, the
    parking lot, question-time structure, follow-through via raw notes +
    **meeting-notes-summarizer-cli**
  - `06-freeze-ups.md` — recovering from freeze-ups kindly: why the freeze
    happens (working-memory throttle), "nobody knows my plan", five recovery
    moves, a comeback script, longer-freeze options, after-kindness section
  - `07-ai-sparring.md` — AI as a rehearsal sparring partner: setup order,
    four copy-ready prompts (structure critique, tough-audience role-play,
    timing check, notes pressure round), a fully-local/private option
    (Ollama / LM Studio), and hard limits (facts stay yours, it's never been
    in your room)
  - `worksheet.md` — the one-page outline worksheet (printable)
  - `checklist.md` — the two-days-before / night-before / day-of checklist,
    tech pass, first-sixty-seconds list, question-time card (printable)
  - `glossary.md` — plain-English glossary
- **Static site (`site/`, 11 HTML pages):** warm print-friendly template,
  chapter nav with current-page highlight, prev/next pager, embedded CSS
  (no external assets, no network requests, no analytics, no cookies). Print
  CSS hides chrome for clean printouts — worksheet and checklist are meant
  to be printed.
- **Build system:** `build.py` (Python 3.10+, stdlib-first) converts Markdown
  to HTML; uses the `markdown` library when installed and falls back to a
  built-in converter that covers exactly the constructs the book uses
  (headings, multi-line paragraphs, loose bullet/ordered lists with checkbox
  items, fenced code, blockquotes including hr-in-blockquote and python-markdown's
  one-blank-line merge behavior, tables, hr, inline emphasis with nested
  italics inside bold and bold spanning line breaks). `build.sh` wraps it.
  `--check` includes a docs-wide fallback-vs-library parity verification.
- **Legal/identity:** MIT `LICENSE` with the exact line
  `Copyright (c) 2026 Asdale Dynamics, LLC`; `README.md` credits Asdale
  Dynamics, LLC. No secrets, API keys, or personal data anywhere in the repo.

## How to run it

```sh
./build.sh                 # rebuild site/ from docs/
./build.sh --check         # rebuild + run all verification checks
python3 build.py --check-fallback   # test only the fallback markdown converter
```

Then open `site/index.html` in any browser — fully offline capable, or serve
with `python3 -m http.server --directory site`.

## Verification results (all passing, exit code 0)

- `python3 build.py --check`
  - LICENSE copyright line: ok
  - required project files present (README.md, LICENSE, STATUS.md, build.py,
    build.sh, docs, site): ok
  - 11 source docs found and 11/11 HTML pages built: ok
  - no embedded images / external assets / unexpected external links: ok
  - all internal links across all pages resolve: ok
  - fallback converter matches the `markdown` library output at block level
    for every chapter (tag parity incl. `<ul>`, `<ol>`, `<li>`, tables,
    blockquotes, hr, headings): ok
- `python3 build.py --check-fallback` — fallback handles every markdown
  construct used by the book (sample-based test): ok
- `python3 -m py_compile build.py` — no syntax errors: ok
- `bash -n build.sh` — no shell syntax errors: ok
- Ad-hoc checks: 0 raw markdown tokens leaking into fallback output across
  all chapters; 64 checkbox items rendered consistently on both converter
  paths; all 11 generated pages contain DOCTYPE/charset/closing html.

## Known gaps

- The site renders with the third-party `markdown` library when installed
  and with the built-in fallback otherwise; both paths are verified to
  produce block-identical output for this book, but the fallback does not
  attempt general Markdown beyond the constructs used here.
- No table of contents with anchor jumps inside long pages (headings do get
  ids from the library path, but no in-page TOC widget is built).
- Chapter 7's AI prompts are written for generic chat assistants and Ollama-
  style local runners; output quality depends on the model you bring.
- The guide is deliberately not an exhaustive public-speaking course; scope
  is the six pressure points listed in the task (structure, slides, notes,
  rehearsal, questions, freeze-ups) plus the AI-rehearsal complement.
- Companion "meeting-notes-summarizer-cli" integration is documentation-level
  (workflow hand-off described in README, chapter 5 and the checklist); the
  two projects do not share code.
