import pandas as pd
import numpy as np
import plotly.express as px
from scipy.interpolate import make_interp_spline

df = pd.read_excel("Medidas cozinha.xlsx", sheet_name="Planilha1", engine="openpyxl")

# Selecionar colunas relevantes
medidas = df.iloc[1:, 1].astype(float)  # λ/2 em cm
quantidades = df.iloc[1:, 2].astype(int)  # frequência

# Filtrar apenas valores com quantidade > 0
mask = quantidades > 0
medidas = medidas[mask]
quantidades = quantidades[mask]

#Criar gráfico de pontos
fig = px.scatter(x=medidas, y=quantidades, labels={"x": "λ/2 (cm)", "y": "Frequência"}, title="Distribuição das medidas de λ/2")


x_new = np.linspace(medidas.min(), medidas.max(), 300)
spline = make_interp_spline(medidas, quantidades)
y_smooth = spline(x_new)

fig.add_scatter(x=x_new, y=y_smooth, mode='lines', name='Curva Ajustada')

fig.write_json("grafico_lambda2.json")
fig.write_image("grafico_lambda2.png")

# Encontrar pico da curva (valor mais provável de λ/2)
idx_max = np.argmax(y_smooth)
lambda2_cm = x_new[idx_max]

freq = 2.45e9  # Hz
lambda_m = (lambda2_cm * 2) / 100  # converter cm para m e dobrar
c_calculado = freq * lambda_m


c_esperado = 3e8
erro = abs(c_calculado - c_esperado) / c_esperado * 100

print(f"Valor mais provável de λ/2: {lambda2_cm:.2f} cm")
print(f"Comprimento de onda λ: {lambda_m:.4f} m")
print(f"Velocidade da luz calculada: {c_calculado:.2e} m/s")
print(f"Erro percentual: {erro:.2f}%")
if erro < 10:
    print("Resultado válido: está próximo do valor esperado.")
else:
    print("Resultado não muito preciso: possíveis erros experimentais.")
