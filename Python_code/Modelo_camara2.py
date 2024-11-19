import cv2
from ultralytics import YOLO
import time
import csv
from datetime import datetime
import winsound

model = YOLO(r'Python_code\PyTorch\best.pt') 
cap = cv2.VideoCapture(0)

# Diccionarios para almacenar el tiempo de detección y el estado actual de cada implemento
status_timers = { "guantes": None, "chaleco": None, "gafas_protec": None, "casco": None }
current_status = { "guantes": "usando", "chaleco": "usando", "gafas_protec": "usando", "casco": "usando" }
missing_timers = { "guantes": None, "chaleco": None, "gafas_protec": None, "casco": None }

# Ruta del archivo CSV
csv_file = r'Histori_data\cumplimiento_registros.csv'
with open(csv_file, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Hora", "Implemento", "Estado", "Duración"])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar la imagen de la cámara")
        break

    results = model(frame)
    detected_labels = set()  # Mantener un registro de lo que se detecta en cada frame

    # Proceso de detección
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0]) 
        label_index = int(result.cls[0])           
        conf = result.conf[0]                      

        # Mapear el índice al nombre de la etiqueta
        labels = {
            0: "usando_guantes", 1: "sin_guantes",
            2: "usando_chaleco", 3: "sin_chaleco",
            4: "usando_gafas_protec", 5: "sin_gafas_protec",
            6: "usando_casco", 7: "sin_casco"
        }
        label_text = labels[label_index]
        
        # Extraer estado e implemento
        estado, implemento = label_text.split("_", 1)
        detected_labels.add(implemento)
        
        # Dibujar el rectángulo en la imagen
        color = (0, 255, 0) if estado == "usando" else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Si el estado cambia, registra el tiempo en CSV
        if implemento in current_status and current_status[implemento] != estado:
            if status_timers[implemento] is not None:
                duration = time.time() - status_timers[implemento]
                with open(csv_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([datetime.now(), f"{estado}_{implemento}", estado, round(duration, 2)])
            
            # Actualizar estado y temporizadores
            current_status[implemento] = estado
            status_timers[implemento] = time.time()
            missing_timers[implemento] = None
    
    # Verificar si cualquier implemento está ausente durante más de 30 segundos
    alert_triggered = False  # Indicador para disparar la alarma una sola vez por ciclo
    for implemento in status_timers.keys():
        if implemento not in detected_labels:
            if missing_timers[implemento] is None:
                missing_timers[implemento] = time.time()  # Inicia el temporizador de falta
            else:
                elapsed_time = time.time() - missing_timers[implemento]

                # Emitir alerta si el tiempo de ausencia es mayor a 30 segundos
                if elapsed_time > 30:
                    if current_status[implemento] != "sin":
                        print(f"ALERTA: La persona está sin {implemento} por más de 30 segundos.")
                        alert_triggered = True  # Activar la alarma para cualquier EPP faltante
                        
                        # Registrar en el CSV solo si el temporizador de estado no es None
                        if status_timers[implemento] is not None:
                            duration = time.time() - status_timers[implemento]
                            with open(csv_file, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([datetime.now(), f"sin_{implemento}", "sin", round(duration, 2)])

                        # Actualizar el estado a "sin" y reiniciar el temporizador de estado
                        current_status[implemento] = "sin"
                        status_timers[implemento] = time.time()

        else:
            missing_timers[implemento] = None

    # Disparar el sonido de alerta si hay algún EPP ausente durante más de 30 segundos
    if alert_triggered:
        winsound.Beep(1000, 500)  # Sonido de alerta a 1000 Hz por 500 ms

    # Mostrar imagen con detección en tiempo real
    cv2.imshow("Detección en tiempo real", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
