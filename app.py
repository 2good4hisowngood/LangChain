import logging
from flask import Flask, request, jsonify, render_template
from langchain import OpenAI, ConversationChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize language model with a specific temperature
llm = OpenAI(temperature=0)

# Initialize conversation chain with the language model
conversation = ConversationChain(llm=llm)

# Initialize chat model with a specific temperature
chat_model = ChatOpenAI(temperature=0)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
