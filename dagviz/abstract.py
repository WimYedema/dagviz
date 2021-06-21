"""
Abstract table-like representation of a DAG visualization.

Like a table, a DAG visualization has a number of rows. Each row has a
number of columns, but empty columns are not represented in the row.
Each cell (column, row) will have information regarding:

* whether it contains a node
* whether it contains an input for the node on this row
* what the color is of the item in this cell
* how many successor are remaining for the active node in this column

This information can later be used to render the plot.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Mapping, Tuple


class iRowBuilder(ABC):
    """
    Interface for mapping nodes to columns.
    """

    @abstractmethod
    def map_node(self, nd: Any) -> Tuple[int, int]:
        """
        Assign a new node to a column.

        Args:
            nd: the node to add
        Returns:
            (column, color) of the node.
        """
        ...

    @abstractmethod
    def unmap_node(self, nd: Any) -> None:
        """
        Remove a node, freeing the column for new nodes.

        Args:
            nd: the node to remove
        """
        ...

    @abstractmethod
    def node_column(self, nd: Any) -> int:
        """
        Fetch the column that a node has been mapped to.

        Args:
            nd: A mapped node
        Returns:
            The column number the node was assigned to.
        """
        ...


class AbstractColumn:
    "Column information for a single row."

    column: int
    "The column number, can be positive and negative."

    start_row: "AbstractRow"
    "The row that contains the active node."

    next_row: "AbstractRow"
    "The value of start_row for the next row."

    color: int
    "The color number for the item in this column."

    remaining: int
    "The number of remaining successors for the node in `start_row`."

    is_input: bool
    "Does this (column, row) contain an input?"

    is_node: bool
    "Does this (column, row) contain a node?"

    @property
    def is_last(self) -> bool:
        "Is this the last successor of the node in `start_row`"
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
    def copy_from_last(other: "AbstractColumn") -> "AbstractColumn":
        "copy relevant column information from the previous row"
        return AbstractColumn(
            other.column, other.next_row, other.color, other.remaining
        )


class AbstractRow:
    """
    An abstract row containing a single (labeled) node, an arbitrary number
    of inputs, and an arbitrary number of edges.

    A row is iterable, iterating over the columns from left to right.
    """

    _builder: iRowBuilder
    row: int
    "The 0-based index of this row"

    columns: Dict[int, AbstractColumn]
    "The columns in this row. The keys are integers, but can have arbitrary values, smaller integers are on the left."

    label: str
    "The label of the node on this row."

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
        """
        Construct a new abstract row.

        Args:
            builder: interface to map nodes to columns
            row:     the index of this row
            columns: the columns of the previous node, or {}
            label:   the label of the node on this row
        """
        self._builder = builder
        self.row = row
        self.columns = {
            k: AbstractColumn.copy_from_last(s)
            for k, s in columns.items()
            if s.remaining != 0
        }
        self.label = label

    def add_input(self, pred: Any) -> None:
        """
        Add an input to the node on this row.

        Args:
            pred: a predecessor node of the node on this row
        """
        col = self._builder.node_column(pred)
        self.columns[col].is_input = True
        self.columns[col].remaining -= 1
        if self.columns[col].remaining == 0:
            self._builder.unmap_node(pred)

    def add_node(self, nd: Any, nsuccs: int) -> None:
        """
        Add the node of this row. This method must be called exactly once
        for each row.

        Args: nd:     the node, this is only used as identifier nsuccs: the
            number of successors of `nd`
        """
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
    """
    An abstract table-like visualization of a DAG.
    """

    columns: range = range(0)
    "The range of columns present in the rows. Does not need to start at 0."

    colors: int = 0
    "The number of colors in this plot."

    rows: List["AbstractRow"] = field(default_factory=list)
    "The rows of this visualization."

    _gaps: List[int] = field(default_factory=list)
    _mapping: Dict[Any, int] = field(default_factory=dict)

    def add_row(self, label: str) -> AbstractRow:
        """
        Add a new row to the bottom of this visualization.

        Args:
            label: the label of the node in this row.
        Returns:
            The AbstractRow that was added.
        """
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
