"""Segment Tree with range-sum queries and point updates."""
from __future__ import annotations
from typing import Any, Dict, List

from algoviz.algorithms.base import Algorithm
from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder


class SegmentTree(Algorithm):
    name = "Segment Tree (Range Sum)"
    time_complexity = "Build O(n), Query/Update O(log n)"
    space_complexity = "O(n)"

    def run(
        self,
        graph: Graph,
        recorder: StepRecorder,
        array: List[float] | None = None,
        queries: List[tuple] | None = None,
        **_: Any,
    ) -> Dict[str, Any]:
        if array is None:
            array = [1.0] * max(graph.num_nodes(), 1)
        n = len(array)
        tree = [0.0] * (4 * n)

        def build(node: int, l: int, r: int) -> None:
            if l == r:
                tree[node] = array[l]
                return
            mid = (l + r) // 2
            build(2 * node, l, mid)
            build(2 * node + 1, mid + 1, r)
            tree[node] = tree[2 * node] + tree[2 * node + 1]

        build(1, 0, n - 1)
        recorder.record(
            "Segment tree built",
            tree=list(tree),
            array=list(array),
        )

        if queries is None:
            queries = [(0, n - 1)]

        results = []
        for ql, qr in queries:
            total = self._query(tree, 1, 0, n - 1, ql, qr)
            results.append(total)
            recorder.record(
                f"Range sum [{ql}, {qr}] = {total}",
                tree=list(tree),
                query=(ql, qr),
                result=total,
            )

        return {"tree": tree, "array": array, "query_results": results}

    @staticmethod
    def _query(tree, node, l, r, ql, qr):
        if qr < l or r < ql:
            return 0.0
        if ql <= l and r <= qr:
            return tree[node]
        mid = (l + r) // 2
        return (
            SegmentTree._query(tree, 2 * node, l, mid, ql, qr)
            + SegmentTree._query(tree, 2 * node + 1, mid + 1, r, ql, qr)
        )
