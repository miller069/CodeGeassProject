[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/W0nBRQPI)
# Lab 7: NPC Dialog with Graphs

**Due Date:** See course calendar
**Points:** 100
**Language:** Python (Pygame)

---

## Overview

In this lab you will implement a **Graph** data structure and use it to power a
branching NPC dialog system. Each NPC carries a directed graph of dialog states;
edges represent the player's choices; traversal moves the conversation forward.
One of your NPCs will use the **Gemini API** to generate responses dynamically,
turning a scripted tree into an open-ended conversation.

By the end of the lab you will have:

- A working `Graph` class with BFS, DFS, and shortest-path search.
- At least three unique NPCs with hand-crafted dialog trees.
- Original NPC pixel-art sprites.
- One NPC powered by a live generative AI model.
- Performance benchmarks and a written complexity analysis.

---

## Learning Objectives

- Implement a graph with an adjacency-list representation.
- Understand BFS vs. DFS and when each is appropriate.
- Use graph traversal to drive interactive dialog trees.
- Integrate a third-party REST API (Gemini) into a running Python program.
- Measure and reason about graph algorithm performance.

---

## Part 0: Copy Files from Previous Labs (0 pts)

The game builds on every previous lab. Copy your completed implementations before
writing any new code.

### From Lab 3
```
cp ../2026spring-lab-03/code/game/datastructures/array.py   code/game/datastructures/
```

### From Lab 4
```
cp ../2026spring-lab-04/code/game/datastructures/stack.py   code/game/datastructures/
```

### From Lab 5
```
cp ../2026spring-lab-05/code/game/datastructures/waypoint.py    code/game/datastructures/
cp ../2026spring-lab-05/code/game/datastructures/patrol_path.py code/game/datastructures/
```

### From Lab 6
```
cp ../2026spring-lab-06/code/game/datastructures/sparse_matrix.py code/game/datastructures/
cp ../2026spring-lab-06/code/game/datastructures/hash_table.py    code/game/datastructures/
```

### From Project 1 / Lab 1 — serializers
```
cp ../2026spring-project-01/code/server/src/text_serializer.cpp   code/server/src/
cp ../2026spring-project-01/code/server/src/json_serializer.cpp   code/server/src/
cp ../2026spring-project-01/code/server/src/binary_serializer.cpp code/server/src/
```

### From Project 2 — position smoother
```
cp ../2026spring-project-02/code/server/include/circular_buffer.h   code/server/include/
cp ../2026spring-project-02/code/server/src/position_smoother.cpp   code/server/src/
```

Also copy `subcharacter.py` and `item.py` if you customised them in earlier labs.

> **The game will not launch until Part 0 is complete.**

### Optional: Copy your Tiled map from Lab 6

If you designed a tile map in Lab 6, bring it into this lab so the world renders with your art:

```
cp ../2026spring-lab-06/code/game/map/*.csv          code/game/map/
cp -r ../2026spring-lab-06/code/game/graphics/tilemap code/game/graphics/
```

The game loads `graphics/tilemap/Map.tmx` and all referenced tileset images automatically.
If those files are not present the game falls back to the plain `WORLD_MAP` grid.

---

## Part 1: Implement `Graph` (40 pts)

**File:** `code/game/datastructures/graph.py`

Implement an **adjacency-list graph** that supports both directed and undirected modes.

> **Points note:** The table below shows implementation points (manual grading).
> Automated test points are awarded separately when you push to GitHub Classroom CI.

### What to implement

| Method            | Description                                              | Impl pts |
|-------------------|----------------------------------------------------------|----------|
| `__init__`        | Initialise empty adjacency list storage                  | 2        |
| `add_node`        | Add node with optional data payload; O(1) avg            | 2        |
| `add_edge`        | Add edge(s); create missing nodes automatically          | 3        |
| `remove_node`     | Remove node and all touching edges; O(V + E)             | 3        |
| `remove_edge`     | Remove one edge (and reverse for undirected); O(degree)  | 2        |
| `has_node`        | O(1) membership test                                     | 1        |
| `has_edge`        | O(degree) edge lookup                                    | 1        |
| `get_neighbors`   | Return list of `(neighbor_id, weight, edge_data)` tuples | 2        |
| `get_node_data`   | Return payload stored at a node                          | 1        |
| `nodes`           | Return list of all node IDs                              | 1        |
| `bfs`             | Breadth-first traversal; returns nodes in discovery order| 4        |
| `dfs`             | Depth-first traversal (iterative)                        | 4        |
| `shortest_path`   | BFS-based shortest path; returns node list or `[]`       | 4        |
| `__len__`         | Number of nodes; O(1)                                    | 1        |
| `__str__`         | Human-readable summary                                   | 1        |

