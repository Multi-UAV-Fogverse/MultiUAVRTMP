import cv2
import os

# Set your RTMP server URL
rtmp_url = 'rtmp://yourserver/live/streamkey'

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Change '0' to your video source

# Check if the video capture object is initialized correctly
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# Define the GStreamer pipeline
gst_pipeline = (
    'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! '
    'flvmux streamable=true ! rtmpsink location={}'
).format(rtmp_url)

# Open the GStreamer pipeline
out = cv2.VideoWriter(gst_pipeline, cv2.CAP_GSTREAMER, 0, 30, (640, 480), True)

if not out.isOpened():
    print("Error: Could not open GStreamer pipeline.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Write the frame to the GStreamer pipeline
    out.write(frame)

    # Display the frame (optional)
    cv2.imshow('frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()