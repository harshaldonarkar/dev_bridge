"""
Database Initialization Script

This script initializes the SQLite database for the DevBridge platform.
It creates the necessary tables for storing user projects and documentation.
"""

import sqlite3
import os

# Create the database directory if it doesn't exist
os.makedirs('database', exist_ok=True)

# Connect to database
conn = sqlite3.connect('database/devbridge.db')
cursor = conn.cursor()

# Create projects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    prompt TEXT NOT NULL,
    documentation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create users table for future use
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully.")