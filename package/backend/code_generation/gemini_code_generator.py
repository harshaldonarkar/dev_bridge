"""
Gemini-based Code Generator

This module generates code using Google's Gemini API based on the AI-generated documentation.
"""

import os
import json
import shutil
import re
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv
from .code_generation_architecture import CodeGenerator

# Load environment variables
load_dotenv()

class GeminiCodeGenerator(CodeGenerator):
    """
    Generates code using Google's Gemini model based on documentation.
    """
    
    def __init__(self, config=None):
        """
        Initialize the Gemini code generator.
        
        Args:
            config: Configuration options for the generator
        """
        super().__init__(config)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            # Use Gemini 1.5 Pro for optimal code generation
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            print("Warning: No Gemini API key found. Code generation will fail.")
            self.model = None
    
    def generate_code(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate code based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated code
            
        Returns:
            Path to the generated code package
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        # Define the structure of files to generate
        file_structure = self._plan_file_structure(documentation)
        
        # Generate each file
        for file_path, file_info in file_structure.items():
            # Create prompt for this specific file
            prompt = self._create_file_prompt(documentation, file_path, file_info)
            
            # Generate code content using Gemini
            file_content = self._generate_file_content(prompt)
            
            # Save the file
            full_path = os.path.join(output_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(file_content)
        
        # Create package
        package_name = documentation.get('project_summary', {}).get('title', 'code').replace(' ', '_').lower()
        return self._create_package(output_dir, os.path.join(os.path.dirname(output_dir), package_name))
    
    def _plan_file_structure(self, documentation: Dict[str, Any]) -> Dict[str, Dict]:
        """
        Plan the file structure based on documentation.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Dictionary mapping file paths to file information
        """
        # Ask Gemini to plan the file structure
        project_type = documentation.get('project_summary', {}).get('title', 'Project')
        features = documentation.get('features', [])
        tech_stack = documentation.get('tech_stack', [])
        
        prompt = f"""
        Create a file structure plan for a {project_type} project with these features:
        {json.dumps(features, indent=2)}
        
        And this tech stack:
        {json.dumps(tech_stack, indent=2)}
        
        Return a JSON object where keys are file paths and values are objects with:
        - "description": Brief description of the file's purpose
        - "type": File type (e.g., "component", "model", "controller", "config")
        
        Only return the JSON, nothing else.
        """
        
        try:
            response = self.model.generate_content(prompt)
            structure_text = response.text
            
            # Parse JSON from response
            json_pattern = r'(\{[\s\S]*\})'
            matches = re.search(json_pattern, structure_text)
            
            if matches:
                structure = json.loads(matches.group(1))
                return structure
            else:
                # Fallback to a basic structure
                return self._default_file_structure()
        except Exception as e:
            print(f"Error planning file structure: {e}")
            return self._default_file_structure()
    
    def _default_file_structure(self) -> Dict[str, Dict]:
        """
        Provide a default file structure.
        
        Returns:
            Dictionary mapping file paths to file information
        """
        return {
            "src/index.js": {"description": "Main entry point", "type": "config"},
            "src/App.js": {"description": "Main application component", "type": "component"},
            "src/components/Header.js": {"description": "Header component", "type": "component"},
            "src/components/Footer.js": {"description": "Footer component", "type": "component"},
            "src/styles/global.css": {"description": "Global styles", "type": "styles"},
            "README.md": {"description": "Project documentation", "type": "documentation"}
        }
    
    def _create_file_prompt(self, documentation: Dict[str, Any], file_path: str, file_info: Dict) -> str:
        """
        Create a prompt for generating a specific file.
        
        Args:
            documentation: The documentation object
            file_path: Path to the file
            file_info: Information about the file
            
        Returns:
            Prompt for generating the file
        """
        project_title = documentation.get('project_summary', {}).get('title', 'Project')
        project_description = documentation.get('project_summary', {}).get('description', '')
        
        prompt = f"""
        You are an expert developer creating code for a {project_title} project.
        
        Project description: {project_description}
        
        I need you to write the code for {file_path} which is a {file_info['type']}.
        This file's purpose: {file_info['description']}
        
        The overall project has these features:
        {json.dumps(documentation.get('features', []), indent=2)}
        
        And uses this tech stack:
        {json.dumps(documentation.get('tech_stack', []), indent=2)}
        
        Write the complete code for this file. Include good comments and follow best practices.
        Only output the code, no explanations or markdown formatting.
        """
        
        return prompt
    
    def _generate_file_content(self, prompt: str) -> str:
        """
        Generate file content using Gemini.
        
        Args:
            prompt: The prompt for generating the file
            
        Returns:
            The generated file content
        """
        try:
            if not self.model:
                return "// Error: No Gemini API key configured"
            
            # Add retry logic for rate limits
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = self.model.generate_content(prompt)
                    content = response.text
                    
                    # Clean up potential markdown code blocks
                    if re.search(r'```[\w]*\n', content):
                        content = re.sub(r'```[\w]*\n', '', content)
                        content = re.sub(r'```\n?$', '', content)
                    
                    return content
                except Exception as e:
                    if "rate limit" in str(e).lower() and retry_count < max_retries - 1:
                        retry_count += 1
                        import time
                        time.sleep(2 ** retry_count)  # Exponential backoff
                        continue
                    raise
            
        except Exception as e:
            print(f"Error generating file content: {e}")
            return f"// Error generating content: {str(e)}"


class GeminiFrontendGenerator(GeminiCodeGenerator):
    """Specialized Gemini generator for frontend code"""
    
    def _plan_file_structure(self, documentation: Dict[str, Any]) -> Dict[str, Dict]:
        """
        Plan a frontend-specific file structure based on documentation.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Dictionary mapping file paths to file information
        """
        # Check if using React or other frontend framework
        tech_stack = documentation.get('tech_stack', [])
        features = documentation.get('features', [])
        content_structure = documentation.get('content_structure', [])
        
        # Determine if using React/Next.js
        uses_react = any('react' in tech.get('name', '').lower() for tech in tech_stack)
        uses_nextjs = any('next' in tech.get('name', '').lower() for tech in tech_stack)
        uses_tailwind = any('tailwind' in tech.get('name', '').lower() for tech in tech_stack)
        
        if uses_nextjs:
            # Next.js project structure
            structure = {
                "README.md": {"description": "Project documentation", "type": "documentation"},
                "package.json": {"description": "Project dependencies and scripts", "type": "config"},
                "next.config.js": {"description": "Next.js configuration", "type": "config"},
                ".env.local": {"description": "Environment variables", "type": "config"},
                "pages/_app.js": {"description": "Next.js application wrapper", "type": "component"},
                "pages/index.js": {"description": "Home page", "type": "component"},
                "styles/globals.css": {"description": "Global styles", "type": "styles"}
            }
            
            # Add page components based on content structure
            for i, section in enumerate(content_structure):
                section_name = section.get('section_name', '').lower().replace(' ', '-')
                if section_name and section_name != 'home':
                    structure[f"pages/{section_name}.js"] = {
                        "description": f"{section.get('section_name', '')} page", 
                        "type": "component"
                    }
            
            # Add components based on features
            for i, feature in enumerate(features):
                feature_name = feature.get('name', '').replace(' ', '')
                structure[f"components/{feature_name}.js"] = {
                    "description": f"{feature.get('name', '')} component", 
                    "type": "component"
                }
            
            # Add utility files
            structure["components/Layout.js"] = {"description": "Layout component with header and footer", "type": "component"}
            structure["utils/api.js"] = {"description": "API utility functions", "type": "utility"}
            
            if uses_tailwind:
                structure["tailwind.config.js"] = {"description": "Tailwind CSS configuration", "type": "config"}
                structure["postcss.config.js"] = {"description": "PostCSS configuration", "type": "config"}
        
        elif uses_react:
            # React project structure
            structure = {
                "README.md": {"description": "Project documentation", "type": "documentation"},
                "package.json": {"description": "Project dependencies and scripts", "type": "config"},
                ".env": {"description": "Environment variables", "type": "config"},
                "public/index.html": {"description": "HTML entry point", "type": "config"},
                "src/index.js": {"description": "JavaScript entry point", "type": "config"},
                "src/App.js": {"description": "Main application component", "type": "component"},
                "src/styles/global.css": {"description": "Global styles", "type": "styles"}
            }
            
            # Add components based on features and content structure
            for i, feature in enumerate(features):
                feature_name = feature.get('name', '').replace(' ', '')
                structure[f"src/components/{feature_name}.js"] = {
                    "description": f"{feature.get('name', '')} component", 
                    "type": "component"
                }
            
            # Add page components based on content structure
            for i, section in enumerate(content_structure):
                section_name = section.get('section_name', '').replace(' ', '')
                structure[f"src/pages/{section_name}.js"] = {
                    "description": f"{section.get('section_name', '')} page component", 
                    "type": "component"
                }
            
            # Add utility files
            structure["src/components/Layout.js"] = {"description": "Layout component with header and footer", "type": "component"}
            structure["src/utils/api.js"] = {"description": "API utility functions", "type": "utility"}
            
            if uses_tailwind:
                structure["tailwind.config.js"] = {"description": "Tailwind CSS configuration", "type": "config"}
                structure["postcss.config.js"] = {"description": "PostCSS configuration", "type": "config"}
        
        else:
            # Basic frontend structure
            structure = {
                "README.md": {"description": "Project documentation", "type": "documentation"},
                "package.json": {"description": "Project dependencies and scripts", "type": "config"},
                "index.html": {"description": "HTML entry point", "type": "markup"},
                "js/main.js": {"description": "Main JavaScript file", "type": "script"},
                "css/styles.css": {"description": "CSS styles", "type": "styles"}
            }
            
            # Add pages based on content structure
            for i, section in enumerate(content_structure):
                section_name = section.get('section_name', '').lower().replace(' ', '-')
                if section_name and section_name != 'home':
                    structure[f"{section_name}.html"] = {
                        "description": f"{section.get('section_name', '')} page", 
                        "type": "markup"
                    }
                    structure[f"js/{section_name}.js"] = {
                        "description": f"JavaScript for {section.get('section_name', '')} page", 
                        "type": "script"
                    }
        
        return structure


class GeminiBackendGenerator(GeminiCodeGenerator):
    """Specialized Gemini generator for backend code"""
    
    def _plan_file_structure(self, documentation: Dict[str, Any]) -> Dict[str, Dict]:
        """
        Plan a backend-specific file structure based on documentation.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Dictionary mapping file paths to file information
        """
        # Check backend technologies
        tech_stack = documentation.get('tech_stack', [])
        features = documentation.get('features', [])
        
        # Determine backend technology
        uses_node = any('node' in tech.get('name', '').lower() for tech in tech_stack)
        uses_express = any('express' in tech.get('name', '').lower() for tech in tech_stack)
        uses_mongodb = any('mongo' in tech.get('name', '').lower() for tech in tech_stack)
        uses_sql = any(db in tech.get('name', '').lower() for tech in tech_stack for db in ['sql', 'postgres', 'mysql'])
        
        if uses_node and uses_express:
            # Node.js + Express structure
            structure = {
                "README.md": {"description": "Project documentation", "type": "documentation"},
                "package.json": {"description": "Project dependencies and scripts", "type": "config"},
                ".env": {"description": "Environment variables", "type": "config"},
                "server.js": {"description": "Main server file", "type": "config"},
                "app.js": {"description": "Express application setup", "type": "config"},
                "routes/index.js": {"description": "API route index", "type": "route"},
                "middleware/auth.js": {"description": "Authentication middleware", "type": "middleware"},
                "utils/logger.js": {"description": "Logging utility", "type": "utility"},
                "utils/errorHandler.js": {"description": "Error handling utility", "type": "utility"}
            }
            
            # Add database configuration
            if uses_mongodb:
                structure["config/database.js"] = {"description": "MongoDB connection setup", "type": "config"}
                structure["models/index.js"] = {"description": "Database models index", "type": "model"}
            elif uses_sql:
                structure["config/database.js"] = {"description": "SQL database connection setup", "type": "config"}
                structure["models/index.js"] = {"description": "Sequelize models index", "type": "model"}
                structure["migrations"] = {"description": "Database migrations directory", "type": "config"}
            
            # Add feature-specific routes, controllers, and models
            for i, feature in enumerate(features):
                feature_name = feature.get('name', '').lower().replace(' ', '_')
                
                # Create route
                structure[f"routes/{feature_name}.js"] = {
                    "description": f"Routes for {feature.get('name', '')}",
                    "type": "route"
                }
                
                # Create controller
                structure[f"controllers/{feature_name}Controller.js"] = {
                    "description": f"Controller for {feature.get('name', '')}",
                    "type": "controller"
                }
                
                # Create model
                structure[f"models/{feature_name.replace('_', '')}.js"] = {
                    "description": f"Model for {feature.get('name', '')}",
                    "type": "model"
                }
                
                # Create service if needed
                if feature.get('priority', '').lower() == 'high':
                    structure[f"services/{feature_name}Service.js"] = {
                        "description": f"Service layer for {feature.get('name', '')}",
                        "type": "service"
                    }
            
            # Add user model and auth if there are any high priority features
            has_high_priority = any(feature.get('priority', '').lower() == 'high' for feature in features)
            if has_high_priority:
                structure["models/user.js"] = {"description": "User model", "type": "model"}
                structure["controllers/authController.js"] = {"description": "Authentication controller", "type": "controller"}
                structure["routes/auth.js"] = {"description": "Authentication routes", "type": "route"}
        
        else:
            # Generic backend structure
            structure = {
                "README.md": {"description": "Project documentation", "type": "documentation"},
                "server.js": {"description": "Main server file", "type": "config"},
                "config/config.js": {"description": "Configuration file", "type": "config"},
                "api/routes.js": {"description": "API routes", "type": "route"},
                "api/controllers.js": {"description": "API controllers", "type": "controller"},
                "api/models.js": {"description": "Data models", "type": "model"}
            }
        
        return structure