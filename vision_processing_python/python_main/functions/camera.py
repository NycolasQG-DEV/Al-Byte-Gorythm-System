import cv2
import time

# //=================================================================
# camera index
CAMERA = 0;
# //=================================================================

class Camera:
    def __init__(self, camera_index=CAMERA):  # default is 2 ( switch if you need )
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)  # if on Windows

        if not self.cap.isOpened():
            raise RuntimeError(f"Error: Could not open camera at index {self.camera_index}.")

        time.sleep(2)  # Wait for the camera to initialize

        self.setup_window()

    def setup_window(self):
        cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def get_frame(self):
        # Try up to 10 times to ensure the camera is "awake"
        for attempt in range(10):
            success, img = self.cap.read()
            if success:
                return cv2.flip(img, 1)
            else:
                print(f"[Camera] Attempt {attempt + 1}: failed to capture frame.")
                time.sleep(0.3)

        raise RuntimeError("Could not capture camera frame after several attempts.")

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
