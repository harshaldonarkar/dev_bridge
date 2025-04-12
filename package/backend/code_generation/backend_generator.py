"""
Node.js/Express Backend Generator

This module generates a Node.js/Express backend based on the AI-generated documentation.
It implements the BackendGenerator interface from the code_generation_architecture module.
"""

import os
import json
import shutil
from typing import Dict, List, Any
from .code_generation_architecture import BackendGenerator

class NodeExpressGenerator(BackendGenerator):
    """
    Generates a Node.js/Express backend application.
    """
    
    def __init__(self, config=None):
        """
        Initialize the Node.js/Express generator.
        
        Args:
            config: Configuration options for the generator
        """
        super().__init__(config)
        self.template_dir = self.config.get('template_dir', os.path.join(os.path.dirname(__file__), 'templates', 'node_express'))
    
    def generate_code(self, documentation: Dict[str, Any], output_dir: str) -> str:
        """
        Generate a Node.js/Express application based on the documentation.
        
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
        
        # Generate models
        self.generate_models(documentation, os.path.join(output_dir, 'models'))
        
        # Generate controllers
        self.generate_controllers(documentation, os.path.join(output_dir, 'controllers'))
        
        # Generate routes
        self.generate_routes(documentation, os.path.join(output_dir, 'routes'))
        
        # Generate services
        self.generate_services(documentation, os.path.join(output_dir, 'services'))
        
        # Create package
        package_name = documentation.get('project_summary', {}).get('title', 'backend').replace(' ', '_').lower()
        return self._create_package(output_dir, os.path.join(os.path.dirname(output_dir), package_name))
    
    def _generate_project_structure(self, documentation: Dict[str, Any], output_dir: str) -> None:
        """
        Generate the basic project structure.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated code
        """
        # Create directories
        os.makedirs(os.path.join(output_dir, 'models'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'controllers'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'routes'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'services'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'middleware'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'config'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'utils'), exist_ok=True)
        
        # Generate package.json
        package_json = {
            "name": documentation.get('project_summary', {}).get('title', 'backend').replace(' ', '-').lower(),
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js",
                "test": "jest"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "dotenv": "^16.0.3",
                "helmet": "^6.0.1",
                "morgan": "^1.10.0"
            },
            "devDependencies": {
                "nodemon": "^2.0.20",
                "jest": "^29.3.1"
            }
        }
        
        # Add additional dependencies based on tech stack
        tech_stack = documentation.get('tech_stack', [])
        for tech in tech_stack:
            if tech.get('category') == 'Backend':
                if 'mongodb' in tech.get('name', '').lower():
                    package_json['dependencies']['mongoose'] = "^6.8.0"
                elif 'postgresql' in tech.get('name', '').lower() or 'postgres' in tech.get('name', '').lower():
                    package_json['dependencies']['pg'] = "^8.8.0"
                    package_json['dependencies']['sequelize'] = "^6.28.0"
                elif 'mysql' in tech.get('name', '').lower():
                    package_json['dependencies']['mysql2'] = "^2.3.3"
                    package_json['dependencies']['sequelize'] = "^6.28.0"
                
                if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                    package_json['dependencies']['jsonwebtoken'] = "^9.0.0"
                    package_json['dependencies']['bcrypt'] = "^5.1.0"
                    package_json['dependencies']['passport'] = "^0.6.0"
                    package_json['dependencies']['passport-jwt'] = "^4.0.1"
                    package_json['dependencies']['passport-local'] = "^1.0.0"
        
        # Write package.json
        self._create_file(os.path.join(output_dir, 'package.json'), json.dumps(package_json, indent=2))
        
        # Generate .env
        env_content = """
