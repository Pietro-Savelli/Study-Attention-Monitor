import cv2
from ultralytics import YOLO

class DeskDetector:
    def __init__(self):
        self.model = YOLO("yolov8s.pt") #versione nano"yolov8n.pt" (non funzionava)

        self.distrazioni = [67]  # cod di Cell phone
        self.studio = [63, 64, 66, 73, 62]# cod di:Laptop, Mouse, Keyboard, Book, (TV/Monitor) non esiste tablet

        self.nomi_oggetti = {
            67: "TELEFONO (No!)",
            63: "Laptop",
            64: "Mouse",
            66: "Tastiera",
            73: "Libro",
            62: "Tablet (Monitor)", 
            999: "TABLET"          #se entra in un certo range allora assegno qeusto codice
        }
    
    def detect(self, frame):
        results = self.model(frame, verbose=False)
        
        stato_attuale = "Neutro"
        trovata_distrazione = False
        trovato_studio = False  
        for r in results:
            boxes = r.boxes
            
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                classeOggetto = int(box.cls[0])
                confidenza = float(box.conf[0])

                if confidenza > 0.4:
                    
                    if classeOggetto == 67 and confidenza > 0.25: #controllo la dimensione del telefono, nel caso lo scambiasse con il tablet
                        larghezza = x2 - x1
                        altezza = y2 - y1
                        area = larghezza * altezza
                        rapporto = larghezza / altezza

                        if area > 30000 and rapporto > 0.8: #NON E' ABBASTANZA SELETTIVO
                            classeOggetto = 999 
                        else:
                            pass
            
                    if classeOggetto in self.distrazioni:
                        trovata_distrazione = True

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        label = self.nomi_oggetti.get(classeOggetto, "Distrazione")
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                    elif classeOggetto in self.studio or classeOggetto == 999:
                        trovato_studio = True

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = self.nomi_oggetti.get(classeOggetto, "Studio")
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if trovata_distrazione:
            stato_attuale = "DISTRAZIONE"
        elif trovato_studio:
            stato_attuale = "STUDIO"
        else:
            stato_attuale = "Neutro"
            
        return stato_attuale