import streamlit as st
from PIL import Image
import io

# Configuración de la página
st.set_page_config(
    page_title="Convertidor a WebP",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ Convertidor de Imágenes a WebP")
st.write("Convierte hasta **10 imágenes JPEG o PNG** a formato WebP optimizado.")

# Subida de archivos
uploaded_files = st.file_uploader(
    "Selecciona hasta 10 imágenes",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Control de calidad de compresión
quality = st.slider("Calidad de compresión (0-100)", min_value=10, max_value=100, value=85)

# Verificación y procesamiento
if uploaded_files:
    if len(uploaded_files) > 10:
        st.error("⚠️ Solo se permiten hasta 10 imágenes a la vez. Por favor, reduce la selección.")
    else:
        for uploaded_file in uploaded_files:
            try:
                # Abrir imagen
                image = Image.open(uploaded_file).convert("RGB")

                # Convertir y guardar en memoria
                output = io.BytesIO()
                image.save(output, format="WEBP", quality=quality)
                output.seek(0)

                # Nombre de salida
                webp_filename = uploaded_file.name.rsplit(".", 1)[0] + ".webp"

                # Mostrar imagen y botón de descarga
                st.image(image, caption=f"{uploaded_file.name}", use_container_width=True)
                st.download_button(
                    label=f"📥 Descargar {webp_filename}",
                    data=output,
                    file_name=webp_filename,
                    mime="image/webp"
                )
            except Exception as e:
                st.error(f"Error al procesar {uploaded_file.name}: {e}")
else:
    st.info("Por favor, sube una o más imágenes (máximo 10).")
