"""
DevBridge Backend Server

This is the main application file for the DevBridge backend.
It sets up the Flask server and provides API endpoints for:
- Documentation generation
- Visualization generation
- Export functionality
- Code generation
"""

import os
import json
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Import components
from documentation_generator import DocumentationGenerator
from export.export_engine import ExportEngine
from code_generation.code_generation_architecture import CodeGenerationOrchestrator
from code_generation.frontend_generator import ReactNextGenerator
from code_generation.backend_generator import NodeExpressGenerator
from code_generation.ai_agent_generator import OpenAIAgentGenerator
from visualization.visualization_generator import VisualizationGenerator
from code_generation.gemini_code_generator import GeminiCodeGenerator
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
documentation_generator = DocumentationGenerator()
export_engine = ExportEngine()
code_orchestrator = CodeGenerationOrchestrator()
code_orchestrator.register_generator('frontend', ReactNextGenerator())
code_orchestrator.register_generator('backend', NodeExpressGenerator())
code_orchestrator.register_generator('ai_agent', OpenAIAgentGenerator())
code_orchestrator.register_generator('gemini', GeminiCodeGenerator())


@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "DevBridge API is running",
        "version": "1.0.0"
    })

@app.route('/api/generate-documentation', methods=['POST'])
def generate_documentation():
    """Generate documentation from a project prompt"""
    data = request.json
    
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Missing prompt parameter'}), 400
    
    try:
        # Generate documentation
        documentation = documentation_generator.generate_documentation(data['prompt'])
        return jsonify({
            'status': 'success',
            'documentation': documentation
        })
    except Exception as e:
        print(f"Error generating documentation: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-visualization', methods=['POST'])
def generate_visualization():
    """Generate visualization data from documentation"""
    data = request.json
    
    if not data or 'documentation' not in data:
        return jsonify({'error': 'Missing documentation parameter'}), 400
    
    try:
        # Generate visualization data
        visualization_data = VisualizationGenerator.generateVisualizations(data['documentation'])
        return jsonify({
            'status': 'success',
            'visualization': visualization_data
        })
    except Exception as e:
        print(f"Error generating visualization: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Export documentation to PDF format"""
    data = request.json
    
    if not data or 'documentation' not in data:
        return jsonify({'error': 'Missing documentation data'}), 400
    
    try:
        documentation = data['documentation']
        
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_path = temp_pdf.name
        
        # Export to PDF
        result_path = export_engine.export_to_pdf(documentation, pdf_path)
        
        if not result_path:
            return jsonify({'error': 'Failed to generate PDF'}), 500
        
        # Return PDF file
        return send_file(
            result_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{documentation.get('project_summary', {}).get('title', 'documentation').replace(' ', '_')}.pdf"
        )
    except Exception as e:
        print(f"Error exporting to PDF: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.unlink(pdf_path)
@app.route('/api/export/simple-pdf', methods=['POST'])
def export_simple_pdf():
    """Export documentation to a simple PDF format using reportlab"""
    data = request.json
    
    if not data or 'documentation' not in data:
        return jsonify({'error': 'Missing documentation data'}), 400
    
    try:
        documentation = data['documentation']
        
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_path = temp_pdf.name
        
        print(f"Created temporary file at {pdf_path}")
        
        # Export to simple PDF
        result_path = export_engine.export_to_simple_pdf(documentation, pdf_path)
        
        if not result_path:
            return jsonify({'error': 'Failed to generate PDF'}), 500
        
        print(f"PDF generated successfully at {result_path}, size: {os.path.getsize(result_path)} bytes")
        
        # Return PDF file
        response = send_file(
            result_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{documentation.get('project_summary', {}).get('title', 'documentation').replace(' ', '_')}.pdf"
        )
        
        return response
    except Exception as e:
        print(f"Error exporting to simple PDF: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file (after response is sent)
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            try:
                os.unlink(pdf_path)
                print(f"Temporary file {pdf_path} removed")
            except Exception as e:
                print(f"Error removing temporary file: {e}")
                
@app.route('/api/export/docx', methods=['POST'])
def export_docx():
    """Export documentation to DOCX format"""
    data = request.json
    
    if not data or 'documentation' not in data:
        return jsonify({'error': 'Missing documentation data'}), 400
    
    try:
        documentation = data['documentation']
        
        # Create temporary file for DOCX
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_docx:
            docx_path = temp_docx.name
        
        # Export to DOCX
        result_path = export_engine.export_to_docx(documentation, docx_path)
        
        if not result_path:
            return jsonify({'error': 'Failed to generate DOCX'}), 500
        
        # Return DOCX file
        return send_file(
            result_path,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f"{documentation.get('project_summary', {}).get('title', 'documentation').replace(' ', '_')}.docx"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    """Generate code based on documentation"""
    data = request.json
    
    if not data or 'documentation' not in data or 'type' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        documentation = data['documentation']
        code_type = data['type']  # 'frontend', 'backend', or 'ai_agent'
        
        # Create temporary directory for code generation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate code
            generator = code_orchestrator.generators.get(code_type)
            if not generator:
                return jsonify({'error': f'Invalid code type: {code_type}'}), 400
            
            output_path = generator.generate_code(documentation, temp_dir)
            
            # Return zip file
            return send_file(
                output_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f"{documentation.get('project_summary', {}).get('title', 'project').replace(' ', '_')}_{code_type}.zip"
            )
    except Exception as e:
        print(f"Error generating code: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)