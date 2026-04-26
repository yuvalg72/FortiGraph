from graphviz import Digraph

def _build_dot(G):
    dot = Digraph(comment='FortiGraph Topology', format='png')
    dot.attr(rankdir='LR')
    dot.attr('node', fontname="Helvetica", fontsize="10")
    dot.attr('edge', fontname="Helvetica", fontsize="8")

    for node, attrs in G.nodes(data=True):
        dot.node(node,
                 label=attrs.get('label', node),
                 shape=attrs.get('shape', 'oval'),
                 style=attrs.get('style', ''),
                 fillcolor=attrs.get('fillcolor', ''))

    for u, v, attrs in G.edges(data=True):
        dot.edge(u, v,
                 label=str(attrs.get('label', '')),
                 style=attrs.get('style', 'solid'),
                 color=attrs.get('color', 'black'))

    return dot

def get_dot_source(G):
    return _build_dot(G).source

def render_graph(G, output_name="output"):
    dot = _build_dot(G)
    dot.save(f"{output_name}.dot")
    print(f"Generated {output_name}.dot")
    try:
        output_path = dot.render(output_name, view=False)
        print(f"Generated {output_path}")
    except Exception as e:
        print(f"Error rendering Graphviz image: {e}")
        print("Ensure Graphviz is installed and in your PATH.")
