"""
Test Cases for AI-Powered Pre-Development Automation Platform

This file contains test cases to verify the functionality of the platform components.
"""

import unittest
import json
import os
import sys
import tempfile

# Add project directory to path
sys.path.append('/home/ubuntu/project')

# Import components to test
from backend.documentation_generator import DocumentationGenerator
from backend.export.export_engine import ExportEngine
from backend.code_generation.code_generation_architecture import CodeGenerationOrchestrator
from backend.code_generation.frontend_generator import ReactNextGenerator
from backend.code_generation.backend_generator import NodeExpressGenerator
from backend.code_generation.ai_agent_generator import OpenAIAgentGenerator

class TestDocumentationGenerator(unittest.TestCase):
    """Test cases for the DocumentationGenerator component."""
    
    def setUp(self):
        """Set up test environment."""
        self.generator = DocumentationGenerator()
        self.sample_prompt = "Create a portfolio website with a contact form and Instagram feed"
    
    def test_generate_documentation_structure(self):
        """Test that documentation has the correct structure."""
        # Note: This is a mock test since we can't actually call the OpenAI API
        # In a real test, we would use a mock for the API calls
        
        # Create a sample documentation result
        documentation = {
            "project_summary": {
                "title": "Portfolio Website",
                "description": "A professional portfolio website with contact form and Instagram integration",
                "objectives": ["Showcase work", "Allow visitors to contact", "Display Instagram feed"],
                "scope": "Personal portfolio website for a photographer"
            },
            "target_audience": {
                "primary_audience": "Potential clients",
                "secondary_audience": "Photography enthusiasts",
                "user_characteristics": ["Interested in photography", "Looking for professional services"],
                "user_needs": ["View portfolio", "Contact the photographer", "See recent work"]
            },
            "features": [
                {
                    "name": "Portfolio Gallery",
                    "description": "Display photography work in a grid layout",
                    "priority": "High",
                    "details": ["Filterable by category", "Lightbox for full-size viewing"]
                },
                {
                    "name": "Contact Form",
                    "description": "Allow visitors to send messages",
                    "priority": "High",
                    "details": ["Name, email, and message fields", "Form validation", "Email notification"]
                },
                {
                    "name": "Instagram Feed",
                    "description": "Display recent Instagram posts",
                    "priority": "Medium",
                    "details": ["Show latest 6 posts", "Link to Instagram profile"]
                }
            ],
            "tech_stack": [
                {
                    "name": "React",
                    "category": "Frontend",
                    "description": "JavaScript library for building user interfaces",
                    "benefits": ["Component-based architecture", "Virtual DOM for performance"],
                    "alternatives": ["Vue.js", "Angular"]
                },
                {
                    "name": "Node.js",
                    "category": "Backend",
                    "description": "JavaScript runtime for server-side code",
                    "benefits": ["Same language as frontend", "Large ecosystem"],
                    "alternatives": ["Python/Django", "PHP/Laravel"]
                }
            ],
            "content_structure": [
                {
                    "section_name": "Home",
                    "description": "Landing page with hero section",
                    "content_elements": ["Hero image with tagline", "Brief introduction", "Featured work samples"],
                    "design_considerations": ["Minimalist design", "Focus on imagery"]
                },
                {
                    "section_name": "Portfolio",
                    "description": "Gallery of photography work",
                    "content_elements": ["Filterable gallery", "Project descriptions"],
                    "design_considerations": ["Grid layout", "Minimal text"]
                },
                {
                    "section_name": "Contact",
                    "description": "Contact form and information",
                    "content_elements": ["Contact form", "Email and phone", "Social media links"],
                    "design_considerations": ["Clear call to action", "Simple form design"]
                }
            ]
        }
        
        # Verify documentation structure
        self.assertIn("project_summary", documentation)
        self.assertIn("target_audience", documentation)
        self.assertIn("features", documentation)
        self.assertIn("tech_stack", documentation)
        self.assertIn("content_structure", documentation)
        
        # Verify project summary
        self.assertIn("title", documentation["project_summary"])
        self.assertIn("description", documentation["project_summary"])
        self.assertIn("objectives", documentation["project_summary"])
        
        # Verify features
        self.assertTrue(len(documentation["features"]) >= 1)
        feature = documentation["features"][0]
        self.assertIn("name", feature)
        self.assertIn("description", feature)
        self.assertIn("priority", feature)
        self.assertIn("details", feature)
        
        # Verify tech stack
        self.assertTrue(len(documentation["tech_stack"]) >= 1)
        tech = documentation["tech_stack"][0]
        self.assertIn("name", tech)
        self.assertIn("category", tech)
        self.assertIn("description", tech)
        self.assertIn("benefits", tech)
        
        # Verify content structure
        self.assertTrue(len(documentation["content_structure"]) >= 1)
        section = documentation["content_structure"][0]
        self.assertIn("section_name", section)
        self.assertIn("description", section)
        self.assertIn("content_elements", section)

