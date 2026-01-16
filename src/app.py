import os
from flask import Flask, request, render_template, jsonify
from parser import parse_config
from graph_builder import build_graph
from visualizer import get_dot_source

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        try:
            # Parse and Build
            data = parse_config(filepath)
            G = build_graph(data)
            dot_source = get_dot_source(G)
            
            # Clean up
            os.remove(filepath)
            
            return jsonify({'dot': dot_source})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
