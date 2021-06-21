# DAGVIZ
DAGVIZ offers a "git log"-like visualization for DAGs represented in networkx.

## Installation

DAGVIZ can be installed with `pip`:

```bash
pip install dagviz
```

## Usage

DAGVIZ relies on networkx for the representation and manipulation of the
DAG. An SVG file can be generated as follows:

```py
    import dagviz
    import networkx as nx
    # Create the DAG
    G = nx.DiGraph()
    for i in range(5):
        G.add_node(f"n{i}")
    G.add_edge(f"n0", f"n1")
    G.add_edge(f"n0", f"n2")
    G.add_edge(f"n0", f"n4")
    G.add_edge(f"n1", f"n3")
    G.add_edge(f"n2", f"n3")
    G.add_edge(f"n3", f"n4")
    # Create an SVG as a string
    r = dagviz.render_svg(G)
    with open("simple.svg", "wt") as fs:
        fs.write(r)
```
This will yield this graph: ![Simple example](./gallery/simple.svg)
