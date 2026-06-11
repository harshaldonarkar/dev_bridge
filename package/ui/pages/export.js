// pages/export.js - simplified version without original PDF export
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function Export() {
  const router = useRouter();
  const [documentation, setDocumentation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [exportSuccess, setExportSuccess] = useState(null);
  const [debugInfo, setDebugInfo] = useState(null);
  
  useEffect(() => {
    // Get the documentation from localStorage
    try {
      const savedDocumentation = localStorage.getItem('documentation');
      
      if (!savedDocumentation) {
        setError('No documentation found. Please generate documentation first.');
        return;
      }
      
      const parsed = JSON.parse(savedDocumentation);
      setDocumentation(parsed);
      console.log("Documentation loaded:", parsed.project_summary?.title);
    } catch (error) {
      console.error('Error loading documentation:', error);
      setError('Error loading documentation. Please regenerate documentation.');
    }
  }, []);
  
  // Handler for the simple PDF export using reportlab
  const handleSimplePdfExport = async () => {
    if (!documentation) {
      setError('No documentation to export.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setExportSuccess(null);
    setDebugInfo(null);
    
    try {
      const apiUrl = 'http://localhost:5001/api/export/simple-pdf';
      
      console.log('Exporting to simple PDF');
      setDebugInfo('Starting simple PDF export...');
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documentation }),
      });
      
      setDebugInfo(prev => `${prev}\nFetch completed with status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Export failed with status ${response.status}: ${errorText}`);
      }
      
      // Get the blob directly
      const blob = await response.blob();
      
      setDebugInfo(prev => 
        `${prev}\nBlob received: size=${blob.size}, type=${blob.type}`
      );
      
      if (blob.size === 0) {
        throw new Error('Received empty file from server');
      }
      
      // Create a download link
      const downloadUrl = window.URL.createObjectURL(blob);
      const filename = `${documentation.project_summary?.title || 'documentation'}.pdf`;
      
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      setTimeout(() => {
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(link);
      }, 100);
      
      setExportSuccess('Documentation exported successfully as PDF.');
    } catch (error) {
      console.error('Error exporting to PDF:', error);
      setError(`Error exporting to PDF: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Handler for DOCX export
  const handleDocxExport = async () => {
    if (!documentation) {
      setError('No documentation to export.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setExportSuccess(null);
    setDebugInfo(null);
    
    try {
      const apiUrl = 'http://localhost:5001/api/export/docx';
      
      console.log('Exporting to DOCX');
      setDebugInfo('Starting DOCX export...');
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documentation }),
      });
      
      setDebugInfo(prev => `${prev}\nFetch completed with status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Export failed with status ${response.status}: ${errorText}`);
      }
      
      // Get the blob directly
      const blob = await response.blob();
      
      setDebugInfo(prev => 
        `${prev}\nBlob received: size=${blob.size}, type=${blob.type}`
      );
      
      if (blob.size === 0) {
        throw new Error('Received empty file from server');
      }
      
      // Create a download link
      const downloadUrl = window.URL.createObjectURL(blob);
      const filename = `${documentation.project_summary?.title || 'documentation'}.docx`;
      
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      setTimeout(() => {
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(link);
      }, 100);
      
      setExportSuccess('Documentation exported successfully as DOCX.');
    } catch (error) {
      console.error('Error exporting to DOCX:', error);
      setError(`Error exporting to DOCX: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };
  
  // HTML export (client-side only)
  const handleHtmlExport = () => {
    if (!documentation) {
      setError('No documentation to export.');
      return;
    }
    
    try {
      // Generate a simple HTML representation
      const html = generateHtml(documentation);
      
      // Create a blob with the HTML content
      const blob = new Blob([html], { type: 'text/html' });
      const url = window.URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `${documentation.project_summary?.title || 'documentation'}.html`;
      document.body.appendChild(link);
      link.click();
      
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
      }, 100);
      
      setExportSuccess('Documentation exported successfully as HTML.');
    } catch (error) {
      console.error('Error exporting to HTML:', error);
      setError(`Error exporting to HTML: ${error.message}`);
    }
  };
  
  // Simple HTML generator function
  const generateHtml = (doc) => {
    return `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${doc.project_summary?.title || 'Project Documentation'}</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
          }
          h1, h2, h3 {
            color: #4f46e5;
          }
          .section {
            margin-bottom: 30px;
          }
          .feature, .tech-item {
            background-color: #f9fafb;
            border-left: 4px solid #4f46e5;
            padding: 15px;
            margin-bottom: 15px;
          }
        </style>
      </head>
      <body>
        <h1>${doc.project_summary?.title || 'Project Documentation'}</h1>
        
        <div class="section">
          <h2>Project Summary</h2>
          <p>${doc.project_summary?.description || ''}</p>
          <h3>Objectives</h3>
          <ul>
            ${(doc.project_summary?.objectives || []).map(obj => `<li>${obj}</li>`).join('')}
          </ul>
          <p><strong>Scope:</strong> ${doc.project_summary?.scope || ''}</p>
        </div>
        
        <div class="section">
          <h2>Features</h2>
          ${(doc.features || []).map(feature => `
            <div class="feature">
              <h3>${feature.name}</h3>
              <p>${feature.description}</p>
              <p><strong>Priority:</strong> ${feature.priority}</p>
              <h4>Details</h4>
              <ul>
                ${(feature.details || []).map(detail => `<li>${detail}</li>`).join('')}
              </ul>
            </div>
          `).join('')}
        </div>
        
        <!-- Add other sections as needed -->
        
        <footer>
          <p>Generated by DevBridge - AI-Powered Pre-Development Automation Platform</p>
        </footer>
      </body>
      </html>
    `;
  };
  
  return (
    <div>
      <header className="header">
        <div className="container header-container">
          <div className="logo">
            <i className="fas fa-bridge"></i> DevBridge
          </div>
          <nav className="nav">
            <Link href="/" className="nav-link">Home</Link>
            <Link href="/documentation" className="nav-link">Documentation</Link>
            <Link href="/visualization" className="nav-link">Visualizations</Link>
            <Link href="/export" className="nav-link active">Export</Link>
            <Link href="/code" className="nav-link">Code Generation</Link>
            <Link href="#" className="nav-link">My Projects</Link>
          </nav>
        </div>
      </header>
      
      <section className="export-section">
        <div className="container">
          <div className="section-title">
            <h2>Export Options</h2>
            <p>Download your documentation in your preferred format</p>
          </div>
          
          {error && (
            <div style={{ 
              backgroundColor: '#fee2e2', 
              color: '#b91c1c', 
              padding: '1rem', 
              borderRadius: 'var(--radius-md)',
              marginBottom: '2rem',
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}
          
          {exportSuccess && (
            <div style={{ 
              backgroundColor: '#dcfce7', 
              color: '#166534', 
              padding: '1rem', 
              borderRadius: 'var(--radius-md)',
              marginBottom: '2rem',
              textAlign: 'center'
            }}>
              {exportSuccess}
            </div>
          )}
          
          {/* Debug information */}
          {debugInfo && (
            <div style={{ 
              backgroundColor: '#f3f4f6', 
              color: '#1f2937', 
              padding: '1rem', 
              borderRadius: 'var(--radius-md)',
              marginBottom: '2rem',
              fontFamily: 'monospace',
              whiteSpace: 'pre-wrap'
            }}>
              <h4>Debug Info:</h4>
              {debugInfo}
            </div>
          )}
          
          <div className="export-options">
            
            {/* DOCX export */}
            <div className="export-option">
              <div className="export-icon">
                <i className="fas fa-file-word"></i>
              </div>
              <h3 className="export-title">DOCX Export</h3>
              <p className="export-description">Editable document format for further customization</p>
              <button 
                className="btn btn-primary" 
                onClick={handleDocxExport}
                disabled={isLoading || !documentation}
              >
                {isLoading ? 'Exporting...' : 'Export as DOCX'}
              </button>
            </div>
            
            {/* HTML export (client-side) */}
            <div className="export-option">
              <div className="export-icon">
                <i className="fas fa-file-code"></i>
              </div>
              <h3 className="export-title">HTML Export</h3>
              <p className="export-description">Simple HTML document that works in any browser</p>
              <button 
                className="btn btn-primary" 
                onClick={handleHtmlExport}
                disabled={isLoading || !documentation}
              >
                Export as HTML
              </button>
            </div>
          </div>
          
          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <Link href="/documentation">
              <button className="btn btn-secondary">Back to Documentation</button>
            </Link>
          </div>
        </div>
      </section>
      
      <footer className="footer">
        <div className="container footer-container">
          <div>
            <div className="footer-logo">
              <i className="fas fa-bridge"></i> DevBridge
            </div>
            <p className="footer-description">Bridging the gap between concept and creation with AI-powered automation.</p>
          </div>
          <div>
            <h4 className="footer-heading">Product</h4>
            <div className="footer-links">
              <a href="#" className="footer-link">Features</a>
              <a href="#" className="footer-link">Pricing</a>
              <a href="#" className="footer-link">Documentation</a>
            </div>
          </div>
          <div>
            <h4 className="footer-heading">Resources</h4>
            <div className="footer-links">
              <a href="#" className="footer-link">Blog</a>
              <a href="#" className="footer-link">Tutorials</a>
              <a href="#" className="footer-link">Support</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 DevBridge. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}