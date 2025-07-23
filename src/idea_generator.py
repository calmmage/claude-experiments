"""Idea generation module for experiment ideas"""
import random
from typing import List, Dict, Tuple
from enum import Enum

class IdeaMode(Enum):
    RANDOM = "random"
    AI = "ai"
    STRUCTURED_AI = "structured_ai"

class IdeaCategory(Enum):
    TOOLS = "Developer Tools"
    DATA = "Data Processing"
    GAMES = "Games & Entertainment"
    WEB = "Web Applications"
    ML = "Machine Learning"
    AUTOMATION = "Automation"
    VISUALIZATION = "Data Visualization"
    API = "APIs & Services"

# Plain list of cool project ideas
COOL_IDEAS = [
    # Developer Tools
    "Git commit message generator using AI",
    "Code snippet organizer with tags",
    "Terminal dashboard for system monitoring",
    "Markdown preview server with hot reload",
    "Project scaffolding generator",
    
    # Data Processing
    "CSV to JSON/YAML converter with schemas",
    "Log file analyzer with pattern detection",
    "Data pipeline orchestrator",
    "File deduplication tool",
    
    # Games & Entertainment
    "Conway's Game of Life with patterns",
    "ASCII art generator from images",
    "Terminal-based music player",
    "Code golf challenge runner",
    
    # Web Applications
    "Personal link shortener",
    "Pastebin clone with syntax highlighting",
    "Real-time collaborative notepad",
    "Static site generator from markdown",
    
    # Machine Learning
    "Text sentiment analyzer",
    "Image color palette extractor",
    "Simple recommendation engine",
    "Spam classifier for emails",
    
    # Automation
    "Desktop notifier for various events",
    "Batch file renamer with patterns",
    "Screenshot organizer by content",
    "Automated backup tool",
    
    # Visualization
    "GitHub contribution graph generator",
    "Network traffic visualizer",
    "Folder size treemap generator",
    "CPU/Memory usage plotter",
    
    # APIs & Services
    "Weather API aggregator",
    "Currency converter with caching",
    "URL health checker service",
    "RSS feed aggregator with filters"
]

# Structured ideas by framework/technology
STRUCTURED_IDEAS = {
    "Python + FastAPI": [
        "REST API for todo management with SQLite",
        "File upload service with virus scanning",
        "URL shortener with analytics",
        "Simple authentication service",
        "Rate limiter middleware"
    ],
    "Python + Click": [
        "Database migration tool",
        "Project template generator",
        "File organizer by type/date",
        "Bulk image resizer",
        "Git repository analyzer"
    ],
    "Python + Streamlit": [
        "Data explorer for CSV files",
        "Image filter playground",
        "Text analysis dashboard",
        "Stock price tracker",
        "Personal finance dashboard"
    ],
    "JavaScript + Node": [
        "Markdown blog engine",
        "WebSocket chat server",
        "File sharing service",
        "API mock server",
        "Task scheduler service"
    ],
    "Python + SQLAlchemy": [
        "Contact management system",
        "Inventory tracker",
        "Habit tracking app",
        "Simple CRM backend",
        "Event logging system"
    ]
}

# AI-powered idea generation directions
AI_DIRECTIONS = [
    "Create a tool that helps developers be more productive",
    "Build something that processes or transforms data",
    "Design a utility for organizing digital content",
    "Develop a visualization tool for complex information",
    "Create an automation tool for repetitive tasks",
    "Build a learning tool or educational game",
    "Design a communication or collaboration tool",
    "Create a monitoring or analytics tool",
    "Build a creative tool for content generation",
    "Develop a security or privacy tool"
]

def get_random_idea() -> str:
    """Get a random idea from the curated list"""
    return random.choice(COOL_IDEAS)

def get_structured_idea() -> Tuple[str, str]:
    """Get a structured idea with framework context"""
    framework = random.choice(list(STRUCTURED_IDEAS.keys()))
    idea = random.choice(STRUCTURED_IDEAS[framework])
    return framework, idea

def get_ai_direction() -> str:
    """Get a random AI generation direction"""
    return random.choice(AI_DIRECTIONS)

def get_idea_by_category(category: IdeaCategory) -> str:
    """Get an idea from a specific category"""
    category_ideas = [idea for idea in COOL_IDEAS if any(
        cat_keyword in idea.lower() 
        for cat_keyword in category.value.lower().split()
    )]
    return random.choice(category_ideas) if category_ideas else get_random_idea()

def get_experiment_idea(mode: str = "random") -> str:
    """
    Get experiment idea based on mode
    
    Args:
        mode: One of "random", "ai", "structured", "structured_ai"
    
    Returns:
        String describing the experiment idea
    """
    if mode == "random":
        return get_random_idea()
    
    elif mode == "structured":
        framework, idea = get_structured_idea()
        return f"{idea} (using {framework})"
    
    elif mode == "ai":
        # This would be replaced with actual AI call
        return "Generate a creative programming experiment idea"
    
    elif mode == "structured_ai":
        direction = get_ai_direction()
        # This would be enhanced with actual AI call using the direction
        return f"Generate an idea to: {direction}"
    
    else:
        # Fallback to old simple ideas for compatibility
        simple_ideas = [
            "CLI tool for file organization",
            "Visualization of sorting algorithms",
            "Simple REST API with FastAPI",
            "Web scraper for news headlines",
            "Pomodoro timer with notifications",
            "Markdown to HTML converter",
            "Password strength checker",
            "CSV data analyzer",
            "Image metadata extractor",
            "Mini text-based adventure game"
        ]
        return random.choice(simple_ideas)