class TestExportEngine(unittest.TestCase):
    """Test cases for the ExportEngine component."""
    
    def setUp(self):
        """Set up test environment."""
        self.export_engine = ExportEngine()
        
        # Sample documentation for testing
        self.documentation = {
            "project_summary": {
                "title": "Test Project",
                "description": "A test project for unit testing",
                "objectives": ["Test objective 1", "Test objective 2"],
                "scope": "Limited scope for testing"
            },
            "target_audience": {
                "primary_audience": "Testers",
                "user_characteristics": ["Technical knowledge", "Attention to detail"],
                "user_needs": ["Verify functionality", "Ensure quality"]
            },
            "features": [
                {
                    "name": "Test Feature",
                    "description": "A feature for testing",
                    "priority": "High",
                    "details": ["Detail 1", "Detail 2"]
                }
            ],
            "tech_stack": [
                {
                    "name": "Test Tech",
                    "category": "Testing",
                    "description": "A technology for testing",
                    "benefits": ["Benefit 1", "Benefit 2"]
                }
            ],
            "content_structure": [
                {
                    "section_name": "Test Section",
                    "description": "A section for testing",
                    "content_elements": ["Element 1", "Element 2"]
                }
            ],
            "implementation_plan": [
                {
                    "step_number": 1,
                    "title": "Test Step",
                    "description": "A step for testing",
                    "estimated_time": "1 day"
                }
            ],
            "deployment_strategy": {
                "hosting_recommendation": "Test Hosting",
                "deployment_steps": ["Step 1", "Step 2"],
                "scaling_considerations": ["Consideration 1", "Consideration 2"]
            }
        }
    
    def test_generate_html(self):
        """Test HTML generation from documentation."""
        html = self.export_engine._generate_html(self.documentation)
        
        # Verify HTML contains key elements
        self.assertIn("<html", html)
        self.assertIn("</html>", html)
        self.assertIn(self.documentation["project_summary"]["title"], html)
        self.assertIn(self.documentation["project_summary"]["description"], html)
        self.assertIn(self.documentation["features"][0]["name"], html)
        self.assertIn(self.documentation["tech_stack"][0]["name"], html)
    
    def test_export_to_pdf(self):
        """Test PDF export functionality."""
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            pdf_path = temp_file.name
        
        try:
            # This test will be skipped in environments without wkhtmltopdf
            # In a real test environment, we would ensure wkhtmltopdf is installed
            if os.path.exists('/usr/bin/wkhtmltopdf'):
                result_path = self.export_engine.export_to_pdf(self.documentation, pdf_path)
                
                # Verify PDF was created
                self.assertTrue(os.path.exists(result_path))
                self.assertTrue(os.path.getsize(result_path) > 0)
            else:
                print("Skipping PDF export test: wkhtmltopdf not found")
        finally:
            # Clean up
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
    
    def test_export_to_docx(self):
        """Test DOCX export functionality."""
        # Create a temporary file for the DOCX
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            docx_path = temp_file.name
        
        try:
            result_path = self.export_engine.export_to_docx(self.documentation, docx_path)
            
            # Verify DOCX was created
            self.assertTrue(os.path.exists(result_path))
            self.assertTrue(os.path.getsize(result_path) > 0)
        finally:
            # Clean up
            if os.path.exists(docx_path):
                os.unlink(docx_path)

