import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Cargar el modelo entrenado
with open("modelo_agua.pkl", "rb") as f:
    modelo = pickle.load(f)

st.title("💧 Clasificación de Riesgo del Agua")

# Entrada de parámetros
pH = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1)
conductividad = st.number_input("Conductividad (µS/cm)", min_value=0.0, step=1.0)
turbidez = st.number_input("Turbidez (NTU)", min_value=0.0, step=0.1)
oxigeno = st.number_input("Oxígeno disuelto (mg/L)", min_value=0.0, step=0.1)
temperatura = st.number_input("Temperatura (°C)", min_value=0.0, step=0.1)
ecoli = st.number_input("E. coli (UFC/100mL)", min_value=0, step=1)
coliformes_fecales = st.number_input("Coliformes fecales (UFC/100mL)", min_value=0, step=1)
coliformes_totales = st.number_input("Coliformes totales (UFC/100mL)", min_value=0, step=1)
no3 = st.number_input("Nitratos NO3 (mg/L)", min_value=0.0, step=0.1)
no2 = st.number_input("Nitritos NO2 (mg/L)", min_value=0.0, step=0.01)
nh4 = st.number_input("Amonio NH4 (mg/L)", min_value=0.0, step=0.01)
po4 = st.number_input("Fosfatos PO4 (mg/L)", min_value=0.0, step=0.01)

# Función para recomendaciones con nombre de la variable
def recomendar(valor, tipo):
    if tipo == "pH":
        if 6.5 <= valor <= 8.5:
            return f"pH: Bajo riesgo. pH dentro del rango adecuado."
        elif valor < 6.5:
            return f"pH: Riesgo Alto. pH bajo, lo que favorece la proliferación de patógenos."
        else:
            return f"pH: Riesgo Alto. pH alto, lo que aumenta el riesgo sanitario."
    
    elif tipo == "Conductividad":
        if valor < 200:
            return f"Conductividad: Bajo riesgo. Baja concentración de contaminantes y buena calidad del agua."
        elif 200 <= valor <= 500:
            return f"Conductividad: Riesgo Medio. Contaminantes moderados, pero aún aceptable."
        else:
            return f"Conductividad: Riesgo Alto. Alta contaminación fecal y presencia de nutrientes."
    
    elif tipo == "Turbidez":
        if valor < 5:
            return f"Turbidez: Bajo riesgo. Buena calidad, baja suspensión de sólidos."
        elif 5 <= valor <= 10:
            return f"Turbidez: Riesgo Medio. Moderada turbidez que podría alojar patógenos."
        else:
            return f"Turbidez: Riesgo Alto. Alta turbidez que facilita la propagación de microorganismos."

    elif tipo == "Oxígeno disuelto":
        if valor > 6:
            return f"Oxígeno disuelto: Bajo riesgo. Buen nivel de oxígeno, condiciones saludables para vida acuática."
        elif 4 <= valor <= 6:
            return f"Oxígeno disuelto: Riesgo Medio. Reducción del oxígeno disuelto, posible contaminación orgánica."
        else:
            return f"Oxígeno disuelto: Riesgo Alto. Condiciones anaeróbicas, afectando vida acuática."

    elif tipo == "Temperatura":
        if 20 <= valor <= 25:
            return f"Temperatura: Bajo riesgo. Condiciones naturales, con baja proliferación bacteriana."
        elif 26 <= valor <= 30:
            return f"Temperatura: Riesgo Medio. Condiciones que favorecen crecimiento bacteriano moderado."
        else:
            return f"Temperatura: Riesgo Alto. Temperatura alta, favoreciendo la proliferación bacteriana."

    elif tipo == "E. coli":
        if valor == 0:
            return f"E. coli: Bajo riesgo. Agua libre de E. coli."
        elif 0 < valor <= 1:
            return f"E. coli: Riesgo Medio. Posible contaminación incipiente."
        else:
            return f"E. coli: Riesgo Alto. Contaminación fecal activa."

    # Aquí puedes agregar los demás parámetros como coliformes, nitratos, etc.

# Clasificar riesgo (sin mostrar riesgo general)
if st.button("Clasificar Riesgo"):
    # Crear dataframe con los datos ingresados
    datos = pd.DataFrame([[pH, conductividad, turbidez, oxigeno, temperatura,
                           ecoli, coliformes_fecales, coliformes_totales,
                           no3, no2, nh4, po4]],
                         columns=["pH", "Conductividad (µS/cm)", "Turbidez (NTU)",
                                  "Oxígeno disuelto (mg/L)", "Temperatura (°C)",
                                  "E. coli (UFC/100mL)", "Coliformes fecales (UFC/100mL)",
                                  "Coliformes totales (UFC/100mL)",
                                  "NO3 (mg/L)", "NO2 (mg/L)", "NH4 (mg/L)", "PO4 (mg/L)"])

    # Predecir riesgo general (pero ya no lo mostramos)
    # pred = modelo.predict(datos)[0]  # Esta línea la quitamos, ya no se necesita mostrar el riesgo general.

    # Mostrar las recomendaciones personalizadas
    st.subheader("Recomendaciones por Parámetro:")
    st.write(recomendar(pH, "pH"))
    st.write(recomendar(conductividad, "Conductividad"))
    st.write(recomendar(turbidez, "Turbidez"))
    st.write(recomendar(oxigeno, "Oxígeno disuelto"))
    st.write(recomendar(temperatura, "Temperatura"))
    st.write(recomendar(ecoli, "E. coli"))
    # Añadir más parámetros aquí como coliformes, nitratos, etc.

    # Gráfica de los parámetros ingresados
    fig, ax = plt.subplots()
    valores = [pH, conductividad, turbidez, oxigeno, temperatura, ecoli,
               coliformes_fecales, coliformes_totales, no3, no2, nh4, po4]
    etiquetas = ["pH", "Cond.", "Turb.", "O2", "Temp", "E. coli",
                 "C. fecales", "C. totales", "NO3", "NO2", "NH4", "PO4"]

    ax.bar(etiquetas, valores, color="skyblue")
    ax.set_ylabel("Valores ingresados")
    ax.set_title("Parámetros del Agua")
    plt.xticks(rotation=45)
    st.pyplot(fig)
