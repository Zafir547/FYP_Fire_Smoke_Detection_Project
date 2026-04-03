import cv2
import time
import math
import cvzone
from ultralytics import YOLO
from utils import get_color, play_sound, stop_sound
from alerts import send_email_alert, send_sms_alert

model = YOLO("models/best.pt")

classnames = ['fire', 'smoke']
CONF_THRESHOLD = 60

# Detection confirmation
DETECTION_FRAMES = 3
detection_count = {'fire': 0, 'smoke': 0}

# Alert Control
alert_sent = {'fire': False, 'smoke': False}
last_alert_time = {'fire': 0, 'smoke': 0}
ALERT_RESET_TIME = 30

# FPS
prev_time = 0

def process_frame(frame):
    global prev_time

    current_time = time.time()
    frame = cv2.resize(frame, (640, 640))

    detected_this_frame = {'fire': False, 'smoke': False}

    # YOLO inference
    results = model(frame)

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            confidence = math.ceil(float(box.conf[0]) * 100)
            cls = int(box.cls[0])

            if cls >= len(classnames):
                continue

            if confidence > CONF_THRESHOLD:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                label = classnames[cls]
                color = get_color(label)

                detected_this_frame[label] = True

                # Draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                cvzone.putTextRect(frame, f'{label.upper()} {confidence}%', (x1, y1 - 10))

                # 🔊 Sound (handled inside utils with interval control)
                play_sound(label)

    # Detection confirmation (anti-false-positive)
    for det_type in ['fire', 'smoke']:
        if detected_this_frame[det_type]:
            detection_count[det_type] += 1
        else:
            detection_count[det_type] = 0

    # Send alerts after confirmation
    for det_type in ['fire', 'smoke']:
        if detection_count[det_type] >= DETECTION_FRAMES:
            if not alert_sent[det_type]:
                print(f"🔥 {det_type.upper()} CONFIRMED")

                send_email_alert(det_type, frame)
                send_sms_alert(det_type)

                alert_sent[det_type] = True
                last_alert_time[det_type] = current_time

    # Cooldown reset
    for det_type in ['fire', 'smoke']:
        if alert_sent[det_type]:
            if current_time - last_alert_time[det_type] > ALERT_RESET_TIME:
                alert_sent[det_type] = False
                detection_count[det_type] = 0
                stop_sound(det_type)

                print(f"♻️ {det_type.upper()} RESET")

    # FPS Calculation
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    cvzone.putTextRect(frame, f'FPS: {int(fps)}', (20, 50))

    # Status Display
    status_fire = "FIRE DETECTED" if alert_sent['fire'] else "No Fire"
    status_smoke = "SMOKE DETECTED" if alert_sent['smoke'] else "No Smoke"

    cvzone.putTextRect(
        frame,
        status_fire,
        (20, 90),
        colorR=(0, 0, 255) if alert_sent['fire'] else (0, 200, 0)
    )

    cvzone.putTextRect(
        frame,
        status_smoke,
        (20, 130),
        colorR=(128, 128, 128) if alert_sent['smoke'] else (0, 200, 0)
    )

    return frame, detected_this_frame