PORT=5000
NODE_ENV=development
"""
        
        # Add database connection string based on tech stack
        for tech in tech_stack:
            if tech.get('category') == 'Database':
                if 'mongodb' in tech.get('name', '').lower():
                    env_content += "MONGODB_URI=mongodb://localhost:27017/your_database\n"
                elif 'postgresql' in tech.get('name', '').lower() or 'postgres' in tech.get('name', '').lower():
                    env_content += "DATABASE_URL=postgresql://postgres:password@localhost:5432/your_database\n"
                elif 'mysql' in tech.get('name', '').lower():
                    env_content += "DATABASE_URL=mysql://root:password@localhost:3306/your_database\n"
        
        # Add JWT secret if authentication is needed
        for tech in tech_stack:
            if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                env_content += "JWT_SECRET=your_jwt_secret_key\n"
                env_content += "JWT_EXPIRES_IN=90d\n"
        
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
# {documentation.get('project_summary', {}).get('title', 'Backend API')}

{documentation.get('project_summary', {}).get('description', 'A Node.js/Express backend API.')}

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

The API will be available at [http://localhost:5000](http://localhost:5000).

## Features

{self._generate_features_list(documentation)}

## Tech Stack

{self._generate_tech_stack_list(documentation)}

## API Endpoints

{self._generate_api_endpoints_list(documentation)}

## Project Structure

- `/models` - Database models
- `/controllers` - Request handlers
- `/routes` - API routes
- `/services` - Business logic
- `/middleware` - Express middleware
- `/config` - Configuration files
- `/utils` - Utility functions
"""
        self._create_file(os.path.join(output_dir, 'README.md'), readme)
        
        # Generate server.js
        server_js = """
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Import routes
const indexRouter = require('./routes/index');
"""
        
        # Add additional imports based on features
        features = documentation.get('features', [])
        for feature in features:
            feature_name = feature.get('name', '').lower().replace(' ', '_')
            if feature_name:
                server_js += f"const {feature_name}Router = require('./routes/{feature_name}');\n"
        
        server_js += """
// Initialize Express app
const app = express();

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // Enable CORS
app.use(morgan('dev')); // Request logging
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies

// Routes
app.use('/', indexRouter);
"""
        
        # Add additional routes based on features
        for feature in features:
            feature_name = feature.get('name', '').lower().replace(' ', '_')
            if feature_name:
                server_js += f"app.use('/api/{feature_name}', {feature_name}Router);\n"
        
        server_js += """
// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    status: 'error',
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app; // For testing
"""
        self._create_file(os.path.join(output_dir, 'server.js'), server_js)
        
        # Generate config/db.js based on tech stack
        db_js = """
// Database configuration
"""
        
        for tech in tech_stack:
            if tech.get('category') == 'Database':
                if 'mongodb' in tech.get('name', '').lower():
                    db_js = """
const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`Error connecting to MongoDB: ${error.message}`);
    process.exit(1);
  }
};

module.exports = connectDB;
"""
                elif 'postgresql' in tech.get('name', '').lower() or 'postgres' in tech.get('name', '').lower() or 'mysql' in tech.get('name', '').lower():
                    db_js = """
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: process.env.DATABASE_URL.startsWith('mysql') ? 'mysql' : 'postgres',
  logging: false,
});

const connectDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('Database connection established successfully');
  } catch (error) {
    console.error(`Error connecting to database: ${error.message}`);
    process.exit(1);
  }
};

module.exports = {
  sequelize,
  connectDB
};
"""
        
        self._create_file(os.path.join(output_dir, 'config', 'db.js'), db_js)
        
        # Generate middleware/auth.js if authentication is needed
        for tech in tech_stack:
            if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                auth_js = """
const jwt = require('jsonwebtoken');
const { promisify } = require('util');

/**
 * Middleware to protect routes that require authentication
 */
exports.protect = async (req, res, next) => {
  try {
    // 1) Get token from Authorization header
    let token;
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
      token = req.headers.authorization.split(' ')[1];
    }
    
    if (!token) {
      return res.status(401).json({
        status: 'error',
        message: 'You are not logged in. Please log in to get access.'
      });
    }
    
    // 2) Verify token
    const decoded = await promisify(jwt.verify)(token, process.env.JWT_SECRET);
    
    // 3) Check if user still exists
    // In a real implementation, you would check if the user still exists in the database
    // const currentUser = await User.findById(decoded.id);
    // if (!currentUser) {
    //   return res.status(401).json({
    //     status: 'error',
    //     message: 'The user belonging to this token no longer exists.'
    //   });
    // }
    
    // 4) Grant access to protected route
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      status: 'error',
      message: 'Invalid token. Please log in again.'
    });
  }
};

/**
 * Middleware to restrict access to certain roles
 */
exports.restrictTo = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        status: 'error',
        message: 'You do not have permission to perform this action'
      });
    }
    
    next();
  };
};
"""
                self._create_file(os.path.join(output_dir, 'middleware', 'auth.js'), auth_js)
        
        # Generate utils/catchAsync.js
        catch_async_js = """
/**
 * Wrapper function to catch async errors
 * @param {Function} fn - Async function to wrap
 * @returns {Function} - Express middleware function
 */
module.exports = fn => {
  return (req, res, next) => {
    fn(req, res, next).catch(next);
  };
};
"""
        self._create_file(os.path.join(output_dir, 'utils', 'catchAsync.js'), catch_async_js)
        
        # Generate utils/apiResponse.js
        api_response_js = """
/**
 * Standard API response format
 */
exports.success = (res, data, statusCode = 200) => {
  return res.status(statusCode).json({
    status: 'success',
    data
  });
};

exports.error = (res, message, statusCode = 400) => {
  return res.status(statusCode).json({
    status: 'error',
    message
  });
};
"""
        self._create_file(os.path.join(output_dir, 'utils', 'apiResponse.js'), api_response_js)
        
        # Generate routes/index.js
        index_route_js = """
const express = require('express');
const router = express.Router();

/**
 * @route   GET /
 * @desc    API status check
 * @access  Public
 */
router.get('/', (req, res) => {
  res.json({
    status: 'success',
    message: 'API is running'
  });
});

module.exports = router;
"""
        self._create_file(os.path.join(output_dir, 'routes', 'index.js'), index_route_js)
    
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
        Generate a markdown list of backend technologies.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Markdown string with tech stack list
        """
        tech_stack = documentation.get('tech_stack', [])
        if not tech_stack:
            return "- Node.js\n- Express\n"
        
        result = ""
        for tech in tech_stack:
            if tech.get('category') in ['Backend', 'Database']:
                result += f"- **{tech.get('name', '')}**: {tech.get('description', '')}\n"
        
        if not result:
            return "- Node.js\n- Express\n"
        
        return result
    
    def _generate_api_endpoints_list(self, documentation: Dict[str, Any]) -> str:
        """
        Generate a markdown list of API endpoints based on features.
        
        Args:
            documentation: The documentation object
            
        Returns:
            Markdown string with API endpoints list
        """
        features = documentation.get('features', [])
        if not features:
            return "- `GET /` - API status check"
        
        result = "- `GET /` - API status check\n"
        
        for feature in features:
            feature_name = feature.get('name', '').lower().replace(' ', '_')
            if feature_name:
                result += f"- `GET /api/{feature_name}` - Get all {feature.get('name', '')}\n"
                result += f"- `GET /api/{feature_name}/:id` - Get {feature.get('name', '')} by ID\n"
                result += f"- `POST /api/{feature_name}` - Create new {feature.get('name', '')}\n"
                result += f"- `PUT /api/{feature_name}/:id` - Update {feature.get('name', '')} by ID\n"
                result += f"- `DELETE /api/{feature_name}/:id` - Delete {feature.get('name', '')} by ID\n"
        
        return result
    
    def generate_models(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate data models based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated models
            
        Returns:
            List of paths to the generated model files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Determine database type from tech stack
        db_type = 'mongodb'  # Default to MongoDB
        tech_stack = documentation.get('tech_stack', [])
        for tech in tech_stack:
            if tech.get('category') == 'Database':
                if 'postgresql' in tech.get('name', '').lower() or 'postgres' in tech.get('name', '').lower() or 'mysql' in tech.get('name', '').lower():
                    db_type = 'sql'
        
        # Generate models based on features
        features = documentation.get('features', [])
        for feature in features:
            feature_name = feature.get('name', '')
            if not feature_name:
                continue
            
            model_name = feature_name.replace(' ', '')
            file_name = model_name.lower() + '.js'
            
            if db_type == 'mongodb':
                model_content = self._generate_mongoose_model(feature)
            else:
                model_content = self._generate_sequelize_model(feature)
            
            model_path = os.path.join(output_dir, file_name)
            self._create_file(model_path, model_content)
            generated_files.append(model_path)
        
        # Generate User model if authentication is needed
        for tech in tech_stack:
            if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                if db_type == 'mongodb':
                    user_model = """
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Please provide your name']
  },
  email: {
    type: String,
    required: [true, 'Please provide your email'],
    unique: true,
    lowercase: true,
    match: [/^\\S+@\\S+\\.\\S+$/, 'Please provide a valid email address']
  },
  password: {
    type: String,
    required: [true, 'Please provide a password'],
    minlength: 8,
    select: false
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  // Only run this function if password was modified
  if (!this.isModified('password')) return next();
  
  // Hash the password with cost of 12
  this.password = await bcrypt.hash(this.password, 12);
  
  next();
});

