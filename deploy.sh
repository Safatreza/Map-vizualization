#!/bin/bash

echo "========================================"
echo "AboutWater Customer Map - Vercel Deploy"
echo "========================================"
echo

echo "Checking prerequisites..."
echo

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Please install Node.js from: https://nodejs.org/"
    echo
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI!"
        exit 1
    fi
fi

echo "✅ Prerequisites check passed!"
echo

echo "Starting Vercel deployment..."
echo

# Deploy to Vercel
vercel --prod

if [ $? -eq 0 ]; then
    echo
    echo "🎉 Deployment successful!"
    echo
    echo "Your customer map is now live on Vercel!"
    echo "Share the URL with your colleagues."
    echo
    echo "Next steps:"
    echo "1. Test the deployed app"
    echo "2. Share the URL with your team"
    echo "3. Add to company intranet/bookmarks"
    echo
else
    echo
    echo "❌ Deployment failed!"
    echo "Check the error messages above."
    echo
fi
