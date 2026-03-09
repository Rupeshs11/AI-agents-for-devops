import subprocess
from strands import Agent, tool
from strands.models.ollama import OllamaModel

@tool
def docker_command(command: str) -> str:
    """Run a Docker CLI command and return the output.

    Args:
        command: The Docker command to run (e.g., 'docker ps', 'docker images').
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:3b"
)

SYSTEM_PROMPT = """You are a Docker assistant. When the user asks about Docker, 
use the docker_command tool to run the appropriate Docker CLI commands and return the results.
Always use the tool to get real data, never make up responses."""

agent = Agent(model=ollama_model, tools=[docker_command], system_prompt=SYSTEM_PROMPT)

user_input = input("Enter your Docker query: ")
agent(user_input)