// Method to check if password is correct
userSchema.methods.correctPassword = async function(candidatePassword, userPassword) {
  return await bcrypt.compare(candidatePassword, userPassword);
};

const User = mongoose.model('User', userSchema);

module.exports = User;
"""
                else:
                    user_model = """
const { DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');
const { sequelize } = require('../config/db');

const User = sequelize.define('User', {
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [8, 100]
    }
  },
  role: {
    type: DataTypes.ENUM('user', 'admin'),
    defaultValue: 'user'
  }
}, {
  hooks: {
    beforeCreate: async (user) => {
      user.password = await bcrypt.hash(user.password, 12);
    },
    beforeUpdate: async (user) => {
      if (user.changed('password')) {
        user.password = await bcrypt.hash(user.password, 12);
      }
    }
  }
});

// Method to check if password is correct
User.prototype.correctPassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = User;
"""
                
                user_model_path = os.path.join(output_dir, 'user.js')
                self._create_file(user_model_path, user_model)
                generated_files.append(user_model_path)
        
        return generated_files
    
    def _generate_mongoose_model(self, feature: Dict[str, Any]) -> str:
        """
        Generate a Mongoose model based on a feature.
        
        Args:
            feature: The feature object
            
        Returns:
            String with Mongoose model code
        """
        feature_name = feature.get('name', '')
        model_name = feature_name.replace(' ', '')
        
        # Generate schema fields based on feature details
        schema_fields = {}
        for detail in feature.get('details', []):
            # Try to extract field name and type from detail
            if ':' in detail:
                field_parts = detail.split(':', 1)
                field_name = field_parts[0].strip().lower().replace(' ', '_')
                field_type = 'String'  # Default type
                
                # Try to determine field type
                if 'number' in field_parts[1].lower() or 'count' in field_parts[1].lower() or 'price' in field_parts[1].lower():
                    field_type = 'Number'
                elif 'date' in field_parts[1].lower() or 'time' in field_parts[1].lower():
                    field_type = 'Date'
                elif 'boolean' in field_parts[1].lower() or 'yes/no' in field_parts[1].lower():
                    field_type = 'Boolean'
                
                schema_fields[field_name] = field_type
        
        # If no fields were extracted, add some default fields
        if not schema_fields:
            schema_fields = {
                'name': 'String',
                'description': 'String',
                'active': 'Boolean'
            }
        
        # Always add timestamps
        schema_fields['createdAt'] = 'Date'
        schema_fields['updatedAt'] = 'Date'
        
        # Generate model code
        model_code = f"""
