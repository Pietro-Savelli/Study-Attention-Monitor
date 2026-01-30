import cv2

class Camera:
    def __init__(self, camera_index, width=1280, height=720):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise RuntimeError(f"Impossibile aprire la webcam (indice {camera_index})")
        print(f"Webcam aperta con successo (indice {camera_index})")
    
    def get_frame(self):
        catturato, frame = self.cap.read()
        if catturato:
            return cv2.flip(frame, 1)
        return None
    
    def release(self):
        self.cap.release()