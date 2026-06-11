// pages/visualization.js
import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import * as d3 from 'd3';

export default function Visualization() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('sitemap');
  const [visualization, setVisualization] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [documentation, setDocumentation] = useState(null);
  
  // Refs for visualization containers
  const sitemapRef = useRef(null);
  const relationshipsRef = useRef(null);
  const userFlowRef = useRef(null);
  
  useEffect(() => {
    // Get the documentation from localStorage
    try {
      const savedDocumentation = localStorage.getItem('documentation');
      console.log("Retrieved from localStorage:", savedDocumentation ? "Documentation found" : "No documentation");
      
      if (!savedDocumentation) {
        setError('No documentation found. Please generate documentation first.');
        setIsLoading(false);
        return;
      }
      
      const parsedDoc = JSON.parse(savedDocumentation);
      setDocumentation(parsedDoc);
      
      // Generate visualization data directly from documentation
      // This is a fallback in case the API doesn't work
      const mockVisualization = {
        siteMapD3: {
          name: parsedDoc.project_summary.title || "Project",
          children: [
            {
              name: "Home",
              children: []
            }
          ]
        },
        relationshipsD3: {
          nodes: [
            { id: "node-1", name: "Project", type: "Project" }
          ],
          links: []
        },
        userFlowD3: {
          name: "User Flow",
          nodes: [
            { id: "step-1", name: "User Lands on Home Page", description: "First interaction" }
          ],
          links: []
        }
      };
      
      // Add content structure to sitemap
      if (parsedDoc.content_structure && Array.isArray(parsedDoc.content_structure)) {
        mockVisualization.siteMapD3.children = parsedDoc.content_structure.map((section, i) => ({
          name: section.section_name || `Section ${i+1}`,
          children: (section.content_elements || []).map((element, j) => ({
            name: element
          }))
        }));
      }
      
      // Add features and tech stack to relationships
      if (parsedDoc.features && Array.isArray(parsedDoc.features)) {
        parsedDoc.features.forEach((feature, i) => {
          mockVisualization.relationshipsD3.nodes.push({
            id: `feature-${i}`,
            name: feature.name,
            type: "Feature"
          });
        });
      }
      
      if (parsedDoc.tech_stack && Array.isArray(parsedDoc.tech_stack)) {
        parsedDoc.tech_stack.forEach((tech, i) => {
          mockVisualization.relationshipsD3.nodes.push({
            id: `tech-${i}`,
            name: tech.name,
            type: tech.category
          });
          
          // Connect to related features
          mockVisualization.relationshipsD3.links.push({
            source: "node-1",
            target: `tech-${i}`,
            type: "uses"
          });
        });
      }
      
      // Add implementation steps to user flow
      if (parsedDoc.implementation_plan && Array.isArray(parsedDoc.implementation_plan)) {
        mockVisualization.userFlowD3.nodes = parsedDoc.implementation_plan
          .sort((a, b) => a.step_number - b.step_number)
          .map((step) => ({
            id: `step-${step.step_number}`,
            name: step.title,
            description: step.description
          }));
          
        // Create links between steps
        for (let i = 0; i < mockVisualization.userFlowD3.nodes.length - 1; i++) {
          mockVisualization.userFlowD3.links.push({
            source: mockVisualization.userFlowD3.nodes[i].id,
            target: mockVisualization.userFlowD3.nodes[i + 1].id
          });
        }
      }
      
      setVisualization(mockVisualization);
      setIsLoading(false);
      
      // Also try to fetch from API in parallel
      fetchVisualizationFromAPI(parsedDoc);
      
    } catch (error) {
      console.error('Error processing saved documentation:', error);
      setError('Error processing saved documentation. Please regenerate documentation.');
      setIsLoading(false);
    }
  }, []);
  
  const fetchVisualizationFromAPI = async (doc) => {
    try {
      // Call the backend API to generate visualization data
      const response = await fetch('http://localhost:5001/api/generate-visualization', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documentation: doc }),
      });
      
      if (!response.ok) {
        console.error(`API call failed with status ${response.status}`);
        return; // Use the mockup data instead
      }
      
      const data = await response.json();
      
      if (data.status === 'success' && data.visualization) {
        console.log("Received visualization data from API");
        setVisualization(data.visualization);
      }
    } catch (error) {
      console.error('Error fetching visualization from API:', error);
      // Continue with the mock visualization
    }
  };
  
  useEffect(() => {
    // Render visualizations when data is available and refs are ready
    if (visualization && !isLoading) {
      renderVisualizations();
    }
  }, [visualization, isLoading, activeTab]);
  
  const renderVisualizations = () => {
    switch (activeTab) {
      case 'sitemap':
        renderSiteMap();
        break;
      case 'relationships':
        renderRelationships();
        break;
      case 'userflow':
        renderUserFlow();
        break;
      default:
        break;
    }
  };
  
  const renderSiteMap = () => {
    if (!sitemapRef.current || !visualization?.siteMapD3) return;
    
    // Clear previous visualization
    d3.select(sitemapRef.current).selectAll('*').remove();
    
    try {
      const width = sitemapRef.current.clientWidth || 800;
      const height = sitemapRef.current.clientHeight || 600;
      
      // Create simple nested list view instead of complex D3 visualization
      const container = d3.select(sitemapRef.current)
        .append('div')
        .style('padding', '20px')
        .style('overflow', 'auto')
        .style('height', '100%');
      
      container.append('h3')
        .text(visualization.siteMapD3.name)
        .style('color', '#4f46e5')
        .style('margin-bottom', '10px');
      
      const renderChildren = (parent, children, level = 0) => {
        if (!children || children.length === 0) return;
        
        const list = parent.append('ul')
          .style('margin-left', `${level * 20}px`)
          .style('list-style-type', 'none')
          .style('padding-left', '20px');
        
        children.forEach(child => {
          const item = list.append('li')
            .style('margin-bottom', '8px');
          
          item.append('div')
            .style('background-color', '#4f46e5')
            .style('color', 'white')
            .style('padding', '8px 12px')
            .style('border-radius', '4px')
            .text(child.name);
          
          if (child.children && child.children.length > 0) {
            renderChildren(item, child.children, level + 1);
          }
        });
      };
      
      renderChildren(container, visualization.siteMapD3.children);
      
    } catch (error) {
      console.error('Error rendering site map:', error);
      d3.select(sitemapRef.current).append('div')
        .style('color', 'red')
        .style('padding', '20px')
        .text('Error rendering site map visualization.');
    }
  };
  
  const renderRelationships = () => {
    if (!relationshipsRef.current || !visualization?.relationshipsD3) return;
    
    // Clear previous visualization
    d3.select(relationshipsRef.current).selectAll('*').remove();
    
    try {
      // Create simple list instead of complex force simulation
      const container = d3.select(relationshipsRef.current)
        .append('div')
        .style('padding', '20px')
        .style('overflow', 'auto')
        .style('height', '100%');
      
      container.append('h3')
        .text('Component Relationships')
        .style('color', '#4f46e5')
        .style('margin-bottom', '20px');
      
      // Group nodes by type
      const nodesByType = {};
      visualization.relationshipsD3.nodes.forEach(node => {
        if (!nodesByType[node.type]) {
          nodesByType[node.type] = [];
        }
        nodesByType[node.type].push(node);
      });
      
      // Create a section for each type
      Object.keys(nodesByType).forEach(type => {
        container.append('h4')
          .text(type)
          .style('margin-top', '15px')
          .style('margin-bottom', '10px')
          .style('color', '#6b7280');
        
        const nodeList = container.append('div')
          .style('display', 'flex')
          .style('flex-wrap', 'wrap')
          .style('gap', '10px')
          .style('margin-bottom', '20px');
        
        nodesByType[type].forEach(node => {
          nodeList.append('div')
            .style('background-color', type === 'Feature' ? '#4f46e5' : 
                                      type === 'Frontend' ? '#10b981' :
                                      type === 'Backend' ? '#ef4444' :
                                      type === 'Database' ? '#f59e0b' : '#6b7280')
            .style('color', 'white')
            .style('padding', '8px 12px')
            .style('border-radius', '4px')
            .style('flex', '0 0 auto')
            .text(node.name);
        });
      });
      
      // Show some of the relationships
      if (visualization.relationshipsD3.links.length > 0) {
        container.append('h4')
          .text('Relationships')
          .style('margin-top', '20px')
          .style('margin-bottom', '10px')
          .style('color', '#6b7280');
        
        const list = container.append('ul')
          .style('padding-left', '20px');
        
        visualization.relationshipsD3.links.slice(0, 10).forEach(link => {
          const sourceNode = visualization.relationshipsD3.nodes.find(n => n.id === link.source) || { name: link.source };
          const targetNode = visualization.relationshipsD3.nodes.find(n => n.id === link.target) || { name: link.target };
          
          list.append('li')
            .text(`${sourceNode.name} → ${targetNode.name}`);
        });
      }
      
    } catch (error) {
      console.error('Error rendering relationships:', error);
      d3.select(relationshipsRef.current).append('div')
        .style('color', 'red')
        .style('padding', '20px')
        .text('Error rendering component relationships visualization.');
    }
  };
  
  const renderUserFlow = () => {
    if (!userFlowRef.current || !visualization?.userFlowD3) return;
    
    // Clear previous visualization
    d3.select(userFlowRef.current).selectAll('*').remove();
    
    try {
      // Create simple flow diagram
      const container = d3.select(userFlowRef.current)
        .append('div')
        .style('padding', '20px')
        .style('overflow', 'auto')
        .style('height', '100%');
      
      container.append('h3')
        .text('User Flow')
        .style('color', '#4f46e5')
        .style('margin-bottom', '20px');
      
      const flowContainer = container.append('div');
      
      // Create a step card for each node
      visualization.userFlowD3.nodes.forEach((node, index) => {
        const stepCard = flowContainer.append('div')
          .style('background-color', '#f3f4f6')
          .style('border-left', '4px solid #4f46e5')
          .style('padding', '15px')
          .style('margin-bottom', '15px')
          .style('border-radius', '4px');
        
        stepCard.append('h4')
          .style('margin', '0 0 8px 0')
          .style('color', '#4f46e5')
          .text(node.name);
        
        stepCard.append('p')
          .style('margin', '0')
          .text(node.description);
        
        // Add arrow if not the last step
        if (index < visualization.userFlowD3.nodes.length - 1) {
          flowContainer.append('div')
            .style('text-align', 'center')
            .style('margin-bottom', '15px')
            .html('↓');
        }
      });
      
    } catch (error) {
      console.error('Error rendering user flow:', error);
      d3.select(userFlowRef.current).append('div')
        .style('color', 'red')
        .style('padding', '20px')
        .text('Error rendering user flow visualization.');
    }
  };
  
  if (isLoading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '4rem 0' }}>
        <div className="spinner"></div>
        <p>Generating visualizations...</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '4rem 0' }}>
        <h2>Error generating visualizations</h2>
        <p>{error}</p>
        <Link href="/documentation">
          <button className="btn btn-primary">Back to Documentation</button>
        </Link>
      </div>
    );
  }
  
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
            <Link href="/visualization" className="nav-link active">Visualizations</Link>
            <Link href="/export" className="nav-link">Export</Link>
            <Link href="/code" className="nav-link">Code Generation</Link>
            <Link href="#" className="nav-link">My Projects</Link>
          </nav>
        </div>
      </header>
      
      <section className="visualization">
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>
            Visualizations for {documentation?.project_summary?.title || 'Project'}
          </h2>
          
          <div className="viz-container">
            <div className="viz-tabs">
              <div 
                className={`viz-tab ${activeTab === 'sitemap' ? 'active' : ''}`}
                onClick={() => setActiveTab('sitemap')}
              >
                Site Map
              </div>
              <div 
                className={`viz-tab ${activeTab === 'relationships' ? 'active' : ''}`}
                onClick={() => setActiveTab('relationships')}
              >
                Component Relationships
              </div>
              <div 
                className={`viz-tab ${activeTab === 'userflow' ? 'active' : ''}`}
                onClick={() => setActiveTab('userflow')}
              >
                User Flow
              </div>
            </div>
            
            <div className="viz-content">
              {activeTab === 'sitemap' && (
                <div className="canvas-container" ref={sitemapRef}></div>
              )}
              
              {activeTab === 'relationships' && (
                <div className="canvas-container" ref={relationshipsRef}></div>
              )}
              
              {activeTab === 'userflow' && (
                <div className="canvas-container" ref={userFlowRef}></div>
              )}
            </div>
          </div>
          
          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <Link href="/documentation">
              <button className="btn btn-primary">Back to Documentation</button>
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