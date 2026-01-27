import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError(f"Impossibile aprire la webcam (indice {camera_index})")
        print(f"Webcam aperta con successo (indice {camera_index})")
    
    def get_frame(self):
        catturato, frame = self.cap.read()
        return frame if catturato else None
    
    def release(self):
        self.cap.release()