class TestCodeGeneration(unittest.TestCase):
    """Test cases for the code generation components."""
    
    def setUp(self):
        """Set up test environment."""
        # Sample documentation for testing
        self.documentation = {
            "project_summary": {
                "title": "Test Project",
                "description": "A test project for unit testing",
                "objectives": ["Test objective 1", "Test objective 2"],
                "scope": "Limited scope for testing"
            },
            "features": [
                {
                    "name": "User Authentication",
                    "description": "Allow users to register and login",
                    "priority": "High",
                    "details": ["Registration form", "Login form", "Password reset"]
                },
                {
                    "name": "Profile Management",
                    "description": "Allow users to manage their profiles",
                    "priority": "Medium",
                    "details": ["Edit profile", "Change password", "Delete account"]
                }
            ],
            "tech_stack": [
                {
                    "name": "React",
                    "category": "Frontend",
                    "description": "JavaScript library for building user interfaces",
                    "benefits": ["Component-based", "Virtual DOM"]
                },
                {
                    "name": "Node.js",
                    "category": "Backend",
                    "description": "JavaScript runtime for server-side code",
                    "benefits": ["Non-blocking I/O", "Same language as frontend"]
                },
                {
                    "name": "MongoDB",
                    "category": "Database",
                    "description": "NoSQL database",
                    "benefits": ["Flexible schema", "JSON-like documents"]
                }
            ],
            "content_structure": [
                {
                    "section_name": "Home",
                    "description": "Landing page",
                    "content_elements": ["Hero section", "Features overview"]
                },
                {
                    "section_name": "Dashboard",
                    "description": "User dashboard",
                    "content_elements": ["User stats", "Recent activity"]
                }
            ]
        }
        
        # Initialize generators
        self.frontend_generator = ReactNextGenerator()
        self.backend_generator = NodeExpressGenerator()
        self.ai_agent_generator = OpenAIAgentGenerator()
        self.orchestrator = CodeGenerationOrchestrator()
    
    def test_frontend_generator(self):
        """Test frontend code generation."""
        # Create a temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate frontend code
            output_path = self.frontend_generator.generate_code(self.documentation, temp_dir)
            
            # Verify output is a zip file
            self.assertTrue(output_path.endswith('.zip'))
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Verify key files were generated
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'package.json')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'pages', 'index.js')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'components', 'Layout.js')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'styles', 'globals.css')))
    
    def test_backend_generator(self):
        """Test backend code generation."""
        # Create a temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate backend code
            output_path = self.backend_generator.generate_code(self.documentation, temp_dir)
            
            # Verify output is a zip file
            self.assertTrue(output_path.endswith('.zip'))
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Verify key files were generated
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'package.json')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'server.js')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'routes', 'index.js')))
            
            # Verify feature-specific files were generated
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'models', 'userauthentication.js')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'controllers', 'userauthenticationController.js')))
    
    def test_ai_agent_generator(self):
        """Test AI agent code generation."""
        # Create a temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate AI agent code
            output_path = self.ai_agent_generator.generate_code(self.documentation, temp_dir)
            
            # Verify output is a zip file
            self.assertTrue(output_path.endswith('.zip'))
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Verify key files were generated
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'package.json')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'agent.js')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'prompts', 'system_prompt.txt')))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'agent_definition.json')))
    
    def test_orchestrator(self):
        """Test code generation orchestration."""
        # Register generators with orchestrator
        self.orchestrator.register_generator('frontend', self.frontend_generator)
        self.orchestrator.register_generator('backend', self.backend_generator)
        self.orchestrator.register_generator('ai_agent', self.ai_agent_generator)
        
        # Create a temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set output directory in generators
            self.frontend_generator._create_package = lambda src, dst: os.path.join(temp_dir, 'frontend.zip')
            self.backend_generator._create_package = lambda src, dst: os.path.join(temp_dir, 'backend.zip')
            self.ai_agent_generator._create_package = lambda src, dst: os.path.join(temp_dir, 'ai_agent.zip')
            
            # Generate code using orchestrator
            results = self.orchestrator.generate_code(self.documentation, ['frontend', 'backend', 'ai_agent'])
            
            # Verify results contain expected keys
            self.assertIn('frontend', results)
            self.assertIn('backend', results)
            self.assertIn('ai_agent', results)
            
            # Verify paths are correct
            self.assertEqual(results['frontend'], os.path.join(temp_dir, 'frontend.zip'))
            self.assertEqual(results['backend'], os.path.join(temp_dir, 'backend.zip'))
            self.assertEqual(results['ai_agent'], os.path.join(temp_dir, 'ai_agent.zip'))

