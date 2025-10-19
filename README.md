# Smart Posture Detector (Ready-to-run)

This is a small Flask web app that uses MediaPipe and OpenCV to analyze posture from an uploaded image.
It is prepared for local use and testing.

## How to run

1. Create and activate a Python virtual environment (optional but recommended):
   ```
   python -m venv venv
   .\venv\Scripts\activate    # on Windows PowerShell
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   python app.py
   ```

4. Open in your browser:
   http://127.0.0.1:5000

## Notes
- Upload an image (person standing or doing exercise). The app will analyze and produce `static/result.jpg`.
- If you prefer to use webcam/video instead of uploaded images, open `smart_posture.py` and run it directly with Python (example included).
