import subprocess
import sys
import os
import docx2txt
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama

# Verificar e instalar dependências necessárias
try:
    import docx2txt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "docx2txt"])
    import docx2txt

try:
    import streamlit as st
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-huggingface"])
    from langchain_huggingface import HuggingFaceEmbeddings

try:
    from llama_index.llms.ollama import Ollama
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "llama-index"])
    from llama_index.llms.ollama import Ollama
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

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

# Inicialização do modelo de embeddings
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

if "chat_engine" not in st.session_state:
    if banco_vetorial is not None:
        st.session_state.chat_engine = banco_vetorial.as_chat_engine(chat_mode="condense_question", verbose=True)
    else:
        st.session_state.chat_engine = None

if prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    if st.session_state.chat_engine is None:
        with st.chat_message("assistant"):
            st.error("Chat engine não inicializado. Verifique se os documentos estão no diretório 'docs' e se todos os modelos foram carregados corretamente.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    user_message = st.session_state.messages[-1]["content"]
                    contextual_prompt = f"Você é um atendente de suporte especializado. O usuário fez a seguinte pergunta: '{user_message}'. Considere todos os documentos com perguntas e respostas disponíveis e forneça uma resposta detalhada e precisa, fazendo recomendações quando isso for pertinente. Seja pró-ativo."
                    response = st.session_state.chat_engine.chat(contextual_prompt)
                    st.write(response.response)
                    st.session_state.messages.append({"role": "assistant", "content": response.response})
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": "Desculpe, ocorreu um erro ao processar sua solicitação."})


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