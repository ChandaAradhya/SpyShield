from flask import Flask, render_template, Response, send_file
from detector import generate_frames
import os
import csv
import glob
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download_logs')
def download_logs():
    if os.path.exists("event_log.csv"):
        return send_file("event_log.csv", as_attachment=True)
    else:
        return "No log file found."

@app.route('/logs')
def logs():
    logs_data = []
    chart_data = {"labels": [], "counts": []}

    try:
        with open("event_log.csv", "r") as f:
            reader = csv.reader(f)
            logs_data = list(reader)
            for row in logs_data[1:]:
                chart_data["labels"].append(row[0])
                chart_data["counts"].append(int(row[1]))
    except FileNotFoundError:
        logs_data = [["Timestamp", "Face Count", "Mode"], ["No log data found", "", ""]]

    image_files = sorted(glob.glob("static/screenshots/*.jpg"), reverse=True)

    return render_template("logs.html", logs=logs_data, screenshots=image_files, chart=json.dumps(chart_data))

if __name__ == "__main__":
    app.run(debug=True)
