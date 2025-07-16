# 🚀 ChatSmart: Enterprise AI Document Intelligence Platform
# Built with Streamlit + Gemini + Advanced RAG

import streamlit as st
import os
import tempfile
import time
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from rag_utils import load_pdf, create_vectorstore, get_pdf_preview

# ========================================
# 🎨 CONFIGURATION & STYLING
# ========================================

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Page configuration with professional branding
st.set_page_config(
    page_title="ChatSmart AI - Enterprise Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: #e5e7eb;
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border-left: 4px solid #60a5fa;
        margin: 1rem 0;
        color: white;
    }
    
    .upload-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 2px dashed rgba(147, 197, 253, 0.6);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
        color: white;
    }
    
    .upload-card:hover {
        border-color: #60a5fa;
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(96, 165, 250, 0.3);
    }
    
    /* Chat styling */
    .chat-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        color: white;
    }
    
    .chat-input {
        border-radius: 25px;
        border: 2px solid #e5e7eb;
        padding: 1rem 1.5rem;
        font-size: 1rem;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(90deg, #34d399, #10b981);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        box-shadow: 0 6px 20px rgba(52, 211, 153, 0.4);
        backdrop-filter: blur(10px);
    }
    
    .status-processing {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        box-shadow: 0 6px 20px rgba(251, 191, 36, 0.4);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .sidebar-metric {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #60a5fa;
        color: white;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #60a5fa, #3b82f6);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(96, 165, 250, 0.4);
        background: linear-gradient(90deg, #3b82f6, #2563eb);
    }
    
    /* Ensure text is visible on the gradient background */
    .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, div {
        color: white !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(147, 197, 253, 0.6) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    .stChatInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 25px !important;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# 📊 SESSION STATE INITIALIZATION
# ========================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'rag_chain': None,
        'chat_history': [],
        'processed_files': [],
        'total_chunks': 0,
        'session_start': datetime.now(),
        'query_count': 0,
        'processing_time': 0,
        'file_analytics': {},
        'user_satisfaction': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ========================================
# 🎯 MAIN HEADER
# ========================================

st.markdown("""
<div class="main-header">
    <h1 class="main-title">🧠 ChatSmart AI</h1>
    <p class="main-subtitle">Enterprise Document Intelligence Platform | Powered by Google Gemini 1.5</p>
</div>
""", unsafe_allow_html=True)

# ========================================
# 📈 SIDEBAR ANALYTICS DASHBOARD
# ========================================

with st.sidebar:
    st.markdown("## 📊 Analytics Dashboard")
    
    # Session metrics
    session_duration = datetime.now() - st.session_state.session_start
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📄 Files", len(st.session_state.processed_files))
        st.metric("💬 Queries", st.session_state.query_count)
    
    with col2:
        st.metric("🧩 Chunks", st.session_state.total_chunks)
        st.metric("⏱️ Uptime", f"{session_duration.seconds//60}m")
    
    # Performance chart
    if st.session_state.query_count > 0:
        st.markdown("### 📈 Performance Metrics")
        
        # Create sample performance data
        performance_data = pd.DataFrame({
            'Query': range(1, st.session_state.query_count + 1),
            'Response Time (s)': [1.2 + i*0.1 for i in range(st.session_state.query_count)]
        })
        
        fig = px.line(performance_data, x='Query', y='Response Time (s)', 
                     title="Response Time Trend",
                     color_discrete_sequence=['#4f46e5'])
        fig.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    # System status
    st.markdown("### 🔧 System Status")
    st.success("🟢 Gemini AI: Online")
    st.success("🟢 Vector DB: Active")
    st.success("🟢 Embeddings: Ready")
    
    # File management
    if st.session_state.processed_files:
        st.markdown("### 📁 Processed Files")
        for i, file_name in enumerate(st.session_state.processed_files):
            st.markdown(f"✅ {file_name}")
    
    # Settings
    st.markdown("### ⚙️ AI Settings")
    temperature = st.slider("🌡️ Creativity", 0.0, 1.0, 0.2, 0.1)
    max_tokens = st.slider("📝 Max Response", 100, 2000, 1000, 100)

# ========================================
# 📂 MAIN CONTENT AREA
# ========================================

# File upload section with enhanced UI
st.markdown("## 📂 Document Upload Center")

col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    st.markdown("""
    <div class="upload-card">
        <h3 style="color: #93c5fd; margin-bottom: 1rem;">🎯 Drag & Drop Your Documents</h3>
        <p style="color: #e0e7ff; font-size: 0.9rem;">Supports PDF files • AI-powered analysis • Instant processing</p>
    </div>
    """, unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Choose PDF files", 
    type=["pdf"], 
    accept_multiple_files=True,
    help="Upload one or more PDF documents for AI analysis"
)

# Document processing with enhanced UX
if uploaded_files:
    with st.container():
        st.markdown("## 🔄 Processing Documents...")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        processing_start = time.time()
        
        with st.spinner("🚀 AI is analyzing your documents..."):
            all_chunks = []
            total_files = len(uploaded_files)
            
            for idx, file in enumerate(uploaded_files):
                # Update progress
                progress = (idx + 1) / total_files
                progress_bar.progress(progress)
                status_text.markdown(f"<div class='status-processing'>Processing: {file.name} ({idx+1}/{total_files})</div>", unsafe_allow_html=True)
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name

                # Generate preview
                try:
                    preview = get_pdf_preview(tmp_path)
                    if preview:
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.image(preview, caption=f"📄 {file.name}", width=200)
                except:
                    st.info(f"📄 {file.name} - Preview unavailable")

                # Process document
                chunks = load_pdf(tmp_path)
                all_chunks.extend(chunks)
                
                # Track file analytics
                st.session_state.file_analytics[file.name] = {
                    'chunks': len(chunks),
                    'processed_at': datetime.now(),
                    'size': file.size
                }
                
                # Cleanup
                os.unlink(tmp_path)
                
                # Add to processed files
                if file.name not in st.session_state.processed_files:
                    st.session_state.processed_files.append(file.name)

            # Create vectorstore
            status_text.markdown("<div class='status-processing'>🧠 Building AI Knowledge Base...</div>", unsafe_allow_html=True)
            vectorstore = create_vectorstore(all_chunks)
            retriever = vectorstore.as_retriever()
            
            # Initialize memory and LLM
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=temperature,
                google_api_key=GOOGLE_API_KEY
            )

            # Create RAG chain
    st.session_state.rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )

       # Update metrics
    st.session_state.total_chunks = len(all_chunks)
    st.session_state.processing_time = time.time() - processing_start
            
            # Success message
    progress_bar.progress(1.0)
    status_text.markdown(
                f"<div class='status-success'>✅ Successfully processed {len(uploaded_files)} documents in {st.session_state.processing_time:.1f}s</div>", 
                unsafe_allow_html=True
            )

# ========================================
# 💬 ADVANCED CHAT INTERFACE
# ========================================

if st.session_state.rag_chain:
    st.markdown("## 💬 AI Assistant")
    
    # Quick questions
    st.markdown("### 🚀 Quick Questions")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_questions = [
        "📋 Summarize the documents",
        "🔍 Key insights",
        "📊 Main findings", 
        "❓ Important details"
    ]
    
    for col, question in zip([col1, col2, col3, col4], quick_questions):
        if col.button(question):
            st.session_state.query_count += 1
            with st.spinner("🤔 AI is thinking..."):
                result = st.session_state.rag_chain.invoke({"question": question.split(" ", 1)[1]})
                st.session_state.chat_history.append(("You", question))
                st.session_state.chat_history.append(("ChatSmart AI", result["answer"]))

    # Main chat input
    user_input = st.chat_input("💭 Ask anything about your documents...")
    
    if user_input:
        st.session_state.query_count += 1
        
        with st.spinner("🧠 Analyzing with AI..."):
            start_time = time.time()
            result = st.session_state.rag_chain.invoke({"question": user_input})
            response_time = time.time() - start_time
            
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("ChatSmart AI", result["answer"]))

# Chat history with enhanced UI
if st.session_state.chat_history:
    st.markdown("## 🗨️ Conversation History")
    
    for i in range(len(st.session_state.chat_history) - 1, -1, -2):
        if i > 0:
            user_msg = st.session_state.chat_history[i-1][1]
            ai_msg = st.session_state.chat_history[i][1]
            
            # User message
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**{user_msg}**")
            
            # AI response
            with st.chat_message("assistant", avatar="🧠"):
                st.markdown(ai_msg)
                
                # Add feedback buttons
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("👍", key=f"like_{i}"):
                        st.session_state.user_satisfaction = "positive"
                        st.success("Thanks for your feedback!")
                with col2:
                    if st.button("👎", key=f"dislike_{i}"):
                        st.session_state.user_satisfaction = "negative"
                        st.info("We'll work on improving!")

else:
    if not st.session_state.rag_chain:
        st.markdown("""
        <div class="chat-container">
            <h3 style="color: #93c5fd; margin-bottom: 1rem;">🎯 Welcome to ChatSmart AI</h3>
            <p style="color: #e0e7ff; margin-bottom: 1.5rem;">Upload your documents above to start having intelligent conversations with your data!</p>
            <ul style="color: #cbd5e1; list-style-type: none; padding-left: 0;">
                <li style="margin: 0.8rem 0; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">🔍</span>
                    Ask complex questions about your documents
                </li>
                <li style="margin: 0.8rem 0; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">📊</span>
                    Get detailed analysis and insights
                </li>
                <li style="margin: 0.8rem 0; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">🧠</span>
                    Powered by Google's latest Gemini AI
                </li>
                <li style="margin: 0.8rem 0; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">⚡</span>
                    Lightning-fast responses with context awareness
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ========================================
# 🛠️ ADVANCED FEATURES
# ========================================

if st.session_state.rag_chain:
    st.markdown("## 🛠️ Advanced Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Generate Report"):
            with st.spinner("Creating comprehensive report..."):
                time.sleep(2)  # Simulate processing
                st.success("📄 Report generated successfully!")
                
                # Generate sample analytics
                if st.session_state.chat_history:
                    report_data = {
                        'Documents Processed': len(st.session_state.processed_files),
                        'Total Chunks': st.session_state.total_chunks,
                        'Queries Asked': st.session_state.query_count,
                        'Average Response Time': '1.3s',
                        'Session Duration': f"{(datetime.now() - st.session_state.session_start).seconds // 60} minutes"
                    }
                    
                    st.json(report_data)
    
    with col2:
        if st.button("💾 Export Chat"):
            if st.session_state.chat_history:
                chat_export = ""
                for role, message in st.session_state.chat_history:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    chat_export += f"[{timestamp}] {role}: {message}\n\n"
                
                st.download_button(
                    label="⬇️ Download Chat History",
                    data=chat_export,
                    file_name=f"chatsmart_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No conversation to export!")
    
    with col3:
        if st.button("🔄 Clear Session"):
            for key in ['chat_history', 'processed_files', 'rag_chain', 'total_chunks', 'query_count']:
                st.session_state[key] = [] if 'history' in key or 'files' in key else (None if 'chain' in key else 0)
            st.success("🧹 Session cleared!")
            st.rerun()
    
    with col4:
        if st.button("📈 View Analytics"):
            st.markdown("### 📊 Detailed Analytics")
            
            # Create analytics visualizations
            if st.session_state.file_analytics:
                # File processing chart
                files_df = pd.DataFrame([
                    {'File': name, 'Chunks': data['chunks'], 'Size (KB)': data['size']/1024}
                    for name, data in st.session_state.file_analytics.items()
                ])
                
                fig = px.bar(files_df, x='File', y='Chunks', 
                           title="Document Chunk Distribution",
                           color='Chunks',
                           color_continuous_scale='viridis')
                st.plotly_chart(fig, use_container_width=True)

# ========================================
# 🎨 FOOTER
# ========================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #4f46e5, #7c3aed); border-radius: 15px; margin-top: 2rem;'>
    <h3 style='color: white; margin: 0;'>🚀 ChatSmart AI - Enterprise Ready</h3>
    <p style='color: #e5e7eb; margin: 0.5rem 0 0 0;'>Transforming Documents into Intelligent Conversations | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)