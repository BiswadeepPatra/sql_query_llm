"""
Git Integration - Clone, find SQL files, commit and push results
"""

import os
import subprocess
from typing import List, Dict


def clone_or_pull_repo(repo_url: str, target_dir: str = "/tmp/sql_optimizer_repos") -> str:
    """
    Clone a Git repository or pull if it already exists.
    
    Args:
        repo_url: GitHub repository URL
        target_dir: Local directory to clone into
    
    Returns:
        Local path to the cloned repo
    """
    
    # Extract repo name from URL
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    repo_path = f"{target_dir}/{repo_name}"
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    
    if os.path.exists(repo_path):
        print(f"🔄 Updating existing repo: {repo_name}")
        subprocess.run(["git", "-C", repo_path, "pull"], check=True, capture_output=True)
    else:
        print(f"📥 Cloning repo: {repo_name}")
        subprocess.run(["git", "clone", repo_url, repo_path], check=True, capture_output=True)
    
    print(f"✅ Repository ready at: {repo_path}")
    return repo_path


def find_sql_files(repo_path: str) -> List[Dict[str, str]]:
    """
    Find all .sql files in the repository's input/ folder.
    
    Args:
        repo_path: Path to the Git repository
    
    Returns:
        List of dictionaries with SQL file information
    """
    sql_files = []
    
    # Look in input/ folder first, fall back to repo root
    input_dir = os.path.join(repo_path, "input")
    search_dir = input_dir if os.path.exists(input_dir) else repo_path
    
    for root, dirs, files in os.walk(search_dir):
        # Skip .git, optimized, and output directories
        if '.git' in root or 'optimized' in root or 'output' in root:
            continue
            
        for file in files:
            if file.endswith('.sql'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract relative path and clean name
                    rel_path = os.path.relpath(file_path, repo_path)
                    clean_name = file.replace('.sql', '')
                    
                    sql_files.append({
                        'name': clean_name,
                        'file': file,
                        'path': rel_path,
                        'full_path': file_path,
                        'content': content
                    })
                except Exception as e:
                    print(f"⚠️  Error reading {file}: {e}")
    
    return sql_files


def commit_and_push(repo_path: str, git_token: str = None, commit_message: str = "SQL Optimizer: Add optimized queries") -> bool:
    """
    Commit and push changes to Git repository.
    
    Args:
        repo_path: Path to the Git repository
        git_token: GitHub Personal Access Token (optional)
        commit_message: Commit message
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Configure Git
        subprocess.run(["git", "-C", repo_path, "config", "user.name", "SQL Optimizer Bot"], 
                      check=True, capture_output=True)
        subprocess.run(["git", "-C", repo_path, "config", "user.email", "optimizer@databricks.local"],
                      check=True, capture_output=True)
        
        # Stage all changes
        subprocess.run(["git", "-C", repo_path, "add", "."], check=True, capture_output=True)
        print("✅ Files staged for commit")
        
        # Commit
        result = subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message],
                               capture_output=True, text=True)
        print(result.stdout)
        print(f"✅ Committed: {commit_message}")
        
        # Push if token provided
        if git_token:
            # Get remote URL and inject token
            result = subprocess.run(["git", "-C", repo_path, "remote", "get-url", "origin"],
                                   capture_output=True, text=True, check=True)
            remote_url = result.stdout.strip()
            
            # Inject token into URL
            if remote_url.startswith("https://"):
                remote_url_with_token = remote_url.replace("https://", f"https://{git_token}@")
                
                subprocess.run(["git", "-C", repo_path, "push", remote_url_with_token, "main"],
                              check=True, capture_output=True)
                print("✅ Pushed to remote repository!")
                return True
        else:
            print("ℹ️  No Git token provided - skipping push")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