const mongoose = require('mongoose');

const {model_name.lower()}Schema = new mongoose.Schema({{
"""
        
        for field_name, field_type in schema_fields.items():
            if field_name in ['createdAt', 'updatedAt']:
                model_code += f"  {field_name}: {{\n    type: {field_type},\n    default: Date.now\n  }},\n"
            else:
                model_code += f"  {field_name}: {{\n    type: {field_type}"
                
                # Add required validation for name field
                if field_name == 'name':
                    model_code += ",\n    required: [true, 'Please provide a name']"
                
                model_code += "\n  },\n"
        
        model_code += """});

"""
        
        # Add timestamps option
        model_code += f"""const {model_name} = mongoose.model('{model_name}', {model_name.lower()}Schema);

module.exports = {model_name};
"""
        
        return model_code
    
    def _generate_sequelize_model(self, feature: Dict[str, Any]) -> str:
        """
        Generate a Sequelize model based on a feature.
        
        Args:
            feature: The feature object
            
        Returns:
            String with Sequelize model code
        """
        feature_name = feature.get('name', '')
        model_name = feature_name.replace(' ', '')
        
        # Generate schema fields based on feature details
        schema_fields = {}
        for detail in feature.get('details', []):
            # Try to extract field name and type from detail
            if ':' in detail:
                field_parts = detail.split(':', 1)
                field_name = field_parts[0].strip().lower().replace(' ', '_')
                field_type = 'STRING'  # Default type
                
                # Try to determine field type
                if 'number' in field_parts[1].lower() or 'count' in field_parts[1].lower():
                    field_type = 'INTEGER'
                elif 'price' in field_parts[1].lower() or 'cost' in field_parts[1].lower():
                    field_type = 'DECIMAL(10, 2)'
                elif 'date' in field_parts[1].lower() or 'time' in field_parts[1].lower():
                    field_type = 'DATE'
                elif 'boolean' in field_parts[1].lower() or 'yes/no' in field_parts[1].lower():
                    field_type = 'BOOLEAN'
                
                schema_fields[field_name] = field_type
        
        # If no fields were extracted, add some default fields
        if not schema_fields:
            schema_fields = {
                'name': 'STRING',
                'description': 'TEXT',
                'active': 'BOOLEAN'
            }
        
        # Generate model code
        model_code = f"""
const {{ DataTypes }} = require('sequelize');
const {{ sequelize }} = require('../config/db');

const {model_name} = sequelize.define('{model_name}', {{
"""
        
        for field_name, field_type in schema_fields.items():
            model_code += f"  {field_name}: {{\n    type: DataTypes.{field_type}"
            
            # Add required validation for name field
            if field_name == 'name':
                model_code += ",\n    allowNull: false"
            
            model_code += "\n  },\n"
        
        model_code += """}, {
  timestamps: true
});

module.exports = """ + model_name + ";\n"
        
        return model_code
    
    def generate_controllers(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate controllers based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated controllers
            
        Returns:
            List of paths to the generated controller files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Generate controllers based on features
        features = documentation.get('features', [])
        for feature in features:
            feature_name = feature.get('name', '')
            if not feature_name:
                continue
            
            model_name = feature_name.replace(' ', '')
            controller_name = model_name.lower() + 'Controller.js'
            
            controller_content = self._generate_controller(feature, model_name)
            
            controller_path = os.path.join(output_dir, controller_name)
            self._create_file(controller_path, controller_content)
            generated_files.append(controller_path)
        
        # Generate auth controller if authentication is needed
        tech_stack = documentation.get('tech_stack', [])
        for tech in tech_stack:
            if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                auth_controller = """
const jwt = require('jsonwebtoken');
const User = require('../models/user');
const catchAsync = require('../utils/catchAsync');
const { success, error } = require('../utils/apiResponse');

/**
 * Generate JWT token
 */
const signToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN
  });
};

