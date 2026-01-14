import json
import os
from typing import Dict, Any
from pathlib import Path

class PromptManager:
    def __init__(self, prompts_dir: str = "app/static/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = self.load_all_prompts()
    
    def load_all_prompts(self) -> Dict[str, Any]:
        """Charger tous les prompts depuis les fichiers JSON"""
        prompts = {}
        
        for prompt_file in self.prompts_dir.glob("*.json"):
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompts[prompt_file.stem] = json.load(f)
        
        return prompts
    
    def get_prompt(self, prompt_type: str, key: str = None) -> Dict[str, str]:
        """Récupérer un prompt spécifique"""
        if prompt_type not in self.prompts:
            raise ValueError(f"Type de prompt inconnu: {prompt_type}")
        
        prompts_dict = self.prompts[prompt_type]
        
        if key:
            return prompts_dict.get(key, prompts_dict.get("default", {}))
        
        return prompts_dict
    
    def get_system_prompt(self, role: str, discipline: str, difficulty: str = None) -> str:
        """Obtenir le prompt système approprié"""
        prompt_key = f"{discipline}_{difficulty}" if difficulty else discipline
        
        try:
            prompts = self.get_prompt(f"{role}_prompts", prompt_key)
            return prompts.get("system", "")
        except ValueError:
            # Fallback au prompt par défaut
            default_prompts = self.get_prompt(f"{role}_prompts", "default")
            return default_prompts.get("system", "")
    
    def update_prompt(self, prompt_type: str, key: str, prompt_data: Dict[str, str]):
        """Mettre à jour un prompt"""
        if prompt_type not in self.prompts:
            self.prompts[prompt_type] = {}
        
        self.prompts[prompt_type][key] = prompt_data
        self.save_prompts(prompt_type)
    
    def save_prompts(self, prompt_type: str):
        """Sauvegarder les prompts dans le fichier"""
        file_path = self.prompts_dir / f"{prompt_type}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.prompts[prompt_type], f, indent=2, ensure_ascii=False)