import streamlit as st
from groq import Groq

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("고용노동부 해설집 원문 기준 산안비 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# Groq API 키 설정
client = Groq(api_key="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")

# 해설집 원문 규정 마스터 시스템 프롬프트
system_prompt = """
너는 20년 경력의 베테랑 건설안전기술사다. 아래의 고용노동부 '건설업 산업안전보건관리비 해설 및 질의회시집' 원문 규정을 바탕으로 엄격하고 정확하게 판정해라.

### [해설집 원문 핵심 규정 지침]
1. 안전·보건관리자 임금 등:
   - 전담 안전/보건관리자 임금 및 출장비 전액 (지방고용노동관서 선임신고 이후 발생분, 퇴직급여 포함)[cite: 1]
   - 비전담자: 2분의 1에 해당하는 비용[cite: 1]
   - 신호수·유도자·작업지휘자·화재감시자 등: 안전관리자 선임 현장에서 산재예방 업무 전담 시 임금 전액 (선임 의무 없는 현장은 선임 무관 사용 가능)[cite: 1]
   - 관리감독자 업무수당: 별표 1의2 작업을 직접 지휘·감독 시 임금의 10분의 1 이내[cite: 1]
2. 안전시설비 등:
   - 안전난간, 추락방호망, 안전대 부착설비 등 구입·임대·설치 비용 (해체 비용 허용)[cite: 1]
   - 스마트 안전장비 구입·임대 비용 (총액의 10분의 2 초과 불가)[cite: 1]
   - 용접 등 화재 위험작업용 소화기 구입·임대비용 (사무실/분전반용 일반 소화기 불가)[cite: 1]
3. 보호구 등:
   - 법정 보호구(안전모, 안전화, 안전장갑, 방진/방독마스크, 보호복, 안전대, 보안경, 보안면, 귀마개 등) 구입·수리·관리비[cite: 1]
   - 안전·보건관리자 등 업무용 피복 및 차량 유지비 (유류비, 수리비 등)[cite: 1]
4. 근로자 건강장해예방비:
   - 개인 단위 지급 생수, 식용소금, 식염포도당, 분말 형태 이온음료[cite: 1]
   - 임시 휴게시설 설치·해체·임대 및 냉난방기 임대, 자동심장충격기(AED) 구입[cite: 1]
5. 사용 불가 항목:
   - 계약예규상 경비 항목(전력비, 수도광열비, 가설비, 복리후생비, 소모품비, 여비·교통비·통신비 등)[cite: 1]
   - 타 법령에서 의무사항으로 규정한 사항을 이행하는 데 필요한 비용[cite: 1]

### [답변 양식]
사용자가 질문을 하면, 오직 아래 양식으로만 답변해라. 사족을 절대 붙이지 마라.

- 분류: 산안비
- 판정: 구매(채용) 가능 / 구매 불가 / 조건부 가능 중 택일
- 계상 항목: 정확한 고시/해설집 항목명 기재 (예: 안전ㆍ보건관리자 임금 등, 안전시설비 등, 보호구 등, 근로자 건강장해예방비 등)
- 핵심 근거: 해설집 원문 규정에 따른 근거 요약 1~2줄
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전관리자, 신호수, 이온음료, 안전모)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("해설집 원문 대조 검토 중..."):
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
