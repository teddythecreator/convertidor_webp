import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Convertidor WebP", page_icon="🖼️")

st.title("🖼️ Convertidor de imágenes a WebP")
st.write("Sube una imagen JPEG o PNG y te la devolveremos en formato WebP optimizado.")

uploaded_files = st.file_uploader(
    "Selecciona una o varias imágenes", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

quality = st.slider("Calidad de compresión (0-100)", min_value=10, max_value=100, value=85)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")

        output = io.BytesIO()
        image.save(output, format="WEBP", quality=quality)
        output.seek(0)

        webp_filename = uploaded_file.name.rsplit(".", 1)[0] + ".webp"

        st.image(image, caption="Imagen original", use_column_width=True)
        st.download_button(
            label=f"📥 Descargar {webp_filename}",
            data=output,
            file_name=webp_filename,
            mime="image/webp"
        )
