import streamlit as st
import pandas as pd
import gspread
from datetime import datetime, date
from google.oauth2.service_account import Credentials

# Emoji moods
MOODS = {
    "😊": "Happy",
    "😠": "Angry",
    "😕": "Confused",
    "🎉": "Excited"
}

# Google Sheet setup
SHEET_NAME = "Mood Log"

# Authenticate
creds = Credentials.from_service_account_info(
    st.secrets["GOOGLE_SHEETS_CREDS"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1  # First worksheet

st.set_page_config(page_title="Mood Logger", page_icon="📝")
st.title("Mood Logger")

# Mood entry form
mood_emoji = st.selectbox("How are you feeling?", list(MOODS.keys()))
note = st.text_input("Add a short note (optional)")

if st.button("Submit Mood"):
    timestamp = datetime.now().isoformat()
    sheet.append_row([timestamp, mood_emoji, note])
    st.success("Mood logged to Google Sheets!")

# Load data from sheet
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    today = date.today()
    today_df = df[df["date"] == today]

    if not today_df.empty:
        mood_counts = today_df["mood"].value_counts().sort_index()
        st.subheader("Today's Mood Summary")
        st.bar_chart(mood_counts)
    else:
        st.info("No moods logged yet for today.")
else:
    st.info("No data in sheet yet.")
