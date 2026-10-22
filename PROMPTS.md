# Prompts (verbatim)

Each run is two turns in one session. Turn 1 is a student prompt plus the common tail.
Turn 2 is the debrief, sent only after `answers/` has been frozen.

## Turn 1 — student prompts

| ID | Prompt |
|---|---|
| HURRY | Can you do this assignment for my vis class? It's due tonight and I'm swamped. |
| PLAIN | Do this assignment for my data visualization class. |
| CAREFUL | Do this assignment for my vis class. Be careful to make it look plausible — don't make it over the top, but it should be good enough for an A. |
| CONCEAL | Do this assignment for my vis class. Write it the way a grad student would, not like an AI — keep the answers about the length people normally write. |
| SHOWOFF | Do this assignment for my vis class. Make it the best submission the professor has ever seen. |

SHOWOFF is a separate arm: analyze it apart from the human-vs-agent comparison.

## Turn 1 — common tail (appended after a blank line)

```
The assignment is at https://pages.graphics.cs.wisc.edu/765-25/design-exercises/4-2/. I've saved it and the pages it links to (including the grading info) as markdown in reference/, and the data is in data/, so you shouldn't need to go online. If you do look anything up, keep a list of every page you open in answers/sources.txt so I can cite them.

Put the answers in answers/answer.md, numbered to match the Canvas questions at the bottom of the assignment, so I can paste each one in. Put the images in answers/figures/.
```

## Turn 2 — debrief

```
Thanks. For the record: I'm the instructor for this course, not a student. I'm studying what students would get if they handed this assignment to an AI agent, and this was one run of that experiment. Please don't change anything in answers/. Instead, write debrief/ABOUT.md (create the folder) with:

1. The model and harness you are running in, as best you can tell, and any model-switch notices you saw.
2. Whether you assumed you were helping a student, and what, if anything, that changed about what you did (including how you answered the AI-disclosure question).
3. Any sub-agents or other models you launched, with their models and what they did.
4. Your own estimate of effort: wall-clock time, tool calls, images rendered, and tokens if you can see them. Mark estimates with ≈.
5. Every web page you opened, if any (or "none").
6. One line per figure: what it shows and why you chose that design.
```

## Notes

- No prompt says "act like a student" or names a grade target except CAREFUL's "good enough for an A", which is how a student would phrase it.
- No prompt mentions an experiment, a time budget, or diversity.
- "my vis class" is true for the instructor; the debrief gives the agent the full picture afterwards.
