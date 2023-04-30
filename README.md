# LangChain App

This application is a Flask API that provides chat, agent, and memory functionalities using the LangChain library. It is built with Docker for easy setup and deployment.

## Prerequisites

- Docker installed on your machine. If you don't have it installed, you can download it from the [Docker website](https://www.docker.com/get-started).
- OpenAI API key and SERPAPI API key. These keys should be placed in a `.env` file within the `langchain-app` folder.

## Setup

1. Clone this repository or create a new folder called `langchain-app` and place the `app.py`, `requirements.txt`, and `Dockerfile` files inside it.

2. Create a `.env` file in the `langchain-app` folder with the following content:

```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

Replace `your_openai_api_key` and `your_serpapi_api_key` with your actual API keys.

## Build and Run

### PowerShell/Docker Desktop (Windows)

1. Open PowerShell and navigate to the `langchain-app` folder.

2. Build the Docker image by running the following command:

```powershell
$openaiApiKey = ((Get-Content -Path .\.env | Select-String -Pattern '^OPENAI_API_KEY=') -replace 'OPENAI_API_KEY=','')
$serpapiKey = ((Get-Content -Path .\.env | Select-String -Pattern '^SERPAPI_API_KEY=') -replace 'SERPAPI_API_KEY=','')
docker build --build-arg OPENAI_API_KEY="${openaiApiKey}" --build-arg SERPAPI_API_KEY="${serpapiKey}" -t langchain-app .
```

3. Run the Docker container with the following command:

```
docker run -p 5000:5000 langchain-app
```

### Linux

1. Open a terminal window and navigate to the `langchain-app` folder.

2. Export your API keys as environment variables:

```
export OPENAI_API_KEY="your_openai_api_key"
export SERPAPI_API_KEY="your_serpapi_api_key"
```

Replace `your_openai_api_key` and `your_serpapi_api_key` with your actual API keys.

3. Build the Docker image by running the following command:

```
docker build --build-arg OPENAI_API_KEY="$OPENAI_API_KEY" --build-arg SERPAPI_API_KEY="$SERPAPI_API_KEY" -t langchain-app .
```

4. Run the Docker container with the following command:

```
docker run -p 5000:5000 langchain-app
```

## Usage

The application should now be running on your local machine at `http://localhost:5000`.

You can test the `/chat`, `/agent`, and `/memory` endpoints by sending POST requests with JSON data containing the input message. You can use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/) to test the endpoints.

For example, using curl, you can test the `/chat` endpoint like this:

```
curl -X POST -H "Content-Type: application/json" -d '{"input": "Hello!"}' http://localhost:5000/chat
```

This should return a JSON response with the AI's reply.

---

Feel free to modify the README according to your needs.