import networkx as nx

def build_graph(parsed_data):
    G = nx.DiGraph()

    G.add_node("FortiGate", type="device", shape="box", style="filled", fillcolor="lightblue")

    interfaces = parsed_data.get("interfaces", {})

    for name, intf in interfaces.items():
        # An interface named "FortiGate" would silently merge with the central hub node
        if name == "FortiGate":
            continue

        ip = intf.get('ip')
        label = f"{name}\n{ip}" if ip else name
        if intf.get('alias'):
            label += f"\n({intf['alias']})"

        node_type = intf.get('type', 'physical')

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
        elif node_type == 'loopback':
            shape = "circle"
            color = "lightcyan"
        else:
            shape = "oval"
            color = "white"

        G.add_node(name, label=label, shape=shape, style="filled", fillcolor=color, type="interface")

        parent = None
        members = intf.get('member', [])
        if members:
            parent = members[0]

        if parent and parent in interfaces:
            G.add_edge(parent, name, style="solid")
        else:
            G.add_edge("FortiGate", name, style="bold")

    routes = parsed_data.get("routes", [])
    for route in routes:
        dst = route.get('dst', '0.0.0.0/0')
        gateway = route.get('gateway')
        device = route.get('device')

        safe_dst = dst.replace(' ', '_').replace('/', '_')
        net_node = f"NET_{safe_dst}"
        if not G.has_node(net_node):
            G.add_node(net_node, label=dst, shape="note", style="filled", fillcolor="white")

        if device and device in interfaces and device != "FortiGate":
            edge_label = f"GW: {gateway}" if gateway else ""
            if G.has_edge(device, net_node):
                # Append to existing label rather than silently overwrite (failover routes)
                existing = G[device][net_node].get('label', '')
                G[device][net_node]['label'] = f"{existing}\n{edge_label}".strip('\n')
            else:
                G.add_edge(device, net_node, label=edge_label, style="dashed", color="blue")

    return G
