# """# AI Documentation Generator Implementation
# This module processes user prompts and generates comprehensive documentation using OpenAIs GPT-4 model with LangChain for orchestration.

# ## Configuration
# - Uses OpenAI GPT-4 for natural language understanding and content generation
# - Implements a multi-step prompting strategy for different documentation sections
# - Structures output in a consistent format for frontend display
# - Handles error cases and provides fallback strategies

# ## Usage
# 1. Initialize the DocumentationGenerator with your OpenAI API key
# 2. Call generate_documentation() with the users project description
# 3. Receive structured documentation object with all sections

# """
# import os
# import json
# from typing import Dict, List, Any, Optional
# from dotenv import load_dotenv
# from openai import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.output_parsers import PydanticOutputParser
# from pydantic import BaseModel, Field


# # Load environment variables
# load_dotenv()

# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

# # Define output models for structured parsing
# class ProjectSummary(BaseModel):
#     title: str = Field(description="A concise title for the project")
#     description: str = Field(description="A comprehensive description of the project")
#     objectives: List[str] = Field(description="Key objectives for the project")
#     scope: str = Field(description="The scope of the project")

# class TargetAudience(BaseModel):
#     primary_audience: str = Field(description="Description of the primary target audience")
#     secondary_audience: Optional[str] = Field(description="Description of the secondary target audience if applicable")
#     user_characteristics: List[str] = Field(description="Key characteristics of the target users")
#     user_needs: List[str] = Field(description="Primary needs and goals of the target users")

# class Feature(BaseModel):
#     name: str = Field(description="Name of the feature")
#     description: str = Field(description="Description of what the feature does")
#     details: List[str] = Field(description="Detailed aspects of the feature")
#     priority: str = Field(description="Priority level (High, Medium, Low)")

# class TechStackItem(BaseModel):
#     category: str = Field(description="Category of technology (Frontend, Backend, Database, etc.)")
#     name: str = Field(description="Name of the technology")
#     description: str = Field(description="Description of the technology")
#     benefits: List[str] = Field(description="Benefits of using this technology for the project")
#     alternatives: Optional[List[str]] = Field(description="Alternative technologies that could be used instead")

# class ContentSection(BaseModel):
#     section_name: str = Field(description="Name of the content section")
#     description: str = Field(description="Description of the section's purpose")
#     content_elements: List[str] = Field(description="Elements to include in this section")
#     design_considerations: Optional[List[str]] = Field(description="Design considerations for this section")

# class ImplementationStep(BaseModel):
#     step_number: int = Field(description="Step number in the implementation sequence")
#     title: str = Field(description="Title of the implementation step")
#     description: str = Field(description="Detailed description of what this step involves")
#     estimated_time: Optional[str] = Field(description="Estimated time to complete this step")
#     dependencies: Optional[List[int]] = Field(description="Step numbers that must be completed before this step")

# class DeploymentStrategy(BaseModel):
#     hosting_recommendation: str = Field(description="Recommended hosting solution")
#     deployment_steps: List[str] = Field(description="Steps to deploy the project")
#     scaling_considerations: List[str] = Field(description="Considerations for scaling the project")
#     maintenance_plan: Optional[str] = Field(description="Recommended maintenance plan")

# class ProjectDocumentation(BaseModel):
#     project_summary: ProjectSummary = Field(description="Summary of the project")
#     target_audience: TargetAudience = Field(description="Target audience analysis")
#     features: List[Feature] = Field(description="List of project features")
#     tech_stack: List[TechStackItem] = Field(description="Recommended technology stack")
#     content_structure: List[ContentSection] = Field(description="Content structure for the project")
#     implementation_plan: List[ImplementationStep] = Field(description="Implementation plan with steps")
#     deployment_strategy: DeploymentStrategy = Field(description="Deployment strategy recommendations")

# class DocumentationGenerator:
#     """
#     Generates comprehensive project documentation from a simple prompt.
#     Uses a multi-step prompting strategy with OpenAIs GPT-4.
#     """
    
#     def __init__(self, api_key: Optional[str] = None):
        
#         # Initialize the DocumentationGenerator.
        
