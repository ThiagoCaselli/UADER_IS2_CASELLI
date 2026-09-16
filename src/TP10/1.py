import pandas as pd

r = 0.01  # Tasa efectiva mensual del 1%
flujo_mensual_base = 1000
valor_futuro_beneficio = 18000

def calcular_vp_costos(cuota, meses):
    return sum([cuota / (1 + r)**i for i in range(1, meses + 1)])

def calcular_vp_beneficio(valor, mes_realizacion):
    return valor / (1 + r)**mes_realizacion

# a. VPN plan original (12 meses)
vp_costos_a = calcular_vp_costos(flujo_mensual_base, 12)
vp_benef_a = calcular_vp_beneficio(valor_futuro_beneficio, 12)
vpn_a = vp_benef_a - vp_costos_a

# b. VPN extendido (15 meses)
vp_costos_b = calcular_vp_costos(flujo_mensual_base, 15)
vp_benef_b = calcular_vp_beneficio(valor_futuro_beneficio, 15)
vpn_b = vp_benef_b - vp_costos_b

# c. Rentabilidad (VPN / VP Inversión)
rentabilidad_a = vpn_a / vp_costos_a
rentabilidad_b = vpn_b / vp_costos_b

# d. Impacto de retraso de 6 meses (18 meses total)
vp_costos_d = calcular_vp_costos(flujo_mensual_base, 18)
vp_benef_d = calcular_vp_beneficio(valor_futuro_beneficio, 18)
vpn_d = vp_benef_d - vp_costos_d

# e. Gestión profesional (+5% costo mensual = $1050) en 12 meses garantizados
flujo_mensual_pm = 1050
vp_costos_e = calcular_vp_costos(flujo_mensual_pm, 12)
vp_benef_e = calcular_vp_beneficio(valor_futuro_beneficio, 12)
vpn_e = vp_benef_e - vp_costos_e

# f. Desafío: VPN a 15 meses igual al VPN planeado original (vpn_a)
# Queremos que: vp_benef_b - vp_costos_f = vpn_a
# vp_costos_f = vp_benef_b - vpn_a
vp_costos_f_objetivo = vp_benef_b - vpn_a
# Factor de anualidad para 15 meses al 1%:
factor_anualidad_15 = sum([1 / (1 + r)**i for i in range(1, 16)])
cuota_maxima_f = vp_costos_f_objetivo / factor_anualidad_15

print(f"a. VPN Original (12m): ${vpn_a:.2f}")
print(f"b. VPN Extendido (15m): ${vpn_b:.2f}")
print(f"c. Rentabilidad Original: {rentabilidad_a*100:.2f}% | Rentabilidad Extendida: {rentabilidad_b*100:.2f}%")
print(f"d. VPN con 6 meses de retraso: ${vpn_d:.2f} (Destrucción de valor por retraso)")
print(f"e. VPN con PM Profesional (12m): ${vpn_e:.2f}")
print(f"f. Costo mensual máximo a 15 meses para mantener utilidad: ${cuota_maxima_f:.2f}")