from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import math
import matplotlib.pyplot as plt

app = Flask(__name__)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
mp_drawing = mp.solutions.drawing_utils

def detectPose(image, pose, display=True):
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)

        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

    return output_image, landmarks

def calculateAngle(a, b, c):
    x1, y1, _ = a
    x2, y2, _ = b
    x3, y3, _ = c

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

    if angle < 0:
        angle += 360

    return angle

def classifyPose(landmarks, output_image, display=False):
    label = 'Unknown Pose'
    color = (0, 0, 255)

    if len(landmarks) < 33:
        return output_image, label  # Not enough landmarks

    # Angles
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    # T Pose
    if (165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195 and
        80 < left_shoulder_angle < 110 and 80 < right_shoulder_angle < 110 and
        165 < left_knee_angle < 195 and 165 < right_knee_angle < 195):
        label = 'T Pose'

    # Warrior II Pose
    elif (165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195 and
          80 < left_shoulder_angle < 110 and 80 < right_shoulder_angle < 110 and
          ((165 < left_knee_angle < 195 and 90 < right_knee_angle < 120) or
           (165 < right_knee_angle < 195 and 90 < left_knee_angle < 120))):
        label = 'Warrior II Pose'

    # Tree Pose
    elif ((165 < left_knee_angle < 195 and 25 < right_knee_angle < 45) or
          (165 < right_knee_angle < 195 and 315 < left_knee_angle < 335)):
        label = 'Tree Pose'

        # Trikonasana (Triangle Pose)
    elif (160 < left_knee_angle < 200 and 160 < right_knee_angle < 200 and
          150 < left_elbow_angle < 200 and 20 < right_elbow_angle < 70):
        label = 'Trikonasana'

    # Bhujangasana (Cobra Pose)
    elif (70 < left_shoulder_angle < 110 and 70 < right_shoulder_angle < 110 and
          80 < left_elbow_angle < 140 and 80 < right_elbow_angle < 140 and
          left_knee_angle > 160 and right_knee_angle > 160):
        label = 'Bhujangasana'

    # Chakrasana (Wheel Pose)
    elif (30 < left_shoulder_angle < 80 and 30 < right_shoulder_angle < 80 and
          40 < left_elbow_angle < 100 and 40 < right_elbow_angle < 100 and
          40 < left_knee_angle < 90 and 40 < right_knee_angle < 90):
        label = 'Chakrasana'

    # Balasana (Child Pose)
    elif (40 < left_knee_angle < 100 and 40 < right_knee_angle < 100 and
          100 < left_shoulder_angle < 160 and 100 < right_shoulder_angle < 160):
        label = 'Balasana'

    # Naukasana (Boat Pose)
    elif (40 < left_knee_angle < 70 and 40 < right_knee_angle < 70 and
          120 < left_shoulder_angle < 160 and 120 < right_shoulder_angle < 160):
        label = 'Naukasana'

    # Sukhasana (Easy Sitting Pose)
    elif (70 < left_knee_angle < 120 and 70 < right_knee_angle < 120 and
          60 < left_elbow_angle < 120 and 60 < right_elbow_angle < 120):
        label = 'Sukhasana'

    # Shavasana (Corpse Pose)
    elif (160 < left_knee_angle < 195 and 160 < right_knee_angle < 195 and
          160 < left_elbow_angle < 195 and 160 < right_elbow_angle < 195 and
          80 < left_shoulder_angle < 110 and 80 < right_shoulder_angle < 110):
        label = 'Shavasana'

    if label != 'Unknown Pose':
        color = (0, 255, 0)

    cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    if display:
        plt.figure(figsize=[10, 10])
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')
    else:
        return output_image, label

def webcam_feed():
    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 1380)
    camera_video.set(4, 960)

    while camera_video.isOpened():
        ok, frame = camera_video.read()
        if not ok:
            continue

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        aspect_ratio = frame_width / frame_height
        frame = cv2.resize(frame, (int(640 * aspect_ratio), 640))

        frame, landmarks = detectPose(frame, pose, display=False)

        if landmarks:
            frame, _ = classifyPose(landmarks, frame, display=False)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera_video.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yoga_try')
def yoga_try():
    return render_template('yoga_try.html')

@app.route('/video_feed1')
def video_feed1():
    return Response(webcam_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
