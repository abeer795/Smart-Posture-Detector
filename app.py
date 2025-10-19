from flask import Flask, render_template, request, send_from_directory
import cv2
import mediapipe as mp
import numpy as np
import os

app = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return render_template('index.html', result="❌ لا يوجد ملف مرفوع")
    file = request.files['image']
    if file.filename == '':
        return render_template('index.html', result="❌ اسم الملف فارغ")
    image_path = os.path.join(UPLOAD_FOLDER, 'uploaded.jpg')
    file.save(image_path)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        image = cv2.imread(image_path)
        if image is None:
            return render_template('index.html', result="❌ فشل في قراءة الصورة")
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            return render_template('index.html', result="❌ لم يتم اكتشاف الجسم", image_file='uploaded.jpg')

        landmarks = results.pose_landmarks.landmark
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        angle = calculate_angle(shoulder, hip, knee)

        cv2.putText(image, f'Angle: {int(angle)}°', (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        if angle < 150:
            posture = 'Back Bent ❌'
            color = (0, 0, 255)
        else:
            posture = 'Good Posture ✅'
            color = (0, 255, 0)

        cv2.putText(image, posture, (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        output_path = os.path.join(UPLOAD_FOLDER, 'result.jpg')
        cv2.imwrite(output_path, image)

        return render_template('index.html', result=posture, image_file='result.jpg')

# optional route to download result
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
