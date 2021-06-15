from typing import Callable, List

import svgwrite as svg  # type: ignore
from IPython.display import SVG  # type: ignore

from .abstract import AbstractColumn, AbstractPlot
from .draw_style import Style


def toSvg(plot: AbstractPlot, styler: Callable[..., Style]) -> SVG:
    d = svg.Drawing()

    style: Style = styler(d, plot.colors, -plot.columns.start)
    for row in plot.rows:
        last_col = 0
        arcs: List[AbstractColumn] = []
        nodepos = (0, 0)
        node_pos = 1
        for col in row:
            last_col = col.column
            curpos = (col.column, row.row)
            if col.is_node:
                nodepos = curpos
                style.place_node(curpos, col.color)
                if len(arcs) != 0:
                    style.place_left_hline(
                        (arcs[0].column, row.row), curpos, arcs[0].color
                    )
                    arcs = []
                arcs.append(col)

                node_pos = 0
            if col.is_input:
                if node_pos < 0:
                    arcs.append(col)
                    style.place_left_arc(curpos, col.color)
                    if col.is_last:
                        style.place_vline_arc(
                            (col.column, col.start_row.row),
                            curpos,
                            col.start_row.columns[col.column].color,
                        )

                elif node_pos == 0:
                    style.place_vline_node(
                        (col.column, col.start_row.row),
                        curpos,
                        col.start_row.columns[col.column].color,
                    )
                else:
                    arcs.append(col)
                    style.place_right_arc(curpos, col.color)
                    if col.is_last:
                        style.place_vline_arc(
                            (col.column, col.start_row.row),
                            curpos,
                            col.start_row.columns[col.column].color,
                        )
            if col.is_node:
                node_pos = -1
        if len(arcs) >= 2:
            style.place_right_hline(
                (arcs[0].column, row.row), (arcs[-1].column, row.row), arcs[-1].color
            )

        style.place_label(nodepos, (last_col + 1, row.row), row.label)

    t, l, b, r = style.box
    d.viewbox(l, t, r - l, b - t)
    return SVG(d.tostring())
