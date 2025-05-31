import streamlit as st
import requests
import json

st.set_page_config(page_title="Multi-Agent AI Interface", layout="centered")
st.title("🧠 Multi-Agent AI System Interface")

API_BASE = "http://localhost:8000"

# Helper to show API responses
def show_response(res):
    if res.status_code == 200:
        try:
            st.subheader("✅ Response:")
            st.json(res.json())
        except Exception as e:
            st.error(f"Response was not valid JSON: {e}")
            st.text(res.text)
    else:
        st.error(f"❌ Error {res.status_code}")
        try:
            st.json(res.json())
        except:
            st.text(res.text)

# Select Input Type
option = st.selectbox("📂 Select Input Type", ["Email", "JSON", "PDF"])

# Handle Email Input
if option == "Email":
    content = st.text_area("📧 Paste Email Content")
    if st.button("📨 Submit Email"):
        try:
            res = requests.post(f"{API_BASE}/process/email", json={"content": content})
            show_response(res)
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")

# Handle JSON Input
elif option == "JSON":
    json_input = st.text_area("🔧 Paste JSON Payload")
    if st.button("📨 Submit JSON"):
        try:
            parsed = json.loads(json_input)
            res = requests.post(f"{API_BASE}/process/json", json=parsed)
            show_response(res)
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")

# Handle PDF Upload
elif option == "PDF":
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
    if st.button("📨 Submit PDF") and uploaded_file:
        try:
            # Read file into memory buffer before sending
            file_bytes = uploaded_file.read()
            res = requests.post(
                f"{API_BASE}/process/pdf",
                files={"file": (uploaded_file.name, file_bytes, "application/pdf")}
            )
            show_response(res)
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")

# View Memory Log
if st.button("📜 View Memory Log"):
    try:
        mem = requests.get(f"{API_BASE}/memory")
        show_response(mem)
    except requests.RequestException as e:
        st.error(f"Failed to fetch memory log: {e}")