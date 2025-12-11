import cv2
import mediapipe as mp
import pyautogui
import time
import math

# Setup
pyautogui.FAILSAFE = False
time.sleep(2.0)

# Define keys
accelerator_key = 'right'
brake_key = 'left'
move_left_key = 'a'
move_right_key = 'd'
up_key = 'w'
down_key = 's'
pinch_key = 'space'

current_keys_pressed = set()
pinch_state = False
drag_state = False
cursor_enabled = True
cursor_toggle_cooldown = 1.0
last_toggle_time = time.time()

# MediaPipe setup
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5,
                   max_num_hands=2) as hands:
    while True:
        ret, image = video.read()
        image = cv2.flip(image, 1)
        h, w, _ = image.shape

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        lmListAll = []
        hand_centers = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                lmListAll.append(lmList)
                hand_centers.append(lmList[0][1])  # Wrist x position
                mp_draw.draw_landmarks(image, handLms, mp_hand.HAND_CONNECTIONS)

        # === Cursor Toggle using index-index pinch ===
        if len(lmListAll) == 2:
            left_index = lmListAll[0][8]
            right_index = lmListAll[1][8]
            dist = math.hypot(left_index[1] - right_index[1], left_index[2] - right_index[2])
            if dist < 40 and (time.time() - last_toggle_time > cursor_toggle_cooldown):
                cursor_enabled = not cursor_enabled
                last_toggle_time = time.time()

        fingers = []
        if len(lmListAll) > 0:
            lmList = lmListAll[0]
            hand_center_x = lmList[0][1]

            # Thumb and fingers up
            fingers.append(1 if lmList[4][1] > lmList[3][1] else 0)
            for id in range(1, 5):
                fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

            total = fingers.count(1)
            x_thumb, y_thumb = lmList[4][1], lmList[4][2]
            x_index, y_index = lmList[8][1], lmList[8][2]

            pinch_distance = math.hypot(x_index - x_thumb, y_index - y_thumb)

            # === CURSOR CONTROL via Midpoint of Thumb & Index ===
            mid_x = (x_thumb + x_index) // 2
            mid_y = (y_thumb + y_index) // 2

            # Draw yellow dot
            cv2.circle(image, (mid_x, mid_y), 8, (0, 255, 255), -1)

            # Move cursor based on midpoint
            if cursor_enabled:
                screen_w, screen_h = pyautogui.size()
                scaled_x = int(screen_w * mid_x / w)
                scaled_y = int(screen_h * mid_y / h)
                pyautogui.moveTo(scaled_x, scaled_y)
                cv2.putText(image, 'CURSOR: ON', (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(image, 'CURSOR: OFF', (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # === PINCH to Click/Drag ===
            if pinch_distance < 40:
                if not drag_state:
                    pyautogui.mouseDown()
                    drag_state = True
                cv2.putText(image, 'PINCH & HOLD (Dragging)', (w // 2 - 150, h - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            else:
                if drag_state:
                    pyautogui.mouseUp()
                    drag_state = False
                    cv2.putText(image, 'RELEASE (Launch)', (w // 2 - 100, h - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Space Key (pinch trigger)
            if pinch_distance < 40:
                if not pinch_state:
                    pyautogui.keyDown(pinch_key)
                    current_keys_pressed.add(pinch_key)
                    pinch_state = True
                    cv2.putText(image, 'PINCH (GRAB)', (w//2 - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            else:
                if pinch_state:
                    pyautogui.keyUp(pinch_key)
                    current_keys_pressed.discard(pinch_key)
                    pinch_state = False

            # === Game Key Mappings ===
            if hand_center_x < w * 0.5:  # Left hand
                if total == 0:
                    if brake_key not in current_keys_pressed:
                        pyautogui.keyDown(brake_key)
                        current_keys_pressed.add(brake_key)
                    cv2.putText(image, 'BRAKE (Left Fist)', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif total == 5:
                    if move_left_key not in current_keys_pressed:
                        pyautogui.keyDown(move_left_key)
                        current_keys_pressed.add(move_left_key)
                    cv2.putText(image, 'MOVE LEFT (Open Left Hand)', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                elif fingers == [0, 1, 0, 0, 0]:
                    if up_key not in current_keys_pressed:
                        pyautogui.keyDown(up_key)
                        current_keys_pressed.add(up_key)
                    cv2.putText(image, 'UP (Left Index Up)', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:   # Right hand
                if total == 0:
                    if accelerator_key not in current_keys_pressed:
                        pyautogui.keyDown(accelerator_key)
                        current_keys_pressed.add(accelerator_key)
                    cv2.putText(image, 'GAS (Right Fist)', (w - 350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                elif total == 5:
                    if move_right_key not in current_keys_pressed:
                        pyautogui.keyDown(move_right_key)
                        current_keys_pressed.add(move_right_key)
                    cv2.putText(image, 'MOVE RIGHT (Open Right Hand)', (w - 350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                elif fingers == [0, 1, 0, 0, 0]:
                    if down_key not in current_keys_pressed:
                        pyautogui.keyDown(down_key)
                        current_keys_pressed.add(down_key)
                    cv2.putText(image, 'DOWN (Right Index Up)', (w - 350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

        else:
            for key in list(current_keys_pressed):
                pyautogui.keyUp(key)
                current_keys_pressed.remove(key)
            pinch_state = False
            if drag_state:
                pyautogui.mouseUp()
                drag_state = False

        cv2.imshow("Hand Gesture Controller", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
