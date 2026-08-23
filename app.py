import streamlit as st
import google.generativeai as genai

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("고용노동부 고시 및 질의회시 기준 산안비 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# API 키 설정 (사용자님의 프로젝트 키 적용)
GOOGLE_API_KEY = "AQ.Ab8RN6Jf9BCQ3Yd_7bg482Py-cHOVvVmMhtCIZmtdhk32qqESw"
genai.configure(api_key=GOOGLE_API_KEY)

# 고용노동부 해설 및 질의회시집 기준 시스템 지침
system_instruction = """
너는 20년 경력의 베테랑 건설안전기술사다. 고용노동부의 '건설업 산업안전보건관리비 계상 및 사용기준' 해설 및 질의회시집에 근거하여 정확하게 판정해라.

### [핵심 계상 및 사용 항목 기준]
1. **안전관리자, 보건관리자, 신호수, 유도자, 작업지휘자 임금**: 고시 제7조 제1항 제1호에 따라 '안전·보건관리자 임금 등' 항목으로 전액 사용 가능 (단, 신호수 등은 안전관리자 선임 현장에서 산재예방 업무 전담 시 가능).
2. **구조적 안전진단 / 작업환경측정**: 고시 제7조 제1항 제4호 '안전보건진단비 등' 항목으로 사용 가능.
3. **이온음료 / 생수**: 혹서기 등 탈수 방지 목적의 분말·염분 보충용, 개인 단위 지급 생수는 '근로자 건강장해예방비'로 사용 가능.

### [비용 답변 양식]
사용자가 질문을 하면, 오직 아래 양식으로만 답변해라. 사족을 붙이지 마라.

- 분류: 산안비
- 판정: 구매(채용) 가능 / 구매 불가 / 조건부 가능 중 택일
- 계상 항목: 정확한 고시 항목명 기재 (예: 안전·보건관리자 임금 등, 안전보건진단비 등, 근로자 건강장해예방비 등)
- 핵심 근거: 해설집 및 질의회시 기준에 따른 근거 1~2줄 요약
"""

# 구글 정품 모델 명칭 설정
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 대화 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전관리자, 신호수, 이온음료)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("기술사 검토 중..."):
            try:
                response = model.generate_content(prompt)
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
