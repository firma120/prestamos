
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Título y menú lateral
st.set_page_config(page_title="Tu Préstamo Express", layout="wide")
st.sidebar.title("Menú")
opcion = st.sidebar.radio("Ir a:", ["Registrar Cliente", "Ver Créditos", "Consulta de Clientes", "Reportes"])

# Inicialización de base de datos en sesión
if "data" not in st.session_state:
    st.session_state.data = []

def calcular_total(monto, cuotas, interes=0.15):
    return monto * (1 + interes)

def calcular_comision(monto, porcentaje=0.02):
    return monto * porcentaje

# Registrar Cliente
if opcion == "Registrar Cliente":
    st.header("📝 Registro de nuevo cliente")

    with st.form("formulario_prestamo"):
        nombre = st.text_input("Nombre del cliente")
        cedula = st.text_input("Cédula")
        celular = st.text_input("Celular")
        correo = st.text_input("Correo (opcional)")
        fecha = st.date_input("Fecha del préstamo", value=datetime.today())
        cuotas = st.selectbox("Número de cuotas", [1, 2, 3, 4])
        monto = st.number_input("Monto del préstamo", min_value=100000, step=50000)
        observaciones = st.text_area("Observaciones")

        submitted = st.form_submit_button("Registrar préstamo")

        if submitted:
            if not (nombre and cedula and celular and monto):
                st.warning("❗ Por favor, completa todos los campos obligatorios.")
            else:
                total_pagar = calcular_total(monto, cuotas)
                comision = calcular_comision(monto)
                st.session_state.data.append({
                    "Nombre": nombre,
                    "Cédula": cedula,
                    "Celular": celular,
                    "Correo": correo,
                    "Fecha": fecha.strftime("%Y-%m-%d"),
                    "Cuotas": cuotas,
                    "Monto": monto,
                    "Comisión": comision,
                    "Total a pagar": total_pagar,
                    "Observaciones": observaciones
                })
                st.success("✅ Préstamo registrado con éxito")

# Reportes
elif opcion == "Reportes":
    st.header("📊 Tu Préstamo Express")
    st.subheader("📈 Reporte General")

    df = pd.DataFrame(st.session_state.data)

    if not df.empty:
        total_clientes = len(df)
        ganancia_total = df["Total a pagar"].sum() - df["Monto"].sum()
        comision_total = df["Comisión"].sum()
        total_recaudar = df["Total a pagar"].sum()

        st.markdown(f"- 👥 **Total clientes registrados:** {total_clientes}")
        st.markdown(f"- 💸 **Ganancia neta total:** ${ganancia_total:,.0f}")
        st.markdown(f"- 🤝 **Comisión total pagada:** ${comision_total:,.0f}")
        st.markdown(f"- 🪙 **Total a recaudar:** ${total_recaudar:,.0f}")

        st.divider()
        st.subheader("📄 Tabla de Créditos Registrados")
        st.dataframe(df, use_container_width=True)

        # Descargar Excel
        def convertir_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Préstamos')
            return output.getvalue()

        excel_data = convertir_excel(df)
        st.download_button(
            label="📥 Descargar Reporte en Excel",
            data=excel_data,
            file_name="reporte_prestamos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No hay datos registrados aún.")
