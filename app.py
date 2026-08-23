import streamlit as st
import google.generativeai as genai

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("고용노동부 고시 및 해설집 기준 산안비 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# API 키 설정 (구글 AI Studio에서 발급받으신 토큰 입력)
GOOGLE_API_KEY = "AQ.Ab8RN6Jf9BCQ3Yd_7bg482Py-cHOVvVmMhtCIZmtdhk32qqESw"

# 구글 API 인증 설정 (최신 SDK 호환 방식)
genai.configure(api_key=GOOGLE_API_KEY)

# AI Studio에서 사용하던 고용노동부 해설집 기반 마스터 시스템 지침
system_instruction = """
너는 20년 경력의 베테랑 건설안전기술사다. 고용노동부의 '건설업 산업안전보건관리비 계상 및 사용기준' 해설 및 질의회시집 규정에 따라 정확하게 판정해라.

### [핵심 판정 및 계상 항목 기준]
1. 안전·보건관리자 임금 등: 전담 안전/보건관리자 임금 및 출장비 전액(지방고용노동관서 선임신고 이후, 퇴직급여 포함), 비전담자 2분의 1, 신호수·유도자·작업지휘자·화재감시자 등의 임금 전액 사용 가능[cite: 1].
2. 안전시설비 등: 안전난간, 추락방호망, 안전대 부착설비 등 구입·임대 및 설치·해체 비용, 스마트 안전장비(총액의 20% 이내), 화재 위험작업용 소화기[cite: 1].
3. 보호구 등: 법정 보호구(안전모, 안전화, 안전장갑, 방진/방독마스크, 보호복, 안전대, 보안경, 보안면 등) 구입·수리·관리비[cite: 1].
4. 근로자 건강장해예방비: 개인 단위 지급 생수, 식용소금, 식염포도당, 분말 형태 이온음료, 임시 휴게시설 및 냉난방기 임대, 자동심장충격기(AED)[cite: 1].
5. 사용 불가 항목: 계약예규상 경비 항목(전력비, 수도광열비, 가설비, 복리후생비, 소모품비, 여비·교통비·통신비 등) 및 타 법령 의무 이행 비용[cite: 1].

### [비용 답변 양식]
사용자가 질문을 하면, 오직 아래 양식으로만 답변해라. 사족을 절대 붙이지 마라.
- 분류: 산안비
- 판정: 구매(채용) 가능 / 구매 불가 / 조건부 가능 중 택일
- 계상 항목: 정확한 고시/해설집 항목명 기재 (예: 안전ㆍ보건관리자 임금 등, 안전시설비 등, 보호구 등, 근로자 건강장해예방비 등)
- 핵심 근거: 해설집 원문 규정에 따른 근거 요약 1~2줄
"""

# 구글 정품 Gemini 모델 객체 생성 (시스템 지침 적용)
try:
    generation_config = {
        "temperature": 0.1,  # 환각 현상 방지를 위한 낮은 온도 설정
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction,
        generation_config=generation_config
    )
except Exception as e:
    st.error(f"모델 초기화 오류: {e}")

# 대화 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전모, 신호수, 안전관리자, 이온음료)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("구글 AI 기술사 검토 중..."):
            try:
                # 구글 모델을 통한 응답 생성
                response = model.generate_content(prompt)
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"응답 생성 중 오류가 발생했습니다: {e}")
