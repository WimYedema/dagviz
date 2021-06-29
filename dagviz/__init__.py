"""
DAGVIZ provides a simple visualization of Directed Acyclic Graphs.
"""
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__)  # type: ignore

from typing import Any, Callable, Sequence, Union

import networkx as nx
from networkx.algorithms import dag

from .abstract import AbstractPlot
from .render import render
from .istyle import iStyle
from .style import metro
from .dagre import Dagre  # noqa


def make_abstract_plot(
    G: nx.Graph,
    *,
    order: Union[Sequence[Any], Callable[..., Sequence[Any]]] = dag.topological_sort,
) -> AbstractPlot:
    """Generate an abstract plot for a DAG.

    The abstract plot comprises a sequence of rows with varying number of
    columns, where each column provide information on what it contains.

    Args:
        G:     The DAG to be visualized
        order: Optional; The order of the nodes, or a function that creates an order
               from the graph. The default is to use a topological sort of the nodes.

    Returns:
        An abstract plot of the graph that can be used to render an image from.
    """
    plot = AbstractPlot()
    if isinstance(order, Sequence):
        sequence = order
    else:
        sequence = order(G)
    for nd in sequence:
        row = plot.add_row(G.nodes[nd].get("label", f"{nd}"))
        for pred in G.pred[nd]:
            row.add_input(pred)

        row.add_node(nd, len(G.succ[nd]))

    return plot


def render_svg(
    G: nx.Graph, *, style: Callable[..., iStyle] = metro.svg_renderer()
) -> str:
    """
    Generate a DAG visualization as an SVG string.

    Args:
        G:     The DAG to visualize
        style: Optional; The visualization style to apply
    Returns:
        A string containing the SVG of the plot
    """
    return render(make_abstract_plot(G), style)


class Metro:
    """
    Render a topological ordering of a DAG using the "metro" style in
    jupyter notebooks.

    Args:
        G: directed acyclic graph to render
    """

    def __init__(self, G: nx.DiGraph):
        self.graph = G

    def _repr_html_(self) -> str:
        return render_svg(self.graph)
