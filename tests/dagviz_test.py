import unittest
import networkx as nx
import dagviz


class DagvizTest(unittest.TestCase):
    def test_abstract_ploy(self):
        G = nx.DiGraph()
        num_nodes = 5
        for i in range(num_nodes):
            G.add_node(f"n{i}")
        G.add_edge(f"n0", f"n1")
        G.add_edge(f"n0", f"n2")
        G.add_edge(f"n0", f"n4")
        G.add_edge(f"n1", f"n3")
        G.add_edge(f"n2", f"n3")
        G.add_edge(f"n3", f"n4")
        p = dagviz.make_abstract_plot(G)
        self.assertEqual(len(p.rows), num_nodes)
        num_inputs = 0
        for i, row in enumerate(p.rows):
            self.assertEqual(row.row, i)
            self.assertTrue(row.label.startswith("n"))
            lastcol = None
            has_node = False
            for col in row:
                if lastcol is not None:
                    self.assertGreater(col.column, lastcol)
                lastcol = col.column
                self.assertGreaterEqual(col.color, 0)
                self.assertGreaterEqual(col.remaining, 0)
                if col.is_node:
                    has_node = True
                if col.is_input:
                    num_inputs += 1
            self.assertTrue(has_node)
        self.assertEqual(num_inputs, 6)

    def test_render_svg(self):
        G = nx.DiGraph()
        for i in range(5):
            G.add_node(f"n{i}")
        G.add_edge(f"n0", f"n1")
        G.add_edge(f"n0", f"n2")
        G.add_edge(f"n0", f"n4")
        G.add_edge(f"n1", f"n3")
        G.add_edge(f"n2", f"n3")
        G.add_edge(f"n3", f"n4")
        r = dagviz.render_svg(G)
        self.assertTrue(r.startswith("<svg"))
        self.assertTrue(r.endswith("</svg>"))

    def test_DAG(self):
        G = dagviz.DAG()
        for i in range(5):
            G.add_node(f"n{i}")
        G.add_edge(f"n0", f"n1")
        G.add_edge(f"n0", f"n2")
        G.add_edge(f"n0", f"n4")
        G.add_edge(f"n1", f"n3")
        G.add_edge(f"n2", f"n3")
        G.add_edge(f"n3", f"n4")
        r = G._repr_html_()
        self.assertTrue(r.startswith("<svg"))
        self.assertTrue(r.endswith("</svg>"))
