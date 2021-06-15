import math
from dataclasses import dataclass
from typing import Any, Callable, Optional, Sequence, Tuple

import svgwrite as svg  # type: ignore

from .colors import palette

_XY = Tuple[float, float]


def _arc(
    dwg: svg.Drawing,
    p0: _XY,
    p1: _XY,
    radius: float,
    clockwise: bool = True,
    **kwargs: Any,
) -> Any:
    """ Adds an arc that bulges to the right as it moves from p0 to p1 """
    x0 = p0[0]
    y0 = p0[1]
    x1 = p1[0] - p0[0]
    y1 = p1[1] - p0[1]
    sweep = 1 if clockwise else 0
    ellipseRotation = 0  # has no effect for circles
    return dwg.path(
        d=f"M {x0},{y0} a{radius},{radius} {ellipseRotation} 0,{sweep} {x1},{y1}",
        **kwargs,
    )


@dataclass
class PlotConfig:
    scale: float = 10.0
    node_radius: float = 6.0
    node_fill: Optional[str] = None
    node_stroke: str = "white"
    node_stroke_width: float = 2.0
    edge_stroke_width: float = 2.0
    label_font_family: str = "sans-serif"
    label_arrow_stroke: str = "lightgrey"
    label_arrow_dash_array: str = "2"
    arc_radius: float = 15.0


default_config = PlotConfig()


class Style:
    d: svg.Drawing
    background: svg.container.Group
    edges: svg.container.Group
    nodes: svg.container.Group
    shift: int
    colors: Sequence[str]
    box_top: float
    box_left: float
    box_bottom: float
    box_right: float

    def __init__(
        self,
        d: svg.Drawing,
        config: PlotConfig,
        colors: int,
        shift: int = 0,
    ):
        self.d = d
        self.background = d.g()
        self.vlines = d.g()
        self.hline_borders = d.g()
        self.hlines = d.g()
        self.nodes = d.g()
        self.d.add(self.background)
        self.d.add(self.vlines)
        self.d.add(self.hline_borders)
        self.d.add(self.hlines)
        self.d.add(self.nodes)
        self._top = math.inf
        self._left = math.inf
        self._bottom = -math.inf
        self._right = -math.inf
        self.config = config
        self.shift = shift
        self.colors = palette(colors)

    @property
    def box(self) -> Tuple[float, float, float, float]:
        return (
            self._top - self.config.scale,
            self._left - self.config.scale,
            self._bottom + self.config.scale,
            self._right * 2,
        )

    def coord(self, xy: Tuple[int, int], dxy: _XY = (0.0, 0.0)) -> _XY:
        x = self.config.scale * (xy[0] + self.shift) * 2 + self.config.arc_radius * (
            dxy[0] + 1
        )
        y = self.config.scale * xy[1] * 2 + self.config.arc_radius * (dxy[1] + 1)
        self._top = min(y, self._top)
        self._left = min(x, self._left)
        self._bottom = max(y, self._bottom)
        self._right = max(x, self._right)
        return (x, y)

    def top(self, xy: Tuple[int, int]) -> _XY:
        return self.coord(xy, (0, -1))

    def right(self, xy: Tuple[int, int]) -> _XY:
        return self.coord(xy, (1, 0))

    def left(self, xy: Tuple[int, int]) -> _XY:
        return self.coord(xy, (-1, 0))

    def place_node(self, at: Tuple[int, int], color: int) -> None:
        self.nodes.add(
            self.d.circle(
                self.coord(at),
                self.config.node_radius,
                fill=self.config.node_fill or self.colors[color],
                stroke=self.config.node_stroke,
                stroke_width=self.config.node_stroke_width,
            )
        )

    def _place_edge(
        self, layer: svg.container.Group, a: _XY, b: _XY, color: int
    ) -> None:
        layer.add(
            self.d.line(
                a,
                b,
                stroke_width=self.config.edge_stroke_width,
                stroke=self.colors[color],
            )
        )

    def _place_hline_border(self, a: _XY, b: _XY) -> None:
        self.hline_borders.add(
            self.d.line(
                a,
                b,
                stroke_width=self.config.edge_stroke_width
                + 2 * self.config.node_stroke_width,
                stroke=self.config.node_stroke,
            )
        )

    def place_left_hline(
        self, left: Tuple[int, int], right: Tuple[int, int], color: int
    ) -> None:
        a, b = self.right(left), self.coord(right)
        self._place_hline_border(a, b)
        self._place_edge(self.hlines, a, b, color)

    def place_right_hline(
        self, left: Tuple[int, int], right: Tuple[int, int], color: int
    ) -> None:
        a, b = self.coord(left), self.left(right)
        self._place_hline_border(a, b)
        self._place_edge(self.hlines, a, b, color)

    def place_vline_arc(
        self, top: Tuple[int, int], bottom: Tuple[int, int], color: int
    ) -> None:
        self._place_edge(self.vlines, self.coord(top), self.top(bottom), color)

    def place_vline_node(
        self, top: Tuple[int, int], bottom: Tuple[int, int], color: int
    ) -> None:
        self._place_edge(self.vlines, self.coord(top), self.coord(bottom), color)

    def place_left_arc(self, at: Tuple[int, int], color: int) -> None:
        center = self.coord(at)
        a = (center[0], center[1] - self.config.arc_radius)
        b = (center[0] - self.config.arc_radius, center[1])
        self.hlines.add(
            _arc(
                self.d,
                a,
                b,
                self.config.arc_radius,
                clockwise=True,
                stroke=self.colors[color],
                stroke_width=self.config.edge_stroke_width,
                fill="none",
            )
        )

    def place_right_arc(self, at: Tuple[int, int], color: int) -> None:
        center = self.coord(at)
        a = (center[0], center[1] - self.config.arc_radius)
        b = (center[0] + self.config.arc_radius, center[1])
        self.hlines.add(
            _arc(
                self.d,
                a,
                b,
                self.config.arc_radius,
                clockwise=False,
                stroke=self.colors[color],
                stroke_width=self.config.edge_stroke_width,
                fill="none",
            )
        )

    def place_label(
        self, nodepos: Tuple[int, int], at: Tuple[int, int], label: str
    ) -> None:
        self.nodes.add(
            self.d.text(
                label,
                self.coord(at),
                dominant_baseline="middle",
                font_family=self.config.label_font_family,
            )
        )
        self.background.add(
            self.d.line(
                self.right(nodepos),
                self.coord(at, (-0.4, 0.0)),
                stroke=self.config.label_arrow_stroke,
                stroke_dasharray=self.config.label_arrow_dash_array,
            )
        )


def styler(config: PlotConfig) -> Callable[..., Style]:
    def builder(d: svg.Drawing, colors: int, shift: int = 0) -> Style:
        return Style(d, config, colors, shift)

    return builder
