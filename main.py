import cv2
from camera import Camera
from faceDetector import FaceDetector
from eyeAnalyzer import EyeAnalyzer
from deskDetector import DeskDetector
from alarm import Alarm


def init_face():
    cam_face = Camera(camera_index=1)
    det_face = FaceDetector()
    analyzer_eye = EyeAnalyzer()
    analizza_face = True
    stato_face = False
    punti_face = None

    return cam_face, det_face, analyzer_eye, analizza_face, stato_face, punti_face

def init_desk():
    cam_desk = Camera(camera_index=0)
    det_desk = DeskDetector()
    stato_desk = "SCONOSCIUTO"

    return cam_desk, det_desk, stato_desk

def process_face_frame(cam_face, det_face, analyzer_eye, analizza_face, stato_face, punti_face):
    frame_face = cam_face.get_frame()
    sta_guardando = False

    if frame_face is None:
        return None, analizza_face, stato_face, punti_face, False, False

    if analizza_face:
        stato_face = det_face.detect(frame_face)
        punti_face = det_face.get_coordinate(frame_face)

    analizza_face = not analizza_face

    if punti_face:
        sta_guardando = analyzer_eye.where_look(punti_face)

    if sta_guardando:
        cv2.putText(frame_face, "Sta studiando al pc", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame_face, "NON sta studiando al pc", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if stato_face:
        cv2.putText(frame_face, "Tracking Attivo", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame_face, "Nessun volto", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Webcam_Face", frame_face)

    return frame_face, analizza_face, stato_face, punti_face, sta_guardando, True

def process_desk_frame(cam_desk, det_desk, stato_desk):

    frame_desk = cam_desk.get_frame()

    if frame_desk is None:
        return None, stato_desk, False

    stato_desk = det_desk.detect(frame_desk)

    if stato_desk == "STUDIO":
        cv2.putText(frame_desk, "Sta studiando ", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame_desk, "NON sta studiando", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Webcam_Desk", frame_desk)

    return frame_desk, stato_desk, True


def main():

    cam_face, det_face, analyzer_eye, analizza_face, stato_face, punti_face = init_face()
    cam_desk, det_desk, stato_desk = init_desk()
    my_alarm = Alarm(soglia_distrazione=1)

    while True:

        _, analizza_face, stato_face, punti_face, sta_guardando, ok_face = process_face_frame(
            cam_face, det_face, analyzer_eye,
            analizza_face, stato_face, punti_face
        )

        if not ok_face:
            print("Errore: nessun frame face")
            break

        _, stato_desk, ok_desk = process_desk_frame(
            cam_desk, det_desk, stato_desk
        )

        if not ok_desk:
            print("Errore: nessun frame desk")
            break

        is_allarme = my_alarm.check_stato(sta_guardando, stato_desk)

        if is_allarme:
            my_alarm.attiva_allarme()

        if cv2.waitKey(1) == ord('q'):
            break

    cam_face.release()
    cam_desk.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
