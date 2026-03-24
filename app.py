import streamlit as st
import pandas as pd
import os

# --- Configuration & Setup ---
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")
DATA_FILE = "data/students.csv"

# --- Helper Function: Save Data ---
def save_student_data(name, grade, major, gpa, activities):
    # Prepare the new data as a dictionary
    new_data = {
        "Name": [name],
        "Grade Level": [grade],
        "Major": [major],
        "GPA": [gpa],
        "Activities": [", ".join(activities) if activities else "None"]
    }
    df_new = pd.DataFrame(new_data)
    
    # If the file exists, append without headers. If not, create it with headers.
    if os.path.exists(DATA_FILE):
        df_new.to_csv(DATA_FILE, mode='a', header=False, index=False)
    else:
        df_new.to_csv(DATA_FILE, mode='w', header=True, index=False)

# --- Custom CSS ---
st.markdown("""
    <style>
    .main-title { font-family: sans-serif; color: #1E3A8A; text-align: center; font-weight: 700; }
    .student-card {
        background-color: #F3F4F6; padding: 25px; border-radius: 12px;
        border-left: 6px solid #3B82F6; color: #333333; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- App UI ---
st.markdown("<h1 class='main-title'>🎓  Student Portal</h1>", unsafe_allow_html=True)
st.write("Enter student details below to generate their profile and save it to the database.")
st.divider()

# Input Columns
col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("👤 Student Name", placeholder="e.g., Alex Johnson")
    grade_level = st.selectbox("📚 Grade Level", ["Freshman", "Sophomore", "Junior", "Senior"])

with col2:
    major = st.text_input("🎯 Major / Stream", placeholder="e.g., Computer Science")
    gpa = st.slider("📊 Current GPA", min_value=0.0, max_value=10.0, value=3.0, step=0.1)

activities = st.multiselect(
    "🏅 Extracurricular Activities", 
    ["Sports", "Debate Club", "Robotics", "Drama", "Music", "Volunteering"]
)

st.write("") 

# --- Submission Logic ---
if st.button("💾 Save Student Record", use_container_width=True):
    if student_name and major:
        # Save to CSV
        save_student_data(student_name, grade_level, major, gpa, activities)
        
        st.balloons() 
        st.success(f"🎉 Record for {student_name} generated and saved successfully!")
        
        # Display Card
        st.markdown("### 📋 Student Profile Summary")
        st.markdown(f"""
        <div class="student-card">
            <h3 style="margin-top: 0; color: #1E3A8A;">{student_name}</h3>
            <p><b>Grade:</b> {grade_level}</p>
            <p><b>Major:</b> {major}</p>
            <p><b>GPA:</b> {gpa}</p>
            <p><b>Activities:</b> {', '.join(activities) if activities else 'None recorded'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.metric(label="Academic Standing (GPA)", value=gpa, delta=round(gpa - 2.5, 1), delta_color="normal")
    else:
        st.error("⚠️ Please fill in both the Student Name and Major before submitting.")

# --- Database Viewer Section ---
st.divider()
if st.checkbox("📁 View Saved Student Database"):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No student records found yet. Submit a record above to create the database.")