# Docker Agent

This folder contains an AI agent that can perform Docker operations using the Strands Agents framework with the `shell` tool. The agent can list containers, build images, manage volumes, networks, and more — all through natural language prompts.

## Requirements

- **Python 3.8+**
- **Docker** installed and running
- **Ollama** installed and running (for local model usage)

## Installation

### 1. Install Docker

- **Windows/macOS**: Download from the [official Docker website](https://www.docker.com/products/docker-desktop/).
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get update
  sudo apt-get install docker.io -y
  sudo systemctl start docker
  sudo systemctl enable docker
  ```

### 2. Install Ollama

- **macOS/Windows**: Download from the [official Ollama website](https://ollama.com/download).
- **Linux**:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### 3. Pull the Model

```bash
ollama run llama3.2:1b
```

### 4. Install Python Dependencies

```bash
pip install strands-agents
pip install strands-agent-tools
pip install "strands-agents[ollama]"
```

## Agent Code (`agent.py`)

```python
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import shell

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:1b"
)

agent = Agent(model=ollama_model, tools=[shell])

agent("List all running Docker containers and show their status")
```

## Using Default Bedrock Agent (Without Ollama)

```python
from strands import Agent
from strands_tools import shell

agent = Agent(tools=[shell])

agent("List all running Docker containers and show their status")
```

## Example Prompts

You can ask the agent to perform various Docker tasks:

```python
agent("List all Docker images on this machine")
agent("Pull the nginx:latest image")
agent("Run an nginx container on port 8080")
agent("Stop all running containers")
agent("Show Docker disk usage")
agent("Remove all stopped containers")
```

## Using with Temporal (Workflow Orchestration)

[Temporal](https://temporal.io/) is a workflow orchestration platform that helps you build reliable, scalable applications. You can combine the Docker agent with Temporal to automate multi-step Docker workflows like CI/CD pipelines, scheduled cleanups, and deployments.

### Install Temporal SDK

```bash
pip install temporalio
```

### Example: Temporal Workflow with Docker Agent

```python
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import shell
import asyncio

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:1b"
)

@activity.defn
async def docker_cleanup():
    agent = Agent(model=ollama_model, tools=[shell])
    agent("Remove all stopped Docker containers and dangling images")
    return "Cleanup done"

@activity.defn
async def docker_health_check():
    agent = Agent(model=ollama_model, tools=[shell])
    agent("List all running containers and check if any are unhealthy")
    return "Health check done"

@workflow.defn
class DockerMaintenanceWorkflow:
    @workflow.run
    async def run(self):
        await workflow.execute_activity(docker_health_check, start_to_close_timeout=timedelta(seconds=60))
        await workflow.execute_activity(docker_cleanup, start_to_close_timeout=timedelta(seconds=60))
        return "Docker maintenance completed"

async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(client, task_queue="docker-tasks", workflows=[DockerMaintenanceWorkflow], activities=[docker_cleanup, docker_health_check]):
        result = await client.execute_workflow(DockerMaintenanceWorkflow.run, id="docker-maintenance", task_queue="docker-tasks")
        print(result)

asyncio.run(main())
```

### Running Temporal Server

To run a Temporal server locally:

```bash
temporal server start-dev
```

> **Note:** The Temporal dev server runs at `localhost:7233` by default.

## How to Run

```bash
python agent.py
```
