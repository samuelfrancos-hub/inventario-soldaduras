import streamlit as st
import pandas as pd
import os

# Nombre del archivo donde se guardan los datos (ahora usaremos CSV para que sea compatible con Excel)
ARCHIVO_CSV = "inventario_soldaduras.csv"

# --- FUNCIONES DE LÓGICA ---
def cargar_datos():
    if os.path.exists(ARCHIVO_CSV):
        return pd.read_csv(ARCHIVO_CSV)
    else:
        # Si no existe, creamos un DataFrame vacío con las columnas
        return pd.DataFrame(columns=["Producto", "Cantidad", "Precio"])

def guardar_datos(df):
    df.to_csv(ARCHIVO_CSV, index=False)

# --- INTERFAZ WEB (STREAMLIT) ---

# Configuración de la página
st.set_page_config(page_title="Inventario Soldaduras", page_icon="🏗️")
st.title("🏗️ Gestión de Almacén de Soldaduras")

# Cargar datos al inicio
df = cargar_datos()

# CREAR TABS (PESTAÑAS) PARA ORGANIZAR LA PANTALLA
tab1, tab2, tab3 = st.tabs(["📋 Ver Inventario", "➕ Agregar Material", "❌ Eliminar/Modificar"])

# --- PESTAÑA 1: VER INVENTARIO ---
with tab1:
    st.header("Inventario Actual")
    
    if df.empty:
        st.info("El inventario está vacío. Ve a la pestaña 'Agregar Material'.")
    else:
        # Muestra una tabla interactiva
        st.dataframe(df, use_container_width=True)
        
        # Estadísticas rápidas
        st.divider()
        st.metric("Total de Artículos Diferentes", len(df))
        st.metric("Costo Total del Inventario", f"${(df['Cantidad'] * df['Precio']).sum():,.2f}")

# --- PESTAÑA 2: AGREGAR MATERIAL ---
with tab2:
    st.header("Ingresar Nuevo Material")
    
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del Material")
            precio = st.number_input("Precio Unitario ($)", min_value=0.0, format="%.2f")
        with col2:
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            
        submitted = st.form_submit_button("Guardar en Inventario")
        
        if submitted:
            if nombre:
                # Crear nuevo registro
                nuevo_dato = pd.DataFrame([{"Producto": nombre, "Cantidad": cantidad, "Precio": precio}])
                # Concatenar con el inventario existente
                df = pd.concat([df, nuevo_dato], ignore_index=True)
                guardar_datos(df)
                st.success(f"¡{nombre} agregado exitosamente!")
                st.rerun() # Recarga la página para mostrar el dato nuevo
            else:
                st.error("Por favor, escribe un nombre para el material.")

# --- PESTAÑA 3: ELIMINAR O MODIFICAR ---
with tab3:
    st.header("Gestionar Existencias")
    
    if df.empty:
        st.write("No hay datos para modificar.")
    else:
        lista_productos = df["Producto"].unique()
        producto_a_editar = st.selectbox("Selecciona el producto:", lista_productos)
        
        # Filtramos los datos actuales de ese producto
        datos_actuales = df[df["Producto"] == producto_a_editar].iloc[0]
        
        st.write(f"Editando: **{producto_a_editar}**")
        
        col_mod1, col_mod2 = st.columns(2)
        with col_mod1:
            nueva_cantidad = st.number_input("Actualizar Cantidad", value=int(datos_actuales["Cantidad"]), key="mod_cant")
        with col_mod2:
            nuevo_precio = st.number_input("Actualizar Precio", value=float(datos_actuales["Precio"]), key="mod_precio")
            
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 Actualizar Datos"):
                # Actualizar el DataFrame
                df.loc[df["Producto"] == producto_a_editar, "Cantidad"] = nueva_cantidad
                df.loc[df["Producto"] == producto_a_editar, "Precio"] = nuevo_precio
                guardar_datos(df)
                st.success("Datos actualizados.")
                st.rerun()

        with col_btn2:
            if st.button("🗑️ Eliminar Producto", type="primary"):
                # Eliminar del DataFrame
                df = df[df["Producto"] != producto_a_editar]
                guardar_datos(df)
                st.warning("Producto eliminado.")
                st.rerun()