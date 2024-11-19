import cv2
from ultralytics import YOLO
import time
import csv
from datetime import datetime
import winsound

# Configuración de YOLO y captura de video
model = YOLO(r'Python_code\PyTorch\best.pt') 
cap = cv2.VideoCapture(0)

# Variables para el estado y temporizadores
status_timers = { "guantes": None, "chaleco": None, "gafas_protec": None, "casco": None }
current_status = { "guantes": "usando", "chaleco": "usando", "gafas_protec": "usando", "casco": "usando" }
missing_timers = { "guantes": None, "chaleco": None, "gafas_protec": None, "casco": None }

# Ruta del archivo CSV
csv_file = r'Histori_data\cumplimiento_registros.csv'

# Inicializa el archivo CSV con encabezados
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Hora", "Implemento", "Estado", "Duración"])

# Función para registrar datos en el CSV
def write_to_csv(timestamp, implemento, estado, duration):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, implemento, estado, duration])

# Proceso de detección en tiempo real
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar la imagen de la cámara")
        break

    results = model(frame)
    detected_labels = set()
    alert_triggered = False

    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        label_index = int(result.cls[0])           
        labels = {
            0: "usando_guantes", 1: "sin_guantes",
            2: "usando_chaleco", 3: "sin_chaleco",
            4: "usando_gafas_protec", 5: "sin_gafas_protec",
            6: "usando_casco", 7: "sin_casco"
        }
        label_text = labels[label_index]
        estado, implemento = label_text.split("_", 1)
        detected_labels.add(implemento)
        color = (0, 255, 0) if estado == "usando" else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if implemento in current_status and current_status[implemento] != estado:
            if status_timers[implemento] is not None:
                duration = time.time() - status_timers[implemento]
                write_to_csv(datetime.now(), implemento, estado, round(duration, 2))
            current_status[implemento] = estado
            status_timers[implemento] = time.time()
            missing_timers[implemento] = None

    for implemento in status_timers.keys():
        if implemento not in detected_labels:
            if missing_timers[implemento] is None:
                missing_timers[implemento] = time.time()
            else:
                elapsed_time = time.time() - missing_timers[implemento]
                if elapsed_time > 30:
                    if current_status[implemento] != "sin":
                        alert_triggered = True
                        duration = time.time() - status_timers[implemento]
                        write_to_csv(datetime.now(), implemento, "sin", round(duration, 2))
                        current_status[implemento] = "sin"
                        status_timers[implemento] = time.time()
        else:
            missing_timers[implemento] = None

    if alert_triggered:
        winsound.Beep(1000, 500)

    cv2.imshow("Detección en tiempo real", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