/**
 * @desc    Register a new user
 * @route   POST /api/auth/register
 * @access  Public
 */
exports.register = catchAsync(async (req, res) => {
  const { name, email, password } = req.body;
  
  // Check if user already exists
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return error(res, 'User already exists', 400);
  }
  
  // Create new user
  const user = await User.create({
    name,
    email,
    password
  });
  
  // Generate token
  const token = signToken(user._id);
  
  // Remove password from output
  user.password = undefined;
  
  return success(res, { user, token }, 201);
});

/**
 * @desc    Login user
 * @route   POST /api/auth/login
 * @access  Public
 */
exports.login = catchAsync(async (req, res) => {
  const { email, password } = req.body;
  
  // Check if email and password exist
  if (!email || !password) {
    return error(res, 'Please provide email and password', 400);
  }
  
  // Check if user exists && password is correct
  const user = await User.findOne({ email }).select('+password');
  
  if (!user || !(await user.correctPassword(password, user.password))) {
    return error(res, 'Incorrect email or password', 401);
  }
  
  // Generate token
  const token = signToken(user._id);
  
  // Remove password from output
  user.password = undefined;
  
  return success(res, { user, token });
});

/**
 * @desc    Get current user profile
 * @route   GET /api/auth/me
 * @access  Private
 */
exports.getMe = catchAsync(async (req, res) => {
  const user = await User.findById(req.user.id);
  
  if (!user) {
    return error(res, 'User not found', 404);
  }
  
  return success(res, { user });
});

/**
 * @desc    Update user profile
 * @route   PUT /api/auth/me
 * @access  Private
 */
