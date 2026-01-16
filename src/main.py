import sys
from parser import parse_config
from graph_builder import build_graph
from visualizer import render_graph

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
        
    config_file = sys.argv[1]
    print(f"Processing {config_file}...")
    
    data = parse_config(config_file)
    G = build_graph(data)
    render_graph(G, output_name="fortigraph_topology")
    
    print("Done.")

if __name__ == "__main__":
    main()
