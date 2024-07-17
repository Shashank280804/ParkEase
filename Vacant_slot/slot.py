import cv2
from flask import Flask, Response
from ultralytics import YOLO

app = Flask(__name__)
#yolo_model = YOLO('C:\\Users\\athar\\Desktop\\Knife-Detection-YOLOV8\\Knife-Detection-YOLOV8\\runs-20240327T164718Z-001\\runs\\detect\\train\\weights\\best.pt')  # Update path if necessary
yolo_model = YOLO('C:\\Shashank\\Shashank\\AI Plate recognition\\Vacant_slot\\runs\\detect\\train\\weights\\best.pt')  

def generate_frames():
    while True:
        try:
            video_capture = cv2.VideoCapture(0)  

            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                results = yolo_model(frame)

                for result in results:
                    classes = result.names
                    cls = result.boxes.cls
                    conf = result.boxes.conf
                    detections = result.boxes.xyxy

                    for pos, detection in enumerate(detections):
                        if conf[pos] >= 0.5:
                            xmin, ymin, xmax, ymax = detection
                            label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}"
                            color = (0, int(cls[pos]), 255)
                            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                            cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    continue
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
            video_capture.release()
        except Exception as e:
            print(f"Error: {e}")


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
