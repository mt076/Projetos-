import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama

st.set_page_config(page_title="ChatBot para Estágiarios", page_icon="🤖💡", layout="centered")

st.sidebar.title("Integração de Novos Estagiários")
st.markdown("### Fundação João Goulart - Departamento de Análise de Dados Comportamentais ###")
st.markdown("AI Chatbot Teste 1.0")

st.title("Chatbot Personalizado com Sistema de Atendimento a Novos Estagiarios usando LLMs")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou o chatbot de suporte para novos estagiários. Como posso ajudar você hoje?"}]

# Inicialização do LLM com tratamento de erro
try:
    llm = Ollama(model='llama3.1')
except Exception as e:
    st.error(f"Erro ao inicializar o Ollama: {e}")
    st.info("Certifique-se de que o Ollama está instalado e rodando. Execute: ollama pull llama3.1")
    llm = None

# Inicialização do modelo de embeddings com tratamento de erro
embed_model = None
try:
    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    st.error(f"Erro ao carregar embeddings: {e}")
    embed_model = None


@st.cache_resource
def cria_database_externo():
    if llm is None or embed_model is None:
        st.error("Modelos não inicializados corretamente")
        return None
        
    with st.spinner(text="Carregando e indexando os documentos. Isso deve levar alguns segundos"):
        try:
            # Verificar se o diretório docs existe
            if not os.path.exists("./docs"):
                os.makedirs("./docs")
                st.warning("Diretório 'docs' criado. Por favor, adicione os documentos necessários.")
                return None
                
            reader = SimpleDirectoryReader(input_dir="./docs", recursive=True)
            docs = reader.load_data()
            
            if not docs:
                st.warning("Nenhum documento encontrado no diretório 'docs'")
                return None
                
            Settings.llm = llm
            Settings.embed_model = embed_model
            index = VectorStoreIndex.from_documents(docs)
            return index
            
        except Exception as e:
            st.error(f"Erro ao criar banco de dados: {e}")
            return None

banco_vetorial = cria_database_externo()

# Inicializa o chat engine no estado da sessão
if "chat_engine" not in st.session_state:
    if banco_vetorial is not None:
        st.session_state.chat_engine = banco_vetorial.as_chat_engine(chat_mode="condense_question", verbose=True)
    else:
        st.session_state.chat_engine = None

# Captura a entrada do usuário
if prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    if st.session_state.chat_engine is None:
        with st.chat_message("assistant"):
            response_text = "Chat engine não inicializado. Verifique se os documentos estão no diretório 'docs' e se todos os modelos foram carregados corretamente."
            st.error(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    user_message = st.session_state.messages[-1]["content"]
                    response = st.session_state.chat_engine.chat(user_message)
                    st.write(response.response)
                    st.session_state.messages.append({"role": "assistant", "content": response.response})
                except Exception as e:
                    error_message = f"Erro ao gerar resposta: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})


# Verificar requisitos
st.sidebar.subheader("Verificação de Requisitos")
if llm:
    st.sidebar.success("✓ Ollama inicializado")
else:
    st.sidebar.error("✗ Ollama não inicializado")

if embed_model:
    st.sidebar.success("✓ Embeddings carregados")
else:
    st.sidebar.error("✗ Embeddings não carregados")

if banco_vetorial:
    st.sidebar.success("✓ Banco de dados vetorial criado")
else:
    st.sidebar.error("✗ Banco de dados não criado")


    '''
    python -m streamlit run chatbot_estagiarios.py
    '''