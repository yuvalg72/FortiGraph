import networkx as nx

def build_graph(parsed_data):
    """
    Builds a NetworkX graph from the parsed configuration data.
    
    Args:
        parsed_data (dict): Data extracted from the config file.
        
    Returns:
        nx.DiGraph: The network topology graph.
    """
    G = nx.DiGraph()
    
    # 1. Add Central Node
    G.add_node("FortiGate", type="device", shape="box", style="filled", fillcolor="lightblue")
    
    # 2. Add Interfaces
    interfaces = parsed_data.get("interfaces", {})
    
    for name, intf in interfaces.items():
        # Node attributes
        ip = intf.get('ip')  # Use .get() to avoid KeyError
        label = f"{name}\n{ip}" if ip else name
        if intf.get('alias'):
            label += f"\n({intf['alias']})"
            
        node_type = intf.get('type', 'physical')
        
        # Style based on type
        if node_type == 'physical':
            shape = "rect"
            color = "lightgrey"
        elif node_type == 'vlan':
            shape = "ellipse"
            color = "lightyellow"
            label += f"\nVLAN {intf.get('vlanid')}"
        elif node_type == 'tunnel':
            shape = "diamond"
            color = "lightpink"
        else:
            shape = "oval"
            color = "white"
            
        G.add_node(name, label=label, shape=shape, style="filled", fillcolor=color, type="interface")
        
        # Connect to FortiGate (Logical Connection)
        # If it's a physical interface, connect directly to FGT
        # If it's a VLAN/Tunnel, connect to its parent interface if known, otherwise FGT
        
        parent = None
        members = intf.get('member', [])
        if members:
            parent = members[0] # Assume one parent for now
        
        if parent and parent in interfaces:
            G.add_edge(parent, name, style="solid") # Parent -> Child (VLAN)
        else:
            G.add_edge("FortiGate", name, style="bold")


    # 3. Add Routes (Visualization of Next Hops)
    routes = parsed_data.get("routes", [])
    for i, route in enumerate(routes):
        dst = route.get('dst', '0.0.0.0/0')
        gateway = route.get('gateway')
        device = route.get('device')
        
        # Sanitize dst for use as node name (replace spaces and special chars)
        safe_dst = dst.replace(' ', '_').replace('/', '_')
        net_node = f"NET_{safe_dst}"
        if not G.has_node(net_node):
            G.add_node(net_node, label=dst, shape="note", style="filled", fillcolor="white")
            
        # Connect: Interface -> Gateway -> Network
        if device and device in interfaces:
            # If we have a gateway IP, maybe show it as a label on the edge or a small intermediate node?
            # Let's use edge label for gateway
            edge_label = f"GW: {gateway}" if gateway else ""
            G.add_edge(device, net_node, label=edge_label, style="dashed", color="blue")
            
    return G