class TestIntegration(unittest.TestCase):
    """Integration tests for the platform components."""
    
    def setUp(self):
        """Set up test environment."""
        # Sample prompt for testing
        self.prompt = "Create a portfolio website with a contact form and Instagram feed"
        
        # Initialize components
        self.documentation_generator = DocumentationGenerator()
        self.export_engine = ExportEngine()
        self.orchestrator = CodeGenerationOrchestrator()
        self.orchestrator.register_generator('frontend', ReactNextGenerator())
        self.orchestrator.register_generator('backend', NodeExpressGenerator())
        self.orchestrator.register_generator('ai_agent', OpenAIAgentGenerator())
        
        # Sample documentation for testing
        self.documentation = {
            "project_summary": {
                "title": "Portfolio Website",
                "description": "A professional portfolio website with contact form and Instagram integration",
                "objectives": ["Showcase work", "Allow visitors to contact", "Display Instagram feed"],
                "scope": "Personal portfolio website for a photographer"
            },
            "target_audience": {
                "primary_audience": "Potential clients",
                "secondary_audience": "Photography enthusiasts",
                "user_characteristics": ["Interested in photography", "Looking for professional services"],
                "user_needs": ["View portfolio", "Contact the photographer", "See recent work"]
            },
            "features": [
                {
                    "name": "Portfolio Gallery",
                    "description": "Display photography work in a grid layout",
                    "priority": "High",
                    "details": ["Filterable by category", "Lightbox for full-size viewing"]
                },
                {
                    "name": "Contact Form",
                    "description": "Allow visitors to send messages",
                    "priority": "High",
                    "details": ["Name, email, and message fields", "Form validation", "Email notification"]
                },
                {
                    "name": "Instagram Feed",
                    "description": "Display recent Instagram posts",
                    "priority": "Medium",
                    "details": ["Show latest 6 posts", "Link to Instagram profile"]
                }
            ],
            "tech_stack": [
                {
                    "name": "React",
                    "category": "Frontend",
                    "description": "JavaScript library for building user interfaces",
                    "benefits": ["Component-based architecture", "Virtual DOM for performance"],
                    "alternatives": ["Vue.js", "Angular"]
                },
                {
                    "name": "Node.js",
                    "category": "Backend",
                    "description": "JavaScript runtime for server-side code",
                    "benefits": ["Same language as frontend", "Large ecosystem"],
                    "alternatives": ["Python/Django", "PHP/Laravel"]
                },
                {
                    "name": "MongoDB",
                    "category": "Database",
                    "description": "NoSQL database for storing data",
                    "benefits": ["Flexible schema", "JSON-like documents"],
                    "alternatives": ["PostgreSQL", "MySQL"]
                }
            ],
            "content_structure": [
                {
                    "section_name": "Home",
                    "description": "Landing page with hero section",
                    "content_elements": ["Hero image with tagline", "Brief introduction", "Featured work samples"],
                    "design_considerations": ["Minimalist design", "Focus on imagery"]
                },
                {
                    "section_name": "Portfolio",
                    "description": "Gallery of photography work",
                    "content_elements": ["Filterable gallery", "Project descriptions"],
                    "design_considerations": ["Grid layout", "Minimal text"]
                },
                {
                    "section_name": "Contact",
                    "description": "Contact form and information",
                    "content_elements": ["Contact form", "Email and phone", "Social media links"],
                    "design_considerations": ["Clear call to action", "Simple form design"]
                }
            ],
            "implementation_plan": [
                {
                    "step_number": 1,
                    "title": "Setup project",
                    "description": "Initialize project and install dependencies",
                    "estimated_time": "1 day"
                },
                {
                    "step_number": 2,
                    "title": "Develop frontend",
                    "description": "Create React components and pages",
                    "estimated_time": "3 days"
                },
                {
                    "step_number": 3,
                    "title": "Develop backend",
                    "description": "Create API endpoints and database models",
                    "estimated_time": "2 days"
                },
                {
                    "step_number": 4,
                    "title": "Deploy",
                    "description": "Deploy to production environment",
                    "estimated_time": "1 day"
                }
            ],
            "deployment_strategy": {
                "hosting_recommendation": "Vercel for frontend, Heroku for backend",
                "deployment_steps": [
                    "Set up Git repository",
                    "Configure environment variables",
                    "Deploy frontend to Vercel",
                    "Deploy backend to Heroku",
                    "Connect frontend to backend API"
                ],
                "scaling_considerations": [
                    "Use CDN for image hosting",
                    "Implement caching for API responses",
                    "Monitor performance and adjust resources as needed"
                ],
                "maintenance_plan": "Regular updates and security patches, backup database weekly"
            }
        }
    
    def test_end_to_end_flow(self):
        """Test the end-to-end flow from prompt to code generation."""
        # Note: This is a mock test since we can't actually call the OpenAI API
        # In a real test, we would use a mock for the API calls
        
        # Step 1: Generate documentation (mocked)
        # documentation = self.documentation_generator.generate_documentation(self.prompt)
        documentation = self.documentation  # Use sample documentation
        
        # Verify documentation structure
        self.assertIn("project_summary", documentation)
        self.assertIn("features", documentation)
        self.assertIn("tech_stack", documentation)
        
        # Step 2: Export documentation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Export to HTML (via internal method)
            html = self.export_engine._generate_html(documentation)
            self.assertIn(documentation["project_summary"]["title"], html)
            
            # Export to DOCX
            docx_path = os.path.join(temp_dir, 'documentation.docx')
            result_docx = self.export_engine.export_to_docx(documentation, docx_path)
            self.assertTrue(os.path.exists(result_docx))
            
            # Step 3: Generate code
            # Set output directory in generators
            for generator_type in ['frontend', 'backend', 'ai_agent']:
                generator = self.orchestrator.generators.get(generator_type)
                if generator:
                    generator._create_package = lambda src, dst: os.path.join(temp_dir, f'{generator_type}.zip')
            
            # Generate code
            results = self.orchestrator.generate_code(documentation, ['frontend', 'backend'])
            
            # Verify results
            self.assertIn('frontend', results)
            self.assertIn('backend', results)
            self.assertEqual(results['frontend'], os.path.join(temp_dir, 'frontend.zip'))
            self.assertEqual(results['backend'], os.path.join(temp_dir, 'backend.zip'))

if __name__ == '__main__':
    unittest.main()
