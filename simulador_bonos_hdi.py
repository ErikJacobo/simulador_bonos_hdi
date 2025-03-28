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
            return porcentaje, bono, f"✅ Aplica según tabla con siniestralidad permitida."
    return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $400,001 para bono del 1%."

def calcular_bono_rentabilidad_autos(produccion, siniestralidad):
    if produccion < 2000000:
        return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $2,000,000 para bono de rentabilidad."
    tabla = [(40, 7.0), (45, 6.0), (50, 4.0), (55, 3.0), (60, 2.0)]
    for limite, porcentaje in tabla:
        if siniestralidad <= limite:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica por siniestralidad del {siniestralidad:.2f}%."
    return 0.0, 0.0, "❌ No aplica. Siniestralidad debe ser menor o igual a 60%."

def calcular_bono_produccion_danos(produccion):
    tabla = [(5300001, 8.00), (4700001, 7.00), (3600001, 6.00), (1900001, 5.00), (1200001, 4.00), (500001, 2.00)]
    for minimo, porcentaje in tabla:
        if produccion >= minimo:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica según tabla con siniestralidad permitida."
    return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $500,001 para bono del 2%."

def calcular_bono_rentabilidad_danos(produccion, siniestralidad):
    if produccion < 1000000:
        return 0.0, 0.0, "❌ No aplica. Producción mínima requerida: $1,000,000 para bono de rentabilidad."
    tabla = [(5.00, 8.0), (15.00, 6.0), (20.00, 4.0), (30.00, 2.0)]
    for limite, porcentaje in tabla:
        if siniestralidad <= limite:
            bono = produccion * (porcentaje / 100)
            return porcentaje, bono, f"✅ Aplica por siniestralidad del {siniestralidad:.2f}%."
    return 0.0, 0.0, "❌ No aplica. Siniestralidad debe ser menor o igual a 30%."

st.set_page_config(page_title="Simulador de Bonos HDI 2025", layout="centered")

st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='font-size: 40px;'>Simulador de Bonos</h1>
            <h3>HDI 2025</h3>
        </div>
        <img src='https://raw.githubusercontent.com/ErikJacobo/simulador_bonos_hdi/main/link%20logo.jpg' width='100' style='margin-top: 20px'/>
    </div>
    <br>
""", unsafe_allow_html=True)

form_container = st.container()
with form_container:
    with st.form("form_bonos"):
        nombre_agente = st.text_input("Nombre del Agente")
        tipo_bono = st.selectbox("Tipo de Bono", ["", "Autos", "Daños"])
        produccion_input = st.text_input("Producción Total ($)", placeholder="Ej. $1,000,000.00")
        siniestralidad = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, step=0.1)
        submitted = st.form_submit_button("Calcular Bonos")

if submitted:
    form_container.empty()

    try:
        produccion = limpiar_formato(produccion_input)

        st.markdown("---")
        st.markdown(f"### 📋 Resultado para **{nombre_agente.upper()}**")

        st.markdown("### 📊 Datos Ingresados:")
        st.markdown(f"- Producción: **{formato_pesos(produccion)}**")
        st.markdown(f"- Siniestralidad: **{siniestralidad:.2f}%**")

        if tipo_bono == "Autos":
            pct_prod, bono_prod, msg_prod = calcular_bono_produccion_autos(produccion)
            pct_rent, bono_rent, msg_rent = calcular_bono_rentabilidad_autos(produccion, siniestralidad)
            total_bono = bono_prod + bono_rent
            st.markdown("### 💵 Resultados de Bono:")
            st.markdown(f"- 🧾 **Bono de Producción:** {pct_prod:.2f}% → **{formato_pesos(bono_prod)}**")
            st.markdown(f"  - {msg_prod}")
            st.markdown(f"- 🛡️ **Bono de Rentabilidad:** {pct_rent:.2f}% → **{formato_pesos(bono_rent)}**")
            st.markdown(f"  - {msg_rent}")
            st.markdown(f"\n📌 **Total del Bono Autos: {formato_pesos(total_bono)}**")

        elif tipo_bono == "Daños":
            pct_prod, bono_prod, msg_prod = calcular_bono_produccion_danos(produccion)
            pct_rent, bono_rent, msg_rent = calcular_bono_rentabilidad_danos(produccion, siniestralidad)
            total_bono = bono_prod + bono_rent
            st.markdown("### 💵 Resultados de Bono:")
            st.markdown(f"- 🧾 **Bono de Producción:** {pct_prod:.2f}% → **{formato_pesos(bono_prod)}**")
            st.markdown(f"  - {msg_prod}")
            st.markdown(f"- 🛡️ **Bono de Rentabilidad:** {pct_rent:.2f}% → **{formato_pesos(bono_rent)}**")
            st.markdown(f"  - {msg_rent}")
            st.markdown(f"\n📌 **Total del Bono Daños: {formato_pesos(total_bono)}**")

        else:
            st.warning("Selecciona un tipo de bono válido.")

        st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de HDI Seguros 2025.</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar los datos: {e}")
