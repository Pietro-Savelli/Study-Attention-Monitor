import cv2
from camera import Camera
from detector import FaceDetector
from eyeAnalyzer import EyeAnalyzer


#RIORGANIZZA IL MAIN 

cam = Camera(camera_index=0)  # creo la camera 
det = FaceDetector()
analyzer = EyeAnalyzer()
analizza = True 

while True:
    frame = cam.get_frame()

    if frame is not None:
        if analizza:
            trovato = det.detect(frame)
            punti = det.get_coordinate(frame)
        analizza = not analizza

        if punti:
            sta_guardando = analyzer.where_look(punti)

        if sta_guardando:
            cv2.putText(frame, "Sta studiando al pc", (100, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "NON sta studiando al pc", (100, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            

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