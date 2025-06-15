import streamlit as st
from PIL import Image
import io

# Configuración general de la app
st.set_page_config(
    page_title="Convertidor a WebP",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="auto"
)

# Encabezado
st.title("🖼️ Convertidor de Imágenes a WebP")
st.write("Sube imágenes JPEG o PNG y conviértelas a WebP con compresión optimizada.")

# Subida de archivos
uploaded_files = st.file_uploader(
    "Selecciona una o varias imágenes",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Control de calidad
quality = st.slider("Calidad de compresión (0-100)", min_value=10, max_value=100, value=85)

# Procesamiento y descarga
if uploaded_files:
    st.info("Procesando imágenes...")

    for uploaded_file in uploaded_files:
        # Abrir y convertir imagen
        image = Image.open(uploaded_file).convert("RGB")

        # Guardar en buffer
        output = io.BytesIO()
        image.save(output, format="WEBP", quality=quality)
        output.seek(0)

        # Crear nombre de archivo
        webp_filename = uploaded_file.name.rsplit(".", 1)[0] + ".webp"

        # Mostrar imagen original
        st.image(image, caption=f"Imagen: {uploaded_file.name}", use_container_width=True)

        # Botón de descarga
        st.download_button(
            label=f"📥 Descargar {webp_filename}",
            data=output,
            file_name=webp_filename,
            mime="image/webp"
        )
else:
    st.warning("Por favor, sube una imagen para comenzar.")
