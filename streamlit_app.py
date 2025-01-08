import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Streamlit 페이지 설정
st.set_page_config(page_title="설문응답공유", page_icon="📊", layout="centered")
st.title("📊 설문결과 공유")

st.info("""통계교육연수 설문 데이터를 조별로 분석하여 결과를 시각적으로 표현하는 페이지입니다. 각 조의 응답을 원그래프로 확인하고, 주관식 응답과 추가 평가 내용을 한눈에 볼 수 있습니다.""")
# Google Sheets 데이터 읽기

try:
        

    conn = st.connection("gsheets", type=GSheetsConnection)
    spreadsheet_url = st.secrets["gsheet"]["url"]
    data = conn.read(spreadsheet=spreadsheet_url).iloc[:, 3:23]

    if st.button("🔄 데이터 새로고침"):
        st.cache_data.clear()

    # 데이터 확인
    if data.empty:
        st.warning("아직 아무도 응답하지 않았어요!")
    else:
        st.success("데이터가 성공적으로 로드되었습니다!")

        # 데이터 처리: 첫 번째~9번째 열 가져오기
        data_2 = data.iloc[:, :9]
        data_2.columns = [f"col_{i+1}" for i in range(data_2.shape[1])]

        # 열 이름을 조 번호로 가정하고 각 열을 조별로 분석
        for i, col in enumerate(data_2.columns):
            group_number = i + 1
            st.write(f"##### {group_number}조 결과")

            group_data = data_2[col].dropna()
            response_counts = group_data.str.split(', ').explode().value_counts()
            st.write("총 요소 수", response_counts.sum())

            # 레이아웃 설정: 원그래프와 텍스트 병렬 표시
            col1, col2 = st.columns(2)

            with col1:
                # 원그래프 생성 (색상 팔레트 지정)
                colors = ["#B1F0F7", "#86C5D9", "#ECE7CB", "#F5D488", "#FFD700", "#FFA07A", "#87CEFA", "#9370DB"]
                fig, ax = plt.subplots()
                ax.pie(response_counts, labels=response_counts.index, autopct="%1.1f%%", startangle=90, colors=colors)
                ax.axis("equal")
                st.pyplot(fig)


            with col2:
                # 주관식 응답 정리
                st.write("##### 주관식 응답")
                if data.shape[1] > 9:
                    subjective_column_index = 9 + i  # 10번째 열부터 각 조별 열 선택
                    subjective_responses = data.iloc[:, subjective_column_index].tolist()
                    # st.write(subjective_responses)
                    if subjective_responses:
                        temp = data.iloc[:, subjective_column_index].dropna()
                        temp.columns = ["주관식 피드백 모아보기"]
                        st.dataframe(temp, hide_index=True)

                        # for j, response in enumerate(subjective_responses, start=1):
                            # st.write(i, response)
                            # st.write(f"- {response}")
    # 마지막 두 열에 대한 데이터 표시
    # st.subheader("추가 평가 및 강의 인상 깊은 점")

    # 추가 평가 요소
    st.write("#### 추가로 평가에 반영하고 싶으셨던 요소")
    additional_feedback = data.iloc[:, 19].dropna().tolist()
    if additional_feedback:
        for idx, feedback in enumerate(additional_feedback, start=1):
            st.write(f"{idx}. {feedback}")
    else:
        st.write("추가 평가 요소가 없습니다.")

    # # 강의에서 인상 깊었던 점
    # st.write("#### 강의에서 인상 깊었던 점 및 적용 계획")
    # lecture_feedback = data.iloc[:, 20].dropna().tolist()
    # if lecture_feedback:
    #     for idx, feedback in enumerate(lecture_feedback, start=1):
    #         st.write(f"{idx}. {feedback}")
    # else:
#     st.write("강의 인상 깊은 점에 대한 응답이 없습니다.")
except:
    st.error("현재 응답을 불러올 수 없네요!")

# 하단 Made by 메시지
st.markdown(
    """
    <div style="text-align: center; padding: 10px; background-color: #f8f9fa; color: #6c757d; border-top: 1px solid #dee2e6;">
        <p><strong>Made with ❤️ by 반포고 황수빈</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)

