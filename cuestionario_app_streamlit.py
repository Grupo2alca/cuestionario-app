
import streamlit as st
import docx2txt
import re
import os

st.set_page_config(page_title="Cuestionario en Línea", layout="centered")

st.title("📝 Resolver Cuestionario desde Documento")

st.markdown("Sube un archivo `.docx` con preguntas para resolverlas en línea.")

uploaded_file = st.file_uploader("Sube tu archivo .docx", type=["docx"])

if uploaded_file:
    with open("temp.docx", "wb") as f:
        f.write(uploaded_file.read())
    text = docx2txt.process("temp.docx")
    os.remove("temp.docx")

    # Extraer preguntas y respuestas del texto (basado en formato de numeración)
    pattern = r"(\d+\.\s+[^\n]+)\nRespuesta:\s+([^\n]+)"
    qa_pairs = re.findall(pattern, text)

    if not qa_pairs:
        st.warning("No se encontraron preguntas con el formato esperado.")
    else:
        score = 0
        total = len(qa_pairs)
        user_answers = []

        st.markdown(f"### Cuestionario: {total} preguntas")
        for i, (q, a) in enumerate(qa_pairs, 1):
            st.markdown(f"**{i}. {q}**")
            user_input = st.text_input(f"Tu respuesta a la pregunta {i}:", key=f"q{i}")
            user_answers.append((user_input.strip().lower(), a.strip().lower()))

        if st.button("Enviar respuestas"):
            st.subheader("Resultados:")
            for idx, ((user, correct), (q, a)) in enumerate(zip(user_answers, qa_pairs), 1):
                if user == correct:
                    st.success(f"{idx}. ¡Correcto!")
                    score += 1
                else:
                    st.error(f"{idx}. Incorrecto. Correcta: {a}")
            st.info(f"Puntaje final: {score} / {total}")
