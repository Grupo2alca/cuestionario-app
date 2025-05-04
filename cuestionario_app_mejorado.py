
import streamlit as st
import docx2txt
import fitz  # PyMuPDF
import re
import os

st.set_page_config(page_title="Cuestionario en Línea Mejorado", layout="centered")
st.title("📝 Resolver Cuestionario desde Documento (.docx o .pdf)")

st.markdown("Sube un archivo `.docx` o `.pdf` con preguntas en formato de opción múltiple o respuesta abierta.")

def extract_text_from_pdf(uploaded_file):
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    doc = fitz.open("temp.pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    os.remove("temp.pdf")
    return text

def extract_text_from_docx(uploaded_file):
    with open("temp.docx", "wb") as f:
        f.write(uploaded_file.read())
    text = docx2txt.process("temp.docx")
    os.remove("temp.docx")
    return text

uploaded_file = st.file_uploader("Sube tu archivo .docx o .pdf", type=["docx", "pdf"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Tipo de archivo no compatible.")
        st.stop()

    # Buscar preguntas tipo opción múltiple
    pattern = r"(\d+\.\s+[^\n]+)\n(A\)[^\n]+)\n(B\)[^\n]+)\n(C\)[^\n]+)\n(D\)[^\n]+)\nRespuesta:\s*([A-D])"
    matches = re.findall(pattern, text)

    if not matches:
        st.warning("No se encontraron preguntas de opción múltiple con el formato esperado.")
    else:
        score = 0
        st.markdown(f"### Cuestionario: {len(matches)} preguntas")
        user_answers = []

        for i, (q, a, b, c, d, correct) in enumerate(matches, 1):
            st.markdown(f"**{i}. {q}**")
            options = {"A": a[2:].strip(), "B": b[2:].strip(), "C": c[2:].strip(), "D": d[2:].strip()}
            choice = st.radio("Selecciona una opción:", options.keys(), key=f"q{i}")
            user_answers.append((choice, correct))

        if st.button("Enviar respuestas"):
            st.subheader("Resultados:")
            for idx, ((user, correct), (q, _, _, _, _, _)) in enumerate(zip(user_answers, matches), 1):
                if user == correct:
                    st.success(f"{idx}. ¡Correcto! Respuesta: {correct}")
                    score += 1
                else:
                    st.error(f"{idx}. Incorrecto. Tu respuesta: {user}. Correcta: {correct}")
            st.info(f"🎯 Puntaje final: {score} / {len(matches)}")
