# DAGVIZ
DAGVIZ offers a "git log"-like visualization for DAGs represented in networkx.

## Installation

DAGVIZ can be installed with `pip`:

```bash
pip install dagviz
```

## Documentation

Documentation is available at https://wimyedema.github.io/dagviz/.
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

### Custom styling

The Metro style can be customized using `StyleConfig`. This is especially
useful for rendering on dark backgrounds:

```py
    from dagviz.style.metro import svg_renderer, StyleConfig

    dark_style = svg_renderer(StyleConfig(
        node_stroke="black",
        label_font_color="white",
        bridge_color="black",
        label_arrow_stroke="grey",
    ))

    r = dagviz.render_svg(G, style=dark_style)
```

See the [Metro styling notebook](https://wimyedema.github.io/dagviz/notebooks/Metro%20styling.html) for a full overview of all available options.
