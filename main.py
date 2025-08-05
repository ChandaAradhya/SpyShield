import cv2
import yagmail
import datetime
import pygetwindow as gw
import pyautogui
import time
import csv
import os

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Setup email (update with your credentials)
SENDER_EMAIL = "chandanaradhya@gmail.com"
SENDER_PASSWORD = "242004"
RECIPIENT_EMAIL = "chandananlchandana@gmail.com"
EMAIL_SUBJECT = "⚠️ SpyShield Alert: Multiple Faces Detected"

yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)

last_alert_time = None
alert_interval = 30  # seconds

def send_alert(count):
    global last_alert_time
    current_time = time.time()
    if not last_alert_time or (current_time - last_alert_time > alert_interval):
        body = f"Multiple faces ({count}) detected at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        yag.send(to=RECIPIENT_EMAIL, subject=EMAIL_SUBJECT, contents=body)
        print("📧 Email alert sent!")
        last_alert_time = current_time

def blur_screen():
    window = gw.getWindowsWithTitle("SpyShield Privacy Overlay")
    if window:
        return  # Already blurred

    screen_width, screen_height = pyautogui.size()
    overlay = pyautogui.screenshot()
    overlay = cv2.cvtColor(np.array(overlay), cv2.COLOR_RGB2BGR)
    blurred = cv2.GaussianBlur(overlay, (99, 99), 30)
    cv2.namedWindow("SpyShield Privacy Overlay", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("SpyShield Privacy Overlay", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        cv2.imshow("SpyShield Privacy Overlay", blurred)
        if cv2.waitKey(100) & 0xFF == ord('u'):  # Press 'u' to unblur
            cv2.destroyWindow("SpyShield Privacy Overlay")
            break

def log_event(face_count):
    log_file = "event_log.csv"
    mode = "Privacy Mode" if face_count > 1 else "Safe"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_data = [timestamp, face_count, mode]

    # Create file with headers if not exists
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Face Count", "Mode"])

    # Append new row
    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(log_data)

# Start webcam
cap = cv2.VideoCapture(0)

print("🛡️ SpyShield is running... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_count = len(faces)
    
    log_event(face_count)

    if face_count > 1:
        # Blur the entire frame if intruder detected
        blurred_frame = cv2.GaussianBlur(frame, (75, 75), 30)
        cv2.putText(blurred_frame, "⚠️ Privacy Mode: Intruder Detected!", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('SpyShield - Privacy Mode', blurred_frame)
    else:
        # Draw rectangles normally
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('SpyShield - Normal Mode', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
