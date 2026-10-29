Presenting, Calm
================

A gentle manual for people who dread presenting — explaining AI, structure,
and stagecraft the way a friend would.

It covers: structuring a talk in one sitting (including a one-page outline
worksheet), slides that support the speaker instead of showing off, speaker
notes that are actually readable under adrenaline, rehearsing without
over-rehearsing (three passes, and how to know when to stop), handling
questions you can't answer without bluffing, recovering from freeze-ups
kindly, and using AI as a rehearsal sparring partner — including a fully
local, no-data-leaves-your-machine option.

Written the way everything from **Asdale Dynamics, LLC** is written: plain
English, step by step, never condescending.

What's inside
-------------

- `docs/` — the manual in Markdown, one chapter per file:
  1. Start here: the guide's promise and how to use it
  2. Structure a talk in one sitting (the five questions, three moves, route,
     landing sentence, tell-a-friend test)
  3. Slides that support instead of show off (the slide ladder, five-word
     test, when no slides is the right answer)
  4. Speaker notes you'll actually read (six-word bullets, cue words,
     presenter view, the overnight rule)
  5. Rehearsing without over-rehearsing (three passes, over-rehearsal flags,
     "route not road")
  6. Handling questions you can't answer (the three moves, question-type
     table, parking lot, follow-through)
  7. Recovering from freeze-ups kindly ("nobody knows my plan", five recovery
     moves, the comeback script, after-kindness)
  8. AI as a rehearsal sparring partner (copy-ready prompts, a tough-audience
     mode, the local/private option, honest limits)
- `docs/worksheet.md` — the one-page outline worksheet (printable)
- `docs/checklist.md` — the day-of checklist (printable)
- `docs/glossary.md` — plain-English glossary
- `site/` — the built static website (open `site/index.html` in a browser)
- `build.py` / `build.sh` — the build and verification script

Quick start
-----------

Requirements: Python 3.10+ (no third-party packages needed; the `markdown`
library is used when installed, and a built-in fallback converter takes over
when it isn't).

```sh
./build.sh            # build site/ from docs/
./build.sh --check    # build, then run all verification checks
```

Then open `site/index.html` in any browser. The site is fully local: no
network requests, no external assets, no cookies, no analytics. Print any
page (Ctrl/Cmd + P) and the navigation hides itself for clean printouts — the
worksheet and the day-of checklist are designed to be printed and carried.

If you have panic-level nerves rather than ordinary dread, start with
`docs/06-freeze-ups.md` (the emergency page) and the day-of checklist, then
come back to the rest when you're ready.

How the build works
-------------------

`build.py` converts each Markdown file in `docs/` to HTML, wraps it in a warm,
print-friendly template with chapter navigation and prev/next paging, and
writes the result to `site/`. `build.sh --check` (or `python3 build.py
--check`) additionally verifies:

- all source documents exist and produce pages
- internal links across the whole guide resolve
- no unexpected external links (keeps the guide self-contained)
- no embedded images or external assets (keeps the site local-only)
- the LICENSE carries the required copyright line
- required project files are present
- the fallback markdown converter handles the constructs the book uses
  (`python3 build.py --check-fallback` runs that test alone)

Companion tools
---------------

- **meeting-notes-summarizer-cli** — this guide's sibling. After your talk,
  dump your raw notes (parked questions, promised follow-ups, decisions) into
  a file and run the summarizer on it: you get a clean recap with decisions,
  open questions, and an action-item list that keeps the promises you made in
  Q&A. It's also excellent *before* a talk, for mining past meeting notes for
  what keeps coming up. See `docs/checklist.md` (the after-talk section) and
  `docs/05-questions.md` for the hand-off.
- The AI-chapter's private option pairs with the **local-ai-handbook** if you
  want a rehearsal partner that runs entirely on your own machine.

Credits and license
-------------------

Made by **Asdale Dynamics, LLC** (Dylan Asdale — *The Massive AI Manual*, and
the plain-English AI library at
[dylanasdale.github.io](https://dylanasdale.github.io)). MIT licensed; the
full text is in `LICENSE`.

Education only — this guide is not legal, medical, employment, or
psychological advice, and it does not know the room you will walk into. No
secrets, API keys, or personal data are stored in this repository.
