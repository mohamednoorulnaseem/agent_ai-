"""
Mock LLM provider for testing and demonstration.
Provides realistic responses without needing an actual LLM service.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
from llm.base import LLM


class MockLLM(LLM):
    """Mock LLM that provides predefined responses for testing."""
    
    def __init__(self):
        self.responses = {
            "plan": [
                "1. Analyze the requirements\n2. Design the solution\n3. Implement the code\n4. Test the implementation\n5. Document the code",
                "1. Create project structure\n2. Set up dependencies\n3. Implement core logic\n4. Add error handling\n5. Create unit tests",
                "1. Understand the goal\n2. Break down into tasks\n3. Implement each task\n4. Integration testing\n5. Performance optimization",
            ],
            "scan": "Repository contains Python files and configuration files",
            "general": "Task completed successfully",
        }
        self.call_count = 0
    
    def completion(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """Generate a mock completion."""
        self.call_count += 1
        
        # Check the last user message
        user_messages = [m for m in messages if m.get("role") == "user"]
        if user_messages:
            last_message = user_messages[-1]["content"].lower()
            
            if "plan" in last_message or "goal" in last_message:
                # Return different plans based on call count
                return self.responses["plan"][self.call_count % len(self.responses["plan"])]
            elif "scan" in last_message:
                return self.responses["scan"]
        
        return self.responses["general"]
