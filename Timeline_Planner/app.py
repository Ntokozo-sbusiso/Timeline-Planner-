from flask import Flask, render_template, request, send_file
from datetime import datetime
import pandas as pd
import os
from planner import TimelinePlanner

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/example')
def download_example():
    return send_file('static/example/timeline_template.csv', as_attachment=True)


@app.route('/user-guide')
def user_guide():
    return render_template('user_guide.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'modules_file' not in request.files:
        return "No file uploaded", 400

    modules_file = request.files['modules_file']
    holidays_file = request.files.get('holidays_file')

    if modules_file.filename == '' or not modules_file.filename.endswith('.csv'):
        return "Invalid modules file", 400

    # Save uploads
    modules_path = os.path.join(UPLOAD_FOLDER, modules_file.filename)
    modules_file.save(modules_path)

    # Load modules CSV
    modules_df = pd.read_csv(modules_path)
    modules_df.columns = [col.strip().lower().replace(" ", "_") for col in modules_df.columns]

    # Load custom holidays if provided
    extra_holidays = None
    if holidays_file and holidays_file.filename.endswith('.csv'):
        holidays_path = os.path.join(UPLOAD_FOLDER, holidays_file.filename)
        holidays_file.save(holidays_path)
        hol_df = pd.read_csv(holidays_path)
        if 'date' in hol_df.columns:
            extra_holidays = hol_df['date'].astype(str)

    # Process with planner
    planner = TimelinePlanner(country_code='ZA', years=[2025, 2026], extra_holidays=extra_holidays)
    timeline_df = planner.calculate_timeline(modules_df)

    # Save output
    output_path = os.path.join(UPLOAD_FOLDER, 'timeline_output.csv')
    tables_html = timeline_df.to_html(classes='data', index=False).replace("\n", "")
    return render_template(
                            'results.html',
                            tables=tables_html,
                            titles=timeline_df.columns.values,
                            download_file='timeline_output.csv'
)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)