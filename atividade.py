import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import curve_fit


try:
    df = pd.read_excel("Medidas cozinha.xlsx", sheet_name="Planilha1", engine="openpyxl")
except:
  
    df = pd.read_csv("Medidas cozinha.xlsx - Planilha1.csv")


medidas = pd.to_numeric(df.iloc[1:, 1], errors='coerce') 
quantidades = pd.to_numeric(df.iloc[1:, 2], errors='coerce') 


mask_valid = ~np.isnan(medidas) & ~np.isnan(quantidades)
medidas = medidas[mask_valid]
quantidades = quantidades[mask_valid]

mask_pos = quantidades > 0
medidas_filtradas = medidas[mask_pos]
quantidades_filtradas = quantidades[mask_pos]

def gaussian(x, amplitude, media, desvio_padrao):
    return amplitude * np.exp(-((x - media) ** 2) / (2 * desvio_padrao ** 2))

chute_inicial = [max(quantidades), np.mean(medidas), 1.0]

try:
    popt, pcov = curve_fit(gaussian, medidas, quantidades, p0=chute_inicial)
    amplitude_otim, media_otim, desvio_otim = popt
    
    
    x_new = np.linspace(min(medidas), max(medidas), 300)
    y_smooth = gaussian(x_new, *popt)
    
 
    lambda2_cm = media_otim
    sucesso_fit = True
except:
    print("Não foi possível ajustar a curva gaussiana. Verifique os dados.")
    lambda2_cm = 0
    sucesso_fit = False

fig = px.scatter(x=medidas_filtradas, y=quantidades_filtradas, 
                 labels={"x": "Medida λ/2 (cm)", "y": "Frequência"}, 
                 title="Ajuste Gaussiano: Velocidade da Luz")

if sucesso_fit:
    fig.add_scatter(x=x_new, y=y_smooth, mode='lines', name=f'Ajuste (Pico: {lambda2_cm:.2f} cm)')

fig.show() 


freq = 2.45e9  
lambda_m = (lambda2_cm * 2) / 100 
c_calculado = freq * lambda_m

c_esperado = 3e8 
erro = abs(c_calculado - c_esperado) / c_esperado * 100


print("-" * 30)
print(f"RESULTADOS DA ANÁLISE:")
print(f"Valor mais provável de λ/2 (Pico da Curva): {lambda2_cm:.4f} cm")
print(f"Comprimento de onda λ: {lambda_m:.4f} m")
print(f"Velocidade da luz calculada: {c_calculado:.2e} m/s")
print(f"Erro percentual: {erro:.2f}%")
print("-" * 30)

if erro < 15:
    print("CONCLUSÃO: O resultado é VÁLIDO. O erro é aceitável para este método caseiro.")
else:
    print("CONCLUSÃO: O erro está alto. Verifique as medidas ou a frequência do aparelho.")
