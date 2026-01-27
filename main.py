import cv2
from camera import Camera
from detector import FaceDetector

cam = Camera(camera_index=0)  # creo la camera 
det = FaceDetector()

while True:
    frame = cam.get_frame()

    if frame is not None:
        trovato = det.detect_and_draw(frame)

        if trovato:
            cv2.putText(frame, "Tracking Attivo", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Nessun volto", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Webcam", frame)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break

    else:
        print("Errore: nessun frame")
        break

cam.release()                #rilascio cam
cv2.destroyAllWindows()