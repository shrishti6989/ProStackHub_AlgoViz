"""Records every algorithm step so the UI can replay it."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Step:
    """A single snapshot of algorithm state."""
    index: int
    description: str
    state: Dict[str, Any] = field(default_factory=dict)


class StepRecorder:
    """Collects ordered Steps during algorithm execution."""

    def __init__(self) -> None:
        self._steps: List[Step] = []

    def record(self, description: str, **state: Any) -> None:
        self._steps.append(
            Step(index=len(self._steps), description=description, state=state)
        )

    def __len__(self) -> int:
        return len(self._steps)

    def __getitem__(self, i: int) -> Step:
        return self._steps[i]

    def all(self) -> List[Step]:
        return list(self._steps)

    def clear(self) -> None:
        self._steps.clear()
