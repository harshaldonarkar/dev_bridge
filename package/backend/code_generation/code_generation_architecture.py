"""
Code Generation Architecture Module

This module defines the architecture for generating starter code based on the AI-generated documentation.
It includes base classes and interfaces for different code generators.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import os
import json
import shutil
import tempfile

class CodeGenerator(ABC):
    """
    Abstract base class for all code generators.
    """
    
    def __init__(self, config=None):
        """
        Initialize the code generator.
        
        Args:
            config: Configuration options for the code generator
        """
        self.config = config or {}
    
    @abstractmethod
    def generate_code(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate code based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated code
            
        Returns:
            Path to the generated code package
        """
        pass
    
    def _create_output_dir(self, output_dir: str) -> None:
        """
        Create the output directory if it doesn't exist.
        
        Args:
            output_dir: Directory to create
        """
        os.makedirs(output_dir, exist_ok=True)
    
    def _create_file(self, path: str, content: str) -> None:
        """
        Create a file with the given content.
        
        Args:
            path: Path to the file
            content: Content to write to the file
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
    
    def _create_package(self, source_dir: str, output_path: str) -> str:
        """
        Create a zip package from the source directory.
        
        Args:
            source_dir: Directory containing the code
            output_path: Path to save the zip package
            
        Returns:
            Path to the zip package
        """
        shutil.make_archive(
            output_path,
            'zip',
            source_dir
        )
        return f"{output_path}.zip"

class FrontendGenerator(CodeGenerator):
    """
    Base class for frontend code generators.
    """
    
    @abstractmethod
    def generate_components(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate UI components based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated components
            
        Returns:
            List of paths to the generated component files
        """
        pass
    
    @abstractmethod
    def generate_pages(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate pages based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated pages
            
        Returns:
            List of paths to the generated page files
        """
        pass
    
    @abstractmethod
    def generate_styles(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate styles based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated styles
            
        Returns:
            List of paths to the generated style files
        """
        pass
    
    @abstractmethod
    def generate_assets(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate assets based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated assets
            
        Returns:
            List of paths to the generated asset files
        """
        pass

class BackendGenerator(CodeGenerator):
    """
    Base class for backend code generators.
    """
    
    @abstractmethod
    def generate_models(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate data models based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated models
            
        Returns:
            List of paths to the generated model files
        """
        pass
    
    @abstractmethod
    def generate_controllers(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate controllers based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated controllers
            
        Returns:
            List of paths to the generated controller files
        """
        pass
    
    @abstractmethod
    def generate_routes(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate API routes based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated routes
            
        Returns:
            List of paths to the generated route files
        """
        pass
    
    @abstractmethod
    def generate_services(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate services based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated services
            
        Returns:
            List of paths to the generated service files
        """
        pass

class AIAgentGenerator(CodeGenerator):
    """
    Base class for AI agent generators.
    """
    
    @abstractmethod
    def generate_agent_definition(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate AI agent definition based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated definition
            
        Returns:
            Path to the generated definition file
        """
        pass
    
    @abstractmethod
    def generate_agent_logic(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate AI agent logic based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated logic
            
        Returns:
            List of paths to the generated logic files
        """
        pass
    
    @abstractmethod
    def generate_agent_integration(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate AI agent integration code based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated integration code
            
        Returns:
            List of paths to the generated integration files
        """
        pass

class CodeGenerationFactory:
    """
    Factory class for creating code generators.
    """
    
    @staticmethod
    def create_generator(generator_type: str, config: Optional[Dict[str, Any]] = None) -> CodeGenerator:
        """
        Create a code generator of the specified type.
        
        Args:
            generator_type: Type of generator to create (frontend, backend, ai_agent)
            config: Configuration options for the generator
            
        Returns:
            A code generator instance
        """
        if generator_type == 'frontend':
            from .frontend_generator import ReactNextGenerator
            return ReactNextGenerator(config)
        elif generator_type == 'backend':
            from .backend_generator import NodeExpressGenerator
            return NodeExpressGenerator(config)
        elif generator_type == 'ai_agent':
            from .ai_agent_generator import OpenAIAgentGenerator
            return OpenAIAgentGenerator(config)
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")

class CodeGenerationOrchestrator:
    """
    Orchestrates the code generation process.
    """
    
    def __init__(self, config=None):
        """
        Initialize the orchestrator.
        
        Args:
            config: Configuration options for the orchestrator
        """
        self.config = config or {}
        self.generators = {}
    
    def register_generator(self, generator_type: str, generator: CodeGenerator) -> None:
        """
        Register a code generator.
        
        Args:
            generator_type: Type of the generator
            generator: The generator instance
        """
        self.generators[generator_type] = generator
    
    def generate_code(self, documentation: Dict[str, Any], generator_types: List[str]) -> Dict[str, str]:
        """
        Generate code using the specified generators.
        
        Args:
            documentation: The documentation object
            generator_types: Types of generators to use
            
        Returns:
            Dictionary mapping generator types to output paths
        """
        results = {}
        
        for generator_type in generator_types:
            if generator_type not in self.generators:
                self.generators[generator_type] = CodeGenerationFactory.create_generator(generator_type, self.config)
            
            # Create temporary directory for code generation
            with tempfile.TemporaryDirectory() as temp_dir:
                # Generate code
                output_path = self.generators[generator_type].generate_code(documentation, temp_dir)
                results[generator_type] = output_path
        
        return results

# Example usage
if __name__ == "__main__":
    # This is just for demonstration purposes
    with open('sample_documentation.json', 'r') as f:
        documentation = json.load(f)
    
    orchestrator = CodeGenerationOrchestrator()
    results = orchestrator.generate_code(documentation, ['frontend', 'backend'])
    
    print(f"Frontend code: {results['frontend']}")
    print(f"Backend code: {results['backend']}")
