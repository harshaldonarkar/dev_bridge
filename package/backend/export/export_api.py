"""
Export API Module

This module provides API endpoints for exporting documentation to various formats.
It uses the ExportEngine to handle the actual export process.
"""

import os
import json
import tempfile
from flask import Flask, request, jsonify, send_file
from export_engine import ExportEngine

app = Flask(__name__)
export_engine = ExportEngine()

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """
    Export documentation to PDF format.
    
    Request body:
    {
        "documentation": {...}  # The documentation object
    }
    
    Returns:
        PDF file download
    """
    try:
        # Get documentation from request
        data = request.json
        if not data or 'documentation' not in data:
            return jsonify({'error': 'Missing documentation data'}), 400
        
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
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.unlink(pdf_path)

@app.route('/api/export/docx', methods=['POST'])
def export_docx():
    """
    Export documentation to DOCX format.
    
    Request body:
    {
        "documentation": {...}  # The documentation object
    }
    
    Returns:
        DOCX file download
    """
    try:
        # Get documentation from request
        data = request.json
        if not data or 'documentation' not in data:
            return jsonify({'error': 'Missing documentation data'}), 400
        
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
    finally:
        # Clean up temporary file
        if 'docx_path' in locals() and os.path.exists(docx_path):
            os.unlink(docx_path)

@app.route('/api/export/html', methods=['POST'])
def export_html():
    """
    Export documentation to HTML format.
    
    Request body:
    {
        "documentation": {...}  # The documentation object
    }
    
    Returns:
        HTML content
    """
    try:
        # Get documentation from request
        data = request.json
        if not data or 'documentation' not in data:
            return jsonify({'error': 'Missing documentation data'}), 400
        
        documentation = data['documentation']
        
        # Generate HTML
        html = export_engine._generate_html(documentation)
        
        # Return HTML content
        return jsonify({'html': html})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
