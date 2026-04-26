import re

def parse_config(file_path):
    """
    Parses the FortiGate configuration file.
    
    Args:
        file_path (str): Path to the configuration file.
        
    Returns:
        dict: Parsed data including interfaces, routes, and policies.
    """
    data = {
        "interfaces": {},
        "routes": [],
        "policies": []
    }
    
    context = [] # stack to track context
    current_interface = None
    current_route = None
    current_policy = None
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Context Switch
            if line.startswith('config '):
                section = line.split(' ', 1)[1]
                context.append(section)
                continue
            
            if line == 'end':
                if context:
                    context.pop()
                continue
                
            if line == 'next':
                if context:
                    if context[-1] == 'system interface':
                        if current_interface:
                            # Save interface
                            name = current_interface.get('name')
                            if name:
                                data['interfaces'][name] = current_interface
                            current_interface = None
                    elif context[-1] == 'router static':
                        if current_route:
                            data['routes'].append(current_route)
                            current_route = None
                    elif context[-1] == 'firewall policy':
                        if current_policy:
                            data['policies'].append(current_policy)
                            current_policy = None
                continue
                
            # Parsing Logic based on Context
            if not context:
                continue
                
            current_section = context[-1]
            
            # --- SYSTEM INTERFACE ---
            if current_section == 'system interface':
                if line.startswith('edit '):
                    name = line.split(' ', 1)[1].strip('"')
                    current_interface = {'name': name, 'ip': None, 'mask': None, 'vlanid': None, 'type': 'physical', 'alias': None, 'member': []}
                
                elif current_interface:
                    if line.startswith('set ip '):
                        parts = line.split()
                        if len(parts) >= 4:
                            current_interface['ip'] = parts[2]
                            current_interface['mask'] = parts[3]
                    elif line.startswith('set vlanid '):
                        current_interface['vlanid'] = line.split()[-1]
                        current_interface['type'] = 'vlan'
                    elif line.startswith('set type '):
                        current_interface['type'] = line.split()[-1]
                    elif line.startswith('set alias '):
                         current_interface['alias'] = line.split(' ', 2)[2].strip('"')
                    elif line.startswith('set interface '): # For VLANs/Tunnels binding to physical
                        member = line.split()[-1].strip('"')
                        current_interface['member'].append(member)
            
            # --- FIREWALL POLICY ---
            elif current_section == 'firewall policy':
                if line.startswith('edit '):
                    current_policy = {'id': line.split(' ', 1)[1].strip('"'), 'srcintf': None, 'dstintf': None, 'srcaddr': None, 'dstaddr': None, 'action': None, 'service': None}

                elif current_policy:
                    if line.startswith('set srcintf '):
                        current_policy['srcintf'] = line.split()[-1].strip('"')
                    elif line.startswith('set dstintf '):
                        current_policy['dstintf'] = line.split()[-1].strip('"')
                    elif line.startswith('set srcaddr '):
                        current_policy['srcaddr'] = line.split()[-1].strip('"')
                    elif line.startswith('set dstaddr '):
                        current_policy['dstaddr'] = line.split()[-1].strip('"')
                    elif line.startswith('set action '):
                        current_policy['action'] = line.split()[-1]
                    elif line.startswith('set service '):
                        current_policy['service'] = line.split()[-1].strip('"')

            # --- ROUTER STATIC ---
            elif current_section == 'router static':
                if line.startswith('edit '):
                    current_route = {'dst': '0.0.0.0/0', 'gateway': None, 'device': None}
                
                elif current_route:
                    if line.startswith('set dst '):
                        # Handling "set dst 10.0.0.0 255.0.0.0" -> CIDR conversion is nice but raw is fine for now
                        parts = line.split()
                        if len(parts) >= 4:
                            current_route['dst'] = f"{parts[2]} {parts[3]}"
                    elif line.startswith('set gateway '):
                        current_route['gateway'] = line.split()[-1]
                    elif line.startswith('set device '):
                        current_route['device'] = line.split()[-1].strip('"')

    return data
