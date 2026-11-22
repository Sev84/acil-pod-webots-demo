"""ACIL-POD class demo; the WWW channel carries simulated commands, not real credentials."""
import json
from math import isfinite

from controller import Keyboard, Robot
from logic import DRIVE, Pod

robot = Robot()
step_ms = int(robot.getBasicTimeStep())
keyboard = robot.getKeyboard()
keyboard.enable(step_ms)
sensor = robot.getDevice("front_sensor")
sensor.enable(step_ms)
wheels = [robot.getDevice(n) for n in ("wheel_fl", "wheel_rl", "wheel_fr", "wheel_rr")]
for motor in wheels:
    motor.setPosition(float("inf"))
    motor.setVelocity(0)
lid = robot.getDevice("lid_motor")
lid.setPosition(0)
lid_sensor = robot.getDevice("lid_sensor")
lid_sensor.enable(step_ms)
pod = Pod()
code = ""
last = ""
visible_status = ""
keys_before = set()
last_update = -1.0


def receive_command():
    """Drain a bounded queue and prioritize STOP over any burst of motion messages."""
    command = None
    stopped = False
    for _ in range(96):
        text = robot.wwiReceiveText()
        if text is None:
            break
        if text in DRIVE or text == "C":
            command = text
        elif text == "X":
            stopped = True
        elif text.startswith("CODE:") and len(text) <= 20:
            command = "ENTER" if text == "CODE:1234" else "WRONG"
    return "X" if stopped else command


while robot.step(step_ms) != -1:
    keys = set()
    key = keyboard.getKey()
    while key != -1:
        keys.add(key & Keyboard.KEY)
        key = keyboard.getKey()
    new_keys = keys - keys_before
    for k in sorted(new_keys):
        if 48 <= k <= 57:
            code = (code + chr(k))[-12:]
    command = next((c for k, c in [(88, "X"), (67, "C"), (Keyboard.END, "X"),
                                  (87, "W"), (65, "A"), (83, "S"), (68, "D")] if k in keys), None)
    if command is None and ({10, 13, 80} & new_keys):
        command = "ENTER" if code == "1234" else "WRONG"
        code = ""
    remote = receive_command()
    if command is None or remote == "X":
        command = remote
    keys_before = keys
    now = robot.getTime()
    distance = sensor.getValue()
    (left, right), angle, message = pod.step(now, distance, command)
    actual_angle = lid_sensor.getValue()
    if not isfinite(actual_angle) or abs(actual_angle) > 0.06:
        left = right = 0.0
        pod.motion = ""
    for i, motor in enumerate(wheels):
        motor.setVelocity(left if i < 2 else right)
    lid.setPosition(angle)
    if message:
        visible_status = message
        if message != last:
            print(message)
    last = message
    if now - last_update >= 0.16:
        robot.wwiSendText(json.dumps({
            "range": round(distance, 2) if isfinite(distance) else None,
            "angle": round(actual_angle, 2) if isfinite(actual_angle) else None,
            "moving": bool(left or right),
            "status": visible_status,
        }, ensure_ascii=True, allow_nan=False))
        last_update = now
