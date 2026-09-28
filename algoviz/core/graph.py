"""Graph data structure supporting weighted, directed/undirected graphs."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math


@dataclass
class Edge:
    u: int
    v: int
    weight: float = 1.0


@dataclass
class Graph:
    directed: bool = False
    nodes: Dict[int, Tuple[float, float]] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)

    def add_node(self, node_id: int, x: float = 0.0, y: float = 0.0) -> None:
        self.nodes[node_id] = (x, y)

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        if u not in self.nodes or v not in self.nodes:
            raise ValueError(f"Both nodes must exist: {u}, {v}")
        self.edges.append(Edge(u, v, weight))
        if not self.directed:
            self.edges.append(Edge(v, u, weight))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        return [(e.v, e.weight) for e in self.edges if e.u == u]

    def adjacency(self) -> Dict[int, List[Tuple[int, float]]]:
        adj: Dict[int, List[Tuple[int, float]]] = {n: [] for n in self.nodes}
        for e in self.edges:
            adj[e.u].append((e.v, e.weight))
        return adj

    def num_nodes(self) -> int:
        return len(self.nodes)

    def num_edges(self) -> int:
        return len(self.edges) // (1 if self.directed else 2)

    @staticmethod
    def euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])
