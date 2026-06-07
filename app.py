import re

import pandas as pd
import streamlit as st
from supabase import create_client


# =========================
# Supabase 연결 정보
# =========================

SUPABASE_URL = "https://enprckfhepllyvukcuga.supabase.co"
SUPABASE_KEY = "sb_publishable_cR7O7Ui1VbAlpyPXHaW7LQ_t5ngH9jP"

TABLE_NAME = "student_life"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================
# 함수 만들기
# =========================

def load_data():
    """Supabase에서 전체 데이터를 불러오는 함수"""
    response = supabase.table(TABLE_NAME).select("*").execute()
    data = response.data
    return pd.DataFrame(data)


def make_next_student_id():
    """
    student_id를 자동으로 생성하는 함수
    예: S001, S002, S003 ...
    """
    df = load_data()

    if df.empty or "student_id" not in df.columns:
        return "S001"

    max_number = 0

    for student_id in df["student_id"].dropna():
        student_id = str(student_id)

        match = re.search(r"\d+", student_id)

        if match:
            number = int(match.group())
            if number > max_number:
                max_number = number

    next_number = max_number + 1

    return f"S{next_number:03d}"


def insert_data(new_data):
    """Supabase에 새 데이터를 저장하는 함수"""
    response = supabase.table(TABLE_NAME).insert(new_data).execute()
    return response


# =========================
# Streamlit 화면 구성
# =========================

st.set_page_config(
    page_title="학생 생활습관 데이터 입력 웹앱",
    page_icon="📘",
    layout="centered"
)

st.title("학생 생활습관 데이터 입력 웹앱")

st.write(
    "학생 생활습관 데이터를 입력하면 Supabase 데이터베이스에 바로 저장됩니다."
)

st.divider()


# =========================
# 데이터 입력 폼
# =========================

st.subheader("1. 데이터 입력하기")

next_student_id = make_next_student_id()

st.info(f"자동 생성될 학생 ID: {next_student_id}")

with st.form("student_form"):
    grade_class = st.text_input("반", placeholder="예: 1-1")

    sleep_hours = st.number_input(
        "수면시간",
        min_value=0.0,
        max_value=24.0,
        step=0.5
    )

    phone_hours = st.number_input(
        "스마트폰사용시간",
        min_value=0.0,
        max_value=24.0,
        step=0.5
    )

    breakfast = st.selectbox(
        "아침식사여부",
        ["YES", "NO"]
    )

    commute_minutes = st.number_input(
        "통학시간",
        min_value=0,
        max_value=300,
        step=5
    )

    tired_score = st.slider(
        "피곤함점수",
        min_value=1,
        max_value=5,
        value=3
    )

    focus_score = st.slider(
        "집중도점수",
        min_value=1,
        max_value=5,
        value=3
    )

    favorite_subject = st.text_input(
        "좋아하는과목",
        placeholder="예: 수학"
    )

    submitted = st.form_submit_button("데이터 저장하기")

if submitted:
    if not grade_class:
        st.warning("반을 입력하세요.")
    elif not favorite_subject:
        st.warning("좋아하는 과목을 입력하세요.")
    else:
        new_data = {
            "student_id": next_student_id,
            "grade_class": grade_class,
            "sleep_hours": sleep_hours,
            "phone_hours": phone_hours,
            "breakfast": breakfast,
            "commute_minutes": commute_minutes,
            "tired_score": tired_score,
            "focus_score": focus_score,
            "favorite_subject": favorite_subject
        }

        try:
            insert_data(new_data)
            st.success(f"데이터가 저장되었습니다. 자동 생성된 학생 ID: {next_student_id}")
            st.rerun()
        except Exception as e:
            st.error("데이터 저장 중 오류가 발생했습니다.")
            st.write(e)


# =========================
# 저장된 데이터 확인
# =========================

st.divider()

st.subheader("2. 저장된 데이터 확인")

try:
    df = load_data()

    if df.empty:
        st.info("아직 저장된 데이터가 없습니다.")
    else:
        st.dataframe(df, use_container_width=True)

        st.write("총 데이터 수:", len(df), "개")

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.write(e)
