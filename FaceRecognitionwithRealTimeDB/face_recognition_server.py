import cv2
import face_recognition
from flask import Flask, Response
import pickle
import numpy as np
from supabase import create_client, Client
from flask_cors import CORS


# Supabase credentials
SUPABASE_URL = "https://nugmsadjxlyswwkstglm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51Z21zYWRqeGx5c3d3a3N0Z2xtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMjc5ODQzMywiZXhwIjoyMDQ4Mzc0NDMzfQ.kiKSm_sMOnoUqJXRMhYzHVPGvfkjU56F4ws2SO7g60g"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)

# Load the encoding file (modify according to your setup)
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # Set the width to 1080
cap.set(4, 480)   # Set the height to 480

def generate_frames():
    global recognized_count, visitor_count, teacher_count, worker_count, student_count

    recognized_count = 0
    visitor_count = 0
    teacher_count = 0
    worker_count = 0
    student_count = 0

    seen_recognized_ids = set()
    seen_visitor_ids = set()

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)  # Horizontal flip

            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis) if len(faceDis) > 0 else -1

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                if matches[matchIndex]:
                    studentId = studentIds[matchIndex]

                    if studentId in seen_visitor_ids:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, "Visitor", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)
                    elif studentId in seen_recognized_ids:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, studentId, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
                    else:
                        response = supabase.table("users").select("position").eq("university_id", studentId).execute()
                        if response.data:
                            position = response.data[0]["position"]

                            if position == "visitor":
                                visitor_count += 1
                                seen_visitor_ids.add(studentId)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                                cv2.putText(frame, "Visitor", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)
                            elif position == "teacher":
                                teacher_count += 1
                                recognized_count += 1
                                seen_recognized_ids.add(studentId)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, "Teacher", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
                            elif position == "worker":
                                worker_count += 1
                                recognized_count += 1
                                seen_recognized_ids.add(studentId)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, "Worker", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
                            elif position == "student":
                                student_count += 1
                                recognized_count += 1
                                seen_recognized_ids.add(studentId)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, "Student", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)

            cv2.putText(frame, f"Recognized: {recognized_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Visitors: {visitor_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats', methods=['GET'])
def get_stats():
    return {
        "teacher_count": teacher_count,
        "worker_count": worker_count,
        "student_count": student_count,
    }, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
