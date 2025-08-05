import cv2
import datetime
import csv
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
log_file = "event_log.csv"
screenshot_dir = "static/screenshots"

# Create folder if not exists
os.makedirs(screenshot_dir, exist_ok=True)

def log_event(face_count):
    mode = "Privacy Mode" if face_count > 1 else "Safe"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_data = [timestamp, face_count, mode]

    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Face Count", "Mode"])

    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(log_data)

def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face_count = len(faces)

        log_event(face_count)

        if face_count > 1:
            # Save screenshot with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            cv2.imwrite(f"{screenshot_dir}/intruder_{timestamp}.jpg", frame)

            # Blur screen
            frame = cv2.GaussianBlur(frame, (75, 75), 30)
            cv2.putText(frame, "Privacy Mode: Intruder Detected!", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
