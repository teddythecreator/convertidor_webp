import streamlit as st
from PIL import Image
import io
import base64
import zipfile

# Configuración general
st.set_page_config(
    page_title="Convertidor a WebP",
    page_icon="🖼️",
    layout="wide"
)

# Header personalizado
st.markdown("""
    <div style='background-color: black; padding: 1.5rem; text-align: center;'>
        <h1 style='color: #FF4191; font-size: 2.5rem; margin: 0;'>🖼️ The Creator: Convertidor a WebP</h1>
    </div>
""", unsafe_allow_html=True)

st.write("Convierte hasta **10 imágenes JPEG o PNG** a formato WebP con diseño elegante.")

uploaded_files = st.file_uploader(
    "Selecciona hasta 10 imágenes",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

quality = st.slider("Calidad de compresión (0-100)", min_value=10, max_value=100, value=85)

MAX_FILES = 10
converted_images = []

if uploaded_files:
    if len(uploaded_files) > MAX_FILES:
        st.error(f"⚠️ Solo se permiten hasta {MAX_FILES} imágenes.")
    else:
        st.markdown("""
            <style>
            .preview-container {
                display: flex;
                overflow-x: auto;
                gap: 16px;
                padding: 10px;
                border-radius: 10px;
                margin-top: 20px;
                background-color: #111;
            }
            .preview-item {
                flex: 0 0 auto;
                width: 140px;
                text-align: center;
                color: white;
            }
            .preview-item img {
                width: 100%;
                border-radius: 8px;
                border: 2px solid #FF4191;
            }
            .download-button {
                margin-top: 8px;
            }
            </style>
        """, unsafe_allow_html=True)

        preview_html = '<div class="preview-container">'

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            for file in uploaded_files:
                try:
                    image = Image.open(file).convert("RGB")
                    output = io.BytesIO()
                    image.save(output, format="WEBP", quality=quality)
                    output.seek(0)

                    webp_name = file.name.rsplit(".", 1)[0] + ".webp"
                    zip_file.writestr(webp_name, output.read())

                    file.seek(0)  # para mostrar preview
                    preview_html += f'''
                        <div class="preview-item">
                            <img src="data:image/png;base64,{base64.b64encode(file.read()).decode()}">
                            <p style="font-size: 0.8rem;">{webp_name}</p>
                        </div>
                    '''
                except Exception as e:
                    st.error(f"❌ Error con {file.name}: {e}")

        preview_html += "</div>"
        st.markdown(preview_html, unsafe_allow_html=True)

        # Descargar ZIP
        zip_buffer.seek(0)
        st.download_button(
            label="📦 Descargar todas las imágenes en ZIP",
            data=zip_buffer,
            file_name="imagenes_convertidas.zip",
            mime="application/zip"
        )
else:
    st.info("Sube tus imágenes para comenzar.")

# Footer personalizado
st.markdown("""
    <hr style="margin-top: 3rem; border-color: #FF4191;">
    <div style="text-align: center; padding: 1rem; background-color: black;">
        <p style="color: white; font-size: 1rem;">
            The Creator Business · 
            <a href="https://www.thecreator.business/" style="color: #FF4191;" target="_blank">Visita nuestro sitio web</a>
        </p>
    </div>
""", unsafe_allow_html=True)
