from graphviz import Digraph

def get_dot_source(G):
    """
    Generates the DOT source string from the NetworkX graph.
    
    Args:
        G (nx.DiGraph): The network topology graph.
        
    Returns:
        str: The DOT source string.
    """
    dot = Digraph(comment='FortiGraph Topology', format='png')
    dot.attr(rankdir='LR')
    dot.attr('node', fontname="Helvetica", fontsize="10")
    dot.attr('edge', fontname="Helvetica", fontsize="8")
    
    # Add Nodes
    for node, attrs in G.nodes(data=True):
        label = attrs.get('label', node)
        shape = attrs.get('shape', 'oval')
        style = attrs.get('style', '')
        fillcolor = attrs.get('fillcolor', '')
        
        dot.node(node, label=label, shape=shape, style=style, fillcolor=fillcolor)
        
    # Add Edges
    for u, v, attrs in G.edges(data=True):
        label = attrs.get('label', '')
        style = attrs.get('style', 'solid')
        color = attrs.get('color', 'black')
        
        dot.edge(u, v, label=str(label), style=style, color=color)
        
    return dot.source

def render_graph(G, output_name="output"):
    """
    Renders the NetworkX graph using Graphviz.
    
    Args:
        G (nx.DiGraph): The network topology graph.
        output_name (str): Base name for the output file.
    """
    dot_source = get_dot_source(G)
    
    # We can rebuild the source into a Digraph object if we want to render it locally like before
    # or just write the file manually. Let's reuse the logic but source from our helper.
    dot = Digraph(comment='FortiGraph Topology', format='png')
    # Use the source we generated (a bit hacky, but consistent)
    # Actually, simpler to just re-instantiate or let get_dot_source return the object.
    # Let's simple return the object from a helper function.
    pass 
    # To keep it compatible with existing main.py if needed, we'll just duplicate logic or leave as is.
    # But for the requested refactor, I will Replace the existing function to be cleaner.

    dot = Digraph(comment='FortiGraph Topology', format='png')
    dot.attr(rankdir='LR')
    dot.attr('node', fontname="Helvetica", fontsize="10")
    dot.attr('edge', fontname="Helvetica", fontsize="8")
    
    # Add Nodes
    for node, attrs in G.nodes(data=True):
        label = attrs.get('label', node)
        shape = attrs.get('shape', 'oval')
        style = attrs.get('style', '')
        fillcolor = attrs.get('fillcolor', '')
        
        dot.node(node, label=label, shape=shape, style=style, fillcolor=fillcolor)
        
    # Add Edges
    for u, v, attrs in G.edges(data=True):
        label = attrs.get('label', '')
        style = attrs.get('style', 'solid')
        color = attrs.get('color', 'black')
        
        dot.edge(u, v, label=str(label), style=style, color=color)
    
    # Save DOT file
    dot.save(f"{output_name}.dot")
    print(f"Generated {output_name}.dot")
    
    # Render PNG
    try:
        output_path = dot.render(output_name, view=False)
        print(f"Generated {output_path}")
    except Exception as e:
        print(f"Error rendering Graphviz image: {e}")
        print("Ensure Graphviz is installed and in your PATH.")
