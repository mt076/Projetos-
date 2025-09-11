# Importações necessárias
import os
import docx2txt
import streamlit as st
import torch
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

torch.classes.__path__ = []

st.set_page_config(
    page_title="Atendimento Estagiários",
    page_icon="https://www.rio.rj.gov.br/wp-content/uploads/2022/02/cropped-favicon-1-32x32.png",
    layout="centered"
)

# Função para carregar e injetar o CSS customizado
def carregar_css(caminho_arquivo):
    with open(caminho_arquivo) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega o CSS customizado
carregar_css("style.css")

st.sidebar.title("Atendimento a Novos Estagiários")
st.sidebar.markdown("Fundação João Goulart - Coodenadoria de Dados e Comportamento")
st.sidebar.markdown("[Coordenadoria de Dados e Comportamento - FJG](https://fjg.prefeitura.rio/coordenadoria-de-dados-e-comportamento/)")
st.sidebar.button("AI Chatbot Versão 1.2")

st.title("Chatbot de Suporte para Novos Estagiários")

DIRETORIO_DOCUMENTOS = "Documentos_FJG"

try:
    with open("COLE A SUA Chave-API AQUI") as f:
        api_key = f.read().strip()
    llm = Gemini(api_key=api_key)
except FileNotFoundError:
    st.error("Arquivo 'Chave-API.txt' não encontrado. Por favor, crie o arquivo no mesmo diretório e insira sua chave de API do Google Gemini.")
    st.stop()
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar a chave de API: {e}")
    st.stop()

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource()
def cria_indice_vetorial(_llm, _embed_model):
    """Cria e retorna o índice vetorial a partir dos documentos de suporte."""
    if not os.path.exists(DIRETORIO_DOCUMENTOS):
        os.makedirs(DIRETORIO_DOCUMENTOS)
        st.warning(f"O diretório '{DIRETORIO_DOCUMENTOS}' não foi encontrado e acaba de ser criado. Adicione seus arquivos de suporte (.pdf, .docx, .txt) nesta pasta e recarregue a página.")
        st.stop()

    with st.spinner(text="Carregando e indexando os documentos. Isso pode levar alguns segundos..."):
        reader = SimpleDirectoryReader(input_dir=DIRETORIO_DOCUMENTOS, recursive=True)
        docs = reader.load_data()
        if not docs:
            st.warning(f"Nenhum documento encontrado em '{DIRETORIO_DOCUMENTOS}'. O chatbot responderá sem a base de conhecimento específica. Adicione arquivos e recarregue.")
        
        Settings.llm = _llm
        Settings.embed_model = _embed_model
        index = VectorStoreIndex.from_documents(docs)
        return index

banco_vetorial = cria_indice_vetorial(llm, embed_model)

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = banco_vetorial.as_chat_engine(chat_mode="condense_question", verbose=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou o assistente virtual da Fundação João Goulart. Como posso ajudar ?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            user_message = st.session_state.messages[-1]["content"]
            contextual_prompt = f"""**Persona:** Você é um assistente virtual de suporte para novos estagiários da Fundação João Goulart.

**Contexto:** Baseie-se exclusivamente nos documentos de suporte fornecidos para formular sua resposta.

**Tarefa:** Responda à pergunta do usuário de forma clara, detalhada e precisa. Seja proativo e, se pertinente, ofereça recomendações úteis que estejam contidas nos documentos.

**Pergunta do Usuário:**
{user_message}"""
            response = st.session_state.chat_engine.chat(contextual_prompt)
            st.write(response.response)
            st.session_state.messages.append({"role": "assistant", "content": response.response})