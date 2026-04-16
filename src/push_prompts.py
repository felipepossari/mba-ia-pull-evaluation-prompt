"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import sys

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

from utils import load_yaml, check_env_vars, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    prompt_obj = ChatPromptTemplate.from_messages([
        ("system", prompt_data.get("system_prompt")),
        ("user", prompt_data.get("user_prompt"))
    ])

    client = Client()
    url = client.push_prompt(
        prompt_name,
        object=prompt_obj,
        tags=prompt_data.get("tags"),
        description=prompt_data.get("description"),
        readme="Técnicas aplicadas: " + ", ".join(prompt_data.get("techniques_applied"))
    )
    print(f"Prompt '{prompt_name}' published. URL: {url}")
    return True


def main():
    """Função principal"""
    print(f"Pushing prompt to LangSmith Hub")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    prompt = load_yaml("../prompts/bug_to_user_story_v1.yml")
    if not prompt:
        print("Prompt not loaded")
        return 1

    is_valid, errors = validate_prompt_structure(prompt)
    if not is_valid:
        print("Prompt invalid. Errors: ")
        for error in errors:
            print(f" - {error}")
        return 1

    if not push_prompt_to_langsmith(prompt.get("name"), prompt):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
