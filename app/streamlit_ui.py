import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI Interface", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🤖"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .wide-tab-content {
        padding: 1rem 0;
    }
    .json-container {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .risk-status-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    .risk-status-item {
        flex: 1;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Multi-Agent AI Processing System</h1>
    <p>Intelligent document processing with classification, risk assessment, and automated actions</p>
</div>
""", unsafe_allow_html=True)

# API Configuration
API_BASE = st.sidebar.text_input("🔗 API Base URL", value="https://multi-agent-bot-1.onrender.com")

# Connection status check
def check_api_connection(retries=3, delay=2):
    for _ in range(retries):
        try:
            response = requests.get(f"{API_BASE}/memory", timeout=10)
            if response.status_code == 200:
                return True
        except:
            time.sleep(delay)
    return False

# Sidebar status
with st.sidebar:
    st.markdown("### 📊 System Status")
    if check_api_connection():
        st.success("✅ API Connected")
    else:
        st.error("❌ API Disconnected")
    
    st.markdown("### ⚙️ Settings")
    auto_refresh = st.checkbox("🔄 Auto-refresh memory", value=False)
    show_raw_response = st.checkbox("📝 Show raw AI responses", value=True)

# Helper function to display JSON with proper formatting
def display_json_data(data, title="JSON Data", expanded=True):
    """Display JSON data with proper formatting and error handling"""
    if data:
        st.markdown(f"**{title}:**")
        st.markdown('<div class="json-container">', unsafe_allow_html=True)
        try:
            if isinstance(data, (dict, list)):
                st.json(data, expanded=expanded)
            else:
                st.text(str(data))
        except Exception as e:
            st.error(f"Error displaying JSON: {e}")
            st.text(str(data))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"No {title.lower()} available")

# Helper function to display API response
def show_response(res, success_message="Operation completed successfully!"):
    if res.status_code == 200:
        st.markdown(f'<div class="success-box">✅ {success_message}</div>', unsafe_allow_html=True)
        try:
            data = res.json()
            # Create tabs for different aspects of the response
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Classification", "🚨 Risk Assessment", "🤖 Agent Data", "⚡ Actions", "🔍 Raw Data"])

            with tab1:
                st.markdown('<div class="wide-tab-content">', unsafe_allow_html=True)
                st.subheader("Classification Results")
                
                if 'classification' in data and data['classification']:
                    display_json_data(data['classification'], "Classification Data")
                else:
                    st.info("No classification data available")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab2:
                st.markdown('<div class="wide-tab-content">', unsafe_allow_html=True)
                st.subheader("Risk Assessment")
                
                # Fixed: Use direct styling instead of nested columns
                anomaly_flagged = data.get('anomaly_flagged', False)
                risk_triggered = data.get('risk_triggered', False)
                
                st.markdown("""
                <div class="risk-status-container">
                    <div class="risk-status-item">
                """, unsafe_allow_html=True)
                
                if anomaly_flagged:
                    st.markdown('<div class="warning-box">🚨 <strong>ANOMALY DETECTED</strong></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">✅ <strong>NO ANOMALY</strong></div>', unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                    <div class="risk-status-item">
                """, unsafe_allow_html=True)
                
                if risk_triggered:
                    st.markdown('<div class="error-box">⚠️ <strong>RISK TRIGGERED</strong></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">✅ <strong>NO RISK</strong></div>', unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display risk-related data if available
                risk_data = {}
                for key in ['risk_score', 'risk_level', 'risk_factors', 'anomaly_details']:
                    if key in data:
                        risk_data[key] = data[key]
                
                if risk_data:
                    display_json_data(risk_data, "Risk Details")
                
                st.markdown('</div>', unsafe_allow_html=True)

            with tab3:
                st.markdown('<div class="wide-tab-content">', unsafe_allow_html=True)
                st.subheader("Agent Data & Trace")
                
                if 'agent_data' in data and data['agent_data']:
                    display_json_data(data['agent_data'], "Agent Data")
                    
                    if 'agent_trace' in data and data['agent_trace']:
                        st.markdown("**Agent Trace:**")
                        if isinstance(data['agent_trace'], list):
                            for i, trace in enumerate(data['agent_trace'], 1):
                                st.markdown(f"{i}. {trace}")
                        else:
                            st.text(str(data['agent_trace']))
                else:
                    st.info("No agent data available")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab4:
                st.markdown('<div class="wide-tab-content">', unsafe_allow_html=True)
                st.subheader("Action Router & Trace")
                
                if 'action_router' in data and data['action_router']:
                    display_json_data(data['action_router'], "Action Router Data")
                    
                    if 'action_trace' in data and data['action_trace']:
                        st.markdown("**Action Trace:**")
                        if isinstance(data['action_trace'], list):
                            for i, trace in enumerate(data['action_trace'], 1):
                                st.markdown(f"{i}. {trace}")
                        else:
                            st.text(str(data['action_trace']))
                else:
                    st.info("No action router data available")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab5:
                st.markdown('<div class="wide-tab-content">', unsafe_allow_html=True)
                st.subheader("Complete Response Data")
                display_json_data(data, "Complete Response")
                
                if 'raw_response' in data and data['raw_response']:
                    st.subheader("Raw AI Response")
                    st.text_area("AI Analysis Details", data['raw_response'], height=150, disabled=True)
                
                if 'error' in data:
                    st.error(f"API Error: {data['error']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"❌ Error parsing response: {e}")
            st.text(res.text)
    else:
        st.markdown(f'<div class="error-box">❌ API Error {res.status_code}</div>', unsafe_allow_html=True)
        try:
            error_data = res.json()
            st.json(error_data)
        except:
            st.text(res.text)

def process_with_loading(endpoint, data=None, files=None):
    with st.spinner('🔄 Processing your request...'):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        try:
            if files:
                response = requests.post(f"{API_BASE}{endpoint}", files=files, timeout=100)
            else:
                response = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=100)
            return response
        except requests.RequestException as e:
            st.error(f"❌ Request failed: {e}")
            return None

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    # Input type selection
    st.markdown("### 📂 Select Processing Type")
    option = st.selectbox("Choose input type:", ["📧 Email", "🔧 JSON", "📄 PDF"], index=0)
    
    # Email Processing
    if option == "📧 Email":
        st.markdown("### 📧 Email Content Processing")
        st.markdown("*Process email content for classification, risk assessment, and automated actions*")
        
        # Email templates for quick testing
        with st.expander("📋 Quick Test Templates"):
            template_option = st.selectbox("Choose a template:", [
                "Custom Input",
                "Normal Business Email",
                "Suspicious Phishing Email",
                "Urgent Financial Request",
                "System Security Alert"
            ])
            
            templates = {
                "Normal Business Email": "Subject: Quarterly Report Submission\n\nHi Team,\n\nPlease find attached the quarterly financial report for Q4 2024. The numbers show steady growth with a 12% increase in revenue compared to last quarter.\n\nKey highlights:\n- Revenue: $2.3M (+12%)\n- New customers: 145\n- Customer retention: 94%\n\nLet me know if you need any clarification.\n\nBest regards,\nSarah Johnson\nFinance Director",
                
                "Suspicious Phishing Email": "Subject: URGENT: Account Verification Required\n\nDear Valued Customer,\n\nYour account has been temporarily suspended due to suspicious activity. To restore access, you must verify your identity immediately.\n\nClick here to verify: http://suspicious-link.com/verify\n\nThis link expires in 24 hours. Failure to verify will result in permanent account closure.\n\nRegards,\nSecurity Team",
                
                "Urgent Financial Request": "Subject: CONFIDENTIAL - Wire Transfer Needed\n\nDear Sir/Madam,\n\nI am writing to request an urgent wire transfer of $50,000 to account number 9876543210 (Bank: International Trust Bank, Swift: INTLUS33).\n\nThis is for a confidential business transaction that must be completed today. Please process immediately and confirm once done.\n\nThis matter is time-sensitive and confidential.\n\nThanks,\nJ. Smith\nCEO",
                
                "System Security Alert": "Subject: Security Breach Detected\n\nATTENTION: Multiple failed login attempts detected on your account.\n\nLocation: Unknown\nTime: 2024-06-02 14:100:00\nIP Address: 192.168.1.100\n\nIf this was not you, please change your password immediately and contact our security team.\n\nSecurity Team\nIT Department"
            }
            
            if template_option != "Custom Input":
                st.text_area("📖 Template Preview:", templates[template_option], height=150, disabled=True)
        
        # Email content input
        content = st.text_area(
            "📧 Email Content", 
            value=templates.get(template_option, "") if template_option != "Custom Input" else "",
            height=200,
            placeholder="Paste your email content here...",
            help="Enter the complete email content including subject, body, and any relevant metadata"
        )
        
        col_a, col_b = st.columns([1, 3])
        with col_a:
            if st.button("🚀 Process Email", type="primary", use_container_width=True):
                if content.strip():
                    response = process_with_loading("/process/email", {"content": content})
                    if response:
                        show_response(response, "Email processed and classified successfully!")
                else:
                    st.warning("⚠️ Please enter email content to process")
    
    # JSON Processing
    elif option == "🔧 JSON":
        st.markdown("### 🔧 JSON Webhook Processing")
        st.markdown("*Process JSON payloads from webhooks, APIs, or other structured data sources*")
        
        # JSON templates
        with st.expander("📋 JSON Test Templates"):
            json_template = st.selectbox("Choose a template:", [
                "Custom Input",
                "User Login Event",
                "Financial Transaction",
                "System Alert",
                "User Registration"
            ])
            
            json_templates = {
                "User Login Event": """{
  "event": "user.login",
  "timestamp": "2024-06-02T10:100:00Z",
  "user_id": "user_12345",
  "email": "john.doe@company.com",
  "ip_address": "203.0.113.45",
  "location": {
    "country": "US",
    "city": "New York",
    "coordinates": [40.7128, -74.0060]
  },
  "device": {
    "browser": "Chrome 120.0",
    "os": "Windows 10",
    "device_type": "desktop"
  },
  "login_method": "password",
  "session_id": "sess_abc123xyz"
}""",
                
                "Financial Transaction": """{
  "transaction_id": "txn_987654321",
  "amount": 15000.00,
  "currency": "USD",
  "transaction_type": "wire_transfer",
  "from_account": {
    "account_number": "****1234",
    "account_type": "checking",
    "bank_name": "First National Bank"
  },
  "to_account": {
    "account_number": "****5678",
    "account_type": "savings",
    "bank_name": "International Bank"
  },
  "timestamp": "2024-06-02T15:45:100Z",
  "status": "pending",
  "risk_score": 7.5,
  "flags": ["high_amount", "international_transfer"]
}""",
                
                "System Alert": """{
  "alert_id": "alert_456789",
  "severity": "high",
  "alert_type": "security_breach",
  "timestamp": "2024-06-02T12:00:00Z",
  "source": "firewall",
  "description": "Multiple failed authentication attempts detected",
  "details": {
    "ip_address": "192.168.1.100",
    "attempts": 15,
    "time_window": "5 minutes",
    "targeted_accounts": ["admin", "root", "user"]
  },
  "status": "active",
  "assigned_to": "security_team"
}""",
                
                "User Registration": """{
  "event": "user.registration",
  "timestamp": "2024-06-02T09:15:00Z",
  "user_data": {
    "email": "newuser@example.com",
    "username": "newuser123",
    "full_name": "Alex Johnson",
    "phone": "+1-555-0123",
    "country": "Canada",
    "age": 28
  },
  "registration_source": "web_form",
  "ip_address": "198.51.100.42",
  "verification_status": "email_pending",
  "account_type": "premium",
  "referral_code": "REF2024"
}"""
            }
            
            if json_template != "Custom Input":
                st.code(json_templates[json_template], language="json")
        
        # JSON input
        json_input = st.text_area(
            "🔧 JSON Payload", 
            value=json_templates.get(json_template, "") if json_template != "Custom Input" else "",
            height=200,
            placeholder="Enter your JSON data here...",
            help="Paste JSON data from webhooks, API calls, or other structured sources"
        )
        
        col_a, col_b = st.columns([1, 3])
        with col_a:
            if st.button("🚀 Process JSON", type="primary", use_container_width=True):
                if json_input.strip():
                    try:
                        parsed_json = json.loads(json_input)
                        response = process_with_loading("/process/json", parsed_json)
                        if response:
                            show_response(response, "JSON payload processed successfully!")
                    except json.JSONDecodeError as e:
                        st.error(f"❌ Invalid JSON format: {e}")
                else:
                    st.warning("⚠️ Please enter JSON data to process")
    
    # PDF Processing
    elif option == "📄 PDF":
        st.markdown("### 📄 PDF Document Processing")
        st.markdown("*Upload and process PDF documents for content analysis and classification*")
        
        uploaded_file = st.file_uploader(
            "📄 Upload PDF Document", 
            type=["pdf"],
            help="Upload a PDF file for AI-powered analysis, classification, and risk assessment"
        )
        
        if uploaded_file:
            # Display file information
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size:,} bytes",
                "File type": uploaded_file.type
            }
            
            st.success("📁 File uploaded successfully!")
            for key, value in file_details.items():
                st.markdown(f"**{key}:** {value}")
            
            col_a, col_b = st.columns([1, 3])
            with col_a:
                if st.button("🚀 Process PDF", type="primary", use_container_width=True):
                    # Read file content
                    file_bytes = uploaded_file.read()
                    files = {"file": (uploaded_file.name, file_bytes, "application/pdf")}
                    
                    response = process_with_loading("/process/pdf", files=files)
                    if response:
                        show_response(response, f"PDF '{uploaded_file.name}' processed successfully!")

