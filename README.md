# 🧘‍♀️ YogAI — Real-Time Yoga Pose Detection with Flask & MediaPipe

**YogAI** is a web-based application that uses computer vision to recognize and classify yoga poses in real-time using your webcam. Built with Python, OpenCV, Flask, and MediaPipe, it helps users practice and validate their yoga form from home.

---

## Features-

-  **Live webcam feed** with pose detection overlay
-  **Real-time pose classification** for 10+ yoga asanas
-  Recognizes poses like **Trikonasana**, **Bhujangasana**, **Vrikshasana**, **Chakrasana**, and more
-  Pose names displayed live on the video
-  Scrollable reference panel with asana images
-  Modular Python code (easy to expand/add new poses)

---

##  Technologies Used-

- **Python 3.10**
- **Flask** — web server and routing
- **OpenCV** — video capture and image processing
- **MediaPipe** — body pose landmark detection
- **HTML/CSS** — frontend layout and styling

---

##  Yoga Poses Supported-

YogAI currently supports detection of the following asanas:

| English Name     | Sanskrit Name     |
|------------------|-------------------|
| T Pose           | Tadasana Variant  |
| Warrior II Pose  | Virabhadrasana    |
| Tree Pose        | Vrikshasana       |
| Triangle Pose    | Trikonasana       |
| Cobra Pose       | Bhujangasana      |
| Wheel Pose       | Chakrasana        |
| Child Pose       | Balasana          |
| Boat Pose        | Naukasana         |
| Easy Pose        | Sukhasana         |
| Corpse Pose      | Shavasana         |

---

## 🚀 Getting Started

## 1. Clone the Repository
git clone https://github.com/avirajdongare/YogAI.git
cd YogAI

## 2. Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
## OR
venv\Scripts\activate     # For Windows

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Run the Flask App
python app.py

## Then open in your browser:
## http://127.0.0.1:5000/yoga_try


---

##  How It Works-

1. Flask serves a web interface with a live webcam feed.
2. OpenCV captures frames from your webcam.
3. MediaPipe detects 33 pose landmarks per frame.
4. Angles between joints are calculated using basic trigonometry.
5. If the angles match a known pose pattern → label is drawn on the frame.

---

## 📌 TODO / Improvements-

- Add pose accuracy scores
- Log detected poses with timestamps to CSV
- Overlay reference skeleton beside live stream
- Add audio guidance or feedback
- Deploy on the cloud (Render, Streamlit, Heroku)

---

## 🧑‍💻 Author

**Aviraj Dongare**  
[GitHub](https://github.com/avirajdongare) 

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

