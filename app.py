import streamlit as st
from supabase import create_client
import pandas as pd

SUPABASE_URL = "https://enprckfhepllyvukcuga.supabase.co"
SUPABASE_KEY = "sb_publishable_cR7O7Ui1VbAlpyPXHaW7LQ_t5ngH9jP"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("학생 생활습관 데이터 입력 웹앱")

with st.form("student_form"):
    student_id = st.text_input("학생 ID", placeholder="예: s_020")
    grade_class = st.text_input("반", placeholder="예: 1-1")
    sleep_hours = st.number_input("수면시간", min_value=0.0, max_value=24.0, step=0.5)
    phone_hours = st.number_input("스마트폰사용시간", min_value=0.0, max_value=24.0, step=0.5)
    breakfast = st.selectbox("아침식사여부", ["YES", "NO"])
    commute_minutes = st.number_input("통학시간", min_value=0, max_value=300, step=5)
    tired_score = st.slider("피곤함점수", 1, 5, 3)
    focus_score = st.slider("집중도점수", 1, 5, 3)
    favorite_subject = st.text_input("좋아하는과목", placeholder="예: 수학")

    submitted = st.form_submit_button("데이터 저장하기")

if submitted:
    new_data = {
        "student_id": student_id,
        "grade_class": grade_class,
        "sleep_hours": sleep_hours,
        "phone_hours": phone_hours,
        "breakfast": breakfast,
        "commute_minutes": commute_minutes,
        "tired_score": tired_score,
        "focus_score": focus_score,
        "favorite_subject": favorite_subject
    }

    supabase.table("student_survey").insert(new_data).execute()
    st.success("데이터가 저장되었습니다.")

st.divider()

st.subheader("저장된 데이터 확인")

response = supabase.table("student_survey").select("*").execute()
df = pd.DataFrame(response.data)

st.dataframe(df)
