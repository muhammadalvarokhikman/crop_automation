import streamlit as st
from PIL import Image
import zipfile
import io
from io import BytesIO

# Tambahkan header dengan judul dan deskripsi
st.set_page_config(page_title="Image Cropper", page_icon="✂️", layout="centered")
st.title("✂️ Image Cropper - Potong Gambar Sesuai Keinginan")
st.write("by : Muhammad Alvaro Khikman")

# Tambahkan area sidebar untuk instruksi
st.sidebar.header("Petunjuk")
st.sidebar.write(
    """
    1. Unggah gambar yang ingin Anda potong.
    2. Tentukan ukuran crop (lebar x tinggi).
    3. Klik 'Proses Crop Gambar' untuk melihat hasil.
    4. Unduh gambar hasil crop atau unduh semua gambar dalam satu file ZIP.
    """
)

# Atur layout untuk uploader dan pengaturan ukuran crop
col1, col2 = st.columns(2)
with col1:
    uploaded_files = st.file_uploader("Unggah gambar", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
with col2:
    crop_width = st.number_input("Lebar Crop (px)", min_value=50, max_value=1000, value=500, step=1)
    crop_height = st.number_input("Tinggi Crop (px)", min_value=50, max_value=1000, value=500, step=1)

# Tombol untuk memulai proses crop
if st.button("Proses Crop Gambar") and uploaded_files:
    cropped_images = []
    
    with st.spinner("Memproses gambar..."):
        for uploaded_file in uploaded_files:
            # Membaca dan meng-crop gambar
            image = Image.open(uploaded_file)
            cropped_image = image.resize((crop_width, crop_height), Image.LANCZOS)
            
            # Simpan hasil crop ke memory
            img_byte_arr = BytesIO()
            cropped_image.save(img_byte_arr, format='PNG')
            cropped_images.append((uploaded_file.name, img_byte_arr.getvalue()))
        
    st.success("Crop selesai! Gulir ke bawah untuk mengunduh gambar.")

    # Menampilkan gambar hasil crop dengan tombol unduh individual
    for img_name, img_data in cropped_images:
        st.image(img_data, caption=f"Hasil Crop - {img_name}", use_column_width=True)
        st.download_button(
            label=f"Unduh {img_name}", data=img_data, 
            file_name=f"Cropped_{img_name}", mime="image/png"
        )
    
    # Membuat file ZIP untuk mengunduh semua gambar
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for img_name, img_data in cropped_images:
            # Menambahkan gambar ke file ZIP
            zip_file.writestr(f"Cropped_{img_name}", img_data)
    
    # Tombol download all untuk file ZIP
    st.download_button(
        label="Unduh Semua (ZIP)", 
        data=zip_buffer.getvalue(), 
        file_name="Cropped_Images.zip",
        mime="application/zip"
    )

# Footer
st.write("💡 **Tip**: Ukuran crop yang dipilih akan diterapkan pada seluruh gambar yang diunggah.")
st.sidebar.write("Dibuat dengan ❤️ menggunakan Streamlit")
