# Study Attention Monitor

Sistema di monitoraggio dell’attenzione in tempo reale che verifica se l’utente è concentrato sullo studio combinando **computer vision**, **tracciamento dello sguardo** e **rilevamento oggetti** tramite due webcam.

---

## Funzionalità

### Analisi con doppia webcam
Utilizza due flussi video contemporaneamente:
1. Face-cam → traccia volto e movimenti degli occhi  
2. Desk-cam → rileva oggetti utili allo studio o fonti di distrazione  

---

### Rilevamento dello sguardo
MediaPipe Face Mesh viene utilizzato per individuare i landmark del volto e stimare la direzione dello sguardo, così da capire se l’utente sta guardando lo schermo.

---

### Rilevamento oggetti
YOLOv8 rileva e classifica gli oggetti presenti sulla scrivania, ad esempio:

- laptop  
- libri  
- tastiera → **studio**
- telefono → **distrazione**

---

### Sistema di allarme distrazione 
Se l’utente rimane distratto per troppo tempo, il sistema riproduce automaticamente un video di richiamo.

Funzionalità:
- monitora il tempo di distrazione
- il telefono viene considerato distrazione immediata
- apre automaticamente un video di avviso
- chiude il video quando l’attenzione torna normale

---

## Come funziona

Il sistema integra diversi moduli che collaborano per analizzare l’attenzione dell’utente in tempo reale.

---

## Moduli principali

### `main.py`
Punto di ingresso dell’applicazione.  
Inizializza le webcam, acquisisce i frame, esegue le analisi e mostra i risultati a schermo.

---

### `camera.py`
Classe di supporto che semplifica l’uso di OpenCV `VideoCapture` per inizializzare e leggere i frame dalle webcam.

---

### `faceDetector.py`
Utilizza MediaPipe Face Mesh per rilevare il volto e i landmark oculari (iride), fornendo le coordinate necessarie all’analisi dello sguardo.

---

### `eyeAnalyzer.py`
Analizza le coordinate degli occhi per determinare se l’utente sta guardando lo schermo oppure altrove.

---

### `deskDetector.py`
Esegue YOLOv8 per rilevare gli oggetti sulla scrivania e classificarli come:
- `STUDIO`
- `DISTRAZIONE`

---

## Sistema di allarme

### `alarm.py`
Gestisce il tempo di distrazione e attiva un allarme quando viene superata una soglia configurabile.

Responsabilità:
- misura la durata della distrazione
- rileva il telefono come distrazione immediata
- riproduce un video di richiamo tramite il player di sistema
- chiude automaticamente il video quando l’utente torna concentrato
- utilizza thread per non bloccare il ciclo principale del programma

---

##  Struttura del progetto
Study-Attention-Monitor/
│
├── main.py
├── camera.py
├── faceDetector.py
├── eyeAnalyzer.py
├── deskDetector.py
├── alarm.py
│
├── video/
│ └── Richiamo.mp4
│
└── README.md

---

## Requisiti

- Python 3.x
- Due webcam collegate
- Sistema operativo Windows (l’apertura automatica del video usa `os.startfile`)

---

## Installazione

Clona il repository e Istalla dipendenze:

```bash
git clone https://github.com/Pietro-Savelli/Study-Attention-Monitor.git
cd Study-Attention-Monitor
pip install opencv-python mediapipe ultralytics numpy

