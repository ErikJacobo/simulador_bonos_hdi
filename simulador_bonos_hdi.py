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
    if produccion >= 4700001:
        porcentaje = 5.00
    elif produccion >= 2850001:
        porcentaje = 4.00
    elif produccion >= 1900001:
        porcentaje = 3.00
    elif produccion >= 700001:
        porcentaje = 2.00
    elif produccion >= 400001:
        porcentaje = 1.00
    else:
        porcentaje = 0.00
    bono = produccion * (porcentaje / 100)
    return porcentaje, bono

def calcular_bono_rentabilidad_autos(produccion, siniestralidad):
    if produccion < 2000000:
        return 0.0, 0.0, "❌ Producción mínima no alcanzada para bono de rentabilidad."
    if siniestralidad <= 40:
        porcentaje = 7.0
    elif siniestralidad <= 45:
        porcentaje = 6.0
    elif siniestralidad <= 50:
        porcentaje = 4.0
    elif siniestralidad <= 55:
        porcentaje = 3.0
    elif siniestralidad <= 60:
        porcentaje = 2.0
    else:
        porcentaje = 0.0
    comentario = "✅ Bono aplicado según siniestralidad." if porcentaje > 0 else "❌ Siniestralidad excede el límite."
    bono = produccion * (porcentaje / 100)
    return porcentaje, bono, comentario

def calcular_bono_produccion_danos(produccion):
    if produccion >= 5300001:
        porcentaje = 8.00
    elif produccion >= 4700001:
        porcentaje = 7.00
    elif produccion >= 3600001:
        porcentaje = 6.00
    elif produccion >= 1900001:
        porcentaje = 5.00
    elif produccion >= 1200001:
        porcentaje = 4.00
    elif produccion >= 500001:
        porcentaje = 2.00
    else:
        porcentaje = 0.00
    bono = produccion * (porcentaje / 100)
    return porcentaje, bono

def calcular_bono_rentabilidad_danos(produccion, siniestralidad):
    if produccion < 1000000:
        return 0.0, 0.0, "❌ Producción mínima no alcanzada para bono de rentabilidad."
    if siniestralidad <= 5:
        porcentaje = 8.0
    elif siniestralidad <= 15:
        porcentaje = 6.0
    elif siniestralidad <= 20:
        porcentaje = 4.0
    elif siniestralidad <= 30:
        porcentaje = 2.0
    else:
        porcentaje = 0.0
    comentario = "✅ Bono aplicado según siniestralidad." if porcentaje > 0 else "❌ Siniestralidad excede el límite."
    bono = produccion * (porcentaje / 100)
    return porcentaje, bono, comentario

# INTERFAZ STREAMLIT
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
                pct_prod, bono_prod = calcular_bono_produccion_autos(produccion)
                pct_rent, bono_rent, comentario_rent = calcular_bono_rentabilidad_autos(produccion, siniestralidad)
            else:
                pct_prod, bono_prod = calcular_bono_produccion_danos(produccion)
                pct_rent, bono_rent, comentario_rent = calcular_bono_rentabilidad_danos(produccion, siniestralidad)

            st.markdown("---")
            st.markdown("### BONO DE PRODUCCIÓN")
            st.markdown(f"**% Aplicado:** {pct_prod}%")
            st.markdown(f"**Monto de Bono:** {formato_pesos(bono_prod)}")
            st.markdown("✅ Aplica" if pct_prod > 0 else "❌ No aplica")

            st.markdown("### BONO DE RENTABILIDAD")
            st.markdown(f"**% Aplicado:** {pct_rent}%")
            st.markdown(f"**Monto de Bono:** {formato_pesos(bono_rent)}")
            st.markdown(comentario_rent)

        except Exception as e:
            st.error("Ocurrió un error al calcular. Verifica los datos ingresados.")
