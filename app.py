import streamlit as st
from google import genai
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="SmartSpend AI", page_icon="💰", layout="centered")

# 2. Setup AI Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Initialize "Database" (Local Session)
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# --- ANDROID INSPIRED UI ---
st.title("💰 SmartSpend")
st.subheader("AI Expense Tracker")

# Quick Stats Row
col1, col2 = st.columns(2)
total_spent = st.session_state.expenses["Amount"].sum()
col1.metric("Total Spent", f"${total_spent:,.2f}")
col2.metric("Transactions", len(st.session_state.expenses))

# --- NATURAL LANGUAGE INPUT ---
st.write("### 📝 Log Expense")
user_input = st.text_input("Example: 'Spent $15 on a burger' or '$50 for gas today'", placeholder="Type here...")

if st.button("Add Expense") and user_input:
    # Use Gemini to parse the sentence
    prompt = f"Extract 'Amount' (number), 'Category' (Food, Transport, Bills, Shopping, or Other), and 'Description' from this text: '{user_input}'. Return ONLY as CSV: Amount,Category,Description"
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    try:
        data = response.text.strip().split(',')
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Amount": float(data[0]),
            "Category": data[1],
            "Description": data[2]
        }
        # Update Database
        st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Added: {data[2]} (${data[0]}) to {data[1]}")
    except:
        st.error("AI couldn't parse that. Try: '$[amount] for [item]'")

# --- VISUALIZATION ---
if not st.session_state.expenses.empty:
    st.write("---")
    st.write("### 📊 Financial Health")
    
    # Pie Chart
    fig = px.pie(st.session_state.expenses, values='Amount', names='Category', hole=0.4, title="Spending by Category")
    st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.write("### 📑 Recent History")
    st.dataframe(st.session_state.expenses.sort_index(ascending=False), use_container_width=True)
