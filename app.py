import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Inventario Soldaduras", page_icon="🏗️", layout="wide")

ARCHIVO_CSV = "inventario_soldaduras.csv"

# --- FUNCIONES ---
def cargar_datos():
    if os.path.exists(ARCHIVO_CSV):
        return pd.read_csv(ARCHIVO_CSV)
    return pd.DataFrame(columns=["Producto", "Cantidad", "Precio", "Categoria"])

def guardar_datos(df):
    df.to_csv(ARCHIVO_CSV, index=False)

# --- INTERFAZ ---
with st.sidebar:
    st.header("🏭 Menú Principal")
    opcion = st.radio("Navegación", ["📊 Ver Inventario", "➕ Agregar Material", "📝 Gestionar Stock"])
    st.info("Sistema de Control v2.0")

df = cargar_datos()

if opcion == "📊 Ver Inventario":
    st.title("📊 Estado del Almacén")
    
    # Métricas
    col1, col2 = st.columns(2)
    col1.metric("Total de Productos", len(df))
    total_valor = (df["Cantidad"] * df["Precio"]).sum()
    col2.metric("Valor Total en Bodega", f"${total_valor:,.2f}")
    
    st.divider()
    
    # Buscador
    filtro = st.text_input("🔍 Buscar material:", "")
    if filtro:
        df_mostrar = df[df["Producto"].str.contains(filtro, case=False)]
    else:
        df_mostrar = df
        
    # Tabla con colores de alerta
    if not df_mostrar.empty:
        st.dataframe(df_mostrar.style.applymap(
            lambda x: 'background-color: #ffcccc' if x < 5 else '', subset=['Cantidad']
        ), use_container_width=True)
    else:
        st.info("No hay productos registrados.")

elif opcion == "➕ Agregar Material":
    st.header("Ingresar Nuevo Material")
    with st.form("form_agregar", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre del Material")
        categoria = col2.selectbox("Categoría", ["Electrodos", "Seguridad", "Herramientas", "Otros"])
        cant = col1.number_input("Cantidad", min_value=1)
        prec = col2.number_input("Precio Unitario", min_value=0.0)
        
        if st.form_submit_button("Guardar Producto", type="primary"):
            nuevo = pd.DataFrame([{"Producto": nombre, "Cantidad": cant, "Precio": prec, "Categoria": categoria}])
            df = pd.concat([df, nuevo], ignore_index=True)
            guardar_datos(df)
            st.success("✅ Guardado exitosamente")
            st.rerun()

elif opcion == "📝 Gestionar Stock":
    st.header("Modificar o Eliminar")
    producto = st.selectbox("Selecciona producto:", df["Producto"].unique())
    
    if producto:
        datos = df[df["Producto"] == producto].iloc[0]
        with st.form("form_editar"):
            c1, c2 = st.columns(2)
            n_cant = c1.number_input("Nueva Cantidad", value=int(datos["Cantidad"]))
            n_prec = c2.number_input("Nuevo Precio", value=float(datos["Precio"]))
            
            if st.form_submit_button("💾 Actualizar"):
                df.loc[df["Producto"] == producto, "Cantidad"] = n_cant
                df.loc[df["Producto"] == producto, "Precio"] = n_prec
                guardar_datos(df)
                st.success("Actualizado")
                st.rerun()