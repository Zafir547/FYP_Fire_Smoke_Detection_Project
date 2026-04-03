import os
import time
import threading
from playsound import playsound

alarm_state = {"fire": False, "smoke": False}

# Beep timing control
last_play_time = {"fire": 0, "smoke": 0}
BEEP_INTERVAL = 2  # seconds

# Sound file paths
SOUND_FILES = {
    "fire": "fire_alert.wav",
    "smoke": "smoke_alert.wav"
}

def get_color(label):
    return (0, 0, 255) if label == "fire" else (128, 128, 128)

def play_sound(label):
    current_time = time.time()

    # Prevent spam
    if current_time - last_play_time[label] < BEEP_INTERVAL:
        return

    if alarm_state[label]:
        return

    sound_path = SOUND_FILES.get(label)

    if not os.path.exists(sound_path):
        print(f"[ERROR] Sound file not found: {sound_path}")
        return

    try:
        alarm_state[label] = True
        last_play_time[label] = current_time

        # Play sound in background thread
        threading.Thread(
            target=playsound,
            args=(sound_path,),
            daemon=True
        ).start()

    except Exception as e:
        print(f"[ERROR] Sound play failed ({label}):", e)

def stop_sound(label):
    # playsound
    alarm_state[label] = False
