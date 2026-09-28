"""Common interface every algorithm must implement."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict

from algoviz.core.graph import Graph
from algoviz.core.step_recorder import StepRecorder


class Algorithm(ABC):
    """Base class for all visualizable algorithms."""

    name: str = "Algorithm"
    time_complexity: str = "O(?)"
    space_complexity: str = "O(?)"

    @abstractmethod
    def run(self, graph: Graph, recorder: StepRecorder, **kwargs: Any) -> Dict[str, Any]:
        """Execute the algorithm, record steps, and return a result dict."""
        raise NotImplementedError
