import cv2

def gstreamer_pipeline(device, capture_width, capture_height, framerate, display_width, display_height):
    return (
        f'v4l2src device=/dev/video{device} ! '
        f'video/x-raw, width={capture_width}, height={capture_height}, framerate={framerate}/1 ! '
        'videoconvert ! videoscale ! '
        f'video/x-raw, width={display_width}, height={display_height} ! appsink'
    )

# Pipeline parameters
capture_width = 1280
capture_height = 720
display_width = 640
display_height = 360
framerate = 30

pipeline = gstreamer_pipeline(0, capture_width, capture_height, framerate, display_width, display_height)
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Failed to open camera.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process the frame here if needed
        
        cv2.imshow('Camera Feed', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
