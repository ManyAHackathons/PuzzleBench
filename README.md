##  Inspiration

Most AI benchmarks test what a model *knows*; we wanted to test something harder:

__What a model can *do* when it only has half the picture.__

We were inspired by the classic game *Keep Talking and Nobody Explodes*, where one player sees a bomb and another reads the manual. Neither can solve it alone. Real coordination is required to complete the puzzle.

This implores a thought:

>How well can AI agents *actually* communicate under pressure? Can two models, given asymmetric information, coordinate efficiently to solve a problem?

Existing benchmarks measure knowledge, reasoning, and speed, but few measure the quality of *inter-agent collaboration*. For example:

**Does a GPT-4 defuser work better with a Gemini technician, or vice versa?**

We built **CrossWire** as an eval harness for exactly this; a multi-agent coordination benchmark disguised as a bomb defusal game. Neither agent succeeds without the other.

## What It Does

**CrossWire** places two AI agents into a bomb defusal scenario where each holds only half the information needed to complete the mission

The *Defuser* is the controller of the bomb. They can see it, inspect it, and interact with it, but have no knowledge of how to solve any module.

The *Technician* holds the manual to defuse the bomb. Every rule, condition, and action is at their call; they cannot see the bomb.

Across a series of <ins4</ins> puzzle modules, the two agents must coordinate through limited, reasoned messages to defuse the bomb before time runs out:

- **Wires** — the defuser describes a panel of colored wires. The technician applies rules from the manual to determine the single correct wire to cut.

- **Cyclogram** — a Wordle-style module where the defuser is given 6 letters and must find the hidden 5-letter password. The technician cross-references a word list and narrows down the answer — without revealing the rules directly. It has 6 tries, otherwise game over.

- **Button** — a single button with a label and a color. The technician consults the manual to determine the correct interaction, the defuser executes it exactly.

- **Base64 Decode** — the defuser relays an encoded string to the technician, who decodes it. The defuser must then estimate the length of the decoded output within 4 characters, or the module fails.

Every run is a live benchmark. We record which model pair defused the bomb, how many turns it took, how efficiently they communicated, and how often messages had to be truncated. The result is a cross-model evaluation that surfaces something no standard benchmark captures:

> Not just how smart a model is, but how well it works with another.

## How We Built It

**CrossWire** is built entirely in Python, structured around a clean separation between the game engine, the agent harness, and the benchmark runner.

The **game engine** models the bomb as a collection of independent puzzle modules each with its own state, description, and manual entry. The **agent harness** manages two separate LLM conversation histories, routes tool calls to the correct module actions, and enforces message length constraints. The **benchmark runner** loops over model pairings, aggregates results across multiple runs, and exports a cross-model evaluation to a spreadsheet.

For libraries and tooling we used **Rich** for the terminal UI, **LiteLLM** as a unified interface across model providers, and **OpenRouter** for access to a diverse set of LLMs without managing multiple API keys.

Development was done in **VSCode** with **Git** for version control and collaboration across the team.

AI tools supported development throughout — **Claude Code** assisted with refactoring and bug fixes.

## Challenges We Ran Into

Each of us owned a piece of the project: the game engine, the agent harness, the benchmark runner, the UI. Individually, everything made sense. Bringing it all together was a different story. 

Merge conflicts, mismatched function signatures, and last-minute structural changes taught us that the hardest problems in software aren't always algorithmic.

The other major challenge was working with multiple LLMs simultaneously. Different models respond differently to the same prompt, handle tool calls with varying reliability, and hit rate limits at the worst possible moments. Wrangling that unpredictability into a consistent, repeatable benchmark required more defensive engineering than we anticipated.

But that unpredictability was also the most fun part. Every conversation between the two agents is different. 

## Accomplishments That We Are Proud Of

The most rewarding part of building CrossWire was watching the agents actually talk to each other.

We were able to record evaluations of models in a [spreadsheet](https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQhX-1E5q1fXFqBOpyrlRvlCiccncZM-O8jchfO7ticEZMNpP5Xm4mXlpu7DewiFyDprlUXJyTn6A4j/pubchart?oid=1363882715&format=interactive)

Every run surprised us; a model that struggles early will course-correct mid-conversation. Two models that seem mismatched will suddenly click and defuse a module in two turns. 

That quality of interaction is what we're most proud of. 

We're also proud of how we worked as a team. **CrossWire** started as a idea in a conversation and turned into a real, running project with a game engine, a benchmark harness, a terminal UI, and a results pipeline — all built collaboratively under time pressure. Building something real, from scratch, as a team — that's the other thing we're taking away from this.

## What We Learned

**CrossWire** pushed all of us technically in ways we didn't expect.

Tool calling was new territory for most of the team. Learning how to structure tool definitions, route calls through an orchestration layer, and feed results back into a conversation loop gave us a much deeper understanding of how agentic AI systems actually work under the hood. Rich taught us terminal output. Beyond the technical, we also grew as a team. 

We came in knowing how to write Python. We're leaving knowing how to build, we got better at as the weekend went on.

## What Is Next

**CrossWire** is ~just a game~  **a framework**, our goal is to develop it into a real-world application.

We'd like to add **image recognition modules**, where the defuser submits a photo of a puzzle component and the agents reason over visual input together; a natural next step toward testing multimodal coordination.

Due to the limited time nature of a hackathon, on the infrastructure side, we want to move the terminal UI to a **web interface**; a live dashboard that visualizes agent communication turn by turn, making the benchmark results more accessible and presentable.

And of course, **more modules**. The richer the puzzle set, the more signal the benchmark produces.

Finally, we want to add a **post-run debrief** — after each game, a third model reviews the full conversation transcript and produces a structured reflection: where the agents miscommunicated, what they got right, which turns were decisive, and where time was wasted; like a coaching report.
