import os
import time
import simpleaudio as sa

alarm_state = {"fire": False, "smoke": False}
current_sound = {"fire": None, "smoke": None}

# Beep timing control
last_play_time = {"fire": 0, "smoke": 0}
BEEP_INTERVAL = 2  # seconds

# Sound file paths (flexible)
SOUND_FILES = {
    "fire": "fire_alert.wav",
    "smoke": "smoke_alert.wav"
}

def get_color(label):
    return (0,0,255) if label == "fire" else (128,128,128)

def play_sound(label):
    current_time = time.time()

    # Prevent spam (beep interval)
    if current_time - last_play_time[label] < BEEP_INTERVAL:
        return
    
    # If already playing, skip
    if alarm_state[label]:
        return
    
    sound_path = SOUND_FILES.get(label)

    if not os.path.exists(sound_path):
        print(f"[ERROR] Sound file not found: {sound_path}")
        return
    
    try:
        wave = sa.WaveObject.from_wave_file(f"{label}_alert.wav")
        current_sound[label] = wave.play()
        alarm_state[label] = True
        last_play_time[label] = current_time

    except Exception as e:
        print(f"[ERROR] Sound play failed ({label}):", e)

def stop_sound(label):
    try:
        if current_sound[label]:
            current_sound[label].stop()
    except Exception as e:
        print(f"[ERROR] Sound stop failed ({label}):", e)

    alarm_state[label] = False