# 🚀 ChatSmart AI - Quick Setup Guide

## Prerequisites

Before you begin, ensure you have:
- **Python 3.8+** installed
- **Git** installed
- **Google API Key** for Gemini AI

## Step-by-Step Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/yourusername/chatsmart-ai.git
cd chatsmart-ai
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Create environment file
cp .env.example .env

# Edit .env file and add your Google API key:
GOOGLE_API_KEY=your_actual_api_key_here
```

### 5. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in your `.env` file

### 6. Run the Application
```bash
streamlit run app.py
```

### 7. Open in Browser
The app will automatically open at: `http://localhost:8501`

## ✅ Verification

1. **Upload a PDF** - Try the drag-and-drop feature
2. **Ask a question** - Test the AI chat functionality
3. **Check analytics** - Verify the sidebar metrics update
4. **Export chat** - Test the download feature

## 🔧 Troubleshooting

### Common Issues:

**"ModuleNotFoundError"**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**"API Key not found"**
```bash
# Check your .env file exists and contains:
GOOGLE_API_KEY=your_actual_key_here
```

**"Permission denied"**
```bash
# On macOS/Linux, you might need:
chmod +x venv/bin/activate
```

**"Port already in use"**
```bash
# Use a different port:
streamlit run app.py --server.port 8502
```

### Performance Tips:

- **First run** might be slower (downloading embedding models)
- **Larger PDFs** take more time to process
- **Multiple documents** are processed sequentially

## 📱 Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use proper secret management
2. **HTTPS**: Enable SSL certificates
3. **Authentication**: Add user authentication if needed
4. **Scaling**: Use cloud services for high traffic
5. **Monitoring**: Add logging and error tracking

## 🆘 Support

If you encounter issues:
1. Check the [Issues](https://github.com/yourusername/chatsmart-ai/issues) page
2. Create a new issue with details
3. Include error messages and system info

---

**🎉 Enjoy using ChatSmart AI!** 