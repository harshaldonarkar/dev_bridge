"""
Gemini-based Documentation Generator

This module generates documentation using Google's Gemini API.
"""

import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiDocumentationGenerator:
    """
    Generates documentation using Google's Gemini API.
    """
    
    def __init__(self):
        """Initialize the documentation generator"""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
        
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
        if not self.model:
            print("No Gemini API key found, falling back to template")
            return self.template_generator.generate_documentation(prompt)
        
        # Determine project type for better prompting
        project_type = self._determine_project_type(prompt)
        
        try:
            # Format instructions for the model
            gemini_prompt = f"""Generate comprehensive documentation for this software project:

Project description: "{prompt}"

This appears to be a {project_type.upper()} project.

Return a JSON object with exactly the following structure (include all sections and subsections):
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

Include at least 3-5 items in each array. Make all content relevant to the specific project type and description.
Your response should be a valid, complete JSON object and nothing else - no explanations, markdown, or extra text.
"""
            
            # Call the Gemini API
            try:
                # Configure safety settings to ensure we get a response
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    }
                ]
                
                # Make API request to Gemini
                response = self.model.generate_content(
                    gemini_prompt,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 8192,
                    },
                    safety_settings=safety_settings
                )
                
                if response:
                    generated_text = response.text
                    
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
                            print(f"JSON attempted to parse: {json_str[:100]}...")
                    else:
                        print("No JSON found in the response")
                        print(f"Response text: {generated_text[:100]}...")
                
                # If we couldn't extract valid JSON, use template-based approach
                print("Could not extract valid JSON from response, using template")
                return self.template_generator.generate_documentation(prompt)
                
            except Exception as e:
                print(f"Error making Gemini API request: {e}")
                return self.template_generator.generate_documentation(prompt)
                
        except Exception as e:
            print(f"Error in Gemini documentation generation: {e}")
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
    
    def _merge_documentation(self, gemini_doc, template_doc):
        """
        Merge the Gemini generated documentation with template documentation
        to ensure all necessary sections are present.
        
        Args:
            gemini_doc: Documentation generated by Gemini
            template_doc: Template documentation
            
        Returns:
            Complete documentation
        """
        # Create a deep copy of the template to avoid modifying it
        import copy
        result = copy.deepcopy(template_doc)
        
        # Override with Gemini generated content where available
        for section in gemini_doc:
            if section in result:
                if isinstance(result[section], dict) and isinstance(gemini_doc[section], dict):
                    # Merge dictionaries
                    for key, value in gemini_doc[section].items():
                        if value:  # Only override if the value is not empty
                            result[section][key] = value
                elif isinstance(result[section], list) and isinstance(gemini_doc[section], list):
                    # Replace list if Gemini provided items
                    if gemini_doc[section]:
                        result[section] = gemini_doc[section]
                else:
                    # Direct replacement
                    result[section] = gemini_doc[section]
            else:
                # Add new section
                result[section] = gemini_doc[section]
        
        return result