exports.updateMe = catchAsync(async (req, res) => {
  const { name, email } = req.body;
  
  // Create filtered object with allowed fields
  const filteredBody = {
    name,
    email
  };
  
  const user = await User.findByIdAndUpdate(req.user.id, filteredBody, {
    new: true,
    runValidators: true
  });
  
  return success(res, { user });
});
"""
                auth_controller_path = os.path.join(output_dir, 'authController.js')
                self._create_file(auth_controller_path, auth_controller)
                generated_files.append(auth_controller_path)
        
        return generated_files
    
    def _generate_controller(self, feature: Dict[str, Any], model_name: str) -> str:
        """
        Generate a controller based on a feature.
        
        Args:
            feature: The feature object
            model_name: The model name
            
        Returns:
            String with controller code
        """
        controller_code = f"""
const {model_name} = require('../models/{model_name.lower()}');
const catchAsync = require('../utils/catchAsync');
const {{ success, error }} = require('../utils/apiResponse');

/**
 * @desc    Get all {feature.get('name', '')}
 * @route   GET /api/{model_name.lower()}
 * @access  Public
 */
exports.getAll = catchAsync(async (req, res) => {{
  const items = await {model_name}.find();
  return success(res, {{ items }});
}});

/**
 * @desc    Get {feature.get('name', '')} by ID
 * @route   GET /api/{model_name.lower()}/:id
 * @access  Public
 */
exports.getById = catchAsync(async (req, res) => {{
  const item = await {model_name}.findById(req.params.id);
  
  if (!item) {{
    return error(res, '{model_name} not found', 404);
  }}
  
  return success(res, {{ item }});
}});

/**
 * @desc    Create new {feature.get('name', '')}
 * @route   POST /api/{model_name.lower()}
 * @access  Private
 */
exports.create = catchAsync(async (req, res) => {{
  const item = await {model_name}.create(req.body);
  return success(res, {{ item }}, 201);
}});

/**
 * @desc    Update {feature.get('name', '')}
 * @route   PUT /api/{model_name.lower()}/:id
 * @access  Private
 */
exports.update = catchAsync(async (req, res) => {{
  const item = await {model_name}.findByIdAndUpdate(req.params.id, req.body, {{
    new: true,
    runValidators: true
  }});
  
  if (!item) {{
    return error(res, '{model_name} not found', 404);
  }}
  
  return success(res, {{ item }});
}});

/**
 * @desc    Delete {feature.get('name', '')}
 * @route   DELETE /api/{model_name.lower()}/:id
 * @access  Private
 */
exports.delete = catchAsync(async (req, res) => {{
  const item = await {model_name}.findByIdAndDelete(req.params.id);
  
  if (!item) {{
    return error(res, '{model_name} not found', 404);
  }}
  
  return success(res, null, 204);
}});
"""
        
        return controller_code
    
    def generate_routes(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate API routes based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated routes
            
        Returns:
            List of paths to the generated route files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # Generate routes based on features
        features = documentation.get('features', [])
        for feature in features:
            feature_name = feature.get('name', '')
            if not feature_name:
                continue
            
            model_name = feature_name.replace(' ', '')
            route_name = model_name.lower() + '.js'
            
            # Check if authentication is needed
            has_auth = False
            tech_stack = documentation.get('tech_stack', [])
            for tech in tech_stack:
                if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                    has_auth = True
                    break
            
            route_content = self._generate_route(feature, model_name, has_auth)
            
            route_path = os.path.join(output_dir, route_name)
            self._create_file(route_path, route_content)
            generated_files.append(route_path)
        
        # Generate auth routes if authentication is needed
        for tech in tech_stack:
            if 'auth' in tech.get('name', '').lower() or 'authentication' in tech.get('name', '').lower():
                auth_route = """
const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const { protect } = require('../middleware/auth');

/**
 * @route   POST /api/auth/register
 * @desc    Register a new user
 * @access  Public
 */
router.post('/register', authController.register);

/**
 * @route   POST /api/auth/login
 * @desc    Login user
 * @access  Public
 */
router.post('/login', authController.login);

/**
 * @route   GET /api/auth/me
 * @desc    Get current user profile
 * @access  Private
 */