#         # Args:
#         #     api_key: OpenAI API key (optional, will use environment variable if not provided)
        
#         if api_key:
#             self.client = OpenAI(api_key=api_key)
#         else:
#             self.client = client
        
#         # Initialize parsers
#         self.project_summary_parser = PydanticOutputParser(pydantic_object=ProjectSummary)
#         self.target_audience_parser = PydanticOutputParser(pydantic_object=TargetAudience)
#         self.features_parser = PydanticOutputParser(pydantic_object=Feature)
#         self.tech_stack_parser = PydanticOutputParser(pydantic_object=TechStackItem)
#         self.content_structure_parser = PydanticOutputParser(pydantic_object=ContentSection)
#         self.implementation_plan_parser = PydanticOutputParser(pydantic_object=ImplementationStep)
#         self.deployment_strategy_parser = PydanticOutputParser(pydantic_object=DeploymentStrategy)
        
#         # Initialize prompt templates
#         self._initialize_prompts()
    
#     def _initialize_prompts(self):
#         """Initialize all prompt templates for different documentation sections."""
        
#         # Initial analysis prompt
#         self.initial_analysis_prompt = PromptTemplate(
#             template="""
#             You are an expert system analyst and technical documentation specialist.
#             Analyze the following project description and extract key information.
            
#             Project Description: {project_description}
            
#             Based on this description, provide a comprehensive analysis including:
#             1. Project type and category
#             2. Core purpose and objectives
#             3. Key features and requirements
#             4. Target audience and user needs
#             5. Technical considerations
            
#             Your analysis will be used to generate detailed documentation.
#             """,
#             input_variables=["project_description"]
#         )
        
#         # Project summary prompt
#         self.project_summary_prompt = PromptTemplate(
#             template="""
#             You are an expert system analyst and technical documentation specialist.
#             Create a comprehensive project summary based on the following project description.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
            
#             {format_instructions}
#             """,
#             input_variables=["project_description", "initial_analysis"],
#             partial_variables={"format_instructions": self.project_summary_parser.get_format_instructions()}
#         )
        
#         # Target audience prompt
#         self.target_audience_prompt = PromptTemplate(
#             template="""
#             You are an expert user researcher and market analyst.
#             Define the target audience for the following project.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
            
#             {format_instructions}
#             """,
#             input_variables=["project_description", "initial_analysis"],
#             partial_variables={"format_instructions": self.target_audience_parser.get_format_instructions()}
#         )
        
#         # Features prompt
#         self.features_prompt = PromptTemplate(
#             template="""
#             You are an expert product manager and feature analyst.
#             Define the key features for the following project.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
            
#             Create a comprehensive list of features that would be required for this project.
#             For each feature, provide a name, description, detailed aspects, and priority level.
            
#             {format_instructions}
            
#             Return a list of features in JSON format.
#             """,
#             input_variables=["project_description", "initial_analysis"],
#             partial_variables={"format_instructions": self.features_parser.get_format_instructions()}
#         )
        
#         # Tech stack prompt
#         self.tech_stack_prompt = PromptTemplate(
#             template="""
#             You are an expert software architect with deep knowledge of modern technology stacks.
#             Recommend an appropriate technology stack for the following project.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
#             Features: {features}
            
#             Consider the project requirements, scalability needs, and modern best practices.
#             For each technology recommendation, provide the category, name, description, benefits, and alternatives.
            
#             {format_instructions}
            
#             Return a list of technology recommendations in JSON format.
#             """,
#             input_variables=["project_description", "initial_analysis", "features"],
#             partial_variables={"format_instructions": self.tech_stack_parser.get_format_instructions()}
#         )
        
#         # Content structure prompt
#         self.content_structure_prompt = PromptTemplate(
#             template="""
#             You are an expert UX designer and content strategist.
#             Define the content structure for the following project.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
#             Features: {features}
            
#             Create a comprehensive content structure that outlines all the sections needed for this project.
#             For each section, provide a name, description, content elements, and design considerations.
            
#             {format_instructions}
            
