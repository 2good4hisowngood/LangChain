# LangChain Chat App

This is a containerized chat application using LangChain, OpenAI, and Flask. The app provides an API endpoint to interact with the chat model.

## Installation

1. Install [Docker](https://docs.docker.com/get-docker/).

2. Clone this repository:

```
git clone https://github.com/2good4hisowngood/langchain-chat-app.git
cd langchain-chat-app
```

## Build and run the Docker container

1. Build the Docker image:

```
docker build -t langchain-chat-app .
```

2. Run the Docker container:

```
docker run -p 5000:5000 langchain-chat-app
```

The chat app is now running on `http://localhost:5000`.

## Usage

Send a POST request to the `/chat` endpoint with the user input as a JSON payload:

```
curl -X POST -H "Content-Type: application/json" -d '{"input":"Hi there!"}' http://localhost:5000/chat
```

You will receive a response from the chat model.

## License

This project is licensed under the MIT License.
```