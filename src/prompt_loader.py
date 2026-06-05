"""
Prompt Loader - Load and format LLM prompts from YAML configuration
"""

import yaml
import os
from typing import Dict, Any


def load_prompts(config_path: str = None) -> Dict[str, Any]:
    """
    Load prompts configuration from YAML file.
    
    Args:
        config_path: Path to prompts.yaml file. If None, searches in standard locations.
    
    Returns:
        Dictionary with prompt configuration
    """
    
    # Search standard locations if path not provided
    if config_path is None:
        search_paths = [
            "config/prompts.yaml",
            "../config/prompts.yaml",
            "/Workspace/Users/12eee056@gmail.com/.sql_optimizer/prompts.yaml",
            os.path.join(os.path.dirname(__file__), "../config/prompts.yaml")
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                config_path = path
                break
    
    if config_path is None or not os.path.exists(config_path):
        raise FileNotFoundError(
            "prompts.yaml not found. Create it in config/ or specify path."
        )
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def format_system_prompt(config: Dict, optimization_mode: str, complexity: Dict) -> str:
    """
    Format system prompt with optimization strategy.
    
    Args:
        config: Loaded prompts configuration
        optimization_mode: 'conservative' or 'aggressive'
        complexity: Complexity detection results
    
    Returns:
        Formatted system prompt
    """
    
    # Get strategy instructions
    strategy = config['strategies'][optimization_mode]['instructions']
    
    # Format with complexity details
    strategy = strategy.format(
        cte_count=complexity.get('cte_count', 0),
        window_count=complexity.get('window_count', 0)
    )
    
    # Format full system prompt
    system_prompt = config['system_prompt_template'].format(
        optimization_strategy=strategy
    )
    
    return system_prompt


def format_user_prompt(config: Dict, query: str) -> str:
    """
    Format user prompt with SQL query.
    
    Args:
        config: Loaded prompts configuration
        query: SQL query to optimize
    
    Returns:
        Formatted user prompt
    """
    
    return config['user_prompt_template'].format(query=query)


def get_llm_config(config: Dict) -> Dict[str, Any]:
    """
    Get LLM endpoint configuration.
    
    Args:
        config: Loaded prompts configuration
    
    Returns:
        Dictionary with LLM settings
    """
    
    return config['llm']
