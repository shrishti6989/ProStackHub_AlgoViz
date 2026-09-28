"""AlgoViz - Streamlit + Plotly interactive visualization."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import time
import streamlit as st
import plotly.graph_objects as go

from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder
from algoviz.core.complexity import analyze
from algoviz.algorithms.dijkstra import Dijkstra
from algoviz.algorithms.astar import AStar
from algoviz.algorithms.union_find import UnionFind
from algoviz.algorithms.segment_tree import SegmentTree
from algoviz.algorithms.trie import Trie


ALGOS = {
    "Dijkstra": Dijkstra,
    "A*": AStar,
    "Union-Find": UnionFind,
    "Segment Tree": SegmentTree,
    "Trie": Trie,
}


def _demo_graph() -> Graph:
    g = Graph(directed=False)
    coords = {
        0: (0, 0),
        1: (1, 2),
        2: (2, 1),
        3: (3, 3),
        4: (4, 0),
        5: (5, 2),
    }
    for n, (x, y) in coords.items():
        g.add_node(n, x, y)
    edges = [
        (0, 1, 2.0),
        (0, 2, 4.0),
        (1, 2, 1.0),
        (1, 3, 7.0),
        (2, 4, 3.0),
        (3, 5, 1.0),
        (4, 5, 5.0),
        (2, 3, 2.0),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g


def init_state():
    defaults = {
        "graph": _demo_graph(),
        "steps": [],
        "cursor": 0,
        "playing": False,
        "algo_name": "Dijkstra",
        "report": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def make_plotly_figure(g: Graph, step_state: dict | None = None):
    fig = go.Figure()

    edge_x, edge_y = [], []
    for e in g.edges:
        x0, y0 = g.nodes[e.u]
        x1, y1 = g.nodes[e.v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="#bdbdbd", width=1.5),
        hoverinfo="none",
        showlegend=False,
    ))

    if step_state and step_state.get("relaxed_edge"):
        u, v = step_state["relaxed_edge"]
        x0, y0 = g.nodes[u]
        x1, y1 = g.nodes[v]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode="lines",
            line=dict(color="#ff9800", width=5),
            hoverinfo="none",
            showlegend=False,
        ))

    if step_state and step_state.get("path"):
        path = step_state["path"]
        for a, b in zip(path, path[1:]):
            x0, y0 = g.nodes[a]
            x1, y1 = g.nodes[b]
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode="lines",
                line=dict(color="#e53935", width=5),
                hoverinfo="none",
                showlegend=False,
            ))

    for e in g.edges:
        x0, y0 = g.nodes[e.u]
        x1, y1 = g.nodes[e.v]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        fig.add_trace(go.Scatter(
            x=[mx], y=[my],
            mode="text",
            text=[f"{e.weight:g}"],
            textfont=dict(size=11, color="#555"),
            hoverinfo="none",
            showlegend=False,
        ))

    node_x, node_y, node_text, node_colors = [], [], [], []
    visited = set(step_state.get("visited", set())) if step_state else set()
    current = step_state.get("current") if step_state else None

    for n, (x, y) in g.nodes.items():
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(n))
        if n == current:
            node_colors.append("#ffca28")
        elif n in visited:
            node_colors.append("#66bb6a")
        else:
            node_colors.append("#e0e0e0")

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        marker=dict(size=34, color=node_colors,
                    line=dict(color="#222", width=1.5)),
        text=node_text,
        textfont=dict(size=13, color="black"),
        textposition="middle center",
        hoverinfo="text",
        hovertext=[f"Node {n}" for n in g.nodes],
        showlegend=False,
    ))

    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="#fafafa",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x"),
        showlegend=False,
        uirevision="keep",
    )
    return fig


def run_algorithm(algo_name: str, start: int, end: int):
    rec = StepRecorder()
    g = st.session_state.graph
    algo = ALGOS[algo_name]()
    try:
        algo.run(g, rec, start=start, end=end)
    except Exception as exc:
        st.error(f"Algorithm error: {exc}")
        return
    st.session_state.steps = rec.all()
    st.session_state.cursor = 0
    st.session_state.playing = False
    st.session_state.algo_name = algo_name
    st.session_state.report = analyze(
        algo.name, g.num_nodes(), g.num_edges(), len(rec), algo.time_complexity
    )


def sidebar():
    st.sidebar.title("AlgoViz")
    st.sidebar.caption("Algorithm Visualization Engine")
    st.sidebar.divider()

    algo_name = st.sidebar.selectbox("Algorithm", list(ALGOS.keys()))

    col1, col2 = st.sidebar.columns(2)
    start = col1.number_input("Start", 0, 99, 0)
    end = col2.number_input("End", 0, 99, 5)

    if st.sidebar.button("Run Algorithm", use_container_width=True, type="primary"):
        run_algorithm(algo_name, start, end)
        st.rerun()

    if st.sidebar.button("Reset", use_container_width=True):
        st.session_state.steps = []
        st.session_state.cursor = 0
        st.session_state.playing = False
        st.session_state.report = None
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("Legend")
    st.sidebar.markdown(
        "- ⚪ Unvisited\n"
        "- 🟢 Visited\n"
        "- 🟡 Current\n"
        "- 🟠 Relaxed edge\n"
        "- 🔴 Final path"
    )
    return algo_name, start, end


def playback_bar():
    steps = st.session_state.steps
    if not steps:
        st.info("Click **Run Algorithm** in the sidebar to start.")
        return

    total = len(steps) - 1
    progress = (st.session_state.cursor / total) if total > 0 else 1.0
    st.progress(progress, text=f"Step {st.session_state.cursor + 1} / {len(steps)}")

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1.4, 1, 1])
    if c1.button("⏮", use_container_width=True, disabled=st.session_state.cursor == 0):
        st.session_state.cursor = 0
        st.rerun()
    if c2.button("◀", use_container_width=True, disabled=st.session_state.cursor == 0):
        st.session_state.cursor -= 1
        st.rerun()

    if c3.button(
        "⏸ Pause" if st.session_state.playing else "▶ Play",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.playing = not st.session_state.playing
        st.rerun()

    if c4.button("▶", use_container_width=True, disabled=st.session_state.cursor == total):
        st.session_state.cursor += 1
        st.rerun()
    if c5.button("⏭", use_container_width=True, disabled=st.session_state.cursor == total):
        st.session_state.cursor = total
        st.rerun()

    speed = st.slider("Speed (steps per second)", 0.5, 8.0, 2.0, 0.5)

    if st.session_state.playing:
        if st.session_state.cursor < total:
            time.sleep(1.0 / speed)
            st.session_state.cursor += 1
            st.rerun()
        else:
            st.session_state.playing = False
            st.rerun()


def step_panel():
    steps = st.session_state.steps
    if not steps:
        return
    cur = steps[st.session_state.cursor]
    st.markdown(
        f"<div style='padding:12px 16px;background:#e3f2fd;"
        f"border-left:4px solid #1976d2;border-radius:6px;"
        f"font-size:15px;color:#0d47a1;'>"
        f"<b>Step {cur.index + 1}:</b> {cur.description}</div>",
        unsafe_allow_html=True,
    )


def complexity_panel():
    r = st.session_state.report
    if not r:
        return
    st.subheader("Complexity Analysis")
    a, b, c = st.columns(3)
    a.metric("Theoretical", r.theoretical)
    b.metric("Actual steps", r.actual_steps)
    c.metric("Nodes / Edges", f"{r.n} / {r.m}")
    st.caption(r.note)


def main():
    st.set_page_config(page_title="AlgoViz", layout="wide")
    init_state()
    st.title("🧭 AlgoViz — Algorithm Visualization Engine")

    sidebar()

    left, right = st.columns([3, 2])

    with left:
        steps = st.session_state.steps
        state = steps[st.session_state.cursor].state if steps else None
        fig = make_plotly_figure(st.session_state.graph, state)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        playback_bar()
        st.divider()
        step_panel()

    st.divider()
    complexity_panel()


if __name__ == "__main__":
    main()
