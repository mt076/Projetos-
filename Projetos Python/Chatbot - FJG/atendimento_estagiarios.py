import os
import streamlit as st
import torch
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

st.set_page_config(
    page_title="Suporte FJG",
    page_icon="instituto_fundao_joo_goulart_fjg_logo.jfif", 
    layout="centered"
)


def carregar_css(caminho_arquivo):
    """Lê um arquivo CSS e o aplica na aplicação Streamlit."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo de estilo '{caminho_arquivo}' não encontrado. Verifique o caminho.")
        st.stop()

carregar_css("style.css")

with st.sidebar:
    st.image("instituto_fundao_joo_goulart_fjg_logo.jfif", use_container_width=True)
    
    st.title("Atendimento a Novos Estagiários")
    st.markdown("##### Fundação João Goulart")
    st.markdown("###### Coordenadoria de Dados e Comportamento")
    st.divider()
    st.info("AI Chatbot | Versão 1.2")
    st.link_button("Acessar Site da FJG", "https://fjg.prefeitura.rio/coordenadoria-de-dados-e-comportamento/")

st.title("Chatbot de Suporte para Novos Estagiários")

DIRETORIO_DOCUMENTOS = "Documentos_FJG"

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Chave de API do Google Gemini não configurada.")
    st.info("Por favor, crie um arquivo .streamlit/secrets.toml e adicione sua chave: GEMINI_API_KEY = 'SUA_CHAVE_AQUI'")
    st.stop()

llm = Gemini(api_key=api_key, model_name="models/gemini-1.5-pro-latest")
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource(show_spinner="Analisando documentos de suporte...")
def cria_indice_vetorial(_llm, _embed_model):
    """Cria e retorna o índice vetorial a partir dos documentos."""
    if not os.path.exists(DIRETORIO_DOCUMENTOS) or not os.listdir(DIRETORIO_DOCUMENTOS):
        st.info(f"O diretório '{DIRETORIO_DOCUMENTOS}' está vazio. Adicione arquivos de suporte (.pdf, .docx, .txt) e recarregue a página.")
        return None

    reader = SimpleDirectoryReader(input_dir=DIRETORIO_DOCUMENTOS, recursive=True)
    docs = reader.load_data()
    
    Settings.llm = _llm
    Settings.embed_model = _embed_model
    index = VectorStoreIndex.from_documents(docs)
    return index

banco_vetorial = cria_indice_vetorial(llm, embed_model)

if banco_vetorial:
    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = banco_vetorial.as_chat_engine(
            chat_mode="condense_question", verbose=True
        )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou o assistente virtual da Fundação João Goulart. Como posso lhe ajudar hoje?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Digite sua pergunta aqui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Estou pensando..."):
                user_message = st.session_state.messages[-1]["content"]
                contextual_prompt = (
                    "Você é um assistente virtual para novos estagiários da Fundação João Goulart. "
                    "Responda à pergunta do usuário baseando-se exclusivamente nos documentos fornecidos. "
                    "Seja claro, detalhado e prestativo.\n\n"
                    f"Pergunta do Usuário: {user_message}"
                )
                response = st.session_state.chat_engine.chat(contextual_prompt)
                st.write(response.response)
                st.session_state.messages.append({"role": "assistant", "content": response.response})