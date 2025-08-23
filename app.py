import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# --- Cargar modelo entrenado ---
with open("modelo_agua.pkl", "rb") as f:
    modelo = pickle.load(f)

st.title("💧 Clasificación de Riesgo del Agua")

st.markdown("Introduce los parámetros fisicoquímicos y microbiológicos del agua para predecir el nivel de **riesgo sanitario**.")

# --- Entradas del usuario ---
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

# --- Clasificación ---
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

    # Predecir
    pred = modelo.predict(datos)[0]

    st.subheader(f"✅ Riesgo Clasificado: **{pred}**")

    # Recomendaciones según el riesgo
    if pred == "Alto":
        st.error("⚠️ El agua **NO es apta** para consumo. Se recomienda hervir, clorar o filtrar antes de usar.")
    elif pred == "Medio":
        st.warning("🟠 Riesgo **moderado**. Se recomienda tratamiento previo al consumo.")
    else:
        st.success("🟢 Agua en condiciones seguras para consumo.")

    # --- Gráfica de los parámetros ingresados ---
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
