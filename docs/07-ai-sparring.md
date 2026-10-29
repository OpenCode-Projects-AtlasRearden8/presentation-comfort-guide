# AI as a Rehearsal Sparring Partner

One of the strangest, kindest gifts of this decade: you can now rehearse a talk
against an audience that never gets bored, never rolls its eyes, never repeats
anything it hears, and is available at 11 p.m. when the talk is at 9 a.m. and
your stomach is doing gymnastics.

This chapter shows you how to use an AI chat — a cloud one, or a fully local one
running on your own machine — as a **sparring partner** for the specific jobs a
rehearsal partner does: poking holes in structure, playing a tough audience,
drilling you on questions, and checking your timing. It also covers what AI
*can't* do, so the tool stays a tool.

## Why AI fits this job (when a human doesn't)

The problem with practicing on other humans is everything you already know:

- **Busy people** give a real rehearsal the energy of "hurry up."
- **Kind people** do not tell you the opening is foggy, and the fog survives to
  the room.
- **Scary people** (your boss' boss) make a rehearsal worse than no rehearsal.
- **Asking for a second session** takes social energy that presenting itself
  already taxed.

An AI chat has none of those problems. It will answer follow-ups instantly,
follow-up, it gives *specific* critique if you ask for specifics, and — the
crucial trait for a nervous presenter — **it doesn't remember asking you to
look at its slides over lunch later.**

Two healthy limits to hold throughout: (1) an AI has never stood in *your*
room and it doesn't know your audience, so treat its outputs as drafts to
test, not verdicts; and (2) facts stay yours — an AI can suggest structure
*about* your numbers but can't be the source of them, and anything factual in
your talk should trace back to a document or a person you can name.

## Setup: what to give it, in what order

The move that changes everything: **don't just paste your slides and say "what
do you think."** You get vague replies to vague questions. Instead, work in
this order — structure first, then words, then questions:

1. **Give it the frame**: who's in the room, what should change afterward, how
   many minutes, how the talk will be delivered (live room / hybrid / video),
   and what you're dreading most.
2. **Give it the route**: your landing sentence and your three move-sentences.
   Ask for structure critique *before* you show any actual slide content, so
   the critique is about the skeleton rather than about your typography.
3. **Only then** paste notes or slide text, one move at a time.

You will get better results in 15 minutes of this order than in an hour of
freeform "here is everything, is it good?"

## Technique 1 — the structure critique (your "tell-a-friend," in writing)

Paste this prompt, filling the brackets (this and the other prompts below are
copy-ready — paste them straight into any chat):

```
You're helping me prepare a short talk. Here is the context:

- Audience: [who's in the room, what they already believe]
- Desired change: [what they can do / decide differently after]
- Length: [X minutes], [live room / hybrid / chat + slides]
- I'm most worried about: [your honest note]

My planned structure:

- Landing sentence: [your one sentence]
- Move 1: [one sentence with a verb]
- Move 2: [one sentence]
- Move 3: [one sentence]

Please challenge this structure. In particular:
1. Where will this be confusing to [audience]?
2. Which move is doing work the audience won't understand yet at that point?
3. What is the single best change I could make to the route?
4. What question would you expect from a skeptic in this room?

Answer as a list of concrete, specific issues, in the order I should fix
them. Do not flatter me; a kind-but-blunt editorial note is welcome.
```

Then do something counter-intuitive: **argue with it a little.** Pick one piece
of its critique and push: "I worry that drop would lose the setup for move 3 —
what would you do instead?" The pushing is where the real thinking happens;
the AI is warm-up weight resistance.

## Technique 2 — the tough audience (it plays the room)

Once the route holds, have it *play* the room for practice:

```
Play my audience. You are three realistic people in the room I described:
[skeptic in the back / newer employee who's just hoping it's not more
paperwork / friendly senior person who asks the sharpest question].
Starting with the skeptic, give me questions about my talk as I answer
them. One question at a time. After each of my answers, rate it:
(a) does it actually answer the question, (b) does it hedge into mush
anywhere, (c) is there a shorter, more honest version? Then give the
next question.
```

This is question-time rehearsal for chapter 5's table of question types. Let
it pitch the fear question ("does this mean my job?") too — practicing the
fear question is something humans almost never offer you. When you hit a
question you can't answer: practice the three moves *out loud*, and practice
"I don't know, I'll find out" with a named follow-through date for the
follow-through.

## Technique 3 — the timing checker

Do a full-length spoken run at your desk against a timer, then compare notes:

```
Here's my rough timing in the run I just did (list it):

- opening: [2:00]
- move 1: [6:30]
- move 2: [7:10]
- move 3: [8:00]
- summary: [1:30]
- total: [25:10]  (slot is [20] minutes)

If I need to cut about [5] minutes, where's the most likely place that
cuts with the least damage? Ask me 2–3 follow-up questions about the
moves before answering, so you know what's load-bearing.
```

The phrase "what's load-bearing" is doing real work here. Any good presenter
will cut what's not load-bearing; the model's useful trick is asking you the
questions that identify it.

## Technique 4 — the sparring partner for your speaker notes

Paste a single move's speaker notes and ask:

```
Here are speaker notes for one move of my talk (chunky bullets, in the
order I say them). Two jobs:
1. Say the move back to me in the natural voice an audience hears — not
   a script to read, but the likely shape of what I'd actually say.
2. Flag the bullets where someone like me would go off the rails under
   adrenaline: no number, missing slide advance, story without a time
   budget, missing [PAUSE].
Then give me a 3-item checklist to improve these notes.
```

## The local, fully-private version

If the talk content is sensitive — an HR matter, unreleased financials,
something private — you can run the whole sparring loop on a model that
**lives on your own machine and talks to nothing.** The manual for that is
the **local-ai-handbook**; the short version:

- Install a local-model runner (Ollama or LM Studio are the common ones),
  download a small open model, and run it completely offline.
- The same prompts above work; local models are a bit slower and wordier, so
  ask for shorter answers ("answer in 6 bullets max").
- Zero data leaves your machine. For sensitive content, this is simply the
  right choice — there is no small-print judgment call to make.

## The hard limits (read this even if you skip the rest)

- **It has never been in your room.** Its "audience" is a bright abstraction.
  The real room has a hum, a clock, three people checking email, and one
  person who means well. Weigh its enthusiasm with a grain of salt: local
  chat models in particular are trained to be encouraging and will tell you
  "great structure!" if you ask weakly. Ask for *problems*, not praise.
- **It can be confidently wrong about facts.** No number, date, name, or
  claim goes in your talk because a chat suggested it. Every fact traces to
  something you can name (a document, a report, a person) in the room.
- **It cannot measure your voice.** Pacing, volume, where you trail off —
  these come from your recording (chapter 4, pass 2), not from a text model.
- **It is not a memory of your organization.** It doesn't know that Randy is
  the one who talks during cost slides, or that the last presenter who tried
  a similar plan was politely murdered in Q&A. The humans you trust still
  hold that map. Use them for a late-stage sanity pass.

A good final rule: **AI helps you think; a human feels the room.** Use AI for
rehearsal and structure; get one real human glance at the actual slides before
you show them to anyone you need to impress.

## One-sentence summary

An AI chat is the rehearsal partner who is always home: use it to stress-test
your route, play your toughest audience, time-check your cuts, and pressure
round your notes — while the facts stay yours and the room stays human.
