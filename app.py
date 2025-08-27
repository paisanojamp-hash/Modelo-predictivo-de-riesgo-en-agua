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

# Función para asignar colores a las recomendaciones
def color_recomendacion(riesgo):
    if riesgo == "Bajo":
        return "green", "Bajo riesgo"
    elif riesgo == "Medio":
        return "yellow", "Riesgo medio"
    else:
        return "red", "Riesgo alto"

# Función para recomendaciones con nombre de la variable
def recomendar(valor, tipo):
    if tipo == "pH":
        if 6.5 <= valor <= 8.5:
            color, texto = color_recomendacion("Bajo")
            return f"pH: {texto}. pH dentro del rango adecuado.", color
        elif valor < 6.5:
            color, texto = color_recomendacion("Alto")
            return f"pH: {texto}. pH bajo, lo que favorece la proliferación de patógenos.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"pH: {texto}. pH alto, lo que aumenta el riesgo sanitario.", color
    
    elif tipo == "Conductividad":
        if valor < 200:
            color, texto = color_recomendacion("Bajo")
            return f"Conductividad: {texto}. Baja concentración de contaminantes y buena calidad del agua.", color
        elif 200 <= valor <= 500:
            color, texto = color_recomendacion("Medio")
            return f"Conductividad: {texto}. Contaminantes moderados, pero aún aceptable.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Conductividad: {texto}. Alta contaminación fecal y presencia de nutrientes.", color
    
    elif tipo == "Turbidez":
        if valor < 5:
            color, texto = color_recomendacion("Bajo")
            return f"Turbidez: {texto}. Buena calidad, baja suspensión de sólidos.", color
        elif 5 <= valor <= 10:
            color, texto = color_recomendacion("Medio")
            return f"Turbidez: {texto}. Moderada turbidez que podría alojar patógenos.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Turbidez: {texto}. Alta turbidez que facilita la propagación de microorganismos.", color

    elif tipo == "Oxígeno disuelto":
        if valor > 6:
            color, texto = color_recomendacion("Bajo")
            return f"Oxígeno disuelto: {texto}. Buen nivel de oxígeno, condiciones saludables para vida acuática.", color
        elif 4 <= valor <= 6:
            color, texto = color_recomendacion("Medio")
            return f"Oxígeno disuelto: {texto}. Reducción del oxígeno disuelto, posible contaminación orgánica.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Oxígeno disuelto: {texto}. Condiciones anaeróbicas, afectando vida acuática.", color

    elif tipo == "Temperatura":
        if 20 <= valor <= 25:
            color, texto = color_recomendacion("Bajo")
            return f"Temperatura: {texto}. Condiciones naturales, con baja proliferación bacteriana.", color
        elif 26 <= valor <= 30:
            color, texto = color_recomendacion("Medio")
            return f"Temperatura: {texto}. Condiciones que favorecen crecimiento bacteriano moderado.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Temperatura: {texto}. Temperatura alta, favoreciendo la proliferación bacteriana.", color

    elif tipo == "E. coli":
        if valor == 0:
            color, texto = color_recomendacion("Bajo")
            return f"E. coli: {texto}. Agua libre de E. coli.", color
        elif 0 < valor <= 1:
            color, texto = color_recomendacion("Medio")
            return f"E. coli: {texto}. Posible contaminación incipiente.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"E. coli: {texto}. Contaminación fecal activa.", color
    
    elif tipo == "Coliformes fecales":
        if valor == 0:
            color, texto = color_recomendacion("Bajo")
            return f"Coliformes fecales: {texto}. Ausencia (0 UFC/100mL) o niveles insignificantes, garantizando seguridad sanitaria.", color
        elif 0 < valor <= 1:
            color, texto = color_recomendacion("Medio")
            return f"Coliformes fecales: {texto}. Pequeñas cantidades (hasta 1 UFC/100mL) que requieren monitoreo y posibles medidas preventivas.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Coliformes fecales: {texto}. Niveles superiores a 1 UFC/100mL indican contaminación fecal presente con riesgo sanitario grave.", color

    elif tipo == "Coliformes totales":
        if valor < 10:
            color, texto = color_recomendacion("Bajo")
            return f"Coliformes totales: {texto}. Valores menores a 10 UFC/100mL, aceptables para buena calidad microbiológica.", color
        elif 10 <= valor <= 40:
            color, texto = color_recomendacion("Medio")
            return f"Coliformes totales: {texto}. Entre 10 y 40 UFC/100mL, alerta de contaminación fecal creciente.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Coliformes totales: {texto}. Más de 40 UFC/100mL, necesidad de acción urgente para evitar riesgos.", color

    elif tipo == "Fosfatos":
        if valor < 0.1:
            color, texto = color_recomendacion("Bajo")
            return f"Fosfatos (PO4): {texto}. Menor a 0.1 mg/L, límites que minimizan riesgo de eutrofización.", color
        elif 0.1 <= valor <= 0.3:
            color, texto = color_recomendacion("Medio")
            return f"Fosfatos (PO4): {texto}. Entre 0.1 y 0.3 mg/L, señales de alerta para proliferación algal.", color
        else:
            color, texto = color_recomendacion("Alto")
            return f"Fosfatos (PO4): {texto}. Mayor a 0.3 mg/L, riesgo alto de eutrofización, floración de algas nocivas y deterioro ambiental.", color

    # Aquí puedes agregar más parámetros como Nitratos, Nitritos, etc.

