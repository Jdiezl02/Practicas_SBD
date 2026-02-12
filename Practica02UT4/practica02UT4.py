import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore

datos_ninja = pd.read_csv("misiones_limpias.csv")

print(datos_ninja.head())

perfil = datos_ninja['Nivel_Chakra'].describe()
print("\nPerfil de Nivel_Chakra:\n", perfil)

media_chakra = perfil['mean']
desv_chakra = perfil['std']
max_chakra = perfil['max']

datos_ninja["Z"] = (datos_ninja["Nivel_Chakra"] - media_chakra)/desv_chakra
datos_ninja_z = datos_ninja[datos_ninja["Z"] >= 3]

print(datos_ninja_z[["ID","Z"]])

datos_ninja_superninja = datos_ninja[(datos_ninja["Z"] >= 2) & (datos_ninja["Z"] <= 3)]

print(datos_ninja_superninja[["ID","Z"]])

print(f"\nMedia de Chakra: {media_chakra}")
print(f"Desviación estándar: {desv_chakra}")
print(f"Valor máximo: {max_chakra}")

datos_ninja_f = datos_ninja[datos_ninja["Nivel_Chakra"] < 0]

print(datos_ninja_f[["ID", "Nivel_Chakra"]])

datos_ninja_a = datos_ninja[(datos_ninja["Aldea"] != "Konoha") & (datos_ninja["Aldea"] != "Suna") & (datos_ninja["Aldea"] != "Iwa") & (datos_ninja["Aldea"] != "Kiri") & (datos_ninja["Aldea"] != "Suna") & (datos_ninja["Aldea"] != "Iwa") & (datos_ninja["Aldea"] != "Kumo")]

print(datos_ninja_a[["ID","Aldea"]])

ninjaTraidor = datos_ninja[(datos_ninja["ID"] == 699)]

print(datos_ninja_a[["ID","Aldea","Rango","Nivel_Chakra","Misiones_Falladas"]])

plt.figure(figsize=(8, 6))
sns.boxplot(y=datos_ninja["Nivel_Chakra"], color='orange')
plt.title('Nivel de Chakra')
plt.show()

