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
    # Verificar los valores según cada parámetro
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

    # Aquí puedes agregar los demás parámetros como Oxígeno, E. coli, etc., siguiendo el mismo patrón.
