from typing import Any, Iterable, Mapping, MappingView, Tuple

class Node:
    def get(self, key: str, deflt: Any) -> Any: ...

class Edge: ...

class EdgesView(MappingView):
    def data(self) -> Iterable[Tuple[Any, Any, Mapping[str, Any]]]: ...

class Graph:
    nodes: Mapping[Any, Node]
    edges: EdgesView
    pred: Mapping[Any, Mapping[Any, Node]]
    succ: Mapping[Any, Mapping[Any, Node]]

class DiGraph(Graph):
    pass
