import cv2
from camera import Camera
from faceDetector import FaceDetector
from eyeAnalyzer import EyeAnalyzer
from deskDetector import DeskDetector


def init_face():
    cam_face = Camera(camera_index=0)
    det_face = FaceDetector()
    analyzer_eye = EyeAnalyzer()
    analizza_face = True
    stato_face = False
    punti_face = None

    return cam_face, det_face, analyzer_eye, analizza_face, stato_face, punti_face

def init_desk():
    cam_desk = Camera(camera_index=1)
    det_desk = DeskDetector()
    stato_desk = "SCONOSCIUTO"

    return cam_desk, det_desk, stato_desk

def process_face_frame(cam_face, det_face, analyzer_eye, analizza_face, stato_face, punti_face):
    frame_face = cam_face.get_frame()
    sta_guardando = False

    if frame_face is None:
        return None, analizza_face, stato_face, punti_face, False

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

    return frame_face, analizza_face, stato_face, punti_face, True

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

    while True:

        _, analizza_face, stato_face, punti_face, ok_face = process_face_frame(
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

        if cv2.waitKey(1) == ord('q'):
            break

    cam_face.release()
    cam_desk.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()


























#-------------MAIN con unione di face e desk--------------------------

# #Variabili Face
# cam_face = Camera(camera_index=0)  # creo la camera 
# det_face = FaceDetector()
# analyzer_eye = EyeAnalyzer()
# analizza_face = True 
# stato_face = False
# punti_face = None

# #Varibili Desk
# cam_desk = Camera(camera_index=1)
# det_desk = DeskDetector()
# stato_desk = "SCONOSCIUTO"

# while True:
#     #Analizza frame face
#     frame_face = cam_face.get_frame()
#     sta_guardando = False

#     if frame_face is not None:
#         if analizza_face:
#             stato_face = det_face.detect(frame_face)
#             punti_face = det_face.get_coordinate(frame_face)
#         analizza_face = not analizza_face

#         if punti_face:
#             sta_guardando = analyzer_eye.where_look(punti_face)

#         if sta_guardando:
#             cv2.putText(frame_face, "Sta studiando al pc", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame_face, "NON sta studiando al pc", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            

#         if stato_face:
#             cv2.putText(frame_face, "Tracking Attivo", (10, 30), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame_face, "Nessun volto", (10, 30), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

#         cv2.imshow("Webcam_Face", frame_face)

#     else:
#         print("Errore: nessun frame")
#         break

#     #Analizza frame desk
#     frame_desk = cam_desk.get_frame()
#     if frame_desk is not None:
#         stato_desk = det_desk.detect(frame_desk)

#         if stato_desk == "STUDIO":
#             cv2.putText(frame_desk, "Sta studiando ", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame_desk, "NON sta studiando", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
#         cv2.imshow("Webcam_Desk", frame_desk)
#     else:
#         print("Errore: nessun frame")
#         break

#     k=cv2.waitKey(1)
#     if k == ord('q'):
#         break


# cam_face.release()                #rilascio cam
# cam_desk.release()   
# cv2.destroyAllWindows()




#------------------------------------------------------#
# # MAIN DELLA PARTE DELLA deskDetector
# cam_desk = Camera(camera_index=0)  # creo la camera 
# det_desk = DeskDetector()

# while True:
#     frame_desk = cam_desk.get_frame()

#     if frame_desk is not None:
#         stato = det_desk.detect(frame_desk)

#         if stato == "STUDIO":
#             cv2.putText(frame_desk, "Sta studiando ", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame_desk, "NON sta studiando", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

#         cv2.imshow("Webcam", frame_desk)
#         k=cv2.waitKey(1)
#         if k == ord('q'):
#             break

#     else:
#         print("Errore: nessun frame")
#         break

# cam_desk.release()                #rilascio cam
# cv2.destroyAllWindows()


# -------------------------------------------------------MAIN DELLA PARTE DELLA faceDetector---------------------------------------------------------------------------------------------------

# cam = Camera(camera_index=0)  # creo la camera 
# det = FaceDetector()
# analyzer = EyeAnalyzer()
# analizza = True 

# while True:
#     frame = cam.get_frame()
#     sta_guardando = False

#     if frame is not None:
#         if analizza:
#             trovato = det.detect(frame)
#             punti = det.get_coordinate(frame)
#         analizza = not analizza

#         if punti:
#             sta_guardando = analyzer.where_look(punti)

#         if sta_guardando:
#             cv2.putText(frame, "Sta studiando al pc", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame, "NON sta studiando al pc", (100, 100), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            

#         if trovato:
#             cv2.putText(frame, "Tracking Attivo", (10, 30), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame, "Nessun volto", (10, 30), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

#         cv2.imshow("Webcam", frame)
#         k=cv2.waitKey(1)
#         if k == ord('q'):
#             break

#     else:
#         print("Errore: nessun frame")
#         break

# cam.release()                #rilascio cam
# cv2.destroyAllWindows()