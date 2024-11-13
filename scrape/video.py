import cv2
import socketio
import base64
import eventlet
import subprocess

from dotenv import load_dotenv
import os

load_dotenv()

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(
    sio, static_files={"/": {"content_type": "text/html", "filename": "index.html"}}
)
VIDEO_ID = os.getenv('VIDEO_ID')

try:
    stream_url = (
        subprocess.check_output(
            ["yt-dlp", "-g", "https://www.youtube.com/watch?v="+VIDEO_ID]
        )
        .decode("utf-8")
        .strip()
    )
except subprocess.CalledProcessError as e:
    print("Error retrieving the stream URL:", e)
    exit(1)

streaming_task_started = False


def stream_video():

    global streaming_task_started

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        streaming_task_started = False
        return

    while streaming_task_started:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode frame to JPEG and convert to base64
        _, buffer = cv2.imencode(".jpg", frame)
        frame_data = base64.b64encode(buffer).decode("utf-8")

        # Send frame to clients
        sio.emit("video_frame", frame_data)

        sio.sleep(1 / 60)  # 60 FPS

    cap.release()
    streaming_task_started = False


@sio.event
def connect(sid, environ):
    global streaming_task_started
    print("connect ", sid)

    # Start the streaming task only if it's not already running
    if not streaming_task_started:
        streaming_task_started = True
        sio.start_background_task(stream_video)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 5050)), app)