router.get('/me', protect, authController.getMe);

/**
 * @route   PUT /api/auth/me
 * @desc    Update user profile
 * @access  Private
 */
router.put('/me', protect, authController.updateMe);

module.exports = router;
"""
                auth_route_path = os.path.join(output_dir, 'auth.js')
                self._create_file(auth_route_path, auth_route)
                generated_files.append(auth_route_path)
        
        return generated_files
    
    def _generate_route(self, feature: Dict[str, Any], model_name: str, has_auth: bool) -> str:
        """
        Generate a route based on a feature.
        
        Args:
            feature: The feature object
            model_name: The model name
            has_auth: Whether authentication is needed
            
        Returns:
            String with route code
        """
        controller_name = model_name.lower() + 'Controller'
        
        route_code = f"""
const express = require('express');
const router = express.Router();
const {controller_name} = require('../controllers/{controller_name}');
"""
        
        if has_auth:
            route_code += "const { protect } = require('../middleware/auth');\n"
        
        route_code += f"""
/**
 * @route   GET /api/{model_name.lower()}
 * @desc    Get all {feature.get('name', '')}
 * @access  Public
 */
router.get('/', {controller_name}.getAll);

/**
 * @route   GET /api/{model_name.lower()}/:id
 * @desc    Get {feature.get('name', '')} by ID
 * @access  Public
 */
router.get('/:id', {controller_name}.getById);

"""
        
        if has_auth:
            route_code += f"""/**
 * @route   POST /api/{model_name.lower()}
 * @desc    Create new {feature.get('name', '')}
 * @access  Private
 */
router.post('/', protect, {controller_name}.create);

/**
 * @route   PUT /api/{model_name.lower()}/:id
 * @desc    Update {feature.get('name', '')}
 * @access  Private
 */
router.put('/:id', protect, {controller_name}.update);

/**
 * @route   DELETE /api/{model_name.lower()}/:id
 * @desc    Delete {feature.get('name', '')}
 * @access  Private
 */
router.delete('/:id', protect, {controller_name}.delete);
"""
        else:
            route_code += f"""/**
 * @route   POST /api/{model_name.lower()}
 * @desc    Create new {feature.get('name', '')}
 * @access  Public
 */
router.post('/', {controller_name}.create);

/**
 * @route   PUT /api/{model_name.lower()}/:id
 * @desc    Update {feature.get('name', '')}
 * @access  Public
 */
router.put('/:id', {controller_name}.update);

/**
 * @route   DELETE /api/{model_name.lower()}/:id
 * @desc    Delete {feature.get('name', '')}
 * @access  Public
 */
router.delete('/:id', {controller_name}.delete);
"""
        
        route_code += "\nmodule.exports = router;\n"
        
        return route_code
    
    def generate_services(self, documentation: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate services based on the documentation.
        
        Args:
            documentation: The documentation object
            output_dir: Directory to save the generated services
            
        Returns:
            List of paths to the generated service files
        """
        # Create output directory
        self._create_output_dir(output_dir)
        
        generated_files = []
        
        # For this simple implementation, we'll just create a basic email service
        email_service = """
/**
 * Email Service
 * 
 * This service handles sending emails from the application.
 * In a real implementation, you would integrate with an email provider like SendGrid, Mailgun, etc.
 */

/**
 * Send an email
 * @param {Object} options - Email options
 * @param {string} options.to - Recipient email
 * @param {string} options.subject - Email subject
 * @param {string} options.text - Email text content
 * @param {string} options.html - Email HTML content
 * @returns {Promise<boolean>} - Success status
 */
exports.sendEmail = async (options) => {
  try {
    // In a real implementation, you would use an email provider SDK here
    console.log('Sending email...');
    console.log(`To: ${options.to}`);
    console.log(`Subject: ${options.subject}`);
    console.log(`Text: ${options.text}`);
    
    // Simulate sending email
    await new Promise(resolve => setTimeout(resolve, 500));
    
    console.log('Email sent successfully');
    return true;
  } catch (error) {
    console.error('Error sending email:', error);
    return false;
  }
};
"""
        
        email_service_path = os.path.join(output_dir, 'emailService.js')
        self._create_file(email_service_path, email_service)
        generated_files.append(email_service_path)
        
        return generated_files
