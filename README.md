**Hand Gesture-Based Game Controller**
This project implements a real-time hand gesture controller using Python, OpenCV, MediaPipe, and PyAutoGUI.
It uses a webcam to detect hand movements and converts them into mouse actions and keyboard controls for gaming.

🚀 Features
🎮 Game Controls
✊ Fist
Left hand → Brake (Left Arrow)
Right hand → Gas (Right Arrow)

✋ Open Hand
Left → Move Left (A)
Right → Move Right (D)

☝️ Index Finger Up
Left → Up (W)
Right → Down (S)

🖱 Mouse Actions
Move cursor using Thumb + Index midpoint
Pinch gesture →
✔ Mouse Drag
✔ Release
✔ SPACE key action
Index-to-Index pinch → Toggle cursor ON/OFF

🧠 Technologies Used
OpenCV
MediaPipe Hands
PyAutoGUI
NumPy
Python 3.11

📂 File Included
gesture_controller.py → Main application script
📦 Installation
Install dependencies:
pip install opencv-python mediapipe==0.10.14 pyautogui numpy

▶️ How to Run
Run the script:
python gesture_controller.py
Press Q to close the webcam window.

📸 How it Works (Summary)
MediaPipe detects hand landmarks
OpenCV renders frames and tracking overlays
PyAutoGUI sends keyboard/mouse signals



<img width="335" height="252" alt="image" src="https://github.com/user-attachments/assets/84ba4ebf-b3a4-41c2-8951-617cfa5c93c2" />
<img width="333" height="206" alt="image" src="https://github.com/user-attachments/assets/ffdbd1bc-eba8-4c49-8733-cd1baffa09ff" />
<img width="342" height="236" alt="image" src="https://github.com/user-attachments/assets/4837ce27-3ed0-4643-83ed-1c457bcfc353" />
<img width="346" height="236" alt="image" src="https://github.com/user-attachments/assets/10449e88-0042-4874-8665-54e045685073" />
<img width="344" height="224" alt="image" src="https://github.com/user-attachments/assets/6cc95b65-7313-4b79-b4ea-05a3c050cde1" />
<img width="348" height="221" alt="image" src="https://github.com/user-attachments/assets/da23e2b4-c464-42b9-aebb-fdbd19239d22" />



Gesture control:
Movement
Acceleration/Brake
Cursor and drag
Special triggers (SPACE)

📝 Notes
Make sure your webcam is enabled
Good lighting improves hand detection
Works with any game that uses keyboard input

👤 Author
Jashmi KS
B.Tech CSE


⭐ 3. Your Repository Will Look Like This
Gesture-Control-Game/
│
├── gesture_controller.py
└── README.md
