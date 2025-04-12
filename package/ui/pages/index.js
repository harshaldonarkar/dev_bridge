import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      alert('Please enter a project description');
      return;
    }
    
    setIsLoading(true);
    
    // In a real implementation, this would call your backend API
    try {
      // For demo purposes, we'll use a timeout to simulate the API call
      setTimeout(() => {
        // After "generating" documentation, redirect to the documentation page
        router.push({
          pathname: '/documentation',
          query: { prompt: prompt }
        });
      }, 2000);
    } catch (error) {
      console.error('Error:', error);
      setIsLoading(false);
      alert('An error occurred. Please try again.');
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
            <a href="#features" className="nav-link">Features</a>
            <a href="#how-it-works" className="nav-link">How It Works</a>
            <a href="#try-it" className="nav-link">Try It</a>
            <a href="#pricing" className="nav-link">Pricing</a>
            <a href="#contact" className="nav-link">Contact</a>
          </nav>
        </div>
      </header>

      <section className="hero">
        <div className="container hero-container">
          <div className="hero-content">
            <h1 className="hero-title">Bridge the Gap Between Idea and Development</h1>
            <p className="hero-subtitle">Transform vague project ideas into detailed technical documentation, visualizations, and starter code with our AI-powered platform.</p>
            <div className="hero-buttons">
              <a href="#try-it" className="btn btn-lg btn-outline">Try It Now</a>
              <a href="#how-it-works" className="btn btn-lg btn-secondary">Learn More</a>
            </div>
          </div>
          <div className="hero-image">
            <img src="https://via.placeholder.com/600x400" alt="AI-powered documentation generation" />
          </div>
        </div>
      </section>

      <section id="features" className="features">
        <div className="container">
          <div className="section-title">
            <h2>Powerful Features</h2>
            <p>Our platform streamlines the pre-development process with these powerful capabilities</p>
          </div>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-file-alt"></i>
              </div>
              <h3 className="feature-title">Instant Documentation</h3>
              <p>Generate comprehensive project documentation from simple prompts, including project summaries, target audience analysis, and feature lists.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-sitemap"></i>
              </div>
              <h3 className="feature-title">Visual Structure</h3>
              <p>Visualize your project structure with interactive site maps and component relationship diagrams that help clarify architecture.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-server"></i>
              </div>
              <h3 className="feature-title">Tech Stack Recommendations</h3>
              <p>Receive intelligent technology recommendations based on your project requirements, ensuring optimal performance and scalability.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-file-export"></i>
              </div>
              <h3 className="feature-title">Export Options</h3>
              <p>Download your documentation in PDF or DOCX formats for easy sharing with stakeholders and team members.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-code"></i>
              </div>
              <h3 className="feature-title">Starter Code Generation</h3>
              <p>Jump-start development with automatically generated frontend and backend code based on your approved documentation.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-robot"></i>
              </div>
              <h3 className="feature-title">AI Agent Creation</h3>
              <p>Build basic AI agents from your requirements, accelerating the development of intelligent features for your project.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="how-it-works">
        <div className="container">
          <div className="section-title">
            <h2>How It Works</h2>
            <p>Our streamlined process takes you from concept to creation in just a few steps</p>
          </div>
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Describe Your Project</h3>
                <p>Enter a simple prompt describing what you want to build, such as "a portfolio website with a contact form and Instagram feed" or "an e-commerce app with user reviews and payment processing."</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Review Generated Documentation</h3>
                <p>Our AI instantly generates detailed documentation including project summary, target audience, feature list, suggested tech stack, and content ideas for each section.</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Visualize & Edit</h3>
                <p>Explore interactive visualizations of your project structure, make edits or refinements to the documentation, and ensure everything aligns with your vision.</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>Export & Share</h3>
                <p>Download your documentation as PDF or DOCX to share with stakeholders, team members, or clients for approval and feedback.</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">5</div>
              <div className="step-content">
                <h3>Generate Starter Code</h3>
                <p>Once approved, generate starter frontend or backend code based on your documentation, giving you a solid foundation to build upon.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="try-it" className="prompt-section">
        <div className="container">
          <div className="section-title">
            <h2>Try It Now</h2>
            <p>Enter your project idea and let our AI generate detailed documentation</p>
          </div>
          <div className="prompt-container">
            <div className="prompt-box">
              <form onSubmit={handleSubmit}>
                <label htmlFor="prompt-input" className="prompt-label">Describe your project:</label>
                <textarea 
                  id="prompt-input" 
                  className="prompt-textarea" 
                  placeholder="e.g., a portfolio website with a contact form and Instagram feed"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  disabled={isLoading}
                ></textarea>
                <div className="prompt-actions">
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setPrompt('')}
                    disabled={isLoading}
                  >
                    Clear
                  </button>
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Generating...' : 'Generate Documentation'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </section>

      <section id="pricing" className="features">
        <div className="container">
          <div className="section-title">
            <h2>Pricing Plans</h2>
            <p>Choose the plan that fits your needs</p>
          </div>
          <div className="features-grid">
            <div className="feature-card">
              <h3 className="feature-title">Free</h3>
              <p className="pricing">$0/month</p>
              <ul>
                <li>3 projects per month</li>
                <li>Basic documentation</li>
                <li>PDF export</li>
                <li>Community support</li>
              </ul>
              <button className="btn btn-primary">Get Started</button>
            </div>
            <div className="feature-card">
              <h3 className="feature-title">Professional</h3>
              <p className="pricing">$29/month</p>
              <ul>
                <li>Unlimited projects</li>
                <li>Advanced documentation</li>
                <li>All export formats</li>
                <li>Basic code generation</li>
                <li>Email support</li>
              </ul>
              <button className="btn btn-primary">Subscribe</button>
            </div>
            <div className="feature-card">
              <h3 className="feature-title">Enterprise</h3>
              <p className="pricing">$99/month</p>
              <ul>
                <li>Unlimited projects</li>
                <li>Premium documentation</li>
                <li>All export formats</li>
                <li>Advanced code generation</li>
                <li>AI agent creation</li>
                <li>Priority support</li>
                <li>Team collaboration</li>
              </ul>
              <button className="btn btn-primary">Contact Sales</button>
            </div>
          </div>
        </div>
      </section>

      <section id="contact" className="prompt-section">
        <div className="container">
          <div className="section-title">
            <h2>Contact Us</h2>
            <p>Have questions? Get in touch with our team</p>
          </div>
          <div className="prompt-container">
            <div className="prompt-box">
              <div className="form-group">
                <label className="prompt-label">Name</label>
                <input type="text" className="prompt-textarea" style={{ minHeight: "auto", height: "40px" }} />
              </div>
              <div className="form-group">
                <label className="prompt-label">Email</label>
                <input type="email" className="prompt-textarea" style={{ minHeight: "auto", height: "40px" }} />
              </div>
              <div className="form-group">
                <label className="prompt-label">Message</label>
                <textarea className="prompt-textarea"></textarea>
              </div>
              <div className="prompt-actions">
                <button className="btn btn-primary">Send Message</button>
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
            <div className="footer-social">
              <a href="#" className="social-icon"><i className="fab fa-twitter"></i></a>
              <a href="#" className="social-icon"><i className="fab fa-linkedin"></i></a>
              <a href="#" className="social-icon"><i className="fab fa-github"></i></a>
            </div>
          </div>
          <div>
            <h4 className="footer-heading">Product</h4>
            <div className="footer-links">
              <a href="#" className="footer-link">Features</a>
              <a href="#" className="footer-link">Pricing</a>
              <a href="#" className="footer-link">Documentation</a>
              <a href="#" className="footer-link">API</a>
            </div>
          </div>
          <div>
            <h4 className="footer-heading">Resources</h4>
            <div className="footer-links">
              <a href="#" className="footer-link">Blog</a>
              <a href="#" className="footer-link">Tutorials</a>
              <a href="#" className="footer-link">Support</a>
              <a href="#" className="footer-link">Community</a>
            </div>
          </div>
          <div>
            <h4 className="footer-heading">Company</h4>
            <div className="footer-links">
              <a href="#" className="footer-link">About</a>
              <a href="#" className="footer-link">Careers</a>
              <a href="#" className="footer-link">Contact</a>
              <a href="#" className="footer-link">Privacy Policy</a>
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