# Memory and System Status Panel
with col2:
    st.markdown("### 🧠 System Memory")
    st.markdown("*View processed entries and system activity*")
    
    # Memory controls
    col_refresh, col_clear = st.columns(2)
    with col_refresh:
        refresh_memory = st.button("🔄 Refresh", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear View", use_container_width=True):
            st.rerun()
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(3)
        st.rerun()
    
    # Fetch and display memory
    if refresh_memory or auto_refresh:
        try:
            memory_response = requests.get(f"{API_BASE}/memory", timeout=30)
            if memory_response.status_code == 200:
                memory_data = memory_response.json()
                
                if memory_data:
                    st.success(f"📊 {len(memory_data)} entries in memory")
                    
                    # Process memory data
                    if isinstance(memory_data, list) and len(memory_data) > 0:
                        # Create summary statistics
                        sources = []
                        timestamps = []
                        
                        for entry in memory_data:
                            if isinstance(entry, dict):
                                sources.append(entry.get('source', 'unknown'))
                                # Try to extract timestamp if available
                                if 'timestamp' in entry:
                                    timestamps.append(entry['timestamp'])
                        
                        if sources:
                            source_counts = pd.Series(sources).value_counts()
                            
                            st.markdown("**📈 Processing Summary:**")
                            for source, count in source_counts.items():
                                st.markdown(f"- **{source}**: {count} entries")
                        
                        # Show recent entries
                        st.markdown("**🕒 Recent Entries:**")
                        recent_entries = memory_data[-5:] if len(memory_data) > 5 else memory_data
                        
                        for i, entry in enumerate(reversed(recent_entries)):
                            entry_num = len(memory_data) - i
                            
                            if isinstance(entry, dict):
                                source = entry.get('source', 'unknown')
                                # Create a summary for the expander
                                summary = f"Entry {entry_num}: {source}"
                                
                                # Add risk indicators if available
                                if 'classification_result' in entry:
                                    class_result = entry['classification_result']
                                    if class_result.get('anomaly_flagged'):
                                        summary += " 🚨"
                                    if class_result.get('risk_triggered'):
                                        summary += " ⚠️"
                                
                                with st.expander(summary):
                                    # Show key information first
                                    if 'classification_result' in entry:
                                        class_result = entry['classification_result']
                                        
                                        # Fixed: Use simple markdown instead of nested columns
                                        st.markdown("**Status Overview:**")
                                        anomaly_status = "🚨 **Anomaly Detected**" if class_result.get('anomaly_flagged') else "✅ **No Anomaly**"
                                        risk_status = "⚠️ **Risk Triggered**" if class_result.get('risk_triggered') else "✅ **No Risk**"
                                        st.markdown(f"{anomaly_status} | {risk_status}")
                                    
                                    # Show actions if any
                                    if 'actions' in entry and entry['actions']:
                                        st.markdown(f"**Actions:** {', '.join(entry['actions'])}")
                                    
                                    # Show full entry
                                    st.json(entry)
                            else:
                                with st.expander(f"Entry {entry_num}: {type(entry).__name__}"):
                                    if isinstance(entry, (dict, list)):
                                        st.json(entry)
                                    else:
                                        st.text(str(entry))
                    else:
                        st.info("📭 No entries found or unexpected data format")
                else:
                    st.info("📭 No entries in system memory yet")
            else:
                st.error(f"❌ Failed to fetch memory data (Status: {memory_response.status_code})")
                
        except requests.RequestException as e:
            st.error(f"❌ Connection error: {e}")
        except Exception as e:
            st.error(f"❌ Error processing memory data: {e}")

# Footer with system information
st.markdown("---")
st.markdown("### 🔗 API Endpoints")

# Display available endpoints
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔄 Processing Endpoints:**
    - `POST /process/email` - Email content analysis
    - `POST /process/json` - JSON payload processing  
    - `POST /process/pdf` - PDF document analysis
    """)

with col2:
    st.markdown("""
    **📊 System Endpoints:**
    - `GET /memory` - View system memory
    - `POST /crm/escalate` - CRM escalation
    - `POST /risk_alert` - Risk alert system
    - `POST /log` - Log alert system
    """)

# System information
with st.expander("🔧 System Information"):
    st.markdown(f"**🌐 API Base URL:** `{API_BASE}`")
    st.markdown(f"**🕒 Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown(f"**🔄 Auto-refresh:** {'✅ Enabled' if auto_refresh else '❌ Disabled'}")
    st.markdown(f"**🔌 Connection Status:** {'🟢 Connected' if check_api_connection() else '🔴 Disconnected'}")
    st.markdown(f"**📝 Raw Response Display:** {'✅ Enabled' if show_raw_response else '❌ Disabled'}")

# Add some helpful tips
st.markdown("---")
st.markdown("### 💡 Usage Tips")
st.markdown("""
- **Email Processing**: Paste email content including subject lines for best classification results
- **JSON Processing**: Use properly formatted JSON - the system will validate before processing
- **PDF Processing**: Upload PDF documents for content extraction and analysis
- **Memory View**: Monitor all processed entries and their risk assessments in real-time
- **Auto-refresh**: Enable to automatically update the memory view every few seconds
""")