#             Return a list of content sections in JSON format.
#             """,
#             input_variables=["project_description", "initial_analysis", "features"],
#             partial_variables={"format_instructions": self.content_structure_parser.get_format_instructions()}
#         )
        
#         # Implementation plan prompt
#         self.implementation_plan_prompt = PromptTemplate(
#             template="""
#             You are an expert project manager and technical lead.
#             Create an implementation plan for the following project.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
#             Features: {features}
#             Tech Stack: {tech_stack}
            
#             Create a step-by-step implementation plan that outlines how to build this project.
#             For each step, provide a step number, title, description, estimated time, and dependencies.
            
#             {format_instructions}
            
#             Return a list of implementation steps in JSON format.
#             """,
#             input_variables=["project_description", "initial_analysis", "features", "tech_stack"],
#             partial_variables={"format_instructions": self.implementation_plan_parser.get_format_instructions()}
#         )
        
#         # Deployment strategy prompt
#         self.deployment_strategy_prompt = PromptTemplate(
#             template="""
#             You are an expert DevOps engineer and deployment strategist.
#             Create a deployment strategy for the following project.
            
#             Project Description: {project_description}
#             Initial Analysis: {initial_analysis}
#             Tech Stack: {tech_stack}
            
#             Create a comprehensive deployment strategy that outlines how to deploy this project.
#             Include hosting recommendations, deployment steps, scaling considerations, and a maintenance plan.
            
#             {format_instructions}
#             """,
#             input_variables=["project_description", "initial_analysis", "tech_stack"],
#             partial_variables={"format_instructions": self.deployment_strategy_parser.get_format_instructions()}
#         )
    
#     def _call_openai_api(self, prompt: str, model: str = "gpt-4") -> str:
#         """
#         Call the OpenAI API with the given prompt.
        
#         Args:
#             prompt: The prompt to send to the API
#             model: The model to use (default: gpt-4)
            
#         Returns:
#             The API response text
#         """
#         try:
#             response = self.client.chat.completions.create(
#                 model=model,
#                 messages=[
#                     {"role": "system", "content": "You are an expert system analyst and technical documentation specialist."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=2000
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             print(f"Error calling OpenAI API: {e}")
#             return f"Error: {e}"
    
#     def _parse_json_response(self, response: str) -> Dict:
#         """
#         Parse a JSON response from the API.
        
#         Args:
#             response: The API response text
            
#         Returns:
#             The parsed JSON object
#         """
#         try:
#             # Extract JSON from the response (handling cases where there might be markdown or other text)
#             json_str = response
#             if "```json" in response:
#                 json_str = response.split("```json")[1].split("```")[0].strip()
#             elif "```" in response:
#                 json_str = response.split("```")[1].split("```")[0].strip()
            
#             return json.loads(json_str)
#         except Exception as e:
#             print(f"Error parsing JSON response: {e}")
#             print(f"Response: {response}")
#             return {"error": str(e)}
    
#     def generate_documentation(self, project_description: str) -> Dict[str, Any]:
#         """
#         Generate comprehensive documentation from a project description.
        
#         Args:
#             project_description: A simple description of the project
            
#         Returns:
#             A structured documentation object with all sections
#         """
#         try:
#             # Step 1: Initial analysis
#             initial_analysis_prompt = self.initial_analysis_prompt.format(
#                 project_description=project_description
#             )
#             initial_analysis = self._call_openai_api(initial_analysis_prompt)
            
#             # Step 2: Generate project summary
#             project_summary_prompt = self.project_summary_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis
#             )
#             project_summary_response = self._call_openai_api(project_summary_prompt)
#             project_summary = self._parse_json_response(project_summary_response)
            
#             # Step 3: Generate target audience
#             target_audience_prompt = self.target_audience_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis
#             )
#             target_audience_response = self._call_openai_api(target_audience_prompt)
#             target_audience = self._parse_json_response(target_audience_response)
            
#             # Step 4: Generate features
#             features_prompt = self.features_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis
#             )
#             features_response = self._call_openai_api(features_prompt)
#             features_json = self._parse_json_response(features_response)
            
