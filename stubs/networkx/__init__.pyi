from typing import Any, Mapping


class Node:
    def get(self, key: str, deflt: Any) -> Any:
        ...

class Edge:
    ...

class Graph:
    nodes: Mapping[Any, Node]
    edges: Mapping[Any, Edge]
    pred: Mapping[Any, Mapping[Any, Node]]
    succ: Mapping[Any, Mapping[Any, Node]]