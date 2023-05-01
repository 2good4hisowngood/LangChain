from flask import Flask, request, jsonify, render_template
from langchain import OpenAI, ConversationChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

app = Flask(__name__)
llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm)

chat_model = ChatOpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, chat_model, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

memory = ConversationBufferMemory(return_messages=True)
conversation_with_memory = ConversationChain(memory=memory, llm=llm)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['input']
    response = conversation.predict(input=user_input)
    return jsonify({"response": response})

@app.route('/agent', methods=['POST'])
def agent():
    user_input = request.json['input']
    response = agent.run(user_input)
    return jsonify({"response": response})

@app.route('/memory', methods=['POST'])
def memory():
    user_input = request.json['input']
    response = conversation_with_memory.predict(input=user_input)
    return jsonify({"response": response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)