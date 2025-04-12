"""
Hugging Face-based Documentation Generator

This module generates documentation using Hugging Face models.
"""

import os
import json
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class HuggingFaceDocumentationGenerator:
    """
    Generates documentation using Hugging Face models.
    """
    
    def __init__(self):
        """Initialize the documentation generator"""
        self.hf_api_token = os.getenv("HF_API_TOKEN", "")
        # Choose a good model for text generation - this is a smaller model that should work with free tier
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        self.headers = {"Authorization": f"Bearer {self.hf_api_token}"}
        
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
        # If no API token, fall back to templates
        if not self.hf_api_token:
            print("No Hugging Face API token found, falling back to template")
            return self.template_generator.generate_documentation(prompt)
        
        # Determine project type for better prompting
        project_type = self._determine_project_type(prompt)
        
        try:
            # Format instructions for the model
            formatted_prompt = f"""
            Create a documentation structure for this project:
            {prompt}
            
            This is a {project_type} project. Generate a JSON structure with these sections:
            1. project_summary (title, description, objectives, scope)
            2. target_audience (primary_audience, secondary_audience, user_characteristics, user_needs)
            3. features (list of name, description, priority, details)
            4. tech_stack (list of name, category, description, benefits)
            
            Format as proper JSON.
            """
            
            # Call the Hugging Face API
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_length": 1024,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 50,
                    "do_sample": True
                }
            }
            
            # Make API request
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            # If the model is currently loading, wait and retry
            if response.status_code == 503 and "loading" in response.text.lower():
                print("Model is loading, waiting to retry...")
                time.sleep(20)  # Wait for model to load
                response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                # Try to extract JSON from the response
                try:
                    result = response.json()
                    generated_text = result[0]["generated_text"] if isinstance(result, list) else result["generated_text"]
                    
                    # Try to find and parse JSON in the generated text
                    import re
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
                        except json.JSONDecodeError:
                            print("Invalid JSON format in response")
                    
                    # If we couldn't extract valid JSON, use template-based approach
                    print("Could not extract valid JSON from response, using template")
                    return self.template_generator.generate_documentation(prompt)
                    
                except Exception as e:
                    print(f"Error processing response: {e}")
                    return self.template_generator.generate_documentation(prompt)
            else:
                print(f"API call failed with status {response.status_code}: {response.text}")
                return self.template_generator.generate_documentation(prompt)
                
        except Exception as e:
            print(f"Error calling Hugging Face API: {e}")
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
    
    def _merge_documentation(self, hf_doc, template_doc):
        """
        Merge the Hugging Face generated documentation with template documentation
        to ensure all necessary sections are present.
        
        Args:
            hf_doc: Documentation generated by Hugging Face
            template_doc: Template documentation
            
        Returns:
            Complete documentation
        """
        # Create a deep copy of the template to avoid modifying it
        import copy
        result = copy.deepcopy(template_doc)
        
        # Override with Hugging Face generated content where available
        for section in hf_doc:
            if section in result:
                if isinstance(result[section], dict) and isinstance(hf_doc[section], dict):
                    # Merge dictionaries
                    for key, value in hf_doc[section].items():
                        if value:  # Only override if the value is not empty
                            result[section][key] = value
                elif isinstance(result[section], list) and isinstance(hf_doc[section], list):
                    # Replace list if Hugging Face provided items
                    if hf_doc[section]:
                        result[section] = hf_doc[section]
                else:
                    # Direct replacement
                    result[section] = hf_doc[section]
            else:
                # Add new section
                result[section] = hf_doc[section]
        
        return result