### Adjacency list design

Each node has an entry in your adjacency list. The entry stores outgoing edges as a
list of `(neighbor_id, weight, edge_data)` tuples. The `edge_data` slot is used by
the dialog system to store the player's choice text on each edge.

**You may NOT use Python's built-in `dict` or `set` inside your `Graph` class.**
Use your `HashTable` from Lab 6 as the adjacency map. Copy it in Part 0 and import it:

```python
from datastructures.hash_table import HashTable
```

Your adjacency list is a `HashTable` mapping `node_id → list of (neighbor_id, weight, edge_data)`.

### Directed vs. undirected

- `Graph(directed=True)` — `add_edge(a, b)` creates only `a → b`.
- `Graph(directed=False)` — `add_edge(a, b)` creates both `a → b` and `b → a`.

### Testing locally

```bash
cd code/game/datastructures/tests
python graph_tests.py
```

Automated grading runs on GitHub Classroom when you push; the CI suite is separate
from `graph_tests.py` and tests scenarios you may not have written yourself.

---

## Part 2: Design NPC Dialog Trees (20 pts)

**File:** `code/game/dialog_data.py`

Use your `Graph` (via the provided `DialogGraph` wrapper) to define the conversation
trees for at least **three NPCs**.

### Requirements

| Requirement | Description |
|-------------|-------------|
| 3+ NPCs | Each must be distinct (name, position, sprite, personality) |
| 4+ nodes per NPC | Each conversation must have at least four dialog states |
| Branching | At least one NPC must have a node with two or more choices |
| Loop | At least one NPC must have an edge that leads back to an earlier node |
| AI node | At least one NPC must have an `"ai"` node (see Part 4) |

### How `DialogGraph` works

```python
from dialog_graph import DialogGraph

dg = DialogGraph("Merchant")

# Add dialog states (nodes)
dg.add_dialog_node("menu",  "Welcome! What are you looking for?")
dg.add_dialog_node("potions", "I have healing potions — 50 gold each.")
dg.add_dialog_node("bye",     "Come back soon!", node_type="end")

# Add player choices (edges)
dg.add_choice("menu",    "potions", "Show me your potions.")
dg.add_choice("menu",    "bye",     "Nothing, goodbye.")
dg.add_choice("potions", "menu",    "Let me look at something else.")  # loop
dg.add_choice("potions", "bye",     "No thanks.")

dg.set_start("menu")
```

`node_type` options:
- `"fixed"` — static pre-written text (default)
- `"ai"`    — Gemini generates the response at runtime (Part 4)
- `"end"`   — conversation closes after the player acknowledges

Add each NPC to `NPC_DATA` at the bottom of the file, adjusting `grid_x` / `grid_y`
so NPCs stand in walkable areas of your map.

---

## Part 3: Create NPC Sprites (10 pts)

**Folder:** `graphics/npcs/`

Each NPC needs a 64×64 pixel sprite image saved as `idle.png` in its own subfolder:

```
graphics/npcs/
├── town_elder/
│   └── idle.png
├── merchant/
│   └── idle.png
└── sage/
    └── idle.png
```

### Requirements

