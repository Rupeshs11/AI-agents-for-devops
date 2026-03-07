# Ollama Agent Setup

This folder contains the setup for creating and running local AI agents using Ollama and the Strands Agents framework. By leveraging local models, you can build autonomous agents without relying on external API keys.

## Requirements

Before getting started, make sure your system meets the following requirements:

- **Python 3.8+** installed on your machine
- **Ollama** installed and running

## Installation Guide

Follow these steps to set up the project on your local machine.

### 1. Install Ollama

Ollama allows you to run open-source large language models locally. Download and install it based on your operating system:

- **macOS/Windows**: Download the installer from the [official Ollama website](https://ollama.com/download).
- **Linux**: Install via the terminal by running:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### 2. Pull the AI Model

Once Ollama is installed and running, you need to pull the specific model we'll be using for our agent. Our script (`api.py`) uses the `llama3.2:1b` model.

Open a terminal window and run:

```bash
ollama run llama3.2:1b
```

_Note: Make sure your local Ollama server is running (usually hosted at `http://localhost:11434`). This command will download and start the model._

### 3. Install Python Dependencies

Next, install the required packages to run the Strands Agent framework. Run the following commands in your terminal:

```bash
pip install strands-agents
pip install strands-agent-tools
pip install "strands-agents[ollama]"
```

## Explaining the API Code (`api.py`)

The `api.py` file demonstrates how to connect to a local Ollama instance and use it to power an autonomous agent. Here's a quick breakdown of what the code does:

```python
from strands import Agent
from strands.models.ollama import OllamaModel

# 1. Create an Ollama model instance
# - host: The local URL/port where your Ollama server is running.
# - model_id: The specific language model you pulled earlier.
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:1b"
)

# 2. Create an agent
# We initialize our Agent by passing the local Ollama model to it.
agent = Agent(model=ollama_model)

# 3. Use the agent
# Pass a prompt to the agent. By default, it prints the model's output directly to stdout.
agent("Tell me about Strands agents.")
```

### How to Run

Ensure your Ollama server is running and the `llama3.2:1b` model is active. Then, simply execute the script:

```bash
python api.py
```
