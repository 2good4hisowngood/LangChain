import logging
from flask import Flask, request, jsonify, render_template
from langchain import OpenAI, ConversationChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
import json

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import getpass

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Set the upload folder and allowed extensions for the uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Initialize language model with a specific temperature
llm = OpenAI(temperature=0)

# Initialize conversation chain with the language model
conversation = ConversationChain(llm=llm)

# Initialize chat model with a specific temperature
chat_model = ChatOpenAI(temperature=0)

# initialize pinecone
# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# PINECONE_ENV = os.environ.get('PINECONE_ENV')
# pinecone.init(
#     api_key=PINECONE_API_KEY,  # find at app.pinecone.io
#     environment=PINECONE_ENV  # next to api key in console
# )

# Load necessary tools for the agent
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Initialize agent with tools and chat model
agent = initialize_agent(tools, chat_model, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Initialize memory for conversation
memory = ConversationBufferMemory(return_messages=True)

# Initialize conversation chain with memory and language model
conversation_with_memory = ConversationChain(memory=memory, llm=llm)
  
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['input']
        template_id = request.json.get('template_id', None)
        if template_id:
            response = conversation.predict(input=user_input, template_id=template_id)
        else:
            response = conversation.predict(input=user_input)
        return jsonify({"response": response})
    except Exception as e:
        logger.exception("Error in /chat endpoint")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500


@app.route('/agent', methods=['POST'])
def agent():
    try:
        user_input = request.json['input']
        response = agent(user_input)
        return jsonify({"response": response})
    except Exception as e:
        logger.exception("Error in /agent endpoint")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

@app.route('/memory', methods=['POST'])
def memory():
    try:
        user_input = request.json['input']
        response = conversation_with_memory.predict(input=user_input)
        return jsonify({"response": response})
    except Exception as e:
        logger.exception("Error in /memory endpoint")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

@app.route('/templates', methods=['GET'])
def templates():
    try:
        with open('prompt_templates.json', 'r') as f:
            templates = json.load(f)
        return jsonify({"templates": templates})
    except Exception as e:
        logger.exception("Error in /templates endpoint")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.exception("Error in / (index) endpoint")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Load and process the uploaded file
            loader = TextLoader(file_path)
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            documents = text_splitter.split_documents(documents)

            embeddings = OpenAIEmbeddings()
            index_name = "langchain-test"
            docsearch = Pinecone.from_documents(documents, embeddings, index_name=index_name)

            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), docsearch.as_retriever(), memory=memory)

            # Example query
            query = "What did the president say about Ketanji Brown Jackson"
            docs = docsearch.similarity_search(query)
            # query = "What did the president say about Ketanji Brown Jackson"
            # result = qa({"question": query})

            # Return the result as a JSON response
            return jsonify({"answer": docs["answer"]})
            #return jsonify({"answer": result["answer"]})

    return jsonify({"error": "Invalid request"})
    # return jsonify({"error": "Invalid request"})

@app.route('/query', methods=['POST'])
def query():
    try:
        question = request.json['question']
        result = docsearch({"question": question})
        return jsonify({"answer": result["answer"]})
    except Exception as e:
        logger.exception("Error in /query endpoint")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)