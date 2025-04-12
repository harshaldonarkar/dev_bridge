"""
OpenAI Agent Generator

This module generates AI agent code based on the AI-generated documentation.
It implements the AIAgentGenerator interface from the code_generation_architecture module.
"""

import os
import json
import shutil
from typing import Dict, List, Any
from .code_generation_architecture import AIAgentGenerator

class OpenAIAgentGenerator(AIAgentGenerator):
    """
    Generates OpenAI-based AI agent code.
    """
    
    def __init__(self, config=None):
        """
        Initialize the OpenAI agent generator.
        
        Args:
            config: Configuration options for the generator
        """
        super().__init__(config)
        self.template_dir = self.config.get('template_dir', os.path.join(os.path.dirname(__file__), 'templates', 'openai_agent'))
    
    def generate_code(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate an OpenAI-based AI agent based on the documentation.
        
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
        
        # Generate agent definition
        self.generate_agent_definition(documentation, output_dir)
        
        # Generate agent logic
        self.generate_agent_logic(documentation, output_dir)
        
        # Generate agent integration
        self.generate_agent_integration(documentation, output_dir)
        
        # Create package
        package_name = documentation.get('project_summary', {}).get('title', 'ai_agent').replace(' ', '_').lower() + '_agent'
        return self._create_package(output_dir, os.path.join(os.path.dirname(output_dir), package_name))
    
    def _generate_project_structure(self, documentation: Dict[str, Any], output_dir: str) -> None:
        """
        Generate the basic project structure.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated code
        """
        # Create directories
        os.makedirs(os.path.join(output_dir, 'prompts'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'functions'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'utils'), exist_ok=True)
        
        # Generate package.json
        package_json = {
            "name": documentation.get('project_summary', {}).get('title', 'ai_agent').replace(' ', '-').lower() + '-agent',
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "start": "node index.js",
                "dev": "nodemon index.js",
                "test": "jest"
            },
            "dependencies": {
                "openai": "^4.0.0",
                "dotenv": "^16.0.3",
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "body-parser": "^1.20.1"
            },
            "devDependencies": {
                "nodemon": "^2.0.20",
                "jest": "^29.3.1"
            }
        }
        
        # Write package.json
        self._create_file(os.path.join(output_dir, 'package.json'), json.dumps(package_json, indent=2))
        
        # Generate .env
        env_content = """
OPENAI_API_KEY=your_openai_api_key
PORT=3001
"""
        self._create_file(os.path.join(output_dir, '.env'), env_content)
        
        # Generate .gitignore
        gitignore = """
# dependencies
/node_modules

# environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# misc
.DS_Store
"""
        self._create_file(os.path.join(output_dir, '.gitignore'), gitignore)
        
        # Generate README.md
        readme = f"""
# {documentation.get('project_summary', {}).get('title', 'AI Agent')} Agent

An AI agent for {documentation.get('project_summary', {}).get('title', 'your project')}.

## Description

{documentation.get('project_summary', {}).get('description', 'An AI agent built with OpenAI API.')}

## Getting Started

First, install dependencies:

```bash
npm install
# or
yarn install
```

Then, set up your environment variables by copying the `.env.example` file to `.env` and adding your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
PORT=3001
```

Finally, run the development server:

```bash
npm run dev
# or
yarn dev
```

The API will be available at [http://localhost:3001](http://localhost:3001).

## Features

{self._generate_features_list(documentation)}

## API Endpoints

- `POST /api/agent/chat` - Send a message to the agent
- `POST /api/agent/function` - Execute a specific agent function

## Project Structure

- `/prompts` - System prompts and instructions for the agent
- `/functions` - Function definitions and implementations
- `/utils` - Utility functions
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
            return "- Natural language understanding\n- Task automation\n- Integration with external systems"
        
        result = ""
        for feature in features:
            result += f"- **{feature.get('name', '')}**: {feature.get('description', '')}\n"
        
        return result
    
    def generate_agent_definition(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate AI agent definition based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated definition
            
        Returns:
            Path to the generated definition file
        """
        # Generate system prompt
        project_title = documentation.get('project_summary', {}).get('title', 'AI Agent')
        project_description = documentation.get('project_summary', {}).get('description', 'An AI agent built with OpenAI API.')
        
        system_prompt = f"""
You are an AI assistant for {project_title}. Your purpose is to help users with their tasks related to this project.

About the project:
{project_description}

Your capabilities include:
1. Answering questions about {project_title}
2. Helping users understand the features and functionality
3. Providing guidance on how to use the system
4. Assisting with troubleshooting common issues

When responding to users:
- Be helpful, concise, and accurate
- If you don't know something, admit it rather than making up information
- Use a friendly and professional tone
- Format your responses for readability when appropriate
"""
        
        # Add features to system prompt
        features = documentation.get('features', [])
        if features:
            system_prompt += "\n\nKey features of the project:\n"
            for i, feature in enumerate(features, 1):
                system_prompt += f"{i}. {feature.get('name', '')}: {feature.get('description', '')}\n"
        
        # Add tech stack to system prompt
        tech_stack = documentation.get('tech_stack', [])
        if tech_stack:
            system_prompt += "\n\nTechnology stack:\n"
            for tech in tech_stack:
                system_prompt += f"- {tech.get('name', '')}: {tech.get('description', '')}\n"
        
        # Write system prompt to file
        system_prompt_path = os.path.join(output_dir, 'prompts', 'system_prompt.txt')
        self._create_file(system_prompt_path, system_prompt)
        
        # Generate agent definition
        agent_definition = {
            "name": f"{project_title} Assistant",
            "description": f"An AI assistant for {project_title}",
            "instructions": system_prompt,
            "capabilities": [
                "chat",
                "function_calling"
            ],
            "tools": []
        }
        
        # Add tools based on features
        for feature in features:
            feature_name = feature.get('name', '').lower().replace(' ', '_')
            if feature_name:
                agent_definition["tools"].append({
                    "type": "function",
                    "function": {
                        "name": f"get_{feature_name}_info",
                        "description": f"Get information about {feature.get('name', '')}",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "detail_level": {
                                    "type": "string",
                                    "enum": ["basic", "detailed"],
                                    "description": "Level of detail to provide"
                                }
                            },
                            "required": ["detail_level"]
                        }
                    }
                })
        
        # Add general tools
        agent_definition["tools"].extend([
            {
                "type": "function",
                "function": {
                    "name": "search_documentation",
                    "description": "Search the project documentation for specific information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_implementation_steps",
                    "description": "Get steps to implement a specific feature or component",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "Feature or component name"
                            }
                        },
                        "required": ["feature"]
                    }
                }
            }
        ])
        
        # Write agent definition to file
        agent_definition_path = os.path.join(output_dir, 'agent_definition.json')
        self._create_file(agent_definition_path, json.dumps(agent_definition, indent=2))
        
        return agent_definition_path
    
    def generate_agent_logic(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate AI agent logic based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated logic
            
        Returns:
            List of paths to the generated logic files
        """
        generated_files = []
        
        # Generate agent.js
        agent_js = """
const { OpenAI } = require('openai');
const fs = require('fs');
const path = require('path');
const functions = require('./functions');

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Load system prompt
const systemPrompt = fs.readFileSync(
  path.join(__dirname, 'prompts', 'system_prompt.txt'),
  'utf8'
);

/**
 * Agent class for handling conversations and function calls
 */
class Agent {
  constructor() {
    this.conversations = {};
  }
  
  /**
   * Process a user message
   * @param {string} userId - User identifier
   * @param {string} message - User message
   * @returns {Promise<Object>} - Agent response
   */
  async processMessage(userId, message) {
    try {
      // Initialize conversation if it doesn't exist
      if (!this.conversations[userId]) {
        this.conversations[userId] = {
          messages: [
            { role: 'system', content: systemPrompt }
          ]
        };
      }
      
      // Add user message to conversation
      this.conversations[userId].messages.push({
        role: 'user',
        content: message
      });
      
      // Call OpenAI API
      const response = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: this.conversations[userId].messages,
        tools: this._getToolDefinitions(),
        tool_choice: 'auto',
      });
      
      const responseMessage = response.choices[0].message;
      
      // Handle function calls
      if (responseMessage.tool_calls) {
        const toolResults = await this._handleToolCalls(responseMessage.tool_calls);
        
        // Add assistant message with function calls to conversation
        this.conversations[userId].messages.push(responseMessage);
        
        // Add function results to conversation
        for (const result of toolResults) {
          this.conversations[userId].messages.push({
            role: 'tool',
            tool_call_id: result.tool_call_id,
            content: result.content,
          });
        }
        
        // Get final response after function calls
        const finalResponse = await openai.chat.completions.create({
          model: 'gpt-4',
          messages: this.conversations[userId].messages,
        });
        
        const finalResponseMessage = finalResponse.choices[0].message;
        
        // Add final assistant message to conversation
        this.conversations[userId].messages.push(finalResponseMessage);
        
        return {
          role: 'assistant',
          content: finalResponseMessage.content,
          function_calls: responseMessage.tool_calls,
          function_results: toolResults
        };
      }
      
      // Add assistant message to conversation
      this.conversations[userId].messages.push(responseMessage);
      
      return {
        role: 'assistant',
        content: responseMessage.content
      };
    } catch (error) {
      console.error('Error processing message:', error);
      throw error;
    }
  }
  
  /**
   * Execute a specific function
   * @param {string} functionName - Function name
   * @param {Object} parameters - Function parameters
   * @returns {Promise<Object>} - Function result
   */
  async executeFunction(functionName, parameters) {
    try {
      if (!functions[functionName]) {
        throw new Error(`Function ${functionName} not found`);
      }
      
      const result = await functions[functionName](parameters);
      return { success: true, result };
    } catch (error) {
      console.error(`Error executing function ${functionName}:`, error);
      return { success: false, error: error.message };
    }
  }
  
  /**
   * Handle tool calls from OpenAI
   * @private
   * @param {Array} toolCalls - Tool calls from OpenAI
   * @returns {Promise<Array>} - Tool results
   */
  async _handleToolCalls(toolCalls) {
    const results = [];
    
    for (const toolCall of toolCalls) {
      if (toolCall.type === 'function') {
        const functionName = toolCall.function.name;
        const functionArgs = JSON.parse(toolCall.function.arguments);
        
        try {
          const result = await this.executeFunction(functionName, functionArgs);
          results.push({
            tool_call_id: toolCall.id,
            content: JSON.stringify(result)
          });
        } catch (error) {
          results.push({
            tool_call_id: toolCall.id,
            content: JSON.stringify({ error: error.message })
          });
        }
      }
    }
    
    return results;
  }
  
  /**
   * Get tool definitions for OpenAI API
   * @private
   * @returns {Array} - Tool definitions
   */
  _getToolDefinitions() {
    return Object.entries(functions).map(([name, func]) => ({
      type: 'function',
      function: {
        name,
        description: func.description,
        parameters: func.parameters
      }
    }));
  }
}

