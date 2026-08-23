import streamlit as st
import google.generativeai as genai

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("산안비 및 건설안전 기준 비용 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# API 키 설정
GOOGLE_API_KEY = "AQ.Ab8RN6Jf9BCQ3Yd_7bg482Py-cHOVvVmMhtCIZmtdhk32qqESw"
genai.configure(api_key=GOOGLE_API_KEY)

# 시스템 지침(프롬프트) 설정
system_instruction = """
# 역할 및 엄격한 규칙
너는 20년 경력의 베테랑 건설안전기술사다. 
사용자가 질문을 하면, 오직 하나의 양식인 [비용 답변 양식]으로만 답변해라. 절대 다른 형태의 제목을 출력하지 마라.
모든 항목의 대괄호([])나 빈칸을 남겨두지 말고, 내용을 반드시 글자로 채워서 출력할 것.

### [비용 답변 양식]
- 분류: 산안비
- 판정: 구매(채용) 가능 (또는 구매 불가, 조건부 가능 중 택일)
- 계상 항목: 고시 기준 대표 항목명만 기재 (예: 구급 및 보건 관리비, 안전시설비 등)
- 핵심 근거: 1~2줄로 핵심 조건과 법적 근거 요약
"""

# 모델 명칭을 현재 활성화된 최신 표준 모델인 gemini-2.5-flash로 지정
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

# 대화 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전모, 이온음료, 타이레놀)"):
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
