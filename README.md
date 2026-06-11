# DevBridge: AI-Powered Pre-Development Automation Platform
> Prompt → Documentation → Visualizations → Starter Code. Powered by GPT-4 and Gemini, with PDF/DOCX export and D3.js diagrams.
## Overview

DevBridge is an innovative platform that bridges the gap between client ideas and technical implementation. It transforms simple prompts like "a portfolio website with a contact form and Instagram feed" into comprehensive documentation, visualizations, and starter code.

## Features

### AI Documentation Generator
- Transforms simple prompts into detailed project documentation
- Generates project summaries, audience analysis, feature lists, and more
- Uses OpenAI's GPT-4 with specialized prompts for each section

### Interactive Visualizations
- Creates site maps showing the hierarchical structure of pages
- Displays component relationship diagrams
- Generates user flow diagrams
- Provides interactive editing capabilities

### Export Functionality
- Exports documentation to PDF with professional formatting
- Creates DOCX files for easy editing
- Maintains consistent styling across all export formats

### Code Generation
- Generates React/Next.js frontend code with responsive components
- Creates Node.js/Express backend APIs with proper structure
- Builds OpenAI-powered AI agents for project assistance
- Produces ready-to-use starter code based on documentation

## Architecture

The platform consists of several key components:

1. **Documentation Generator**: Processes user prompts and generates structured documentation
2. **Visualization Engine**: Creates interactive diagrams based on the documentation
3. **Export Engine**: Converts documentation to various formats
4. **Code Generation System**: Produces starter code for different technologies
5. **Web Interface**: Provides a user-friendly interface for the entire process

## Installation

### Prerequisites
- Node.js 16+
- Python 3.10+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/harshaldonarkar/dev_bridge.git
cd devbridge
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../ui
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file to add your OpenAI API key
```

5. Start the development server:
```bash
# Start backend
cd backend
python app.py

# In another terminal, start frontend
cd ui
npm run dev
```

6. Access the application at http://localhost:3000

## Usage

1. **Enter a prompt**: Start by entering a simple description of your project
2. **Review documentation**: The AI will generate comprehensive documentation
3. **Explore visualizations**: View and edit the structure of your project
4. **Export documentation**: Download as PDF or DOCX
5. **Generate code**: Create starter code for your project

## Project Structure

```
devbridge/
├── backend/
│   ├── documentation_generator/
│   ├── visualization/
│   ├── export/
│   ├── code_generation/
│   └── app.py
├── ui/
│   ├── components/
│   ├── pages/
│   └── styles/
└── tests/
```

## Technologies Used

- **Frontend**: React, Next.js, D3.js
- **Backend**: Python, Flask, OpenAI API
- **Code Generation**: Node.js, Express, React
- **Export**: pdfkit, python-docx

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
