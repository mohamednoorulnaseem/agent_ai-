"""
Task templates and presets for quick task creation.
Provides common patterns for development workflows.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class TaskTemplate:
    """A reusable task template."""
    id: str
    name: str
    description: str
    tasks: List[str]
    tags: List[str]
    difficulty: str  # easy, medium, hard


class TemplateLibrary:
    """Library of predefined task templates."""
    
    TEMPLATES: Dict[str, TaskTemplate] = {
        "rest_api": TaskTemplate(
            id="rest_api",
            name="REST API Development",
            description="Complete workflow for building a REST API",
            tasks=[
                "Set up FastAPI project structure",
                "Configure database connection",
                "Create data models and schemas",
                "Implement authentication and authorization",
                "Create API endpoints (GET, POST, PUT, DELETE)",
                "Add input validation and error handling",
                "Write unit tests for all endpoints",
                "Add API documentation and Swagger",
                "Configure CORS and security headers",
                "Deploy to production"
            ],
            tags=["api", "backend", "python"],
            difficulty="medium"
        ),
        
        "web_scraper": TaskTemplate(
            id="web_scraper",
            name="Web Scraper Implementation",
            description="Build a web scraper with data processing",
            tasks=[
                "Research target website structure",
                "Set up scraping environment (BeautifulSoup/Selenium)",
                "Implement page navigation and crawling",
                "Extract data from HTML elements",
                "Clean and normalize extracted data",
                "Store data in database",
                "Implement rate limiting and politeness",
                "Handle errors and retries",
                "Create monitoring and logging",
                "Package and deploy"
            ],
            tags=["scraper", "automation", "python"],
            difficulty="medium"
        ),
        
        "machine_learning": TaskTemplate(
            id="machine_learning",
            name="Machine Learning Pipeline",
            description="Complete ML project lifecycle",
            tasks=[
                "Define problem statement and success metrics",
                "Collect and explore dataset",
                "Perform data cleaning and preprocessing",
                "Feature engineering and selection",
                "Split data into train/validation/test sets",
                "Train multiple models and compare",
                "Perform hyperparameter tuning",
                "Evaluate model performance",
                "Create model deployment pipeline",
                "Monitor model in production"
            ],
            tags=["ml", "data-science", "python"],
            difficulty="hard"
        ),
        
        "react_app": TaskTemplate(
            id="react_app",
            name="React Application",
            description="Build a complete React application",
            tasks=[
                "Set up React project with Create React App",
                "Plan component hierarchy",
                "Create reusable UI components",
                "Implement state management (Redux/Context)",
                "Connect to backend API",
                "Add form handling and validation",
                "Implement routing with React Router",
                "Add styling (CSS/Tailwind)",
                "Write unit and integration tests",
                "Deploy to hosting platform"
            ],
            tags=["frontend", "react", "javascript"],
            difficulty="medium"
        ),
        
        "ci_cd_pipeline": TaskTemplate(
            id="ci_cd_pipeline",
            name="CI/CD Pipeline Setup",
            description="Automate build, test, and deployment",
            tasks=[
                "Choose CI/CD platform (GitHub Actions/GitLab CI)",
                "Create pipeline configuration file",
                "Add automated testing stage",
                "Configure code quality checks",
                "Set up artifact building",
                "Configure deployment staging",
                "Add approval gates",
                "Configure production deployment",
                "Set up monitoring and alerts",
                "Document pipeline and runbooks"
            ],
            tags=["devops", "ci-cd", "automation"],
            difficulty="medium"
        ),
        
        "mobile_app": TaskTemplate(
            id="mobile_app",
            name="Mobile App Development",
            description="Build a mobile app for iOS/Android",
            tasks=[
                "Design app UI/UX and wireframes",
                "Set up development environment",
                "Create app architecture and navigation",
                "Implement core features",
                "Add data persistence (local storage)",
                "Integrate with backend API",
                "Implement offline functionality",
                "Add push notifications",
                "Write tests and debug",
                "Prepare for app store submission"
            ],
            tags=["mobile", "ios", "android"],
            difficulty="hard"
        ),
        
        "database_design": TaskTemplate(
            id="database_design",
            name="Database Design and Migration",
            description="Design and implement a database",
            tasks=[
                "Gather requirements and data models",
                "Design database schema",
                "Normalize database design",
                "Create indexes for performance",
                "Implement backup strategy",
                "Set up replication/clustering",
                "Create migration scripts",
                "Write data access layer",
                "Performance testing and optimization",
                "Document schema and procedures"
            ],
            tags=["database", "sql", "backend"],
            difficulty="medium"
        ),
        
        "documentation": TaskTemplate(
            id="documentation",
            name="Documentation Suite",
            description="Create comprehensive project documentation",
            tasks=[
                "Write project README",
                "Create architecture documentation",
                "Document API endpoints",
                "Write user guide",
                "Create developer guide",
                "Add code examples",
                "Create troubleshooting guide",
                "Write deployment guide",
                "Set up documentation site",
                "Maintain and update documentation"
            ],
            tags=["documentation", "writing"],
            difficulty="easy"
        )
    }
    
    @classmethod
    def get_template(cls, template_id: str) -> TaskTemplate:
        """Get a template by ID."""
        return cls.TEMPLATES.get(template_id)
    
    @classmethod
    def list_templates(cls) -> List[Dict[str, Any]]:
        """List all available templates."""
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "task_count": len(t.tasks),
                "tags": t.tags,
                "difficulty": t.difficulty
            }
            for t in cls.TEMPLATES.values()
        ]
    
    @classmethod
    def get_tasks_for_template(cls, template_id: str) -> List[str]:
        """Get task list for a template."""
        template = cls.get_template(template_id)
        return template.tasks if template else []
    
    @classmethod
    def search_templates(cls, query: str) -> List[TaskTemplate]:
        """Search templates by name, description, or tags."""
        query = query.lower()
        results = []
        
        for template in cls.TEMPLATES.values():
            if (query in template.name.lower() or
                query in template.description.lower() or
                any(query in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
    
    @classmethod
    def get_templates_by_tag(cls, tag: str) -> List[TaskTemplate]:
        """Get templates with a specific tag."""
        return [
            t for t in cls.TEMPLATES.values()
            if tag.lower() in [t.lower() for t in t.tags]
        ]
    
    @classmethod
    def get_templates_by_difficulty(cls, difficulty: str) -> List[TaskTemplate]:
        """Get templates by difficulty level."""
        return [
            t for t in cls.TEMPLATES.values()
            if t.difficulty.lower() == difficulty.lower()
        ]


# Example usage
if __name__ == "__main__":
    # List all templates
    print("Available Templates:")
    for template in TemplateLibrary.list_templates():
        print(f"  - {template['name']} ({template['difficulty']})")
        print(f"    {template['description']}")
        print(f"    Tasks: {template['task_count']}\n")
    
    # Get specific template
    api_template = TemplateLibrary.get_template("rest_api")
    if api_template:
        print(f"\n{api_template.name}:")
        for i, task in enumerate(api_template.tasks, 1):
            print(f"  {i}. {task}")
    
    # Search templates
    print("\n\nSearch for 'api':")
    for template in TemplateLibrary.search_templates("api"):
        print(f"  - {template.name}")
