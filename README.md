
---

# SafeSight AI: Real-Time PPE Monitoring

SafeSight AI is an application designed to enhance safety in industrial environments by monitoring the use of personal protective equipment (PPE) in real time. It uses a custom YOLOv8 model to detect and record the status of safety equipment, generating alerts if prolonged non-compliance is detected.

## Features

- **Real-time detection**: Identifies the correct or incorrect use of gloves, vests, safety goggles, and helmets.
- **Historical records**: Stores data on PPE compliance, including duration and timestamps of events.
- **Data visualization**: Interactive interface to analyze historical compliance and trends.
- **Audible alerts**: Triggers alarms if a piece of equipment is missing for more than 30 seconds.

## Requirements

- Python 3.8 or higher
- Required libraries (see [Installation](#installation))
- Functional webcam
- Windows operating system (required for `winsound`)

## Project Structure

```
SafeSightAI/
│
├── Execute_App.bat        # File to run the full application
├── Histori_data/
│   └── cumplimiento_registros.csv  # CSV file for data logging
│
├── Python_code/
│   ├── PyTorch/
│   │   └── best.pt        # Trained YOLOv8 model
│   ├── App.py             # Streamlit application for data visualization
│   ├── detectar_epp.py    # Main script for PPE detection
│   └── Modelo_camara2.py  # Alternate script for camera detection
│
└── README.md              # Project documentation
```

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/isabellaperezcav/SafeSight-AI
   cd SafeSightAI
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   **Note**: Generate a `requirements.txt` file based on the libraries used (`ultralytics`, `pandas`, `streamlit`, `opencv-python`, etc.).

3. **Ensure the YOLOv8 model is available**:
   The `best.pt` file should be located in `Python_code/PyTorch/`.

## Usage

1. **Run the application**:
   - Execute the `Execute_App.bat` file or manually run the required scripts:
     ```bash
     python Python_code/detectar_epp.py
     python Python_code/App.py
     ```

2. **Main features**:
   - Real-time detection is performed through `detectar_epp.py`.
   - Visualize historical data in real time with `App.py` (access it via `http://localhost:8501` in your browser).

## Contributions

Contributions are welcome! If you find any issues or want to add new features, feel free to open an *issue* or submit a *pull request*.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Contact

If you have questions or suggestions, contact isabellaperezcav@gmail.com. 

--- 
