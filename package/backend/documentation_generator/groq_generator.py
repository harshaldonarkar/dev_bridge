"""
Groq-based Documentation Generator

This module generates documentation using Groq's API.
"""

import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

class GroqDocumentationGenerator:
    """
    Generates documentation using Groq models.
    """
    
    def __init__(self):
        """Initialize the documentation generator"""
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        print(f"Groq API key loaded: {'key exists' if self.groq_api_key else 'no key found'}")
        print(f"First few characters: {self.groq_api_key[:5]}..." if self.groq_api_key else "No key to show")
        self.client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        
        # For fallback if API fails
        from .template_generator import TemplateDocumentationGenerator
        self.template_generator = TemplateDocumentationGenerator()
    
    def generate_documentation(self, prompt):
        """
        Generate documentation based on the user prompt.
        
        Args:
            prompt: The user's project description
            
        Returns:
            A structured documentation object
        """
        # If no API key, fall back to templates
        if not self.client:
            print("No Groq API key found, falling back to template")
            return self.template_generator.generate_documentation(prompt)
        
        # Determine project type for better prompting
        project_type = self._determine_project_type(prompt)
        
        try:
            # Format instructions for the model
            system_prompt = """You are a professional documentation generator for software projects. 
You create comprehensive, well-structured documentation based on project descriptions. 
Output must be valid JSON with no explanations, comments, or markdown formatting.
"""
            
            user_prompt = f"""Create detailed documentation for this project:
Project description: "{prompt}"

This appears to be a {project_type.upper()} project.

Generate a valid JSON structure with exactly the following sections and format:
{{
  "project_summary": {{
    "title": "Project title here",
    "description": "Comprehensive description here",
    "objectives": ["Objective 1", "Objective 2", "Objective 3"],
    "scope": "Project scope description here"
  }},
  "target_audience": {{
    "primary_audience": "Description of primary users",
    "secondary_audience": "Description of secondary users",
    "user_characteristics": ["Characteristic 1", "Characteristic 2", "Characteristic 3"],
    "user_needs": ["Need 1", "Need 2", "Need 3"]
  }},
  "features": [
    {{
      "name": "Feature name",
      "description": "Feature description",
      "priority": "High/Medium/Low",
      "details": ["Detail 1", "Detail 2", "Detail 3"]
    }}
  ],
  "tech_stack": [
    {{
      "name": "Technology name",
      "category": "Frontend/Backend/Database/etc",
      "description": "Technology description",
      "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
      "alternatives": ["Alternative 1", "Alternative 2"]
    }}
  ],
  "content_structure": [
    {{
      "section_name": "Section name",
      "description": "Section description",
      "content_elements": ["Element 1", "Element 2", "Element 3"],
      "design_considerations": ["Consideration 1", "Consideration 2"]
    }}
  ],
  "implementation_plan": [
    {{
      "step_number": 1,
      "title": "Step title",
      "description": "Step description",
      "estimated_time": "Time estimate",
      "dependencies": [0]
    }}
  ],
  "deployment_strategy": {{
    "hosting_recommendation": "Hosting recommendation",
    "deployment_steps": ["Step 1", "Step 2", "Step 3"],
    "scaling_considerations": ["Consideration 1", "Consideration 2", "Consideration 3"],
    "maintenance_plan": "Maintenance plan description"
  }}
}}

Ensure the JSON is valid, complete, and properly formatted. Include at least 3-5 items in each array.
"""
            
            # Call the Groq API
            try:
                # Make API request to Groq
                chat_completion = self.client.chat.completions.create(
                    model="llama3-8b-8192",  # You can also use "llama3-70b-8192" for better results
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000,
                    top_p=0.9
                )
                
                # Get the generated content
                if chat_completion and chat_completion.choices:
                    generated_text = chat_completion.choices[0].message.content
                    
                    # Try to find and parse JSON in the generated text
                    json_pattern = r'(\{[\s\S]*\})'
                    matches = re.search(json_pattern, generated_text)
                    
                    if matches:
                        json_str = matches.group(1)
                        try:
                            documentation = json.loads(json_str)
                            
                            # Fill in missing sections with template data
                            template_doc = self.template_generator.get_template_for_type(project_type)
                            full_doc = self._merge_documentation(documentation, template_doc)
                            
                            return full_doc
                        except json.JSONDecodeError as e:
                            print(f"Invalid JSON format in response: {e}")
                    else:
                        print("No JSON found in the response")
                
                # If we couldn't extract valid JSON, use template-based approach
                print("Could not extract valid JSON from response, using template")
                return self.template_generator.generate_documentation(prompt)
                
            except Exception as e:
                print(f"Error making Groq API request: {e}")
                return self.template_generator.generate_documentation(prompt)
                
        except Exception as e:
            print(f"Error in Groq documentation generation: {e}")
            return self.template_generator.generate_documentation(prompt)
    
    def _determine_project_type(self, prompt):
        """
        Determine the project type based on keywords in the prompt.
        
        Args:
            prompt: The user's project description
            
        Returns:
            The project type
        """
        prompt_lower = prompt.lower()
        
        if any(keyword in prompt_lower for keyword in ["portfolio", "personal website", "showcase"]):
            return "portfolio"
        elif any(keyword in prompt_lower for keyword in ["ecommerce", "online store", "shop", "sell"]):
            return "ecommerce"
        elif any(keyword in prompt_lower for keyword in ["blog", "content", "articles"]):
            return "blog"
        elif any(keyword in prompt_lower for keyword in ["social media", "community", "network", "user profiles"]):
            return "social"
        else:
            return "web application"
    
    
    def _merge_documentation(self, groq_doc, template_doc):
        """
        Merge the Groq generated documentation with template documentation
        to ensure all necessary sections are present.
        
        Args:
            groq_doc: Documentation generated by Groq
            template_doc: Template documentation
            
        Returns:
            Complete documentation
        """
        # Create a deep copy of the template to avoid modifying it
        import copy
        result = copy.deepcopy(template_doc)
        
        # Override with Groq generated content where available
        for section in groq_doc:
            if section in result:
                if isinstance(result[section], dict) and isinstance(groq_doc[section], dict):
                    # Merge dictionaries
                    for key, value in groq_doc[section].items():
                        if value:  # Only override if the value is not empty
                            result[section][key] = value
                elif isinstance(result[section], list) and isinstance(groq_doc[section], list):
                    # Replace list if Groq provided items
                    if groq_doc[section]:
                        result[section] = groq_doc[section]
                else:
                    # Direct replacement
                    result[section] = groq_doc[section]
            else:
                # Add new section
                result[section] = groq_doc[section]
        
        return result