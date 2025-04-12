# Installation Guide: DevBridge

This guide provides detailed instructions for installing and setting up the DevBridge platform on your system.

## System Requirements

### Hardware Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB+ recommended
- **Disk Space**: 1GB for the application, plus space for generated code and documentation

### Software Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Ubuntu 20.04+
- **Node.js**: Version 16.0.0 or higher
- **Python**: Version 3.10 or higher
- **npm**: Version 7.0.0 or higher
- **pip**: Version 21.0.0 or higher
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/devbridge.git
cd devbridge
```

### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend

```bash
# Navigate to frontend directory
cd ../ui

# Install dependencies
npm install
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cd ../backend
cp .env.example .env
```

Edit the `.env` file to add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
PORT=5000
```

Create a `.env.local` file in the frontend directory:

```bash
cd ../ui
cp .env.example .env.local
```

Edit the `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 5. Initialize Database

```bash
cd ../backend
python init_db.py
```

### 6. Start the Application

#### Start Backend Server

```bash
# Make sure you're in the backend directory
cd ../backend
python app.py
```

The backend server will start on http://localhost:5000

#### Start Frontend Development Server

In a new terminal:

```bash
# Navigate to frontend directory
cd path/to/devbridge/ui
npm run dev
```

The frontend will be available at http://localhost:3000

## Verifying Installation

1. Open your web browser and navigate to http://localhost:3000
2. You should see the DevBridge landing page
3. Try entering a simple prompt to test the system
4. Check the backend logs to ensure API calls are being processed

## Troubleshooting

### Common Issues

#### Backend Won't Start

- Check if Python and required packages are installed correctly
- Verify that the OpenAI API key is valid
- Ensure port 5000 is not in use by another application

#### Frontend Won't Start

- Verify Node.js and npm versions
- Check if all dependencies were installed correctly
- Ensure port 3000 is not in use by another application

#### API Connection Errors

- Confirm that the backend server is running
- Check that the NEXT_PUBLIC_API_URL in .env.local is correct
- Verify network connectivity between frontend and backend

#### OpenAI API Errors

- Ensure your API key is valid and has sufficient credits
- Check your internet connection
- Verify that your OpenAI account is in good standing

### Getting Help

If you encounter issues not covered in this guide:

1. Check the project's GitHub repository for known issues
2. Join our Discord community for real-time support
3. Contact our support team at support@devbridge.com

## Deployment

For production deployment, please refer to the `DEPLOYMENT.md` guide.

## Next Steps

After successful installation, refer to the `USER_GUIDE.md` for instructions on how to use the platform effectively.
