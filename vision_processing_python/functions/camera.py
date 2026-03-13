import cv2

#objeto da camera ( utilizado para captar valores da camera )
class Camera:
    def __init__(self, camera_index=2):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def get_frame(self):
        success, img = self.cap.read()
        if not success:
            raise RuntimeError("Não foi possível capturar o frame da câmera.")
        return cv2.flip(img, 1)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
