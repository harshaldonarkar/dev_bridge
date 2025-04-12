"""
React/Next.js Frontend Generator

This module generates a React/Next.js frontend based on the AI-generated documentation.
It implements the FrontendGenerator interface from the code_generation_architecture module.
"""

import os
import json
import shutil
from typing import Dict, List, Any
from .code_generation_architecture import FrontendGenerator

class ReactNextGenerator(FrontendGenerator):
    """
    Generates a React/Next.js frontend application.
    """
    
    def __init__(self, config=None):
        """
        Initialize the React/Next.js generator.
        
        Args:
            config: Configuration options for the generator
        """
        super().__init__(config)
        self.template_dir = self.config.get('template_dir', os.path.join(os.path.dirname(__file__), 'templates', 'react_next'))
    
    def generate_code(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate a React/Next.js application based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated code
            
        Returns:
            Path to the generated code package
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        # Generate project structure
        self._generate_project_structure(documentation, output_dir)
        
        # Generate components
        self.generate_components(documentation, os.path.join(output_dir, 'components'))
        
        # Generate pages
        self.generate_pages(documentation, os.path.join(output_dir, 'pages'))
        
        # Generate styles
        self.generate_styles(documentation, os.path.join(output_dir, 'styles'))
        
        # Generate assets
        self.generate_assets(documentation, os.path.join(output_dir, 'public'))
        
        # Create package
        package_name = documentation.get('project_summary', {}).get('title', 'frontend').replace(' ', '_').lower()
        return self._create_package(output_dir, os.path.join(os.path.dirname(output_dir), package_name))
    
    def _generate_project_structure(self, documentation: Dict[str, Any], output_dir: str) -> None:
        """
        Generate the basic project structure.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated code
        """
        # Create directories
        os.makedirs(os.path.join(output_dir, 'components'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'pages'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'styles'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'public'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'lib'), exist_ok=True)
        
        # Generate package.json
        package_json = {
            "name": documentation.get('project_summary', {}).get('title', 'frontend').replace(' ', '-').lower(),
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "^13.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "eslint": "^8.0.0",
                "eslint-config-next": "^13.0.0"
            }
        }
        
        # Add additional dependencies based on tech stack
        tech_stack = documentation.get('tech_stack', [])
        for tech in tech_stack:
            if tech.get('category') == 'Frontend':
                if 'tailwind' in tech.get('name', '').lower():
                    package_json['dependencies']['tailwindcss'] = "^3.3.0"
                    package_json['dependencies']['autoprefixer'] = "^10.4.0"
                    package_json['dependencies']['postcss'] = "^8.4.0"
                elif 'material-ui' in tech.get('name', '').lower() or 'mui' in tech.get('name', '').lower():
                    package_json['dependencies']['@mui/material'] = "^5.0.0"
                    package_json['dependencies']['@mui/icons-material'] = "^5.0.0"
                    package_json['dependencies']['@emotion/react'] = "^11.0.0"
                    package_json['dependencies']['@emotion/styled'] = "^11.0.0"
            
            # Add state management
            if 'redux' in tech.get('name', '').lower():
                package_json['dependencies']['redux'] = "^4.2.0"
                package_json['dependencies']['react-redux'] = "^8.0.0"
                package_json['dependencies']['@reduxjs/toolkit'] = "^1.9.0"
            elif 'context' in tech.get('name', '').lower():
                # Context API is built into React, no additional dependencies needed
                pass
        
        # Write package.json
        self._create_file(os.path.join(output_dir, 'package.json'), json.dumps(package_json, indent=2))
        
        # Generate next.config.js
        next_config = """
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig
"""
        self._create_file(os.path.join(output_dir, 'next.config.js'), next_config)
        
        # Generate .gitignore
        gitignore = """
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
"""
        self._create_file(os.path.join(output_dir, '.gitignore'), gitignore)
        
        # Generate README.md
        readme = f"""
# {documentation.get('project_summary', {}).get('title', 'Frontend Application')}

{documentation.get('project_summary', {}).get('description', 'A Next.js frontend application.')}

## Getting Started

First, install dependencies:

```bash
npm install
# or
yarn install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Features

{self._generate_features_list(documentation)}

## Tech Stack

{self._generate_tech_stack_list(documentation)}

## Project Structure

- `/pages` - Next.js pages
- `/components` - Reusable React components
- `/styles` - CSS and styling files
- `/public` - Static assets
- `/lib` - Utility functions and helpers
"""
        self._create_file(os.path.join(output_dir, 'README.md'), readme)
    
    def _generate_features_list(self, documentation: Dict[str, Any]) -> str:
        """
        Generate a markdown list of features.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Markdown string with features list
        """
        features = documentation.get('features', [])
        if not features:
            return "No features specified."
        
        result = ""
        for feature in features:
            result += f"- **{feature.get('name', '')}**: {feature.get('description', '')}\n"
        
        return result
    
    def _generate_tech_stack_list(self, documentation: Dict[str, Any]) -> str:
        """
        Generate a markdown list of frontend technologies.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Markdown string with tech stack list
        """
        tech_stack = documentation.get('tech_stack', [])
        if not tech_stack:
            return "- Next.js\n- React\n"
        
        result = ""
        for tech in tech_stack:
            if tech.get('category') == 'Frontend':
                result += f"- **{tech.get('name', '')}**: {tech.get('description', '')}\n"
        
        if not result:
            return "- Next.js\n- React\n"
        
        return result
    
    def generate_components(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate UI components based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated components
            
        Returns:
            List of paths to the generated component files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Generate layout component
        layout_component = """
import Head from 'next/head';
import Link from 'next/link';
import { useState } from 'react';

export default function Layout({ children, title = 'Default title' }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>{title}</title>
        <meta name="description" content="Generated by DevBridge" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link href="/">
                  <span className="text-xl font-bold text-indigo-600">
                    {title}
                  </span>
                </Link>
              </div>
              <nav className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link href="/">
                  <span className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                    Home
                  </span>
                </Link>
                {/* Add more navigation links based on content structure */}
              </nav>
            </div>
            <div className="-mr-2 flex items-center sm:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
              >
                <span className="sr-only">Open main menu</span>
                {/* Icon for menu */}
                <svg
                  className={`${isMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
                <svg
                  className={`${isMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        {/* Mobile menu, show/hide based on menu state */}
        <div className={`${isMenuOpen ? 'block' : 'hidden'} sm:hidden`}>
          <div className="pt-2 pb-3 space-y-1">
            <Link href="/">
              <span className="bg-indigo-50 border-indigo-500 text-indigo-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
                Home
              </span>
            </Link>
            {/* Add more mobile navigation links */}
          </div>
        </div>
      </header>
      
      <main className="flex-grow">
        {children}
      </main>
      
      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-12 px-4 overflow-hidden sm:px-6 lg:px-8">
          <p className="mt-8 text-center text-base text-gray-400">
            &copy; 2025 {title}. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
"""
        layout_path = os.path.join(output_dir, 'Layout.js')
        self._create_file(layout_path, layout_component)
        generated_files.append(layout_path)
        
        # Generate hero component
        hero_component = """
import Link from 'next/link';

export default function Hero({ title, subtitle, ctaText, ctaLink }) {
  return (
    <div className="relative bg-white overflow-hidden">
      <div className="max-w-7xl mx-auto">
        <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div className="sm:text-center lg:text-left">
              <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span className="block xl:inline">{title}</span>
              </h1>
              <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                {subtitle}
              </p>
              <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div className="rounded-md shadow">
                  <Link href={ctaLink}>
                    <span className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10">
                      {ctaText}
                    </span>
                  </Link>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
      <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
        <div className="h-56 w-full bg-indigo-100 sm:h-72 md:h-96 lg:w-full lg:h-full"></div>
      </div>
    </div>
  );
}
"""
        hero_path = os.path.join(output_dir, 'Hero.js')
        self._create_file(hero_path, hero_component)
        generated_files.append(hero_path)
        
        # Generate feature card component
        feature_card_component = """
export default function FeatureCard({ title, description, icon }) {
  return (
    <div className="p-6 bg-white rounded-lg border border-gray-200 shadow-md">
      <div className="flex justify-center items-center mb-4 w-10 h-10 rounded-full bg-indigo-100 lg:h-12 lg:w-12">
        <svg
          className="w-5 h-5 text-indigo-600 lg:w-6 lg:h-6"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          {icon || (
            <path
              fillRule="evenodd"
              d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          )}
        </svg>
      </div>
      <h3 className="mb-2 text-xl font-bold">{title}</h3>
      <p className="text-gray-500">{description}</p>
    </div>
  );
}
"""
        feature_card_path = os.path.join(output_dir, 'FeatureCard.js')
        self._create_file(feature_card_path, feature_card_component)
        generated_files.append(feature_card_path)
        
        # Generate contact form component
        contact_form_component = """
import { useState } from 'react';

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submitError, setSubmitError] = useState('');
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitError('');
    
    try {
      // In a real implementation, this would send data to an API
      // await fetch('/api/contact', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(formData),
      // });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSubmitSuccess(true);
      setFormData({
        name: '',
        email: '',
        message: ''
      });
    } catch (error) {
      setSubmitError('An error occurred. Please try again.');
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
      {submitSuccess ? (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Message sent successfully</h3>
              <div className="mt-2 text-sm text-green-700">
                <p>Thank you for your message. We'll get back to you soon.</p>
              </div>
              <div className="mt-4">
                <button
                  type="button"
                  className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  onClick={() => setSubmitSuccess(false)}
                >
                  Send another message
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <form className="space-y-6" onSubmit={handleSubmit}>
          {submitError && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{submitError}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
              Name
            </label>
            <div className="mt-1">
              <input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <div className="mt-1">
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-gray-700">
              Message
            </label>
            <div className="mt-1">
              <textarea
                id="message"
                name="message"
                rows={4}
                required
                value={formData.message}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              disabled={isSubmitting}
              className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${isSubmitting ? 'opacity-75 cursor-not-allowed' : ''}`}
            >
              {isSubmitting ? 'Sending...' : 'Send Message'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
"""
        contact_form_path = os.path.join(output_dir, 'ContactForm.js')
        self._create_file(contact_form_path, contact_form_component)
        generated_files.append(contact_form_path)
        
        # Generate additional components based on content structure
        content_structure = documentation.get('content_structure', [])
        for section in content_structure:
            section_name = section.get('section_name', '')
            if section_name.lower() == 'instagram feed':
                # Generate Instagram feed component
                instagram_component = """
import { useState, useEffect } from 'react';

export default function InstagramFeed({ username, count = 6 }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        // In a real implementation, this would fetch from Instagram API
        // const response = await fetch(`/api/instagram?username=${username}&count=${count}`);
        // const data = await response.json();
        
        // Simulate API response with placeholder data
        await new Promise(resolve => setTimeout(resolve, 1000));
        const placeholderPosts = Array(count).fill().map((_, i) => ({
          id: `post-${i}`,
          image: `https://via.placeholder.com/300x300.png?text=Instagram+Post+${i+1}`,
          caption: `This is a placeholder for an Instagram post #${i+1}`,
          likes: Math.floor(Math.random() * 100) + 10,
          url: 'https://instagram.com'
        }));
        
        setPosts(placeholderPosts);
      } catch (err) {
        console.error('Error fetching Instagram posts:', err);
        setError('Failed to load Instagram posts');
      } finally {
        setLoading(false);
      }
    };
    
    fetchPosts();
  }, [username, count]);
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-40">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <p className="text-red-700">{error}</p>
      </div>
    );
  }
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      {posts.map(post => (
        <a
          key={post.id}
          href={post.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block overflow-hidden rounded-lg hover:opacity-90 transition-opacity"
        >
          <img
            src={post.image}
            alt={post.caption}
            className="w-full h-auto"
          />
        </a>
      ))}
    </div>
  );
}
"""
                instagram_path = os.path.join(output_dir, 'InstagramFeed.js')
                self._create_file(instagram_path, instagram_component)
                generated_files.append(instagram_path)
        
        return generated_files
    
    def generate_pages(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate pages based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated pages
            
        Returns:
            List of paths to the generated page files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Generate _app.js
        app_js = """
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;
"""
        app_path = os.path.join(output_dir, '_app.js')
        self._create_file(app_path, app_js)
        generated_files.append(app_path)
        
        # Generate index.js (home page)
        project_title = documentation.get('project_summary', {}).get('title', 'My Project')
        project_description = documentation.get('project_summary', {}).get('description', 'A Next.js project')
        
        index_js = f"""
import Layout from '../components/Layout';
import Hero from '../components/Hero';
import FeatureCard from '../components/FeatureCard';

export default function Home() {{
  return (
    <Layout title="{project_title}">
      <Hero
        title="{project_title}"
        subtitle="{project_description}"
        ctaText="Learn More"
        ctaLink="#features"
      />
      
      <section id="features" className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">Features</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need
            </p>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
              Discover what makes {project_title} special.
            </p>
          </div>
          
          <div className="mt-10">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {self._generate_feature_cards(documentation)}
            </div>
          </div>
        </div>
      </section>
      
      {self._generate_additional_sections(documentation)}
    </Layout>
  );
}}
"""
        index_path = os.path.join(output_dir, 'index.js')
        self._create_file(index_path, index_js)
        generated_files.append(index_path)
        
        # Generate about.js
        about_js = f"""
import Layout from '../components/Layout';

export default function About() {{
  return (
    <Layout title="About | {project_title}">
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">About Us</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Our Story
            </p>
          </div>
          <div className="mt-10">
            <div className="prose prose-indigo prose-lg text-gray-500 mx-auto">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </p>
              <p>
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}}
"""
        about_path = os.path.join(output_dir, 'about.js')
        self._create_file(about_path, about_js)
        generated_files.append(about_path)
        
        # Generate contact.js
        contact_js = f"""
import Layout from '../components/Layout';
import ContactForm from '../components/ContactForm';

export default function Contact() {{
  return (
    <Layout title="Contact | {project_title}">
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">Contact Us</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Get in Touch
            </p>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
              We'd love to hear from you. Fill out the form below and we'll get back to you as soon as possible.
            </p>
          </div>
          
          <div className="mt-10 max-w-xl mx-auto">
            <ContactForm />
          </div>
        </div>
      </div>
    </Layout>
  );
}}
"""
        contact_path = os.path.join(output_dir, 'contact.js')
        self._create_file(contact_path, contact_js)
        generated_files.append(contact_path)
        
        # Generate additional pages based on content structure
        content_structure = documentation.get('content_structure', [])
        for section in content_structure:
            section_name = section.get('section_name', '')
            if section_name.lower() not in ['home', 'about', 'contact']:
                # Generate page for this section
                section_id = section_name.lower().replace(' ', '-')
                section_js = f"""
import Layout from '../components/Layout';

export default function {section_name.replace(' ', '')}() {{
  return (
    <Layout title="{section_name} | {project_title}">
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">{section_name}</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              {section.get('description', section_name)}
            </p>
          </div>
          <div className="mt-10">
            <div className="prose prose-indigo prose-lg text-gray-500 mx-auto">
              {self._generate_section_content(section)}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}}
"""
                section_path = os.path.join(output_dir, f"{section_id}.js")
                self._create_file(section_path, section_js)
                generated_files.append(section_path)
        
        return generated_files
    
    def _generate_feature_cards(self, documentation: Dict[str, Any]) -> str:
        """
        Generate JSX for feature cards.
        
        Args:
            documentation: The documentation object
            
        Returns:
            JSX string with feature cards
        """
        features = documentation.get('features', [])
        if not features:
            return """
              <FeatureCard
                title="Feature 1"
                description="Description of feature 1"
              />
              <FeatureCard
                title="Feature 2"
                description="Description of feature 2"
              />
              <FeatureCard
                title="Feature 3"
                description="Description of feature 3"
              />
            """
        
        result = ""
        for feature in features:
            result += f"""
              <FeatureCard
                title="{feature.get('name', '')}"
                description="{feature.get('description', '')}"
              />
            """
        
        return result
    
    def _generate_additional_sections(self, documentation: Dict[str, Any]) -> str:
        """
        Generate JSX for additional sections based on content structure.
        
        Args:
            documentation: The documentation object
            
        Returns:
            JSX string with additional sections
        """
        content_structure = documentation.get('content_structure', [])
        if not content_structure:
            return ""
        
        result = ""
        for section in content_structure:
            section_name = section.get('section_name', '')
            if section_name.lower() == 'instagram feed':
                result += """
      <section id="instagram" className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">Instagram</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Follow Us on Instagram
            </p>
          </div>
          
          <div className="mt-10">
            {/* Import and use the InstagramFeed component */}
            {/* <InstagramFeed username="yourusername" count={6} /> */}
            
            {/* Placeholder for Instagram feed */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="bg-gray-200 rounded-lg aspect-square flex items-center justify-center">
                  <p className="text-gray-500">Instagram Post {i}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
                """
        
        return result
    
    def _generate_section_content(self, section: Dict[str, Any]) -> str:
        """
        Generate content for a section.
        
        Args:
            section: The section object
            
        Returns:
            JSX string with section content
        """
        content_elements = section.get('content_elements', [])
        if not content_elements:
            return "<p>Content coming soon...</p>"
        
        result = ""
        for element in content_elements:
            result += f"<p>{element}</p>\n"
        
        return result
    
    def generate_styles(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate styles based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated styles
            
        Returns:
            List of paths to the generated style files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Check if using Tailwind CSS
        using_tailwind = False
        tech_stack = documentation.get('tech_stack', [])
        for tech in tech_stack:
            if 'tailwind' in tech.get('name', '').lower():
                using_tailwind = True
                break
        
        # Generate globals.css
        if using_tailwind:
            globals_css = """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""
            # Generate tailwind.config.js in parent directory
            tailwind_config = """
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}
"""
            self._create_file(os.path.join(os.path.dirname(output_dir), 'tailwind.config.js'), tailwind_config)
            
            # Generate postcss.config.js in parent directory
            postcss_config = """
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
            self._create_file(os.path.join(os.path.dirname(output_dir), 'postcss.config.js'), postcss_config)
        else:
            globals_css = """
html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

* {
  box-sizing: border-box;
}

@media (prefers-color-scheme: dark) {
  html {
    color-scheme: dark;
  }
  body {
    color: white;
    background: black;
  }
}
"""
        
        globals_path = os.path.join(output_dir, 'globals.css')
        self._create_file(globals_path, globals_css)
        generated_files.append(globals_path)
        
        return generated_files
    
    def generate_assets(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate assets based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated assets
            
        Returns:
            List of paths to the generated asset files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Generate favicon.ico (empty file as placeholder)
        favicon_path = os.path.join(output_dir, 'favicon.ico')
        with open(favicon_path, 'wb') as f:
            f.write(b'')
        generated_files.append(favicon_path)
        
        # Generate robots.txt
        robots_txt = """
# Allow all crawlers
User-agent: *
Allow: /
"""
        robots_path = os.path.join(output_dir, 'robots.txt')
        self._create_file(robots_path, robots_txt)
        generated_files.append(robots_path)
        
        return generated_files
