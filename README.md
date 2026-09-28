# ProStackHub_AlgoViz

**Algorithm Visualization Engine** — an interactive web app that animates classic competitive-programming algorithms step by step.

Built as part of the **ProStackHub Python Programming Internship**.

## Features

- 5 algorithms visualized: Dijkstra, A*, Union-Find, Segment Tree, Trie
- Step-by-step playback: pause / play / forward / backward
- Interactive Plotly graph: hover, zoom, pan
- Live node coloring (unvisited / visited / current)
- Edge relaxation highlighting
- Final shortest-path overlay in red
- Complexity analysis: theoretical vs actual step count

## Tech Stack

- Python 3.10+
- Streamlit (UI)
- Plotly (graph rendering)
- NetworkX (layout helpers)

## Installation

    git clone https://github.com/your-username/ProStackHub_AlgoViz.git
    cd ProStackHub_AlgoViz
    pip install -r requirements.txt

## Running

    streamlit run algoviz/ui/app.py

Open http://localhost:8501

## Project Structure

    algoviz/
      core/          graph.py, step_recorder.py, complexity.py
      algorithms/    dijkstra.py, astar.py, union_find.py,
                     segment_tree.py, trie.py, base.py
      ui/            app.py
    tests/
    requirements.txt

## Algorithms

- Dijkstra — O((V + E) log V)
- A* — O(E log V), Euclidean heuristic
- Union-Find — O(alpha(n)) per operation
- Segment Tree — O(n) build, O(log n) query
- Trie — O(m) insert/search (m = word length)

## Author

Sudhir Pandey — ProStackHub Python Internship, 2026
