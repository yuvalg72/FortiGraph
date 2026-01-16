# FortiGraph

**FortiGraph** is a powerful network visualization tool that parses FortiGate configuration files (`.conf`) and renders interactive network topology diagrams directly in your browser.

![FortiGraph Diagram](https://raw.githubusercontent.com/username/repo/main/docs/diagram.png) 
*(Note: Replace with actual screenshot link after upload)*

## Features

*   **Zero Dependencies**: No need to install Graphviz on your server or local machine. Visualization happens entirely in the browser using WebAssembly.
*   **Secure Parsing**: Extracts interfaces, VLANs, tunnels, and static routes locally.
*   **Interactive UI**: Zoom, pan, and explore complex network topologies with ease.
*   **Privacy Focused**: Your config files are processed locally by the Python backend and never sent to a third-party server.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/fortigraph.git
    cd fortigraph
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the application**:
    ```bash
    python src/app.py
    ```

2.  **Open your browser**:
    Navigate to `http://localhost:5000`.

3.  **Upload Config**:
    Drag and drop your FortiGate configuration file (e.g., `backup.conf`) into the drop zone.

## Logic
- **Nodes**:
    - **Physical Interfaces**: Grey rectangles.
    - **VLANs**: Yellow ellipses, connected to their parent interface.
    - **Tunnels**: Pink diamonds.
    - **Routes**: White clouds representing destination networks.
- **Edges**:
    - **Solid Line**: Logical membership (e.g., VLAN -> Parent Port).
    - **Dashed Blue Line**: Static routing path.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
