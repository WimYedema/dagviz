from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Mapping, Tuple

import networkx as nx
import networkx.algorithms.dag as dag


class iRowBuilder(ABC):
    @abstractmethod
    def map_node(self, nd: Any) -> Tuple[int, int]:
        ...

    @abstractmethod
    def unmap_node(self, nd: Any) -> None:
        ...

    @abstractmethod
    def node_column(self, nd: Any) -> int:
        ...


class AbstractColumn:
    column: int
    start_row: "AbstractRow"
    next_row: "AbstractRow"
    color: int
    remaining: int
    is_input: bool
    is_node: bool

    @property
    def is_last(self) -> bool:
        return self.remaining == 0

    def __init__(
        self, column: int, row: "AbstractRow", color: int = 0, remaining: int = 0
    ):
        self.column = column
        self.start_row = row
        self.next_row = row
        self.color = color
        self.remaining = remaining
        self.is_input = False
        self.is_node = False

    @staticmethod
    def copyFromLast(other: "AbstractColumn") -> "AbstractColumn":
        return AbstractColumn(
            other.column, other.next_row, other.color, other.remaining
        )


class AbstractRow:
    _builder: iRowBuilder
    row: int
    columns: Dict[int, AbstractColumn]
    label: str

    def __iter__(self) -> Iterator[AbstractColumn]:
        for col in sorted(self.columns.values(), key=lambda c: c.column):
            yield col

    def __init__(
        self,
        builder: iRowBuilder,
        row: int,
        columns: Mapping[Any, AbstractColumn],
        label: str,
    ):
        self._builder = builder
        self.row = row
        self.columns = {
            k: AbstractColumn.copyFromLast(s)
            for k, s in columns.items()
            if s.remaining != 0
        }
        self.label = label

    def add_input(self, pred: Any) -> None:
        col = self._builder.node_column(pred)
        self.columns[col].is_input = True
        self.columns[col].remaining -= 1
        if self.columns[col].remaining == 0:
            self._builder.unmap_node(pred)

    def add_node(self, nd: Any, nsuccs: int) -> None:
        col, color = self._builder.map_node(nd)
        if col not in self.columns:
            self.columns[col] = AbstractColumn(col, self)
        self.columns[col].remaining = nsuccs
        self.columns[col].color = color
        self.columns[col].is_node = True
        self.columns[col].next_row = self
        if nsuccs == 0:
            self._builder.unmap_node(nd)


@dataclass
class AbstractPlot(iRowBuilder):
    columns: range = range(0)
    colors: int = 0
    _gaps: List[int] = field(default_factory=list)
    _mapping: Dict[Any, int] = field(default_factory=dict)
    rows: List["AbstractRow"] = field(default_factory=list)

    def add_row(self, label: str) -> AbstractRow:
        index = len(self.rows)
        if index == 0:
            row = AbstractRow(self, 0, {}, label)
        else:
            row = AbstractRow(self, index, self.rows[-1].columns, label)
        self.rows.append(row)
        return row

    def map_node(self, nd: Any) -> Tuple[int, int]:
        if len(self._gaps) == 0:
            col = self.columns.start
            self.columns = range(self.columns.start - 1, self.columns.stop)
        else:
            col = self._gaps.pop()
        self._mapping[nd] = col
        self.colors += 1
        return col, self.colors - 1

    def unmap_node(self, nd: Any) -> None:
        col = self._mapping[nd]
        self._gaps.append(col)

    def node_column(self, nd: Any) -> int:
        return self._mapping[nd]


def plot_graph(G: nx.Graph) -> AbstractPlot:
    plot = AbstractPlot()
    for i, nd in enumerate(list(dag.topological_sort(G))):
        row = plot.add_row(G.nodes[nd].get("label", f"{nd}"))
        for pred in G.pred[nd]:
            row.add_input(pred)

        row.add_node(nd, len(G.succ[nd]))

    return plot
