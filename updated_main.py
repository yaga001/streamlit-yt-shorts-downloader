import streamlit as st
import os
import yt_dlp
import shutil
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---- Analytics Counter ----
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 0
st.session_state.visit_count += 1

st.sidebar.markdown(f"👥 Visitors this session: **{st.session_state.visit_count}**")

# ---- Email Collection Section ----
st.sidebar.markdown("---")
st.sidebar.subheader("💌 Stay Updated!")
user_email = st.sidebar.text_input("Enter your email:")

if st.sidebar.button("Subscribe"):
    if user_email:
        try:
            # Connect to Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
            client = gspread.authorize(creds)

            sheet = client.open("ShortsSaverSubscribers").sheet1
            sheet.append_row([user_email])

            st.sidebar.success("Thank you for subscribing!")
        except Exception as e:
            st.sidebar.error(f"Error saving email: {e}")
    else:
        st.sidebar.error("Please enter a valid email address.")

# [Rest of your code remains unchanged until after app logic]

# ---- Footer Section ----

# Donation Button
st.markdown("""
<div style="text-align: center; margin-top: 50px;">
    <a href="https://www.buymeacoffee.com/yourusername" target="_blank">
        <img src="https://img.buymeacoffee.com/button-api/?text=Support me&emoji=☕&slug=yourusername&button_colour=FFDD00&font_colour=000000&font_family=Comic&outline_colour=000000&coffee_colour=ffffff" />
    </a>
</div>
""", unsafe_allow_html=True)

# Affiliate Banner Example
st.markdown("""
<div style='background-color: #e0f7fa; padding: 10px; border: 2px dashed blue; margin-top: 20px; text-align: center;'>
    <b>🌟 Recommended VPN for Privacy!</b><br>
    <a href="https://your-affiliate-link.com" target="_blank">Click here to get 70% off VPN now!</a>
</div>
""", unsafe_allow_html=True)

# Success Notification After Downloads
st.markdown("""
<div style='background-color: #e8f5e9; padding: 10px; border: 2px solid #4caf50; margin-top: 20px; text-align: center;'>
    🎉 <b>Download Complete! Thanks for visiting ShortsSaver!</b>
</div>
""", unsafe_allow_html=True)

# Footer Links (About, Contact, Privacy)
st.markdown("""
<hr style="margin-top: 50px;">
<div style='text-align: center; font-size: 14px;'>
    <a href="/about.html" target="_blank">About</a> | 
    <a href="/contact.html" target="_blank">Contact</a> | 
    <a href="/privacy.html" target="_blank">Privacy Policy</a>
</div>
""", unsafe_allow_html=True)
