"""
Repository scanner module for analyzing codebases.
Scans and catalogs repository structure and content.
"""

import os
from typing import List, Dict, Any
from pathlib import Path


class RepositoryInfo:
    """Information about a repository."""
    
    def __init__(self):
        self.files: List[str] = []
        self.directories: List[str] = []
        self.file_count = 0
        self.total_lines = 0
        self.languages: Dict[str, int] = {}


class Scanner:
    """Scans and analyzes repository structure."""
    
    def __init__(self, repo_path: str, ignore_dirs: List[str] = None):
        self.repo_path = repo_path
        self.ignore_dirs = ignore_dirs or [
            ".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build",
            ".pytest_cache", ".mypy_cache", ".egg-info"
        ]
        self.repo_info = RepositoryInfo()
    
    def scan_repository(self, max_depth: int = 10) -> str:
        """
        Scan the repository and return a summary.
        
        Args:
            max_depth: Maximum directory depth to scan
            
        Returns:
            Formatted string describing the repository
        """
        self.repo_info = RepositoryInfo()
        self._scan_directory(self.repo_path, 0, max_depth)
        return self._format_summary()
    
    def _scan_directory(self, path: str, depth: int, max_depth: int):
        """Recursively scan directory."""
        if depth > max_depth:
            return
        
        try:
            for entry in os.listdir(path):
                if entry.startswith("."):
                    continue
                
                full_path = os.path.join(path, entry)
                rel_path = os.path.relpath(full_path, self.repo_path)
                
                if os.path.isdir(full_path):
                    if entry not in self.ignore_dirs:
                        self.repo_info.directories.append(rel_path)
                        self._scan_directory(full_path, depth + 1, max_depth)
                else:
                    self.repo_info.files.append(rel_path)
                    self.repo_info.file_count += 1
                    self._count_lines(full_path, entry)
        except PermissionError:
            pass
    
    def _count_lines(self, file_path: str, filename: str):
        """Count lines and detect language."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = len(f.readlines())
                self.repo_info.total_lines += lines
            
            # Detect language by extension
            ext = Path(filename).suffix
            if ext:
                self.repo_info.languages[ext] = self.repo_info.languages.get(ext, 0) + 1
        except:
            pass
    
    def _format_summary(self) -> str:
        """Format repository information as a string."""
        summary = f"Repository: {self.repo_path}\n"
        summary += f"Total Files: {self.repo_info.file_count}\n"
        summary += f"Total Lines: {self.repo_info.total_lines}\n"
        
        if self.repo_info.languages:
            summary += "\nLanguages:\n"
            for ext, count in sorted(self.repo_info.languages.items(), key=lambda x: x[1], reverse=True):
                summary += f"  {ext}: {count} files\n"
        
        if self.repo_info.directories:
            summary += f"\nKey Directories ({len(self.repo_info.directories)} total):\n"
            for d in sorted(self.repo_info.directories)[:10]:
                summary += f"  {d}\n"
        
        if len(self.repo_info.directories) > 10:
            summary += f"  ... and {len(self.repo_info.directories) - 10} more\n"
        
        return summary
    
    def get_files_by_extension(self, extension: str) -> List[str]:
        """Get all files with a specific extension."""
        return [f for f in self.repo_info.files if f.endswith(extension)]
    
    def get_file_content(self, file_path: str, max_lines: int = 100) -> str:
        """
        Get content of a specific file.
        
        Args:
            file_path: Relative path to file
            max_lines: Maximum lines to return
            
        Returns:
            File content
        """
        full_path = os.path.join(self.repo_path, file_path)
        
        if not os.path.exists(full_path):
            return f"File not found: {file_path}"
        
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                if len(lines) > max_lines:
                    content = "".join(lines[:max_lines])
                    content += f"\n... ({len(lines) - max_lines} more lines)\n"
                else:
                    content = "".join(lines)
            return content
        except Exception as e:
            return f"Error reading file: {e}"
