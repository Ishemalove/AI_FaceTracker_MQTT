import cv2
import paho.mqtt.client as mqtt
import json
import time

# ========== CONFIG ==========
TEAM_ID = "team05"
BROKER_IP = "10.12.73.101"
BROKER_PORT = 1883

TOPIC = f"vision/{TEAM_ID}/movement"

# MQTT setup
client = mqtt.Client()
client.connect(BROKER_IP, BROKER_PORT, 60)

# Load Haar face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)

def get_status(face_x, frame_width):
    center = frame_width // 2
    threshold = 50

    if face_x < center - threshold:
        return "MOVE_LEFT"
    elif face_x > center + threshold:
        return "MOVE_RIGHT"
    else:
        return "CENTERED"

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    status = "NO_FACE"
    confidence = 0.0

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_center_x = x + w // 2
        status = get_status(face_center_x, frame.shape[1])
        confidence = 0.9

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    payload = {
        "status": status,
        "confidence": confidence,
        "timestamp": int(time.time())
    }

    client.publish(TOPIC, json.dumps(payload))

    cv2.imshow("Vision Node", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
