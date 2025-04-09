import streamlit as st
import json
import ollama

# ✅ Função para carregar dataset
def carregar_dataset(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return [json.loads(linha) for linha in f]

# ✅ Carregar dataset de contexto
dataset = carregar_dataset("./data/dataset_2000.jsonl")

# ✅ Função para construir o contexto
def construir_contexto(area, numeros, problema, numeros_problema, impacto, objetivo):
    contexto = ""
    for exemplo in dataset:
        if (
            area.lower() in exemplo['área'].lower() or
            problema.lower() in exemplo['problema'].lower() or
            impacto.lower() in exemplo['impacto'].lower() or
            objetivo.lower() in exemplo['objetivo'].lower()
        ):
            contexto += f"Área: {exemplo['área']}\n"
            contexto += f"Números: {exemplo['números']}\n"
            contexto += f"Problema: {exemplo['problema']}\n"
            contexto += f"Números problema: {exemplo['números_problema']}\n"
            contexto += f"Impacto: {exemplo['impacto']}\n"
            contexto += f"Objetivo: {exemplo['objetivo']}\n"
            contexto += f"Texto: {exemplo['resposta']}\n\n"
    return contexto

# ✅ Função para gerar texto com o Ollama
def gerar_texto_ollama(prompt):
    resposta = ollama.chat(
        model='deepseek-coder:6.7b',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return resposta['message']['content']

# ✅ Streamlit App
st.title("Gerador de Texto Personalizado com IA")

# Entrada de dados
area = st.text_input("Área:")
numeros = st.text_input("Números:")  # ✅ Campo livre para texto
problema = st.text_input("Problema:")
numeros_problema = st.text_input("Números problema:")  # ✅ Campo livre para texto
impacto = st.text_input("Impacto:")
objetivo = st.text_input("Objetivo:")

# Estado da sessão para manter os dados sempre
if 'texto_gerado' not in st.session_state:
    st.session_state.texto_gerado = ""

if 'texto_editado' not in st.session_state:
    st.session_state.texto_editado = ""

# ✅ Botão de geração de texto
if st.button("Gerar Texto"):
    if all([area, numeros, problema, numeros_problema, impacto, objetivo]):
        contexto = construir_contexto(area, numeros, problema, numeros_problema, impacto, objetivo)

        prompt = (
            f"Com base nos exemplos abaixo, gere um texto claro e objetivo, "
            f"mantendo o mesmo estilo e estrutura dos exemplos anteriores.\n\n"
            f"{contexto}\n"
            f"Agora, para o seguinte caso, gere o texto:\n"
            f"Área: {area}\n"
            f"Números: {numeros}\n"
            f"Problema: {problema}\n"
            f"Números problema: {numeros_problema}\n"
            f"Impacto: {impacto}\n"
            f"Objetivo: {objetivo}\n\n"
            f"Texto:"
        )

        texto_gerado = gerar_texto_ollama(prompt)
        st.session_state.texto_gerado = texto_gerado
        st.session_state.texto_editado = texto_gerado
    else:
        st.warning("Por favor, preencha todos os campos para gerar o texto.")

# ✅ Se houver texto gerado, permite editar e visualizar
if st.session_state.texto_gerado:
    st.subheader("Edite o texto gerado conforme necessário:")

    texto_editado = st.text_area(
        "Texto editável:",
        value=st.session_state.texto_editado,
        height=300,
        key="input_texto_editado"
    )

    # ✅ Atualiza o estado da sessão a cada alteração
    st.session_state.texto_editado = texto_editado

    st.subheader("Texto Final Atualizado:")
    st.write(st.session_state.texto_editado)

    # ✅ Botão para copiar o texto
    copy_code = f'''
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            alert('Texto copiado para a área de transferência!');
        }}, function(err) {{
            console.error('Erro ao copiar texto: ', err);
        }});
    }}
    </script>
    <button onclick="copyToClipboard(`{st.session_state.texto_editado}`)">Copiar Texto</button>
    '''
    st.markdown(copy_code, unsafe_allow_html=True)
