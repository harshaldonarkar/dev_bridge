"""
Template-based Documentation Generator

This module generates documentation based on templates.
"""

class TemplateDocumentationGenerator:
    """
    Generates documentation based on templates.
    """
    
    def __init__(self):
        """Initialize the documentation generator"""
        # Define templates for different project types
        self.templates = {
            "portfolio": self._portfolio_template,
            "ecommerce": self._ecommerce_template,
            "blog": self._blog_template,
            "social": self._social_media_template,
            "web application": self._default_template
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
    
    def get_template_for_type(self, project_type):
        """
        Get the template for a specific project type.
        
        Args:
            project_type: The type of project
            
        Returns:
            The template documentation
        """
        if project_type in self.templates:
            return self.templates[project_type]("")
        return self.templates["web application"]("")
    
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
        # Implement similar to portfolio template but with e-commerce specifics
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
            # Add similar sections to portfolio template
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
                }
                # Add more features
            ]
            # Add other sections
        }
    
    def _blog_template(self, prompt):
        """Generate documentation for a blog website"""
        # Implement similar to portfolio template but with blog specifics
        return {
            "project_summary": {
                "title": "Blog Website",
                "description": "A content-focused website for publishing articles and engaging with readers.",
                "objectives": [
                    "Publish and manage blog content",
                    "Engage with readers through comments",
                    "Build an audience through subscriptions",
                    "Showcase writing and expertise"
                ],
                "scope": "Content management system with blogging features, comments, and subscription options"
            }
            # Add other sections
        }
    
    def _social_media_template(self, prompt):
        """Generate documentation for a social media platform"""
        # Implement similar to portfolio template but with social media specifics
        return {
            "project_summary": {
                "title": "Social Media Platform",
                "description": "A community platform for user interaction, content sharing, and social networking.",
                "objectives": [
                    "Enable users to create profiles and connect",
                    "Allow content sharing and interaction",
                    "Provide messaging and communication features",
                    "Create engagement through notifications and feeds"
                ],
                "scope": "Social networking platform with user profiles, content sharing, and interactive features"
            }
            # Add other sections
        }
    
    def _default_template(self, prompt):
        """Generate documentation for a generic web application"""
        # Implement generic web application template
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
            }
            # Add other sections
        }