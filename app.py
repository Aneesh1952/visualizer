from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import CORS
from visualizer import Plotter  
import io
import json
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

df = None  # Global dataframe to store uploaded CSV/Excel data

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload CSV file and generate a plot from it."""
    global df
    
    if 'file' in request.files:
        file = request.files['file']

        # Check if file is a CSV
        if file and file.filename.endswith('.csv'):
            try:
                df = pd.read_csv(file)
                # Return column names so the user can choose
                return jsonify({"columns": df.columns.tolist()}), 200
            except Exception as e:
                return jsonify({"error": f"Failed to read CSV: {str(e)}"}), 500
        elif file and file.filename.endswith(('.xls', '.xlsx')):
            try:
                df = pd.read_excel(file)  # Read Excel file into a DataFrame
                # Return column names so the user can choose
                return jsonify({"columns": df.columns.tolist()}), 200
            except Exception as e:
                return jsonify({"error": f"Failed to read Excel file: {str(e)}"}), 500
        else:
            return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

    # Check if JSON data is sent for plotting
    elif df is not None and request.is_json:
        try:
            data = request.json
            if data:
                plotter = Plotter()
                plot_image = plotter.create_plot(df, data)  # Use the uploaded DataFrame
                if plot_image:
                    return send_file(plot_image, mimetype='image/jpeg')
                else:
                    return jsonify({"error": "Failed to create plot"}), 500
            else:
                return jsonify({"error": "No plot data provided in the request"}), 400
        except Exception as e:
            return jsonify({"error": f"Error generating plot: {str(e)}"}), 500
    else:
        return jsonify({'error': 'No file uploaded or no data provided for plotting'}), 400

if __name__ == '__main__':
    app.run(debug=True)
