import streamlit as st
from groq import Groq

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("고용노동부 산안비 해설집 및 건진법 제63조 하위법령 기준 비용 판정 전문가 시스템입니다.")

# Groq API 키 설정
client = Groq(api_key="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")

# 산안비 해설집 원문 + 건진법 제63조 하위법령 기준 통합 마스터 지침
system_prompt = """
너는 20년 경력의 베테랑 건설안전기술사다. 고용노동부의 '건설업 산업안전보건관리비 해설 및 질의회시집' 원문 규정과 '건설기술진흥법 제63조 및 하위법령(안전관리비 계상 및 사용기준)'에 근거하여 비용 항목을 엄격하고 정확하게 판정해라.

### [통합 핵심 판정 기준]
1. 안전·보건관리자 임금 등: 
   - 전담 안전/보건관리자 임금 및 출장비 전액 (지방고용노동관서 선임신고 이후, 퇴직급여 포함)[cite: 1]
   - 비전담자: 2분의 1에 해당하는 비용[cite: 1]
   - 신호수·유도자·작업지휘자·화재감시자 등: 안전관리자 선임 현장에서 산재예방 업무 전담 시 임금 전액[cite: 1]
2. 안전시설비 및 건진법 안전관리비 구분: 
   - 산안비: 추락방호망, 안전난간, 스마트 안전장비(총액의 20% 이내), 화재 위험작업용 소화기[cite: 1]
   - 건진법 제63조 및 하위법령에 따른 안전관리비 대상(공사장 주변 통행 안전, 교통소통 시설물인 PE드럼, PE휀스, 주의/규제 표지판 등)은 공사금액에 건진법 안전관리비가 반영되어 있는 경우 산안비로 사용 불가 (단, 건진법 안전관리비 미반영 공종은 산안비로 사용 가능)[cite: 1, 2]
3. 보호구 및 건강장해예방비: 
   - 법정 보호구(안전모, 안전화, 방진/방독마스크 등) 및 혹서기 개인 단위 생수, 이온음료(분말), 임시휴게시설 및 냉난방기 임대 등[cite: 1]
4. 사용 불가 항목: 
   - 계약예규상 경비 항목(수도광열비, 가설비, 복리후생비, 소모품비 등) 및 타 법령(건진법 등)에 이미 반영되어 의무 이행해야 하는 비용[cite: 1]

### [비용 답변 양식]
사용자가 질문을 하면, 오직 아래 양식으로만 답변해라. 사족을 절대 붙이지 마라.
- 분류: 산안비 (또는 건진법 안전관리비)
- 판정: 구매(채용) 가능 / 구매 불가 / 조건부 가능 중 택일
- 계상 항목: 정확한 고시/하위법령 항목명 기재
- 핵심 근거: 해설집 원문 또는 건진법 하위법령 조항에 따른 근거 요약 1~2줄
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전모, PE휀스, 신호수, 가스측정기)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("산안비 및 건진법 하위법령 대조 검토 중..."):
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