module.exports = new Agent();
"""
        agent_js_path = os.path.join(output_dir, 'agent.js')
        self._create_file(agent_js_path, agent_js)
        generated_files.append(agent_js_path)
        
        # Generate index.js
        index_js = """
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const agent = require('./agent');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Routes
app.post('/api/agent/chat', async (req, res) => {
  try {
    const { userId, message } = req.body;
    
    if (!userId || !message) {
      return res.status(400).json({
        success: false,
        error: 'userId and message are required'
      });
    }
    
    const response = await agent.processMessage(userId, message);
    
    return res.json({
      success: true,
      response
    });
  } catch (error) {
    console.error('Error in chat endpoint:', error);
    return res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.post('/api/agent/function', async (req, res) => {
  try {
    const { functionName, parameters } = req.body;
    
    if (!functionName) {
      return res.status(400).json({
        success: false,
        error: 'functionName is required'
      });
    }
    
    const result = await agent.executeFunction(functionName, parameters || {});
    
    return res.json({
      success: true,
      result
    });
  } catch (error) {
    console.error('Error in function endpoint:', error);
    return res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Agent server running on port ${PORT}`);
});
"""
        index_js_path = os.path.join(output_dir, 'index.js')
        self._create_file(index_js_path, index_js)
        generated_files.append(index_js_path)
        
        # Generate functions/index.js
        functions_index_js = """
const searchDocumentation = require('./searchDocumentation');
const getImplementationSteps = require('./getImplementationSteps');
"""
        
        # Add feature-specific functions
        features = documentation.get('features', [])
        for feature in features:
            feature_name = feature.get('name', '').lower().replace(' ', '_')
            if feature_name:
                functions_index_js += f"const get{feature_name.replace('_', ' ').title().replace(' ', '')}Info = require('./get{feature_name.replace('_', ' ').title().replace(' ', '')}Info');\n"
        
        functions_index_js += "\nmodule.exports = {\n"
        functions_index_js += "  searchDocumentation,\n"
        functions_index_js += "  getImplementationSteps,\n"
        
        # Add feature-specific functions to exports
        for feature in features:
            feature_name = feature.get('name', '').lower().replace(' ', '_')
            if feature_name:
                function_name = f"get{feature_name.replace('_', ' ').title().replace(' ', '')}Info"
                functions_index_js += f"  {function_name},\n"
        
        functions_index_js += "};\n"
        
        functions_index_js_path = os.path.join(output_dir, 'functions', 'index.js')
        self._create_file(functions_index_js_path, functions_index_js)
        generated_files.append(functions_index_js_path)
        
        # Generate searchDocumentation.js
        search_documentation_js = """
/**
 * Search the project documentation for specific information
 * @param {Object} params - Function parameters
 * @param {string} params.query - Search query
 * @returns {Promise<Object>} - Search results
 */
async function searchDocumentation({ query }) {
  // In a real implementation, this would search through actual documentation
  console.log(`Searching documentation for: ${query}`);
  
  // Simulate search results
  const results = [
    {
      title: 'Getting Started',
      content: 'Information about getting started with the project...',
      relevance: 0.95
    },
    {
      title: 'API Reference',
      content: 'API documentation and reference...',
      relevance: 0.85
    },
    {
      title: 'Troubleshooting',
      content: 'Common issues and solutions...',
      relevance: 0.75
    }
  ];
  
  return {
    query,
    results
  };
}

// Function metadata
searchDocumentation.description = 'Search the project documentation for specific information';
searchDocumentation.parameters = {
  type: 'object',
  properties: {
    query: {
      type: 'string',
      description: 'Search query'
    }
  },
  required: ['query']
};

module.exports = searchDocumentation;
"""
        search_documentation_js_path = os.path.join(output_dir, 'functions', 'searchDocumentation.js')
        self._create_file(search_documentation_js_path, search_documentation_js)
        generated_files.append(search_documentation_js_path)
        
        # Generate getImplementationSteps.js
        get_implementation_steps_js = """
/**
 * Get steps to implement a specific feature or component
 * @param {Object} params - Function parameters
 * @param {string} params.feature - Feature or component name
 * @returns {Promise<Object>} - Implementation steps
 */
async function getImplementationSteps({ feature }) {
  // In a real implementation, this would retrieve actual implementation steps
  console.log(`Getting implementation steps for: ${feature}`);
  
  // Simulate implementation steps
  const steps = [
    {
      step: 1,
      title: 'Setup environment',
      description: 'Set up the development environment and install dependencies.'
    },
    {
      step: 2,
      title: 'Create basic structure',
      description: 'Create the basic file structure for the feature.'
    },
    {
      step: 3,
      title: 'Implement core functionality',
      description: 'Implement the core functionality of the feature.'
    },
    {
      step: 4,
      title: 'Add tests',
      description: 'Write tests to ensure the feature works correctly.'
    },
    {
      step: 5,
      title: 'Document',
      description: 'Document the feature and its usage.'
    }
  ];
  
  return {
    feature,
    steps
  };
}

// Function metadata
getImplementationSteps.description = 'Get steps to implement a specific feature or component';
getImplementationSteps.parameters = {
  type: 'object',
  properties: {
    feature: {
      type: 'string',
      description: 'Feature or component name'
    }
  },
  required: ['feature']
};

module.exports = getImplementationSteps;
"""
        get_implementation_steps_js_path = os.path.join(output_dir, 'functions', 'getImplementationSteps.js')
        self._create_file(get_implementation_steps_js_path, get_implementation_steps_js)
        generated_files.append(get_implementation_steps_js_path)
        
        # Generate feature-specific functions
        for feature in features:
            feature_name = feature.get('name', '')
            if not feature_name:
                continue
            
            function_name = f"get{feature_name.replace(' ', '')}Info"
            file_name = function_name + '.js'
            
            function_content = f"""
/**
 * Get information about {feature_name}
 * @param {{Object}} params - Function parameters
 * @param {{string}} params.detail_level - Level of detail to provide
 * @returns {{Promise<Object>}} - Feature information
 */
async function {function_name}({{ detail_level }}) {{
  console.log(`Getting {feature_name} info with detail level: ${{detail_level}}`);
  
  const basicInfo = {{
    name: '{feature_name}',
    description: '{feature.get('description', '')}',
    priority: '{feature.get('priority', 'Medium')}'
  }};
  
  if (detail_level === 'basic') {{
    return basicInfo;
  }}
  
  // Detailed information
  return {{
    ...basicInfo,
    details: {json.dumps(feature.get('details', []), indent=2)},
    implementation_time: '{feature.get('estimated_time', 'Not specified')}',
    dependencies: {json.dumps(feature.get('dependencies', []), indent=2)}
  }};
}}

// Function metadata
{function_name}.description = 'Get information about {feature_name}';
{function_name}.parameters = {{
  type: 'object',
  properties: {{
    detail_level: {{
      type: 'string',
      enum: ['basic', 'detailed'],
      description: 'Level of detail to provide'
    }}
  }},
  required: ['detail_level']
}};

module.exports = {function_name};
"""
            
            function_path = os.path.join(output_dir, 'functions', file_name)
            self._create_file(function_path, function_content)
            generated_files.append(function_path)
        
        return generated_files
    
    def generate_agent_integration(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate AI agent integration code based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated integration code
            
        Returns:
            List of paths to the generated integration files
        """
        generated_files = []
        
        # Generate utils/logger.js
        logger_js = """
/**
 * Logger utility
 */
class Logger {
  /**
   * Log an info message
   * @param {string} message - Message to log
   * @param {Object} data - Additional data
   */
  info(message, data = {}) {
    console.log(`[INFO] ${message}`, data);
  }
  
  /**
   * Log an error message
   * @param {string} message - Message to log
   * @param {Error|Object} error - Error object or additional data
   */
  error(message, error = {}) {
    console.error(`[ERROR] ${message}`, error);
  }
  
  /**
   * Log a warning message
   * @param {string} message - Message to log
   * @param {Object} data - Additional data
   */
  warn(message, data = {}) {
    console.warn(`[WARN] ${message}`, data);
  }
  
  /**
   * Log a debug message
   * @param {string} message - Message to log
   * @param {Object} data - Additional data
   */
  debug(message, data = {}) {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`[DEBUG] ${message}`, data);
    }
  }
}

module.exports = new Logger();
"""
        logger_js_path = os.path.join(output_dir, 'utils', 'logger.js')
        self._create_file(logger_js_path, logger_js)
        generated_files.append(logger_js_path)
        
        # Generate frontend integration example
        frontend_integration_js = """
/**
 * Example frontend integration with the AI agent
 * 
 * This is a JavaScript module that can be used in a frontend application
 * to communicate with the AI agent API.
 */

/**
 * AI Agent Client
 */
class AgentClient {
  /**
   * Constructor
   * @param {string} baseUrl - Base URL of the agent API
   */
  constructor(baseUrl = 'http://localhost:3001') {
    this.baseUrl = baseUrl;
    this.userId = this._generateUserId();
  }
  
  /**
   * Send a message to the agent
   * @param {string} message - User message
   * @returns {Promise<Object>} - Agent response
   */
  async sendMessage(message) {
    try {
      const response = await fetch(`${this.baseUrl}/api/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          userId: this.userId,
          message
        })
      });
      
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Unknown error');
      }
      
      return data.response;
    } catch (error) {
      console.error('Error sending message to agent:', error);
      throw error;
    }
  }
  
  /**
   * Execute a specific function
   * @param {string} functionName - Function name
   * @param {Object} parameters - Function parameters
   * @returns {Promise<Object>} - Function result
   */
  async executeFunction(functionName, parameters = {}) {
    try {
      const response = await fetch(`${this.baseUrl}/api/agent/function`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          functionName,
          parameters
        })
      });
      
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Unknown error');
      }
      
      return data.result;
    } catch (error) {
      console.error(`Error executing function ${functionName}:`, error);
      throw error;
    }
  }
  
  /**
   * Generate a unique user ID
   * @private
   * @returns {string} - User ID
   */
  _generateUserId() {
    return 'user_' + Math.random().toString(36).substring(2, 15);
  }
}

