import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# 1. Cargar dataset
df = pd.read_csv("calidad_agua.csv")

# 2. Variables de entrada (todas menos Riesgo)
X = df.drop(columns=["Riesgo"])
y = df["Riesgo"]

# 3. Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entrenar modelo
modelo = RandomForestClassifier(n_estimators=200, random_state=42)
modelo.fit(X_train, y_train)

# 5. Evaluar
y_pred = modelo.predict(X_test)
print("Precisión del modelo:", accuracy_score(y_test, y_pred))
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

# 6. Guardar modelo
with open("modelo_agua.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("✅ Modelo entrenado y guardado como modelo_agua.pkl")
