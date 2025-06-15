import streamlit as st
from PIL import Image
import io
import base64
import zipfile

# Configuración base de Streamlit
st.set_page_config(
    page_title="The Creator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === ESTILO GLOBAL ===
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #000000 !important;
        color: white !important;
        font-family: 'Arial', sans-serif;
    }
    header, footer {visibility: hidden;}
    .main { padding-top: 0rem !important; }

    /* HEADER */
    .custom-header {
        background-color: #000000;
        padding: 2rem 1rem 1.5rem 1rem;
        text-align: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 999;
        border-bottom: 2px solid #FF4191;
    }
    .custom-header h1 {
        color: #FF4191;
        font-size: 3rem;
        margin: 0;
        font-weight: bold;
        letter-spacing: 2px;
    }

    /* ESPACIADO debajo del header */
    .spacer { margin-top: 130px; }

    /* FOOTER */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #000000;
        color: white;
        text-align: center;
        padding: 1rem;
        font-size: 1rem;
        z-index: 999;
        border-top: 1px solid #FF4191;
    }
    .custom-footer a {
        color: #FF4191;
        text-decoration: none;
        font-weight: bold;
    }

    /* CONTENEDOR DE PREVISUALIZACIÓN */
    .preview-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 1rem;
        border-radius: 12px;
        margin: 2rem 0;
        background-color: #111111;
    }
    .preview-item {
        flex: 0 0 auto;
        width: 140px;
        text-align: center;
    }
    .preview-item img {
        width: 100%;
        border-radius: 8px;
        border: 2px solid #FF4191;
    }
    .preview-item p {
        color: #FF4191;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
    }

    /* TEXTO MÁS GRANDE */
    .stSlider > div > div {
        padding: 1rem 0;
    }
    .stSlider label, .stFileUploader label {
        font-size: 1.1rem !important;
    }
    .stMarkdown > p {
        font-size: 1.2rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown('<div class="custom-header"><h1>THE CREATOR</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# === CONTENIDO ===
st.markdown("Convierte hasta **10 imágenes JPEG o PNG** a formato WebP de forma sencilla y visual.")

uploaded_files = st.file_uploader(
    "Selecciona tus imágenes",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

quality = st.slider("Calidad de compresión (0-100)", min_value=10, max_value=100, value=85)

MAX_FILES = 10
if uploaded_files:
    if len(uploaded_files) > MAX_FILES:
        st.error(f"⚠️ Solo se permiten hasta {MAX_FILES} imágenes.")
    else:
        zip_buffer = io.BytesIO()
        preview_html = '<div class="preview-container">'

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            for file in uploaded_files:
                try:
                    image = Image.open(file).convert("RGB")
                    output = io.BytesIO()
                    image.save(output, format="WEBP", quality=quality)
                    output.seek(0)

                    webp_name = file.name.rsplit(".", 1)[0] + ".webp"
                    zip_file.writestr(webp_name, output.read())

                    file.seek(0)
                    preview_html += f'''
                        <div class="preview-item">
                            <img src="data:image/png;base64,{base64.b64encode(file.read()).decode()}">
                            <p>{webp_name}</p>
                        </div>
                    '''
                except Exception as e:
                    st.error(f"Error al procesar {file.name}: {e}")

        preview_html += "</div>"
        st.markdown(preview_html, unsafe_allow_html=True)

        zip_buffer.seek(0)
        st.download_button(
            label="📦 Descargar ZIP con todas las imágenes convertidas",
            data=zip_buffer,
            file_name="imagenes_convertidas.zip",
            mime="application/zip"
        )
else:
    st.info("Sube tus imágenes para comenzar.")

# === FOOTER ===
st.markdown("""
<div class="custom-footer">
    The Creator Business · <a href="https://www.thecreator.business/" target="_blank">Visita nuestro sitio web</a>
</div>
""", unsafe_allow_html=True)