#             # Handle both single feature and list of features
#             if isinstance(features_json, dict) and "name" in features_json:
#                 features = [features_json]
#             else:
#                 features = features_json
            
#             # Step 5: Generate tech stack
#             tech_stack_prompt = self.tech_stack_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis,
#                 features=json.dumps(features)
#             )
#             tech_stack_response = self._call_openai_api(tech_stack_prompt)
#             tech_stack_json = self._parse_json_response(tech_stack_response)
            
#             # Handle both single tech item and list of tech items
#             if isinstance(tech_stack_json, dict) and "category" in tech_stack_json:
#                 tech_stack = [tech_stack_json]
#             else:
#                 tech_stack = tech_stack_json
            
#             # Step 6: Generate content structure
#             content_structure_prompt = self.content_structure_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis,
#                 features=json.dumps(features)
#             )
#             content_structure_response = self._call_openai_api(content_structure_prompt)
#             content_structure_json = self._parse_json_response(content_structure_response)
            
#             # Handle both single content section and list of content sections
#             if isinstance(content_structure_json, dict) and "section_name" in content_structure_json:
#                 content_structure = [content_structure_json]
#             else:
#                 content_structure = content_structure_json
            
#             # Step 7: Generate implementation plan
#             implementation_plan_prompt = self.implementation_plan_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis,
#                 features=json.dumps(features),
#                 tech_stack=json.dumps(tech_stack)
#             )
#             implementation_plan_response = self._call_openai_api(implementation_plan_prompt)
#             implementation_plan_json = self._parse_json_response(implementation_plan_response)
            
#             # Handle both single implementation step and list of implementation steps
#             if isinstance(implementation_plan_json, dict) and "step_number" in implementation_plan_json:
#                 implementation_plan = [implementation_plan_json]
#             else:
#                 implementation_plan = implementation_plan_json
            
#             # Step 8: Generate deployment strategy
#             deployment_strategy_prompt = self.deployment_strategy_prompt.format(
#                 project_description=project_description,
#                 initial_analysis=initial_analysis,
#                 tech_stack=json.dumps(tech_stack)
#             )
#             deployment_strategy_response = self._call_openai_api(deployment_strategy_prompt)
#             deployment_strategy = self._parse_json_response(deployment_strategy_response)
            
#             # Assemble the complete documentation
#             documentation = {
#                 "project_summary": project_summary,
#                 "target_audience": target_audience,
#                 "features": features,
#                 "tech_stack": tech_stack,
#                 "content_structure": content_structure,
#                 "implementation_plan": implementation_plan,
#                 "deployment_strategy": deployment_strategy
#             }
            
#             return documentation
        
#         except Exception as e:
#             print(f"Error generating documentation: {e}")
#             return {"error": str(e)}

# # Example usage
# if __name__ == "__main__":
#     # This is just for demonstration purposes
#     generator = DocumentationGenerator()
#     documentation = generator.generate_documentation(
#         "a portfolio website with a contact form and Instagram feed"
#     )
#     print(json.dumps(documentation, indent=2))

"""
Template-based Documentation Generator

This module generates documentation based on templates rather than using OpenAI.
"""

