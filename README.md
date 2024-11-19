
---

# SafeSight AI: Monitoreo de EPP en Tiempo Real

SafeSight AI es una aplicación diseñada para mejorar la seguridad en entornos industriales mediante el monitoreo en tiempo real del uso de equipos de protección personal (EPP). Utiliza un modelo YOLOv8 personalizado para detectar y registrar el estado de los implementos de seguridad en tiempo real, generando alertas si se detecta incumplimiento prolongado.

## Características

- **Detección en tiempo real**: Identifica el uso correcto o incorrecto de guantes, chalecos, gafas protectoras y cascos.
- **Registros históricos**: Almacena datos sobre el cumplimiento del uso de EPP, incluyendo duración y momento del evento.
- **Visualización de datos**: Interfaz interactiva para analizar el cumplimiento histórico y tendencias.
- **Alertas sonoras**: Emite alarmas si un implemento está ausente por más de 30 segundos.

## Requisitos

- Python 3.8 o superior
- Bibliotecas requeridas (ver [instalación](#instalación))
- Cámara web funcional
- Sistema operativo Windows (requisito para `winsound`)

## Estructura del Proyecto

```
SafeSightAI/
│
├── Execute_App.bat        # Archivo para ejecutar la aplicación completa
├── Histori_data/
│   └── cumplimiento_registros.csv  # Archivo CSV para registrar datos
│
├── Python_code/
│   ├── PyTorch/
│   │   └── best.pt        # Modelo YOLOv8 entrenado
│   ├── App.py             # Aplicación Streamlit para visualización de datos
│   ├── detectar_epp.py    # Script principal para detección de EPP
│   └── Modelo_camara2.py  # Script alternativo para detección en cámara
│
└── README.md              # Documentación del proyecto
```

## Instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/isabellaperezcav/SafeSight-AI
   cd SafeSightAI
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   **Nota**: Genera un archivo `requirements.txt` basado en las bibliotecas utilizadas (`ultralytics`, `pandas`, `streamlit`, `opencv-python`, etc.).

3. **Asegúrate de que el modelo YOLOv8 está disponible**:
   El archivo `best.pt` debe estar ubicado en `Python_code/PyTorch/`.

## Uso

1. **Inicia la aplicación**:
   - Ejecuta el archivo `Execute_App.bat` o lanza manualmente los scripts requeridos:
     ```bash
     python Python_code/detectar_epp.py
     python Python_code/App.py
     ```

2. **Funciones principales**:
   - La detección en tiempo real se realiza a través de `detectar_epp.py`.
   - Visualiza datos históricos en tiempo real con `App.py` (accede desde `http://localhost:8501` en tu navegador).

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras errores o deseas añadir nuevas características, abre un *issue* o envía un *pull request*.

## Licencia

Este proyecto está licenciado bajo los términos de [MIT License](LICENSE).

## Contacto

Si tienes preguntas o sugerencias, contacta a isabellaperezcav@gmail.com.