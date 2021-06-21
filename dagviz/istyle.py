"""
Interface for rendering a plot.
"""
from abc import ABC, abstractmethod
from typing import Tuple


class iStyle(ABC):
    """
    Visualization style interface. This interface is used to render the
    various components of the plot. All component coordinates tuples of
    (column, row), and the colors are indices of a palette that must be
    specified by the style.
    """

    @abstractmethod
    def dumps(self) -> str:
        """
        Produce a string for the rendering of the graph.

        Returns:
            a string representing the graph in the appropriate format.
        """
        ...

    @abstractmethod
    def place_node(self, at: Tuple[int, int], color: int) -> None:
        """
        Place a node on the plot.

        Args:
            at:    The (column, row) coordinate of the node
            color: The color number to use for this node
        """
        ...

    @abstractmethod
    def place_left_hline(
        self, left: Tuple[int, int], right: Tuple[int, int], color: int
    ) -> None:
        """
        Place a horizontal line from a node input on to a node, where the
        input is on the left of the node.

        Args:
            left:  The (column, row) coordinate of the node input.
            right: The (column, row) coordinate of the node .
            color: The color number to use for this line.

        Note:
            The rows of *left* and *right* will have the same value.
        """
        ...

    @abstractmethod
    def place_right_hline(
        self, left: Tuple[int, int], right: Tuple[int, int], color: int
    ) -> None:
        """
        Place a horizontal line from a node input on to a node, where the
        input is on the right of the node.

        Args:
            left:  The (column, row) coordinate of the node.
            right: The (column, row) coordinate of the node input.
            color: The color number to use for this line.

        Note:
            The rows of *left* and *right* will have the same value.
        """
        ...

    @abstractmethod
    def place_vline_arc(
        self, top: Tuple[int, int], bottom: Tuple[int, int], color: int
    ) -> None:
        """
        Place a vertical line from a node to a node input, where the input
        is either on the left or the right of the node, but not in the same
        column.

        Args:
            top:    The (column, row) coordinate of the node.
            bottom: The (column, row) coordinate of the node input.
            color:  The color number to use for this line.

        Note:
            The columns of *top* and *bottom* will have the same value.
        """
        ...

    @abstractmethod
    def place_vline_node(
        self, top: Tuple[int, int], bottom: Tuple[int, int], color: int
    ) -> None:
        """
        Place a vertical line from a node to a node input, where the input
        is on the same column as the node.

        Args:
            top:    The (column, row) coordinate of the node.
            bottom: The (column, row) coordinate of the node input.
            color:  The color number to use for this line.

        Note:
            The columns of *top* and *bottom* will have the same value.
        """
        ...

    @abstractmethod
    def place_left_arc(self, at: Tuple[int, int], color: int) -> None:
        """
        Place an arc from the top to the left.

        Args:
            at:     The (column, row) coordinate of the arc.
            color:  The color number to use for this arc.
        """
        ...

    @abstractmethod
    def place_right_arc(self, at: Tuple[int, int], color: int) -> None:
        """
        Place an arc from the top to the right.

        Args:
            at:     The (column, row) coordinate of the arc.
            color:  The color number to use for this arc.
        """
        ...

    @abstractmethod
    def place_label(
        self, nodepos: Tuple[int, int], at: Tuple[int, int], label: str
    ) -> None:
        """
        Place a label for a node.

        Args:
            nodepos: The (column, row) coordinate of the node.
            at:      The (column, row) coordinate of the label.
            label:   The text to display
        """
        ...
