"""
Setup configuration for AI Agent framework.
"""

from setuptools import setup, find_packages

setup(
    name="agent_ai",
    version="0.2.0",
    description="An intelligent agent framework for automated development tasks",
    author="AI Agent Team",
    packages=find_packages(where="."),
    py_modules=["cli", "config", "api", "persistence", "auth", "websocket_support", "templates", "analytics"],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "openai>=1.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "websockets>=11.0",
        "PyJWT>=2.8.0",
        "python-multipart>=0.0.5",
    ],
    entry_points={
        "console_scripts": [
            "agent-ai=cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
