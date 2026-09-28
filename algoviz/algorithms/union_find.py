"""Union-Find (Disjoint Set Union) with path compression + union by rank."""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

from algoviz.algorithms.base import Algorithm
from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder


class UnionFind(Algorithm):
    name = "Union-Find (DSU)"
    time_complexity = "O(alpha(n)) per op (near-constant)"
    space_complexity = "O(n)"

    def run(
        self,
        graph: Graph,
        recorder: StepRecorder,
        union_pairs: List[Tuple[int, int]] | None = None,
        **_: Any,
    ) -> Dict[str, Any]:
        parent = {n: n for n in graph.nodes}
        rank = {n: 0 for n in graph.nodes}

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        recorder.record(
            "Initialize: each node is its own parent",
            parent=dict(parent),
            rank=dict(rank),
        )

        if union_pairs is None:
            union_pairs = [(e.u, e.v) for e in graph.edges]

        for u, v in union_pairs:
            ru, rv = find(u), find(v)
            recorder.record(
                f"Find({u}) = {ru}, Find({v}) = {rv}",
                parent=dict(parent),
                rank=dict(rank),
                highlight=(u, v),
            )
            if ru == rv:
                recorder.record(
                    f"{u} and {v} already connected - skip",
                    parent=dict(parent),
                    rank=dict(rank),
                )
                continue

            if rank[ru] < rank[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
            recorder.record(
                f"Union: parent[{rv}] = {ru}",
                parent=dict(parent),
                rank=dict(rank),
                highlight=(u, v),
            )

        return {
            "parent": parent,
            "rank": rank,
            "components": len({find(n) for n in graph.nodes}),
        }
