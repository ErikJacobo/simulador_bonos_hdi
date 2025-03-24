import streamlit as st
import locale
import re

locale.setlocale(locale.LC_ALL, '')

def formato_pesos(valor):
    try:
        valor_float = float(valor)
        return f"${valor_float:,.2f}"
    except:
        return valor

def limpiar_formato(valor):
    try:
        return float(str(valor).replace(',', '').replace('$', ''))
    except:
        return 0.0

def calcular_bono_produccion_autos(produccion):
    tabla = [(4700001, 5.00), (2850001, 4.00), (1900001, 3.00), (700001, 2.00), (400001, 1.00)]
    for minimo, porcentaje in tabla:
        if produccion >= minimo:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica. Producción supera ${minimo:,.0f} (Bono del {porcentaje}%)"
    return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $400,001 para bono del 1%."

def calcular_bono_rentabilidad_autos(produccion, siniestralidad):
    if produccion < 2000000:
        return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $2,000,000 para bono de rentabilidad."
    tabla = [(40, 7.0), (45, 6.0), (50, 4.0), (55, 3.0), (60, 2.0)]
    for limite, porcentaje in tabla:
        if siniestralidad <= limite:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica. Siniestralidad menor o igual a {limite}% (Bono del {porcentaje}%)"
    return 0.0, 0.0, "❌ No aplica. Siniestralidad debe ser menor o igual a 60%."

def calcular_bono_produccion_danos(produccion):
    tabla = [(5300001, 8.00), (4700001, 7.00), (3600001, 6.00), (1900001, 5.00), (1200001, 4.00), (500001, 2.00)]
    for minimo, porcentaje in tabla:
        if produccion >= minimo:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica. Producción supera ${minimo:,.0f} (Bono del {porcentaje}%)"
    return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $500,001 para bono del 2%."

def calcular_bono_rentabilidad_danos(produccion, siniestralidad):
    if produccion < 1000000:
        return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $1,000,000 para bono de rentabilidad."
    tabla = [(5, 8.0), (15, 6.0), (20, 4.0), (30, 2.0)]
    for limite, porcentaje in tabla:
        if siniestralidad <= limite:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica. Siniestralidad menor o igual a {limite}% (Bono del {porcentaje}%)"
    return 0.0, 0.0, "❌ No aplica. Siniestralidad debe ser menor o igual a 30%."

st.set_page_config(page_title="Simulador de Bonos HDI 2025")
st.title("Simulador de Bonos")
st.subheader("HDI 2025")

nombre_agente = st.text_input("Nombre del Agente")
tipo_bono = st.selectbox("Tipo de Bono", ["", "Autos", "Daños"])

if tipo_bono:
    produccion_input = st.text_input("Producción Total (en pesos)")
    siniestralidad = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Calcular Bonos"):
        try:
            produccion = limpiar_formato(produccion_input)

            st.markdown(f"**Agente:** {nombre_agente}")
            st.markdown(f"**Tipo:** {tipo_bono}")
            st.markdown(f"**Producción:** {formato_pesos(produccion)}")
            st.markdown(f"**Siniestralidad:** {siniestralidad:.2f}%")

            if tipo_bono == "Autos":
                pct_prod, bono_prod, msg_prod = calcular_bono_produccion_autos(produccion)
                pct_rent, bono_rent, msg_rent = calcular_bono_rentabilidad_autos(produccion, siniestralidad)
            else:
                pct_prod, bono_prod, msg_prod = calcular_bono_produccion_danos(produccion)
                pct_rent, bono_rent, msg_rent = calcular_bono_rentabilidad_danos(produccion, siniestralidad)

            st.markdown("---")
            st.markdown("### BONO DE PRODUCCIÓN")
            st.markdown(f"**% Aplicado:** {pct_prod}%")
            st.markdown(f"**Monto de Bono:** {formato_pesos(bono_prod)}")
            st.markdown(f"{msg_prod}")

            st.markdown("### BONO DE RENTABILIDAD")
            st.markdown(f"**% Aplicado:** {pct_rent}%")
            st.markdown(f"**Monto de Bono:** {formato_pesos(bono_rent)}")
            st.markdown(f"{msg_rent}")

        except Exception as e:
            st.error("Ocurrió un error al calcular. Verifica los datos ingresados.")
