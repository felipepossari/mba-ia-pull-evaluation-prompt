"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1-model.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client

from utils import check_env_vars, save_yaml

load_dotenv()


def pull_prompts_from_langsmith():
    print("Connecting LangSmith Prompt Hub...")

    client = Client()
    prompt = client.pull_prompt("leonanluppi/bug_to_user_story_v1")

    system_prompt = prompt.messages[0].prompt.template
    user_prompt = prompt.messages[1].prompt.template

    output_path = Path("../prompts/bug_to_user_story_v1.yml")

    prompt_dict = {
        "name": prompt.metadata.get("lc_hub_repo"),
        "description": "Prompt para converter relatos de bugs em User Stories",
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "version": "v1",
        "created_at": date.today(),
        "tags": ["bug-analysis", "user-story", "product-management"]
    }

    if save_yaml(prompt_dict, output_path):
        print(f"Prompt saved. Path: {output_path}")
    else:
        print("Failed to save the prompt")


def main():
    """Função principal"""
    print(f"Pulling prompts from LangSmith Prompt Hub...")
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    pull_prompts_from_langsmith()

    return 0


if __name__ == "__main__":
    sys.exit(main())