# Clasificar riesgo (sin mostrar riesgo general)
if st.button("Clasificar Riesgo"):
    # Mostrar las recomendaciones personalizadas
    st.subheader("Recomendaciones por Parámetro:")
    
    recomendacion, color_pH = recomendar(pH, "pH")
    st.markdown(f"<p style='color:{color_pH};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Conductividad = recomendar(conductividad, "Conductividad")
    st.markdown(f"<p style='color:{color_Conductividad};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Turbidez = recomendar(turbidez, "Turbidez")
    st.markdown(f"<p style='color:{color_Turbidez};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Oxigeno = recomendar(oxigeno, "Oxígeno disuelto")
    st.markdown(f"<p style='color:{color_Oxigeno};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Temperatura = recomendar(temperatura, "Temperatura")
    st.markdown(f"<p style='color:{color_Temperatura};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Ecoli = recomendar(ecoli, "E. coli")
    st.markdown(f"<p style='color:{color_Ecoli};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Coliformes = recomendar(coliformes_fecales, "Coliformes fecales")
    st.markdown(f"<p style='color:{color_Coliformes};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_ColiformesTotales = recomendar(coliformes_totales, "Coliformes totales")
    st.markdown(f"<p style='color:{color_ColiformesTotales};'>{recomendacion}</p>", unsafe_allow_html=True)

    recomendacion, color_Fosfatos = recomendar(po4, "Fosfatos")
    st.markdown(f"<p style='color:{color_Fosfatos};'>{recomendacion}</p>", unsafe_allow_html=True)

    # Gráfica de los parámetros ingresados
    fig, ax = plt.subplots()
    valores = [pH, conductividad, turbidez, oxigeno, temperatura, ecoli,
               coliformes_fecales, coliformes_totales, no3, no2, nh4, po4]
    etiquetas = ["pH", "Cond.", "Turb.", "O2", "Temp", "E. coli",
                 "C. fecales", "C. totales", "NO3", "NO2", "NH4", "PO4"]

    # Asignar colores a las barras según los valores
    colores = [color_pH, color_Conductividad, color_Turbidez, color_Oxigeno,
               color_Temperatura, color_Ecoli, color_Coliformes, color_ColiformesTotales, 
               "green", "yellow", "red", "blue"]

    ax.bar(etiquetas, valores, color=colores)
    ax.set_ylabel("Valores ingresados")
    ax.set_title("Parámetros del Agua")
    plt.xticks(rotation=45)
    st.pyplot(fig)
