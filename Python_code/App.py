import streamlit as st
import pandas as pd
import time

# Ruta del archivo CSV
csv_file = r'Histori_data\cumplimiento_registros.csv'

# Configuración de la interfaz de Streamlit
st.title("Monitoreo de EPP - SafeSight AI")
st.subheader("Estado en tiempo real de los implementos de seguridad")

# Placeholder para los datos y gráficos
placeholder_data = st.empty()  # Para mostrar los datos en tiempo real
placeholder_historico = st.empty()  # Para la gráfica de histórico de uso
placeholder_distribucion = st.empty()  # Para la gráfica de distribución
placeholder_duracion_promedio = st.empty()  # Para la gráfica de duración promedio
placeholder_cambios_estado = st.empty()  # Para la gráfica de cambios de estado

# Función para cargar y mostrar datos en tiempo real
def load_and_display_data():
    while True:
        # Leer el archivo CSV y realizar conversiones necesarias
        data = pd.read_csv(csv_file, encoding='latin-1')
        data['Hora'] = pd.to_datetime(data['Hora'], errors='coerce')  # Convertir a datetime

        # Mostrar los datos en tabla
        with placeholder_data.container():
            st.write("Historial de cumplimiento:", data)

        # Verificar si hay datos antes de generar las gráficas
        if data.empty:
            st.error("No hay datos disponibles para generar las gráficas. Intentando de nuevo en 1 segundo...")
            time.sleep(1)
            continue  # Intentar nuevamente si no hay datos

        # Gráfica 1: Histórico de uso por implemento
        with placeholder_historico.container():
            st.write("### Histórico de uso por implemento")
            for implemento in data['Implemento'].unique():
                subset = data[data['Implemento'] == implemento]
                if subset.empty:
                    st.warning(f"No hay datos suficientes para el implemento '{implemento}' en el histórico de uso.")
                    time.sleep(1)
                    continue
                st.line_chart(subset.set_index('Hora')['Duración'], height=300, width=0)

        # Gráfica 2: Distribución de tiempo en cada estado por implemento
        with placeholder_distribucion.container():
            st.write("### Distribución de tiempo en cada estado por implemento")
            estados_counts = data.groupby(['Implemento', 'Estado']).size().unstack(fill_value=0)
            if estados_counts.empty:
                st.error("No hay datos suficientes para generar la gráfica de distribución de tiempo por estado.")
                time.sleep(1)
                continue
            st.bar_chart(estados_counts)

        # Gráfica 3: Duración promedio de cada estado por implemento
        with placeholder_duracion_promedio.container():
            st.write("### Duración promedio de cada estado por implemento")
            duracion_promedio = data.groupby(['Implemento', 'Estado'])['Duración'].mean().unstack(fill_value=0)
            if duracion_promedio.empty:
                st.error("No hay datos suficientes para generar la gráfica de duración promedio por estado.")
                time.sleep(1)
                continue
            st.bar_chart(duracion_promedio)

        # Gráfica 4: Tendencia de cambios de estado
        with placeholder_cambios_estado.container():
            st.write("### Tendencia de cambios de estado")
            data['Cambio'] = data['Estado'].ne(data['Estado'].shift()).astype(int)
            cambios_estado = data.groupby([data['Hora'].dt.date, 'Implemento'])['Cambio'].sum().unstack(fill_value=0)
            if cambios_estado.empty:
                st.error("No hay datos suficientes para generar la gráfica de cambios de estado.")
                time.sleep(1)
                continue
            st.line_chart(cambios_estado)

        time.sleep(5)  # Actualización cada 5 segundos

# Ejecutar la función para cargar datos y actualizar gráficos
load_and_display_data()
