import cv2
import smtplib
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Email Config
SENDER_EMAIL = "zafirabdullah1534@gmail.com"
RECEIVER_EMAIL = "zafirabdullah189@gmail.com"
APP_PASSWORD = "zlqs igwl zvie idzn"

# Twilio SMS Config
TWILIO_SID = "ACc8a507c1022023e623d31f968cbd9640"
TWILIO_AUTH_TOKEN = "2abd54ad503d946d9e9e819da7a4669f"
TWILIO_PHONE_NUMBER = "+16625277675"
TARGET_PHONE_NUMBER = "+923333586147"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_email_alert(detection_type, frame):
    subject = f"🚨 {detection_type.upper()} ALERT"
    body = f"{detection_type.upper()} detected by AI system!"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    msg.attach(MIMEText(body))

    _, img_encoded = cv2.imencode('.jpg', frame)
    image = MIMEImage(img_encoded.tobytes(), name="alert.jpg")
    msg.attach(image)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email Error:", e)

def send_sms_alert(detection_type):
    try:
        client.messages.create(
            body=f"{detection_type.upper()} detected!",
            from_=TWILIO_PHONE_NUMBER,
            to=TARGET_PHONE_NUMBER
        )
    except Exception as e:
        print("SMS Error:", e)
