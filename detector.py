import cv2
import mediapipe as mp 
import numpy as np

#DA RIFARE CON  MediaPipe Face Mesh

#VERSIONE FUNZIONATE CON CV2
# class FaceDetector:

#     def __init__(self):
#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
#         )
#         self.eye_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + 'haarcascade_eye.xml'
#         )
    
    
#     def detect(self, frame):

#         # converti in scala di grigi ?
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
#         #rileva volti
#         faces = self.face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(100, 100)
#         )
        
#         if len(faces) == 0:
#             return None
        
#         # seleziona il primo volto
#         (x, y, w, h) = faces[0]
#         face_rect = (x, y, w, h)
        
#         # trova occhi nell rettangolo superiore
#         face_upper_half_gray = gray[y : y + h // 2, x : x + w] 
#         eyes = self.eye_cascade.detectMultiScale(
#             face_upper_half_gray,
#             scaleFactor=1.1,
#             minNeighbors=8, 
#             minSize=(30, 30)
#         )
        
#         eyes_absolute = []
#         for (ex, ey, ew, eh) in eyes:
#             eyes_absolute.append((x + ex, y + ey, ew, eh))
        
#         return {
#             'face_found': True,
#             'face_rect': face_rect,
#             'eyes': eyes_absolute
#         }

#PROVA CON mediapipe--> NON SO SE FUNZIONA DEVO ISTALLARE PY 3.11
class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,       
            refine_landmarks=True, 
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
       #disegno viso
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def detect_and_draw(self, frame):

        #convaerto da bgr a rgb
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                #disegno i tasselli del viso
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                
                #disegno i tasselli degli occhi
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                )
            
            return True 
            
        return False