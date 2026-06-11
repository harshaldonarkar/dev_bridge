// pages/code.js
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function CodeGeneration() {
  const router = useRouter();
  const [documentation, setDocumentation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [generationSuccess, setGenerationSuccess] = useState(null);
  const [codeType, setCodeType] = useState(null);
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
  
  const handleGenerateCode = async (type) => {
    if (!documentation) {
      setError('No documentation to generate code from.');
      return;
    }
    
    setCodeType(type);
    setIsLoading(true);
    setError(null);
    setGenerationSuccess(null);
    setDebugInfo(null);
    
    try {
      const apiUrl = 'http://localhost:5001/api/generate-code';
      
      console.log(`Generating ${type} code`);
      setDebugInfo(`Starting ${type} code generation...`);
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          documentation,
          type
        }),
      });
      
      setDebugInfo(prev => `${prev}\nFetch completed with status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Code generation failed with status ${response.status}: ${errorText}`);
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
      const filename = `${documentation.project_summary?.title || 'project'}_${type}.zip`;
      
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      setTimeout(() => {
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(link);
      }, 100);
      
      setGenerationSuccess(`${type.charAt(0).toUpperCase() + type.slice(1)} code generated successfully.`);
    } catch (error) {
      console.error(`Error generating ${type} code:`, error);
      setError(`Error generating ${type} code: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
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
            <Link href="/export" className="nav-link">Export</Link>
            <Link href="/code" className="nav-link">Code Generation</Link>
          </nav>
        </div>
      </header>
      
      <section className="code-section">
        <div className="container">
          <div className="section-title">
            <h2>Code Generation</h2>
            <p>Generate starter code based on your documentation</p>
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
          
          {generationSuccess && (
            <div style={{ 
              backgroundColor: '#dcfce7', 
              color: '#166534', 
              padding: '1rem', 
              borderRadius: 'var(--radius-md)',
              marginBottom: '2rem',
              textAlign: 'center'
            }}>
              {generationSuccess}
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
          
          <div className="code-options">
            {/* Frontend code */}
            <div className="code-option">
              <div className="code-icon">
                <i className="fas fa-desktop"></i>
              </div>
              <h3 className="code-title">Frontend Code</h3>
              <p className="code-description">Generate React/Next.js frontend code with components based on your documentation</p>
              <div className="code-features">
                <ul>
                  <li>React components for UI features</li>
                  <li>Next.js project structure</li>
                  <li>Responsive design with CSS</li>
                  <li>Page routing</li>
                </ul>
              </div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleGenerateCode('frontend')}
                disabled={isLoading || !documentation}
              >
                {isLoading && codeType === 'frontend' ? 'Generating...' : 'Generate Frontend Code'}
              </button>
            </div>
            
            {/* Backend code */}
            <div className="code-option">
              <div className="code-icon">
                <i className="fas fa-server"></i>
              </div>
              <h3 className="code-title">Backend Code</h3>
              <p className="code-description">Generate Node.js/Express backend with API endpoints based on your features</p>
              <div className="code-features">
                <ul>
                  <li>Express.js server setup</li>
                  <li>API routes based on features</li>
                  <li>Model definitions</li>
                  <li>Controller logic</li>
                </ul>
              </div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleGenerateCode('backend')}
                disabled={isLoading || !documentation}
              >
                {isLoading && codeType === 'backend' ? 'Generating...' : 'Generate Backend Code'}
              </button>
            </div>
            
            {/* AI Agent code */}
            <div className="code-option">
              <div className="code-icon">
                <i className="fas fa-robot"></i>
              </div>
              <h3 className="code-title">AI Agent</h3>
              <p className="code-description">Generate an OpenAI-powered AI agent based on your project</p>
              <div className="code-features">
                <ul>
                  <li>Project-specific AI assistant</li>
                  <li>Prompt templates</li>
                  <li>Function definitions</li>
                  <li>Integration API</li>
                </ul>
              </div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleGenerateCode('ai_agent')}
                disabled={isLoading || !documentation}
              >
                {isLoading && codeType === 'ai_agent' ? 'Generating...' : 'Generate AI Agent'}
              </button>
            </div>
          </div>
          {/* Gemini Code Generation */}
            <div className="code-option">
              <div className="code-icon">
                <i className="fas fa-magic"></i>
              </div>
              <h3 className="code-title">Gemini Code</h3>
              <p className="code-description">Generate code using Google's Gemini AI model based on your documentation</p>
              <div className="code-features">
                <ul>
                  <li>Free tier available</li>
                  <li>Comprehensive project structure</li>
                  <li>Clean, well-commented code</li>
                  <li>Based directly on your documentation</li>
                </ul>
              </div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleGenerateCode('gemini')}
                disabled={isLoading || !documentation}
              >
                {isLoading && codeType === 'gemini' ? 'Generating...' : 'Generate with Gemini'}
              </button>
            </div>
          <div className="code-guide">
            <h3>How to use the generated code</h3>
            <ol>
              <li>Download the ZIP file containing the generated code</li>
              <li>Extract the ZIP file to your desired location</li>
              <li>Open a terminal in the extracted directory</li>
              <li>Run <code>npm install</code> to install dependencies</li>
              <li>Run <code>npm run dev</code> to start the development server</li>
              <li>Open the project in your code editor to customize further</li>
            </ol>
            <p>The generated code provides a starting point based on your documentation. You can build upon this foundation to create your complete application.</p>
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