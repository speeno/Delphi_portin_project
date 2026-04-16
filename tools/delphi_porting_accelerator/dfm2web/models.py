from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DfmNode:
    kind: str
    name: str
    class_name: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list['DfmNode'] = field(default_factory=list)

    def add_child(self, child: 'DfmNode') -> None:
        self.children.append(child)

    def to_dict(self) -> dict[str, Any]:
        return {
            'kind': self.kind,
            'name': self.name,
            'class_name': self.class_name,
            'props': self.props,
            'children': [child.to_dict() for child in self.children],
        }
