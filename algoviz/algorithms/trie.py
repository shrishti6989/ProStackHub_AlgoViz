"""Trie construction + search visualization."""
from __future__ import annotations
from typing import Any, Dict, List

from algoviz.algorithms.base import Algorithm
from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder


class _TrieNode:
    __slots__ = ("children", "is_end", "node_id")

    def __init__(self, node_id: int) -> None:
        self.children: Dict[str, "_TrieNode"] = {}
        self.is_end = False
        self.node_id = node_id


class Trie(Algorithm):
    name = "Trie Construction"
    time_complexity = "Insert O(m), Search O(m) - m = word length"
    space_complexity = "O(total characters)"

    def run(
        self,
        graph: Graph,
        recorder: StepRecorder,
        words: List[str] | None = None,
        **_: Any,
    ) -> Dict[str, Any]:
        if words is None:
            words = ["cat", "car", "cart", "dog", "do"]

        counter = [0]
        root = _TrieNode(counter[0])
        counter[0] += 1

        def snapshot(prefix="", highlight=None):
            edges = []
            stack = [(root, "")]
            while stack:
                cur, pre = stack.pop()
                for ch, child in cur.children.items():
                    edges.append((cur.node_id, child.node_id, ch))
                    stack.append((child, pre + ch))
            return {
                "edges": edges,
                "is_end_nodes": self._end_nodes(root),
                "prefix": prefix,
                "highlight": highlight,
            }

        recorder.record("Trie initialized (root)", **snapshot())

        for word in words:
            node = root
            for i, ch in enumerate(word):
                if ch not in node.children:
                    node.children[ch] = _TrieNode(counter[0])
                    counter[0] += 1
                    recorder.record(
                        f"Insert '{word}': create node for '{ch}'",
                        **snapshot(word[: i + 1], highlight=ch),
                    )
                else:
                    recorder.record(
                        f"Insert '{word}': follow existing '{ch}'",
                        **snapshot(word[: i + 1], highlight=ch),
                    )
                node = node.children[ch]
            node.is_end = True
            recorder.record(
                f"Mark '{word}' as complete word",
                **snapshot(word),
            )

        return {"num_nodes": counter[0], "words": words}

    @staticmethod
    def _end_nodes(root):
        out, stack = [], [root]
        while stack:
            cur = stack.pop()
            if cur.is_end:
                out.append(cur.node_id)
            stack.extend(cur.children.values())
        return out
