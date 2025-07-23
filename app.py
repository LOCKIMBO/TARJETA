import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import os
import requests
from io import BytesIO

st.set_page_config(page_title="Mi Diario de Compras", layout="centered")

st.title("📔 Mi Diario de Compras")

# Leer datos desde Google Sheets publicado como CSV
sheet_url = "https://docs.google.com/spreadsheets/d/1VSnFxdxVMhjlH5qFGqG1w7Ls2LECEAIvoN9ZxXZQQ2M/export?format=csv"
df = pd.read_csv(sheet_url)
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
df = df.sort_values(by='Fecha', ascending=False)

# Mostrar cada compra
total = 0
for index, row in df.iterrows():
    with st.container():
        st.subheader(f"🛍️ {row['Compra']} – S/{row['Monto']}")
        st.write(f"📅 {row['Fecha'].strftime('%d/%m/%Y')} | 📍 {row['Lugar']}")

        # Mostrar imagen desde URL si es válida
        foto_url = str(row['Foto'])
        if foto_url.startswith('http'):
            try:
                response = requests.get(foto_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, use_column_width=True)
            except Exception as e:
                st.warning(f"No se pudo cargar la imagen desde la URL: {foto_url}")
        else:
            if os.path.exists(foto_url):
                img = Image.open(foto_url)
                st.image(img, use_column_width=True)
            else:
                st.warning(f"No se encontró la imagen: {foto_url}")

        try:
            total += float(row['Monto'])
        except:
            pass

st.markdown("---")
st.success(f"💰 Gasto total registrado: S/{total:.2f}")
