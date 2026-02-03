import time
import threading
import os

#funziona solo con il telefono per ora
class Alarm():
    
    def __init__(self, soglia_distrazione):
        self.soglia_distrazione = soglia_distrazione
        self.start_distrazione = None
        self.video_aperto = False  
        self.video_locale = r".\video\Richiamo.mp4"
    
    def check_stato(self, sta_guardando_pc, stato_desk):
        ora_attuale = time.time()

        if stato_desk.upper() == "TELEFONO":
            return True
        
        if sta_guardando_pc or stato_desk.upper() == "STUDIO":
            if self.video_aperto:
                self.chiudi_video()
            self.start_distrazione = None
            self.video_aperto = False
            return False

        if self.start_distrazione is None:
            self.start_distrazione = ora_attuale
            
        secondi_passati = ora_attuale - self.start_distrazione
        
        if secondi_passati >= self.soglia_distrazione:
            return True

        return False
    
    def attiva_allarme(self):
        
        if not self.video_aperto:
            self.video_aperto = True
            threading.Thread(target=self.riproduci_video, daemon=True).start()

    
    def riproduci_video(self):  

        try:
            os.startfile(self.video_locale)
        except Exception as e:
            print(f" Errore nell'apertura del video: {e}")

    def chiudi_video(self):
    
        try:
            os.system('taskkill /F /IM wmplayer.exe /T 2>nul')
            os.system('taskkill /F /IM Microsoft.Media.Player.exe /T 2>nul')
            os.system('taskkill /F /IM vlc.exe /T 2>nul')
        except Exception as e:
            print(f"Errore chiusura video: {e}")