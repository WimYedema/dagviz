"""
Render directed graphs in a jupyter notebook using [dagre-d3](https://github.com/dagrejs/dagre-d3).

This is as simple as:

```py
from dagviz.dagre import Dagre
import networkx as nx

g = nx.DiGraph()
g.add_edge("a","b")
Dagre(g)
```
"""
import networkx as nx
from string import Template
import json

_css_text = """
text {
  font-weight: 300;
  font-family: sans-serif;
  font-size: 14px;
}

.node rect {
  stroke: #999;
  fill: #fff;
  stroke-width: 1.5px;
}

.edgePath path {
  stroke: #333;
  stroke-width: 1.5px;
}
"""

_template = """
element.html('<style id="css">$css</style>');
require.config({
    paths: {
        d3: 'https://d3js.org/d3.v5.min',
        dagreD3: 'https://cdnjs.cloudflare.com/ajax/libs/dagre-d3/0.6.4/dagre-d3.min'
    }
});
require(["d3", "dagreD3"], function(d3, dag) {
    $buildGraph
    let elem = d3.select(element.get(0))
    let svg = elem.append("svg");
    let inner = svg.append("g")
    let render = new dag.render();
    render(inner, g);
    // Set up zoom support
    var zoom = d3.zoom().on("zoom", function() {
        inner.attr("transform", d3.event.transform);
    });
    svg.call(zoom);
    // Realign the graph, edges may have x<0
    svg.call(zoom.transform, d3.zoomIdentity.translate(g.graph().width/4.0, 20).scale(1));
    svg.attr("height", g.graph().height + 40);
    svg.attr("width", g.graph().width*1.5 + 40);
});
"""


class Dagre:
    """
    Directed graph visualizer for jupyter notebooks using
    [dagre-d3](https://github.com/dagrejs/dagre-d3).

    Args:
        G: directed graph to render
    """

    def __init__(self, G: nx.DiGraph):
        self._css = _css_text
        self.graph = G

    def _repr_javascript_(self) -> str:
        builder = ["let g = new dag.graphlib.Graph().setGraph({});"]
        for n in self.graph.nodes:
            nstr = json.dumps(n)
            label = json.dumps(str(self.graph.nodes[n].get("label", n)))
            builder.append(f'g.setNode({nstr}, {{ "label": {label}}});')
        for e in self.graph.edges.data():
            label = json.dumps(str(e[2].get("label", "")))
            s = json.dumps(e[0])
            d = json.dumps(e[1])
            builder.append(f'g.setEdge({s},{d}, {{"label": {label}}});')

        return Template(_template).substitute(
            css=self._css.replace("\n", ""), buildGraph="\n".join(builder)
        )
