#!/bin/bash

# MEP Contact Web Application Startup Script

echo "🚀 Starting MEP Contact Web Application..."
echo ""

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if MEP data file exists
if [ ! -f "members_by_country.json" ]; then
    echo "⚠️  Warning: members_by_country.json not found!"
    echo "   Please ensure the MEP data file is in this directory."
    echo ""
fi

# Check email configuration
if [ -z "$EMAIL_USER" ] || [ -z "$EMAIL_PASSWORD" ]; then
    echo "⚠️  Email configuration not found!"
    echo "   To enable email sending, set these environment variables:"
    echo "   export EMAIL_USER='your-email@gmail.com'"
    echo "   export EMAIL_PASSWORD='your-app-password'"
    echo ""
fi

echo "🌐 Starting web server..."
echo "   Application will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

# Start the application
python mep_webapp.py
