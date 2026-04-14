"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path


# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:

    def test_prompt_has_system_prompt(self):
        prompt = load_prompts("prompts/bug_to_user_story_v2.yml")
        assert "system_prompt" in prompt
        assert prompt["system_prompt"].strip()

    def test_prompt_has_role_definition(self):
        prompt = load_prompts("prompts/bug_to_user_story_v2.yml")
        assert "Você é" in prompt["system_prompt"]

    def test_prompt_mentions_format(self):
        prompt = load_prompts("prompts/bug_to_user_story_v2.yml")
        assert any(phrase in prompt["system_prompt"].lower() for phrase in [
            'user story', 'como', 'eu quero', 'markdown', 'gherkin'
        ])

    def test_prompt_has_few_shot_examples(self):
        prompt = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = prompt["system_prompt"]
        has_examples = (
                'exemplo' in system_prompt.lower() or
                'output' in system_prompt.lower() or
                'input' in system_prompt.lower()
        )
        assert has_examples

    def test_prompt_no_todos(self):
        prompt = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = prompt["system_prompt"]
        user_prompt = prompt["user_prompt"]
        assert '[todo]' not in user_prompt.lower()
        assert '[TODO]' not in user_prompt.lower()
        assert '[todo]' not in system_prompt.lower()
        assert '[TODO]' not in system_prompt.lower()

    def test_minimum_techniques(self):
        prompt = load_prompts("prompts/bug_to_user_story_v2.yml")
        techniques = prompt["techniques_applied"]
        assert len(techniques) >= 2
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])