// Example usage:
/*
const agent = new AgentClient();

// Send a message
agent.sendMessage('Tell me about the project')
  .then(response => {
    console.log('Agent response:', response);
  })
  .catch(error => {
    console.error('Error:', error);
  });

// Execute a function
agent.executeFunction('searchDocumentation', { query: 'API' })
  .then(result => {
    console.log('Function result:', result);
  })
  .catch(error => {
    console.error('Error:', error);
  });
*/

// Export the client
// export default AgentClient;  // ES modules
// module.exports = AgentClient;  // CommonJS
"""
        frontend_integration_js_path = os.path.join(output_dir, 'frontend-integration.js')
        self._create_file(frontend_integration_js_path, frontend_integration_js)
        generated_files.append(frontend_integration_js_path)
        
        # Generate React component example
        react_component_js = """
/**
 * Example React component for integrating with the AI agent
 * 
 * This is a React component that can be used in a React application
 * to provide a chat interface with the AI agent.
 */

/*
import React, { useState, useEffect, useRef } from 'react';
import AgentClient from './agent-client';

const agent = new AgentClient();

function AgentChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: input
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Send message to agent
      const response = await agent.sendMessage(input.trim());
      
      // Add agent response to chat
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: response.content,
        functionCalls: response.function_calls,
        functionResults: response.function_results
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to chat
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="agent-chat">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
            {message.functionCalls && (
              <div className="function-calls">
                <div className="function-call-label">Function calls:</div>
                {message.functionCalls.map((call, callIndex) => (
                  <div key={callIndex} className="function-call">
                    {call.function.name}({call.function.arguments})
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message assistant loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

export default AgentChat;
*/
"""
        react_component_js_path = os.path.join(output_dir, 'AgentChat.jsx')
        self._create_file(react_component_js_path, react_component_js)
        generated_files.append(react_component_js_path)
        
        return generated_files
