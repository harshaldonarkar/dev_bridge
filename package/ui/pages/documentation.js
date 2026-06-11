// In pages/documentation.js
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function Documentation() {
  const router = useRouter();
  const { prompt } = router.query;
  const [documentation, setDocumentation] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeSection, setActiveSection] = useState('project_summary');
  
// In pages/documentation.js, update the useEffect hook

useEffect(() => {
    // If there's no prompt parameter in the URL, check for existing docs
    if (!prompt) {
      // Try to get documentation from localStorage
      const existingDoc = localStorage.getItem('documentation');
      
      if (existingDoc) {
        // Documentation exists in localStorage
        console.log("Using existing documentation from localStorage");
        setDocumentation(JSON.parse(existingDoc));
        setIsLoading(false);
        return;
      } else {
        // No documentation and no prompt, send back to home
        console.log("No documentation found, redirecting to home");
        router.push('/');
        return;
      }
    }
    
    // At this point, we have a prompt and need to check if we need to regenerate
    
    // Check if we already have documentation for this prompt
    const existingDoc = localStorage.getItem('documentation');
    const savedPrompt = localStorage.getItem('lastPrompt');
    
    // If we have documentation and it matches the current prompt, use it
    if (existingDoc && savedPrompt === prompt) {
      console.log("Using existing documentation for the same prompt");
      setDocumentation(JSON.parse(existingDoc));
      setIsLoading(false);
      return;
    }
    
    // Otherwise, we need to generate new documentation
    const fetchDocumentation = async () => {
      try {
        // Call your backend API
        const response = await fetch('http://localhost:5001/api/generate-documentation', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt }),
        });
        
        if (!response.ok) {
          throw new Error(`API call failed with status ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success' && data.documentation) {
          setDocumentation(data.documentation);
          // Save documentation to localStorage
          localStorage.setItem('documentation', JSON.stringify(data.documentation));
          // Save the prompt that generated this documentation
          localStorage.setItem('lastPrompt', prompt);
        } else {
          throw new Error('Invalid response format');
        }
        
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching documentation:', error);
        setIsLoading(false);
        setError(error.message);
      }
    };
    
    setIsLoading(true);
    fetchDocumentation();
  }, [prompt, router]);
  if (isLoading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '4rem 0' }}>
        <div className="spinner"></div>
        <p>Generating documentation...</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '4rem 0' }}>
        <h2>Error generating documentation</h2>
        <p>{error}</p>
        <Link href="/">
          <button className="btn btn-primary">Go Back</button>
        </Link>
      </div>
    );
  }
  
  if (!documentation) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '4rem 0' }}>
        <h2>No documentation found</h2>
        <p>Please go back and enter a project description.</p>
        <Link href="/">
          <button className="btn btn-primary">Go Back</button>
        </Link>
      </div>
    );
  }
  const handleRegenerate = () => {
    if (!prompt) {
      // If we don't have a prompt in the URL, we can't regenerate
      setError('Cannot regenerate without original prompt');
      return;
    }
    
    // Clear the saved documentation for this prompt
    localStorage.removeItem('lastPrompt');
    
    // Reload the page with the same prompt to trigger regeneration
    router.replace(router.asPath);
  };
  const handleNextSection = () => {
    const sections = [
      'project_summary', 
      'target_audience', 
      'features', 
      'tech_stack', 
      'content_structure', 
      'implementation_plan', 
      'deployment_strategy'
    ];
    const currentIndex = sections.indexOf(activeSection);
    if (currentIndex < sections.length - 1) {
      setActiveSection(sections[currentIndex + 1]);
    }
  };
  
  const handlePreviousSection = () => {
    const sections = [
      'project_summary', 
      'target_audience', 
      'features', 
      'tech_stack', 
      'content_structure', 
      'implementation_plan', 
      'deployment_strategy'
    ];
    const currentIndex = sections.indexOf(activeSection);
    if (currentIndex > 0) {
      setActiveSection(sections[currentIndex - 1]);
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
            <Link href="#" className="nav-link active">Documentation</Link>
            <Link href="/visualization" className="nav-link">Visualizations</Link>
            <Link href="/export" className="nav-link">Export</Link>
            <Link href="/code" className="nav-link">Code Generation</Link>
            <Link href="#" className="nav-link">My Projects</Link>
          </nav>
        </div>
      </header>
      
      <section className="documentation">
        <div className="container">
          <div className="doc-container">
            <div className="doc-sidebar">
              <div className="doc-nav">
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'project_summary' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('project_summary'); }}>
                  Project Summary
                </a>
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'target_audience' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('target_audience'); }}>
                  Target Audience
                </a>
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'features' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('features'); }}>
                  Feature List
                </a>
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'tech_stack' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('tech_stack'); }}>
                  Tech Stack
                </a>
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'content_structure' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('content_structure'); }}>
                  Content Structure
                </a>
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'implementation_plan' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('implementation_plan'); }}>
                  Implementation Plan
                </a>
                <a href="#" 
                   className={`doc-nav-item ${activeSection === 'deployment_strategy' ? 'active' : ''}`}
                   onClick={(e) => { e.preventDefault(); setActiveSection('deployment_strategy'); }}>
                  Deployment Strategy
                </a>
              </div>
              <div style={{ marginTop: '2rem' }}>
                <button className="btn btn-primary" style={{ width: '100%' }}>Save Changes</button>
                <button className="btn btn-secondary" style={{ width: '100%', marginTop: '0.5rem' }} OnClick={handleRegenerate}>Regenerate</button>
              </div>
            </div>
            
            <div className="doc-content">
              {activeSection === 'project_summary' && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-file-alt doc-section-icon"></i>
                    <h3>Project Summary</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    <h4>{documentation.project_summary.title}</h4>
                    <p>{documentation.project_summary.description}</p>
                    <p><strong>Objectives:</strong></p>
                    <ul>
                      {documentation.project_summary.objectives && 
                       documentation.project_summary.objectives.map((objective, index) => (
                        <li key={index}>{objective}</li>
                      ))}
                    </ul>
                    <p><strong>Scope:</strong> {documentation.project_summary.scope}</p>
                  </div>
                </div>
              )}
              
              {activeSection === 'target_audience' && documentation.target_audience && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-users doc-section-icon"></i>
                    <h3>Target Audience</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    <p><strong>Primary Audience:</strong> {documentation.target_audience.primary_audience}</p>
                    {documentation.target_audience.secondary_audience && (
                      <p><strong>Secondary Audience:</strong> {documentation.target_audience.secondary_audience}</p>
                    )}
                    <p><strong>User Characteristics:</strong></p>
                    <ul>
                      {documentation.target_audience.user_characteristics && 
                       documentation.target_audience.user_characteristics.map((characteristic, index) => (
                        <li key={index}>{characteristic}</li>
                      ))}
                    </ul>
                    <p><strong>User Needs:</strong></p>
                    <ul>
                      {documentation.target_audience.user_needs && 
                       documentation.target_audience.user_needs.map((need, index) => (
                        <li key={index}>{need}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
              
              {activeSection === 'features' && documentation.features && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-list-check doc-section-icon"></i>
                    <h3>Features</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    {documentation.features.map((feature, index) => (
                      <div key={index} style={{ marginBottom: '1.5rem' }}>
                        <h4>{feature.name}</h4>
                        <p>{feature.description}</p>
                        <p><strong>Priority:</strong> {feature.priority}</p>
                        <p><strong>Details:</strong></p>
                        <ul>
                          {feature.details && feature.details.map((detail, detailIndex) => (
                            <li key={detailIndex}>{detail}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {activeSection === 'tech_stack' && documentation.tech_stack && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-server doc-section-icon"></i>
                    <h3>Tech Stack</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    {documentation.tech_stack.map((tech, index) => (
                      <div key={index} style={{ marginBottom: '1.5rem' }}>
                        <h4>{tech.name}</h4>
                        <p><strong>Category:</strong> {tech.category}</p>
                        <p>{tech.description}</p>
                        <p><strong>Benefits:</strong></p>
                        <ul>
                          {tech.benefits && tech.benefits.map((benefit, benefitIndex) => (
                            <li key={benefitIndex}>{benefit}</li>
                          ))}
                        </ul>
                        {tech.alternatives && tech.alternatives.length > 0 && (
                          <>
                            <p><strong>Alternatives:</strong></p>
                            <ul>
                              {tech.alternatives.map((alternative, altIndex) => (
                                <li key={altIndex}>{alternative}</li>
                              ))}
                            </ul>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {activeSection === 'content_structure' && documentation.content_structure && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-sitemap doc-section-icon"></i>
                    <h3>Content Structure</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    {documentation.content_structure.map((section, index) => (
                      <div key={index} style={{ marginBottom: '1.5rem' }}>
                        <h4>{section.section_name}</h4>
                        <p>{section.description}</p>
                        <p><strong>Content Elements:</strong></p>
                        <ul>
                          {section.content_elements && section.content_elements.map((element, elementIndex) => (
                            <li key={elementIndex}>{element}</li>
                          ))}
                        </ul>
                        {section.design_considerations && section.design_considerations.length > 0 && (
                          <>
                            <p><strong>Design Considerations:</strong></p>
                            <ul>
                              {section.design_considerations.map((consideration, consIndex) => (
                                <li key={consIndex}>{consideration}</li>
                              ))}
                            </ul>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {activeSection === 'implementation_plan' && documentation.implementation_plan && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-tasks doc-section-icon"></i>
                    <h3>Implementation Plan</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    {documentation.implementation_plan
                      .sort((a, b) => a.step_number - b.step_number)
                      .map((step, index) => (
                      <div key={index} style={{ marginBottom: '1.5rem' }}>
                        <h4>Step {step.step_number}: {step.title}</h4>
                        <p>{step.description}</p>
                        {step.estimated_time && <p><strong>Estimated Time:</strong> {step.estimated_time}</p>}
                        {step.dependencies && step.dependencies.length > 0 && (
                          <>
                            <p><strong>Dependencies:</strong></p>
                            <ul>
                              {step.dependencies.map((dep, depIndex) => (
                                <li key={depIndex}>Step {dep}</li>
                              ))}
                            </ul>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {activeSection === 'deployment_strategy' && documentation.deployment_strategy && (
                <div className="doc-section">
                  <div className="doc-section-title">
                    <i className="fas fa-rocket doc-section-icon"></i>
                    <h3>Deployment Strategy</h3>
                  </div>
                  <div contentEditable="true" style={{ border: '1px dashed var(--neutral-300)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
                    <p><strong>Hosting Recommendation:</strong> {documentation.deployment_strategy.hosting_recommendation}</p>
                    
                    <p><strong>Deployment Steps:</strong></p>
                    <ol>
                      {documentation.deployment_strategy.deployment_steps && 
                       documentation.deployment_strategy.deployment_steps.map((step, index) => (
                        <li key={index}>{step}</li>
                      ))}
                    </ol>
                    
                    <p><strong>Scaling Considerations:</strong></p>
                    <ul>
                      {documentation.deployment_strategy.scaling_considerations && 
                       documentation.deployment_strategy.scaling_considerations.map((consideration, index) => (
                        <li key={index}>{consideration}</li>
                      ))}
                    </ul>
                    
                    {documentation.deployment_strategy.maintenance_plan && (
                      <><p><strong>Maintenance Plan:</strong></p>
                      <p>{documentation.deployment_strategy.maintenance_plan}</p>
                      </>
                    )}
                  </div>
                </div>
              )}
              
              <div className="doc-actions" style={{ display: 'flex', justifyContent: 'space-between', marginTop: '2rem' }}>
                <button 
                  className="btn btn-secondary" 
                  onClick={handlePreviousSection}
                >
                  Previous Section
                </button>
                
                <Link href="/visualization">
                  <button className="btn btn-primary">
                    View Visualizations
                  </button>
                </Link>
                
                <button 
                  className="btn btn-primary"
                  onClick={handleNextSection}
                >
                  Next Section
                </button>
              </div>
            </div>
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