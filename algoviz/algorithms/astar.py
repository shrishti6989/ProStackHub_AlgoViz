"""A* pathfinding using Euclidean heuristic on node coordinates."""
from __future__ import annotations
import heapq
from typing import Any, Dict, Optional

from algoviz.algorithms.base import Algorithm
from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder


class AStar(Algorithm):
    name = "A* Pathfinding"
    time_complexity = "O(E log V) (depends on heuristic)"
    space_complexity = "O(V)"

    def run(
        self,
        graph: Graph,
        recorder: StepRecorder,
        start: int = 0,
        end: int = 1,
        **_: Any,
    ) -> Dict[str, Any]:
        if start not in graph.nodes or end not in graph.nodes:
            raise ValueError("Start and end nodes must exist")

        def h(n: int) -> float:
            return Graph.euclidean(graph.nodes[n], graph.nodes[end])

        adj = graph.adjacency()
        g = {n: float("inf") for n in graph.nodes}
        g[start] = 0
        prev: Dict[int, Optional[int]] = {n: None for n in graph.nodes}
        open_set = [(h(start), start)]
        closed = set()

        recorder.record(
            f"Start A* from {start} to {end}",
            open=set([start]),
            closed=set(),
        )

        while open_set:
            _, u = heapq.heappop(open_set)
            if u in closed:
                continue
            closed.add(u)
            recorder.record(
                f"Expand node {u} (g={g[u]:.2f}, f={g[u] + h(u):.2f})",
                open={n for _, n in open_set},
                closed=set(closed),
                current=u,
            )

            if u == end:
                break

            for v, w in adj[u]:
                if v in closed:
                    continue
                tentative = g[u] + w
                if tentative < g[v]:
                    g[v] = tentative
                    prev[v] = u
                    heapq.heappush(open_set, (tentative + h(v), v))
                    recorder.record(
                        f"Update {v}: g={g[v]:.2f}, f={g[v] + h(v):.2f}",
                        open={n for _, n in open_set},
                        closed=set(closed),
                        current=u,
                    )

        path = self._reconstruct(prev, start, end)
        recorder.record("A* complete", open=set(), closed=set(closed), path=path)
        return {"g": g, "previous": prev, "path": path}

    @staticmethod
    def _reconstruct(prev, start, end):
        if end not in prev or (prev[end] is None and end != start):
            return []
        path, node = [], end
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        return path if path and path[0] == start else []
