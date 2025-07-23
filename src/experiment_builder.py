"""Experiment building module for different implementation scenarios"""
from enum import Enum
from typing import Dict, Any

class ImplementationLevel(Enum):
    SIMPLE_TEST = "simple_test"
    MVP = "mvp"
    FULL_SCENARIO = "full_scenario"

class ExperimentBuilder:
    """Build experiment prompts based on implementation level"""
    
    @staticmethod
    def build_prompt(idea: str, level: ImplementationLevel = ImplementationLevel.MVP) -> str:
        """
        Build a prompt for Claude based on the idea and implementation level
        
        Args:
            idea: The experiment idea
            level: The implementation level (simple_test, mvp, or full_scenario)
            
        Returns:
            A detailed prompt for Claude
        """
        base_requirements = """
Requirements:
1. Create a README.md explaining the project
2. Create a run.sh script to start the project (make it executable)
3. Include all needed code files
4. Make sure the project is self-contained and can run with bash run.sh"""

        if level == ImplementationLevel.SIMPLE_TEST:
            return f"""Create a simple proof-of-concept for: {idea}

Focus on:
- Minimal working implementation
- Basic functionality demonstration
- Simple command-line interface
- No external dependencies if possible
- Clear code comments explaining the approach

{base_requirements}"""

        elif level == ImplementationLevel.MVP:
            return f"""Create an MVP (Minimum Viable Product) for: {idea}

Focus on:
- Core essential features only
- Clean, well-structured code
- Basic error handling
- Simple but functional UI (CLI or web)
- Minimal dependencies
- Clear documentation of features

{base_requirements}"""

        elif level == ImplementationLevel.FULL_SCENARIO:
            return f"""Create a complete implementation for: {idea}

Focus on:
- Full user scenario with multiple use cases
- Well-thought-out UI/UX (even if CLI-based)
- Proper error handling and edge cases
- Configuration options
- Help documentation
- Example usage scenarios

User Story:
1. User discovers the tool and reads README
2. User runs the tool for the first time
3. User explores main features
4. User customizes settings (if applicable)
5. User achieves their goal with the tool

{base_requirements}"""

        else:
            # Default to MVP
            return ExperimentBuilder.build_prompt(idea, ImplementationLevel.MVP)

    @staticmethod
    def get_retry_prompt(error_context: str, idea: str, level: ImplementationLevel = ImplementationLevel.MVP) -> str:
        """Build a retry prompt when validation fails"""
        level_hints = {
            ImplementationLevel.SIMPLE_TEST: "Keep it extremely simple - just make it work!",
            ImplementationLevel.MVP: "Focus on getting the core functionality working.",
            ImplementationLevel.FULL_SCENARIO: "Ensure all components work together properly."
        }
        
        return f"""Previous attempt failed with error: {error_context}

Please fix the issue and create a working {idea}.

{level_hints.get(level, "")}

Make sure to:
1. Create a README.md explaining the project
2. Create a run.sh script to start the project
3. Include all needed code files
4. Test that run.sh actually works"""

    @staticmethod
    def enhance_idea_with_details(idea: str, level: ImplementationLevel) -> Dict[str, Any]:
        """
        Enhance an idea with implementation-specific details
        
        Returns a dictionary with:
        - enhanced_idea: The enhanced idea description
        - tech_suggestions: Suggested technologies
        - features: List of features to implement
        """
        if level == ImplementationLevel.SIMPLE_TEST:
            return {
                "enhanced_idea": f"Simple {idea} prototype",
                "tech_suggestions": ["Python stdlib only", "Bash", "No dependencies"],
                "features": ["Basic core functionality", "Minimal CLI"]
            }
        
        elif level == ImplementationLevel.MVP:
            return {
                "enhanced_idea": f"{idea} with essential features",
                "tech_suggestions": ["Python with minimal deps", "Simple web UI optional", "SQLite if needed"],
                "features": ["Core features", "Basic UI", "Error handling", "Help text"]
            }
        
        elif level == ImplementationLevel.FULL_SCENARIO:
            return {
                "enhanced_idea": f"Full-featured {idea}",
                "tech_suggestions": ["Best tool for the job", "Professional UI", "Proper data storage"],
                "features": [
                    "Complete feature set",
                    "Intuitive UI/UX", 
                    "Configuration system",
                    "Error recovery",
                    "Logging",
                    "Examples and tutorials"
                ]
            }
        
        return {
            "enhanced_idea": idea,
            "tech_suggestions": [],
            "features": []
        }