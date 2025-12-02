"""
Code patcher module for applying changes to files.
Handles reading, modifying, and writing files safely.
"""

import os
from typing import Optional, List
from pathlib import Path


class Patcher:
    """Applies code changes to repository files."""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.change_history: List[dict] = []
    
    def apply_patch(self, file_path: str, new_content: str, backup: bool = True) -> bool:
        """
        Apply a patch to a file by replacing its content.
        
        Args:
            file_path: Relative path to file
            new_content: New file content
            backup: Whether to create a backup
            
        Returns:
            Success status
        """
        full_path = os.path.join(self.repo_path, file_path)
        
        try:
            # Create backup if requested
            if backup and os.path.exists(full_path):
                backup_path = full_path + ".bak"
                with open(full_path, "r", encoding="utf-8") as f:
                    with open(backup_path, "w", encoding="utf-8") as bf:
                        bf.write(f.read())
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write new content
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            # Record change
            self.change_history.append({
                "file": file_path,
                "action": "write",
                "status": "success",
            })
            
            return True
        except Exception as e:
            self.change_history.append({
                "file": file_path,
                "action": "write",
                "status": "failed",
                "error": str(e),
            })
            return False
    
    def apply_diff(self, file_path: str, old_text: str, new_text: str) -> bool:
        """
        Apply a targeted diff to a file.
        Replaces old_text with new_text in the file.
        
        Args:
            file_path: Relative path to file
            old_text: Text to find and replace
            new_text: Replacement text
            
        Returns:
            Success status
        """
        full_path = os.path.join(self.repo_path, file_path)
        
        try:
            if not os.path.exists(full_path):
                return False
            
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if old_text not in content:
                return False
            
            new_content = content.replace(old_text, new_text, 1)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            self.change_history.append({
                "file": file_path,
                "action": "diff",
                "status": "success",
            })
            
            return True
        except Exception as e:
            self.change_history.append({
                "file": file_path,
                "action": "diff",
                "status": "failed",
                "error": str(e),
            })
            return False
    
    def create_file(self, file_path: str, content: str) -> bool:
        """
        Create a new file in the repository.
        
        Args:
            file_path: Relative path for new file
            content: File content
            
        Returns:
            Success status
        """
        full_path = os.path.join(self.repo_path, file_path)
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Don't overwrite existing files
            if os.path.exists(full_path):
                return False
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            self.change_history.append({
                "file": file_path,
                "action": "create",
                "status": "success",
            })
            
            return True
        except Exception as e:
            self.change_history.append({
                "file": file_path,
                "action": "create",
                "status": "failed",
                "error": str(e),
            })
            return False
    
    def delete_file(self, file_path: str, safe: bool = True) -> bool:
        """
        Delete a file from the repository.
        
        Args:
            file_path: Relative path to file
            safe: Whether to back up before deleting
            
        Returns:
            Success status
        """
        full_path = os.path.join(self.repo_path, file_path)
        
        try:
            if not os.path.exists(full_path):
                return False
            
            if safe:
                backup_path = full_path + ".deleted.bak"
                with open(full_path, "r", encoding="utf-8") as f:
                    with open(backup_path, "w", encoding="utf-8") as bf:
                        bf.write(f.read())
            
            os.remove(full_path)
            
            self.change_history.append({
                "file": file_path,
                "action": "delete",
                "status": "success",
            })
            
            return True
        except Exception as e:
            self.change_history.append({
                "file": file_path,
                "action": "delete",
                "status": "failed",
                "error": str(e),
            })
            return False
    
    def get_change_history(self) -> List[dict]:
        """Get the history of applied changes."""
        return self.change_history
    
    def clear_history(self):
        """Clear the change history."""
        self.change_history = []
