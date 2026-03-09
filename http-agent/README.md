# HTTP Agent

This folder contains an AI agent that can make HTTP requests (GET, POST, PUT, DELETE) using the Strands Agents framework. The agent uses the `http_request` tool to interact with web APIs.

## Requirements

- **Python 3.8+**
- **Ollama** installed and running (for local model usage)

## Installation

### 1. Install Ollama

- **macOS/Windows**: Download from the [official Ollama website](https://ollama.com/download).
- **Linux**:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### 2. Pull the Model

```bash
ollama run llama3.2:1b
```

### 3. Install Python Dependencies

```bash
pip install strands-agents
pip install strands-agent-tools
pip install "strands-agents[ollama]"
```

## Agent Code (`agent.py`)

This agent uses a local Ollama model with the `http_request` tool to make API calls:

```python
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import http_request

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:1b"
)

agent = Agent(model=ollama_model, tools=[http_request])

response = agent("Make a GET request to https://jsonplaceholder.typicode.com/posts/1 and summarize the response")
```

## Using Default Bedrock Agent (Without Ollama)

If you don't want to use Ollama, you can use the default **AWS Bedrock** model. No need to specify any model — Strands uses Bedrock by default:

```bash
pip install strands-agents
pip install strands-agent-tools
```

Make sure your AWS credentials are configured:

```bash
aws configure
```

Then create your agent like this:

```python
from strands import Agent
from strands_tools import http_request

agent = Agent(tools=[http_request])

response = agent("Make a GET request to https://jsonplaceholder.typicode.com/posts/1 and summarize the response")
```

> **Note:** The default Bedrock agent requires valid AWS credentials and an active AWS account with Bedrock access enabled.

## How to Run

```bash
python agent.py
```