- At least **3 unique sprites**, one for each NPC.
- Each must be **64×64 pixels**, PNG format.
- Must be **original art** — created by you in a pixel-art editor.
  Recommended free tools: [Piskel](https://www.piskelapp.com/),
  [LibreSprite](https://libresprite.github.io/), [Aseprite](https://www.aseprite.org/).
- The `sprite_name` key in `NPC_DATA` must match the folder name.

To generate colored placeholder images while you work on your art:
```bash
python code/game/generate_npc_sprites.py
```
Replace each placeholder with real art before submitting.

---

## Part 4: Gemini AI Integration (15 pts)

**File:** `code/game/ai_npc.py`  (read the setup instructions at the top)

One-time setup:
1. Get a **free** API key at <https://aistudio.google.com/> (Google account required).
2. Install the SDK: `pip install google-generativeai`
3. Set `GEMINI_API_KEY` as an environment variable (see `ai_npc.py` for details).

In `dialog_data.py`:

```python
from ai_npc import AIHandler

sage_ai = AIHandler(
    personality=(
        "You are Elara, an ancient sage in a fantasy RPG. "
        "You speak in riddles and old-world prose. "
        "Keep responses under three sentences."
    )
)
```

Mark the dialog node that should use Gemini as `node_type="ai"`:
```python
dg.add_dialog_node("wisdom", "Elara gazes into the distance...", node_type="ai")
```

Pass the handler to the NPC in `NPC_DATA`:
```python
{"name": "Elara the Sage", ..., "ai_handler": sage_ai}
```

When the player reaches an `"ai"` node in-game, the dialog box shows `"..."` briefly
while Gemini generates a response, then displays it.

### Requirements

- At least one NPC must have a working `"ai"` node.
- The `AIHandler` must have a custom `personality` string that fits the NPC's role.
- Your `.env` or environment variable must be set up so the game works locally
  (the TA will test with their own key if yours is missing).

---

## Part 5: Write Tests (5 pts)

**File:** `code/game/datastructures/tests/graph_tests.py`

Three example tests are provided. Write at least **eight additional tests** covering:

- `add_node`, `add_edge`, `has_node`, `has_edge`, `get_node_data`
- `remove_node`, `remove_edge`
- `bfs` — check both visited set and that start node is first
- `dfs` — check both visited set and that start node is first
- `shortest_path` — simple path, no path (disconnected), self-path
- Directed vs. undirected edge semantics
- Edge cases: isolated node, disconnected graph

---

## Part 6: Complexity Analysis (5 pts)

**Files:** `code/game/datastructures/complexity/`

1. Run the benchmark:
   ```bash
   cd code/game/datastructures/complexity
   python graph_complexity.py
   ```
2. Paste the output into `analysis_write_up.md`.
3. Fill in the time-complexity table and answer the three reflection questions.

---

## Building and Running

### Start the game

```bash
cd code/game
python main.py YourName
```

Optional flags:
```bash
python main.py YourName --server localhost --port 8080 --serializer json
```

### Build and start the server (optional — for multiplayer)

```bash
cd code/server
make
./server
```

### Controls

| Key        | Action                        |
|------------|-------------------------------|
| Arrow keys | Move                          |
| T          | Talk to nearby NPC            |
| ↑ / ↓      | Navigate dialog choices       |
| Enter      | Confirm choice / close dialog |
| Esc        | Close dialog / quit           |
| Space      | Attack                        |
| I          | Inventory                     |
| R          | Rewind (single-player)        |
| F          | Replay (single-player)        |
| N          | Toggle enemy debug view       |
| M          | Reset enemy patrols           |

---

## Grading Rubric

| Part | Description | Impl | Tests | Total |
|------|-------------|-----:|------:|------:|
| Part 1 | Graph — `__init__`, `add_node`, `add_edge`, `remove_*`, `has_*` | 12 | | |
| Part 1 | Graph — `get_neighbors`, `get_node_data`, `nodes`, `__len__`, `__str__` | 6 | | |
| Part 1 | Graph — `bfs`, `dfs`, `shortest_path` | 12 | | |
| Part 1 | Automated tests (GitHub Classroom CI) | | 10 | **40** |
| Part 2 | NPC dialog trees (3+ NPCs, branching, loop, AI node) | 20 | | **20** |
| Part 3 | Original NPC sprites (3+ unique, 64×64, correct folder) | 10 | | **10** |
| Part 4 | Gemini integration (working AI node, custom personality) | 15 | | **15** |
| Part 5 | Student-written tests (8+ covering all methods) | 5 | | **5** |
| Part 6 | Complexity analysis (benchmarks + write-up) | 5 | | **5** |
| Docs  | `ai_conversations.md` — complete log of AI tool use | 5 | | **5** |
| **Total** | | **90** | **10** | **100** |

Implementation points are graded from your code. Automated test points are awarded
by GitHub Classroom CI when you push.

---

## Documentation Requirements

Every file you modify must have:
- Your name and date at the top.
- Docstrings for every method you implement.
- Time-complexity annotations (e.g. `# O(V + E)`) for each graph method.

---

## Academic Integrity

You may discuss high-level approaches with classmates, but all code you submit must
be your own. Sharing or copying code is prohibited.

You **must** log all AI tool use in `ai_conversations.md`. This includes any use of
ChatGPT, Claude, Copilot, Gemini (for code help), or similar tools while writing
your implementation. The Gemini API calls your NPC makes at runtime are a
*game feature*, not AI tool use for coding — do not log those here.
