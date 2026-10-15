# code.py
import streamlit as st
import pdfplumber
import pytesseract

# Windows: descomenta e ajusta se o Tesseract não for encontrado
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("Extrair texto de PDF")

ficheiro = st.file_uploader("Escolhe um PDF", type="pdf")
idioma = st.selectbox("Idioma do OCR", ["por", "eng", "por+eng"])
forcar_ocr = st.checkbox("Forçar OCR em todas as páginas")

if ficheiro:
    paginas = []
    with pdfplumber.open(ficheiro) as pdf:
        barra = st.progress(0)
        total = len(pdf.pages)
        for i, pagina in enumerate(pdf.pages, start=1):
            texto = "" if forcar_ocr else (pagina.extract_text() or "")
            if not texto.strip():
                imagem = pagina.to_image(resolution=200).original
                texto = pytesseract.image_to_string(imagem, lang=idioma)
            paginas.append(f"--- Página {i} ---\n{texto}")
            barra.progress(i / total)

    resultado = "\n\n".join(paginas)

    st.text_area("Texto extraído", resultado, height=400)
    st.download_button(
        "Descarregar .txt",
        resultado,
        file_name="texto_extraido.txt",
        mime="text/plain",
    )