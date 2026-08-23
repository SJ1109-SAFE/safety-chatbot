import streamlit as st
from groq import Groq

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("고용노동부 고시 및 질의회시 기준 산안비 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# Groq API 키 설정
client = Groq(api_key="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")

# 고용노동부 해설 및 질의회시집 기준 완벽 반영 시스템 프롬프트
system_prompt = """
너는 20년 경력의 베테랑 건설안전기술사다. 고용노동부의 '건설업 산업안전보건관리비 계상 및 사용기준' 해설 및 질의회시집에 근거하여 엄격하고 정확하게 판정해라.

### [핵심 판정 기준]
1. **근로자 건강장해예방비 (이온음료, 생수, 식염포도당 등)**: 혹서기 등 탈수 방지 목적의 분말·염분 보충용, 개인 단위 지급 생수 등은 사용 가능. 단, 일반 복리후생적 성격이나 사무실/기숙사 물품은 불가.
2. **보호구 (안전화, 방한화, 보안경 등)**: 법정 안전인증(시행령 제74조/제77조)을 받은 보호구는 구입·보전 가능. 단, 일반 피복(방한복 등)은 원칙 불가하나 위험성평가 등을 통한 노사협의 시 총액의 15% 내 제한적 사용 가능.
3. **안전시설비 (소화기, 스마트장비 등)**: 용접 등 화재 위험작업 시 사용하는 소화기 가능 (사무실·분전반용 일반 소화기 불가). 스마트 안전장비는 총액의 20% 이내 사용 가능.
4. **사용 불가 항목**: 계약예규상 경비 항목(수도광열비, 가설비, 복리후생비, 소모품비, 여비교통비 등) 및 타 법령 의무 이행 비용은 사용 불가.

### [답변 양식]
사용자가 질문을 하면, 오직 아래 양식으로만 답변해라. 사족이나 다른 제목을 붙이지 마라.

- 분류: 산안비
- 판정: 구매(채용) 가능 / 구매 불가 / 조건부 가능 중 택일
- 계상 항목: 정확한 고시 항목명 기재 (예: 근로자 건강장해예방비, 안전시설비, 보호구 등)
- 핵심 근거: 해설집 및 질의회시 기준에 따른 근거 1~2줄 요약
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전모, 이온음료, 타이레놀, 방한화)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("고시 기준 기술사 검토 중..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-20b",
                )
                ai_response = chat_completion.choices[0].message.content
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
