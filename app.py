import streamlit as st
from groq import Groq

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("산안비 및 건설안전 기준 비용 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# Groq API 키 설정
client = Groq(api_key="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")

# 시스템 지침(프롬프트) 설정
system_prompt = """
너는 20년 경력의 베테랑 건설안전기술사다. 
사용자가 질문을 하면, 오직 하나의 양식인 [비용 답변 양식]으로만 답변해라. 절대 다른 형태의 제목을 출력하지 마라.
모든 항목의 대괄호([])나 빈칸을 남겨두지 말고, 내용을 반드시 글자로 채워서 출력할 것.

### [비용 답변 양식]
- 분류: 산안비
- 판정: 구매(채용) 가능 (또는 구매 불가, 조건부 가능 중 택일)
- 계상 항목: 고시 기준 대표 항목명만 기재 (예: 구급 및 보건 관리비, 안전시설비 등)
- 핵심 근거: 1~2줄로 핵심 조건과 법적 근거 요약
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전모, 이온음료, 타이레놀)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("기술사 검토 중..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-20b",  # Groq 최신 지원 모델 반영
                )
                ai_response = chat_completion.choices[0].message.content
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
