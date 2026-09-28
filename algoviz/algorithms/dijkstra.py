"""Dijkstra's shortest path with step-by-step recording."""
from __future__ import annotations
import heapq
from typing import Any, Dict, Optional

from algoviz.algorithms.base import Algorithm
from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder


class Dijkstra(Algorithm):
    name = "Dijkstra's Shortest Path"
    time_complexity = "O((V + E) log V)"
    space_complexity = "O(V)"

    def run(
        self,
        graph: Graph,
        recorder: StepRecorder,
        start: int = 0,
        end: Optional[int] = None,
        **_: Any,
    ) -> Dict[str, Any]:
        if start not in graph.nodes:
            raise ValueError(f"Start node {start} not in graph")

        adj = graph.adjacency()
        dist = {n: float("inf") for n in graph.nodes}
        prev: Dict[int, Optional[int]] = {n: None for n in graph.nodes}
        dist[start] = 0
        visited = set()

        recorder.record(
            f"Initialize: dist[{start}] = 0, all others = infinity",
            dist=dict(dist),
            visited=set(),
            current=None,
        )

        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue

            visited.add(u)
            recorder.record(
                f"Visit node {u} with distance {d}",
                dist=dict(dist),
                visited=set(visited),
                current=u,
            )

            for v, w in adj[u]:
                if v in visited:
                    continue
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
                    recorder.record(
                        f"Relax edge {u} to {v}: new dist[{v}] = {nd}",
                        dist=dict(dist),
                        visited=set(visited),
                        current=u,
                        relaxed_edge=(u, v),
                    )

        path = self._reconstruct(prev, start, end) if end is not None else []
        recorder.record(
            "Done. Shortest distances computed.",
            dist=dict(dist),
            visited=set(visited),
            current=None,
            path=path,
        )
        return {"distances": dist, "previous": prev, "path": path}

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
