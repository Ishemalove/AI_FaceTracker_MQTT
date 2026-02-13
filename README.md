# Face Tracker MQTT System

**A Real-Time Distributed Vision & Control Platform**

## What This Does

Automatically detects and tracks faces in real-time, commanding a servo motor to follow target movement. Built on MQTT for reliability and WebSocket for responsive dashboards.

### Core Components

1. **Vision Node** (Python on PC) - Analyzes video, detects faces, publishes commands
2. **Backend Service** (Python on PC) - MQTT subscriber that relays data via WebSocket  
3. **ESP8266 Controller** (MicroPython) - Receives MQTT commands, actuates servo motor
4. **Web Dashboard** (Browser) - Real-time status and tracking visualization

### Key Feature: Team Isolation

Multiple teams can operate simultaneously on the same broker using isolated MQTT topics.

## System Architecture

```
PC (Vision Node) 
    └─→ MQTT Broker ←─┐
                      ├─→ Backend (WebSocket Relay) → Browser Dashboard
                      └─→ ESP8266 Controller → Servo Motor
```

**Design Principle**: Vision generates intelligence. Hardware uses MQTT for certainty. Browsers use WebSocket for speed.

## Project Layout

```
face-tracker-mqtt/
├── vision-node/vision_node.py      - Face detection engine
├── backend/backend.py              - Message relay service  
├── esp8266/main.py                 - Servo controller firmware
├── dashboard/index.html            - Live tracking interface
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.8+** with pip
- **Mosquitto MQTT Broker** (local)
- **MicroPython** on ESP8266
- **Modern Web Browser**

### Step 1: Install & Start MQTT Broker

**Windows**
```powershell
Download Mosquitto from https://mosquitto.org/
mosquitto.exe -v
```

**Linux**
```bash
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

### Step 2: Install Python Dependencies

```bash
pip install opencv-python paho-mqtt websockets asyncio
```

### Step 3: Configure Team ID

Set your unique team identifier (prevents cross-team interference):

```python
TEAM_ID = "team01"
MQTT_TOPIC = f"vision/{TEAM_ID}/movement"
```

### Step 4: Launch Services

**Terminal 1** - Start Backend
```bash
python backend/backend.py
```

**Terminal 2** - Run Vision Node
```bash
python vision-node/vision_node.py
```

**Terminal 3** - Flash & Run ESP8266
```bash
# Flash MicroPython, then execute:
ampy --port COM3 put esp8266/main.py
```

**Browser** - Open Dashboard
```
http://localhost:8000/dashboard/index.html
```

## Topic Convention

| Component | Topic | Role |
|-----------|-------|------|
| Vision Node | `vision/{TEAM_ID}/movement` | **Publishes** face position |
| Backend | `vision/{TEAM_ID}/movement` | **Subscribes** & relays |
| ESP8266 | `vision/{TEAM_ID}/movement` | **Subscribes** & actuates |

⚠️ **Critical**: Never use topics from other teams. Always verify `TEAM_ID` matches.

Start Backend WebSocket relay:

cd backend
python backend.py


Run Vision Node (PC):

cd vision-node
python vision_node.py


Open Dashboard:

Open dashboard/index.html in a browser.

Ensure WebSocket URL matches backend:

const ws = new WebSocket("ws://localhost:9002");


Flash ESP8266:

Update broker IP to your PC’s local IP.

Connect servo to GPIO5 (D1).

Run main.py in MicroPython.

4. Optional: Heartbeat messages

You can publish node status to:

vision/<team_id>/heartbeat


Example payload:

{
  "node": "pc",
  "status": "ONLINE",
  "timestamp": 1730000000
}

## 💡 Best Practices

### 1️⃣ Dead-Zone Thresholds
Prevent servo jitter by ignoring small movements below a threshold:
```python
DEAD_ZONE = 5  # degrees
if abs(current_angle - last_angle) > DEAD_ZONE:
    move_servo(current_angle)
```

### 2️⃣ Message Rate Control
Limit MQTT publish frequency to prevent broker flooding:
```python
# Max 10 Hz (100ms between messages)
PUBLISH_INTERVAL = 0.1  # seconds
if (time.time() - last_publish) > PUBLISH_INTERVAL:
    mqtt_client.publish(topic, payload)
```

### 3️⃣ Servo Smoothing
Apply gradual movement instead of abrupt jumps:
```python
# Move servo in 2-5 degree increments
STEP_SIZE = 3  # degrees per update
while abs(target_angle - current_angle) > STEP_SIZE:
    current_angle += STEP_SIZE if target_angle > current_angle else -STEP_SIZE
    servo.write(current_angle)
    time.sleep(0.05)  # 50ms between steps
```

### 4️⃣ Testing Protocol
✅ Always validate locally before deploying  
✅ Test without mechanical load first  
✅ Monitor MQTT message traffic with `mosquitto_sub`  
✅ Verify WebSocket connectivity in browser console  
✅ Gradual transition to closed-loop control

📝 Dependencies

Python 3.10+

OpenCV (opencv-python)

Paho-MQTT (paho-mqtt)

Websockets (websockets)

MicroPython on ESP8266

Mosquitto MQTT Broker

🎯 Features

Real-time face tracking and servo control

Full distributed architecture

Topic isolation for multi-team environments

Web dashboard with live updates

Local-only mode (no VPS required)

Ready for open-loop (phase 1) or closed-loop (phase 2)

🏁 Running Notes

PC camera detects face → publishes MQTT → ESP moves servo → Backend updates dashboard.

Phase 1: Camera fixed.

Phase 2: Camera mounted on servo for closed-loop tracking.

Avoid direct connections between PC ↔ ESP or Dashboard ↔ MQTT.

🔗 References

Gabriel Baziramwabo ResearchGate

BenaxMedia YouTube Channel