class DocumentationGenerator:
    """
    Generates documentation based on user prompts using templates.
    """
    
    def __init__(self):
        """Initialize the documentation generator"""
        # Define templates for different project types
        self.templates = {
            "portfolio": self._portfolio_template,
            "ecommerce": self._ecommerce_template,
            "blog": self._blog_template,
            "social": self._social_media_template,
            "default": self._default_template
        }
    
    def generate_documentation(self, prompt):
        """
        Generate documentation based on the user prompt.
        
        Args:
            prompt: The user's project description
            
        Returns:
            A structured documentation object
        """
        # Determine project type based on keywords in the prompt
        project_type = self._determine_project_type(prompt)
        
        # Generate documentation using the appropriate template
        return self.templates[project_type](prompt)
    
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
            return "default"
    
    def _portfolio_template(self, prompt):
        """Generate documentation for a portfolio website"""
        return {
            "project_summary": {
                "title": "Portfolio Website",
                "description": "A professional portfolio website to showcase work and allow potential clients to make contact.",
                "objectives": [
                    "Showcase professional work and projects",
                    "Provide information about skills and experience",
                    "Allow visitors to contact for inquiries",
                    "Present a professional online presence"
                ],
                "scope": "Personal portfolio website focused on visual presentation and contact capabilities"
            },
            "target_audience": {
                "primary_audience": "Potential clients and employers",
                "secondary_audience": "Fellow professionals and collaborators",
                "user_characteristics": [
                    "Seeking professional services or talent",
                    "Interested in reviewing past work and experience",
                    "Likely to make decisions based on visual presentation",
                    "Looking for contact information"
                ],
                "user_needs": [
                    "Easy navigation to view portfolio items",
                    "Clear information about skills and services",
                    "Simple contact methods",
                    "Professional presentation that reflects quality of work"
                ]
            },
            "features": [
                {
                    "name": "Portfolio Gallery",
                    "description": "A visual display of work samples and projects",
                    "priority": "High",
                    "details": [
                        "Grid layout with filtering options",
                        "Project detail pages for expanded information",
                        "Image gallery with lightbox functionality",
                        "Project categories and tags"
                    ]
                },
                {
                    "name": "About Section",
                    "description": "Information about professional background and skills",
                    "priority": "High",
                    "details": [
                        "Professional bio",
                        "Skills and expertise listing",
                        "Experience timeline",
                        "Education and certifications"
                    ]
                },
                {
                    "name": "Contact Form",
                    "description": "Form for visitors to send messages and inquiries",
                    "priority": "High",
                    "details": [
                        "Name, email, and message fields",
                        "Form validation",
                        "Email notification system",
                        "Anti-spam protection"
                    ]
                },
                {
                    "name": "Social Media Integration",
                    "description": "Integration with social profiles and content",
                    "priority": "Medium",
                    "details": [
                        "Social media profile links",
                        "Social sharing buttons",
                        "Instagram feed display (if mentioned in prompt)"
                    ]
                },
                {
                    "name": "Responsive Design",
                    "description": "Optimal viewing experience across devices",
                    "priority": "High",
                    "details": [
                        "Mobile-first approach",
                        "Fluid layouts",
                        "Touch-friendly navigation",
                        "Performance optimization for mobile"
                    ]
                }
            ],
            "tech_stack": [
                {
                    "name": "React",
                    "category": "Frontend",
                    "description": "JavaScript library for building user interfaces",
                    "benefits": [
                        "Component-based architecture for reusability",
                        "Virtual DOM for performance",
                        "Rich ecosystem of libraries and tools",
                        "Strong developer community"
                    ],
                    "alternatives": ["Vue.js", "Angular", "Svelte"]
                },
                {
                    "name": "Next.js",
                    "category": "Frontend Framework",
                    "description": "React framework for production-grade websites",
                    "benefits": [
                        "Server-side rendering for better SEO",
                        "Automatic code splitting",
                        "Built-in routing system",
                        "Image optimization"
                    ],
                    "alternatives": ["Gatsby", "Create React App", "Remix"]
                },
                {
                    "name": "Tailwind CSS",
                    "category": "CSS Framework",
                    "description": "Utility-first CSS framework",
                    "benefits": [
                        "Rapid UI development",
                        "Highly customizable design system",
                        "Minimal CSS output",
                        "Responsive utilities built-in"
                    ],
                    "alternatives": ["Bootstrap", "Material UI", "Styled Components"]
                },
                {
                    "name": "Node.js",
                    "category": "Backend",
                    "description": "JavaScript runtime for server-side code",
                    "benefits": [
                        "Same language for frontend and backend",
                        "Non-blocking I/O for performance",
                        "Large package ecosystem",
                        "Good for lightweight API services"
                    ],
                    "alternatives": ["Python/Django", "Ruby on Rails", "PHP/Laravel"]
                },
                {
                    "name": "Express",
                    "category": "Backend Framework",
                    "description": "Minimal web framework for Node.js",
                    "benefits": [
                        "Lightweight and flexible",
                        "Easy to set up routing",
                        "Middleware support",
                        "Good for API development"
                    ],
                    "alternatives": ["Fastify", "Koa", "NestJS"]
                }
            ],
            "content_structure": [
                {
                    "section_name": "Home",
                    "description": "Landing page with introduction and featured work",
                    "content_elements": [
                        "Hero section with professional photo and tagline",
                        "Brief introduction",
                        "Featured portfolio items",
                        "Call to action for contact"
                    ],
                    "design_considerations": [
                        "Visual impact is crucial",
                        "Clear navigation to other sections",
                        "Balanced content-to-whitespace ratio",
                        "Mobile-friendly hero section"
                    ]
                },
                {
                    "section_name": "Portfolio",
                    "description": "Comprehensive display of work and projects",
                    "content_elements": [
                        "Filterable gallery grid",
                        "Project thumbnails with hover effects",
                        "Category and tag filtering",
                        "Individual project pages with detailed information"
                    ],
                    "design_considerations": [
                        "Focus on visual presentation",
                        "Easy filtering and searching",
                        "Fast loading of images",
                        "Consistent project presentation"
                    ]
                },
                {
                    "section_name": "About",
                    "description": "Professional background and personal information",
                    "content_elements": [
                        "Professional biography",
                        "Skills and expertise",
                        "Experience timeline",
                        "Education and certifications",
                        "Personal interests (optional)"
                    ],
                    "design_considerations": [
                        "Professional yet personable tone",
                        "Visual representation of skills",
                        "Balance of text and visuals",
                        "Downloadable resume option"
                    ]
                },
                {
                    "section_name": "Contact",
                    "description": "Methods for visitors to get in touch",
                    "content_elements": [
                        "Contact form",
                        "Email and phone information",
                        "Social media links",
                        "Location information (if relevant)",
                        "Availability status (optional)"
                    ],
                    "design_considerations": [
                        "Simple and intuitive form",
                        "Clear call to action",
                        "Form validation feedback",
                        "Privacy policy for data collection"
                    ]
                }
            ],
            "implementation_plan": [
                {
                    "step_number": 1,
                    "title": "Project Setup",
                    "description": "Initialize the project repository and development environment",
                    "estimated_time": "1 day",
                    "dependencies": []
                },
                {
                    "step_number": 2,
                    "title": "Design System Implementation",
                    "description": "Set up the design system and core UI components",
                    "estimated_time": "2 days",
                    "dependencies": [1]
                },
                {
                    "step_number": 3,
                    "title": "Homepage Development",
                    "description": "Implement the homepage layout and components",
                    "estimated_time": "2 days",
                    "dependencies": [2]
                },
                {
                    "step_number": 4,
                    "title": "Portfolio Gallery Implementation",
                    "description": "Develop the portfolio grid and filtering system",
                    "estimated_time": "3 days",
                    "dependencies": [2]
                },
                {
                    "step_number": 5,
                    "title": "Project Detail Pages",
                    "description": "Create the detailed project view pages",
                    "estimated_time": "2 days",
                    "dependencies": [4]
                },
                {
                    "step_number": 6,
                    "title": "About Page Development",
                    "description": "Implement the about page with biography and skills",
                    "estimated_time": "2 days",
                    "dependencies": [2]
                },
                {
                    "step_number": 7,
                    "title": "Contact Form Implementation",
                    "description": "Develop the contact form with validation and submission",
                    "estimated_time": "2 days",
                    "dependencies": [2]
                },
                {
                    "step_number": 8,
                    "title": "Backend API Development",
                    "description": "Create the backend API for the contact form",
                    "estimated_time": "2 days",
                    "dependencies": [7]
                },
                {
                    "step_number": 9,
                    "title": "Social Media Integration",
                    "description": "Implement social media links and feeds",
                    "estimated_time": "1 day",
                    "dependencies": [3, 6]
                },
                {
                    "step_number": 10,
                    "title": "Testing and Bug Fixing",
                    "description": "Comprehensive testing and bug fixing",
                    "estimated_time": "2 days",
                    "dependencies": [5, 8, 9]
                },
                {
                    "step_number": 11,
                    "title": "Deployment",
                    "description": "Deploy the website to production",
                    "estimated_time": "1 day",
                    "dependencies": [10]
                }
            ],
            "deployment_strategy": {
                "hosting_recommendation": "Vercel for frontend, Heroku for backend API",
                "deployment_steps": [
                    "Set up version control with Git",
                    "Create accounts on Vercel and Heroku",
                    "Configure environment variables",
                    "Set up continuous deployment from Git repository",
                    "Configure custom domain and SSL"
                ],
                "scaling_considerations": [
                    "Use CDN for image hosting",
                    "Implement lazy loading for portfolio images",
                    "Setup caching for static content",
                    "Monitor API usage for backend scaling needs"
                ],
                "maintenance_plan": "Regular updates to dependencies, monthly content updates, weekly backups"
            }
        }
    
    def _ecommerce_template(self, prompt):
        """Generate documentation for an e-commerce website"""
        return {
            "project_summary": {
                "title": "E-commerce Website",
                "description": "An online store for selling products with secure payment processing and order management.",
                "objectives": [
                    "Sell products online to customers",
                    "Process payments securely",
                    "Manage inventory and orders",
                    "Provide excellent user experience across devices"
                ],
                "scope": "Full-featured e-commerce platform with product listings, shopping cart, secure checkout, and order management"
            },
            # Add other sections similar to the portfolio template
            # The content would be customized for e-commerce
            "features": [
                {
                    "name": "Product Catalog",
                    "description": "Comprehensive display of products with details",
                    "priority": "High",
                    "details": [
                        "Product listings with images and prices",
                        "Category and tag filtering",
                        "Search functionality",
                        "Product detail pages"
                    ]
                },
                {
                    "name": "Shopping Cart",
                    "description": "Functionality to add and manage products for purchase",
                    "priority": "High",
                    "details": [
                        "Add to cart functionality",
                        "Update quantities",
                        "Remove items",
                        "Cart persistence"
                    ]
                }
                # Add more features...
            ]
            # Add other sections...
        }
    
    def _blog_template(self, prompt):
        """Generate documentation for a blog website"""
        # Similar structure to other templates but with blog-specific content
        return {
            "project_summary": {
                "title": "Blog Website",
                "description": "A content-focused website for publishing articles and engaging with readers.",
                # Add more blog-specific content...
            }
        }
    
    def _social_media_template(self, prompt):
        """Generate documentation for a social media platform"""
        # Similar structure to other templates but with social media-specific content
        return {
            "project_summary": {
                "title": "Social Media Platform",
                "description": "A community platform for user interaction, content sharing, and social networking.",
                # Add more social media-specific content...
            }
        }
    
    def _default_template(self, prompt):
        """Generate documentation for a generic web application"""
        return {
            "project_summary": {
                "title": "Web Application",
                "description": "A comprehensive web application based on the user's requirements.",
                "objectives": [
                    "Create a user-friendly web application",
                    "Implement core functionality described in the prompt",
                    "Ensure responsive design for all devices",
                    "Provide a secure and scalable solution"
                ],
                "scope": "Web application with features as described in the prompt"
            },
            "target_audience": {
                "primary_audience": "General users interested in the application's functionality",
                "secondary_audience": "Administrators and content managers",
                "user_characteristics": [
                    "Varied technical expertise",
                    "Interest in the core functionality",
                    "Expectation of intuitive interface",
                    "Multiple device usage"
                ],
                "user_needs": [
                    "Easy access to core functionality",
                    "Clear navigation and user flow",
                    "Reliable performance",
                    "Security for user data"
                ]
            },
            # Add more generic sections...
            "features": [
                {
                    "name": "User Authentication",
                    "description": "Secure login and registration system",
                    "priority": "High",
                    "details": [
                        "User registration",
                        "Secure login",
                        "Password recovery",
                        "Profile management"
                    ]
                },
                {
                    "name": "Core Functionality",
                    "description": "Main features of the application",
                    "priority": "High",
                    "details": [
                        "Implementation of primary use cases",
                        "User interaction components",
                        "Data processing and display",
                        "Feedback mechanisms"
                    ]
                }
                # Add more generic features...
            ]
            # Add other sections...
        }