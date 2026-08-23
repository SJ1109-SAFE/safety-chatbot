import streamlit as st
import google.generativeai as genai
import os

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 안전관리비 판독기", page_icon="👷‍♂️", layout="centered")

st.title("👷‍♂️ 스마트 안전관리비 판독기")
st.markdown("고용노동부 해설집 PDF 원문 기반 산안비 판정 전문가 시스템입니다. 무엇이든 물어보세요!")

# API 키 설정
GOOGLE_API_KEY = "AQ.Ab8RN6Jf9BCQ3Yd_7bg482Py-cHOVvVmMhtCIZmtdhk32qqESw"
genai.configure(api_key=GOOGLE_API_KEY)

# PDF 파일 경로 설정 (깃허브에 업로드한 PDF 파일명과 일치시켜 주세요)
PDF_PATH = "건설업 산업안전보건관리비 해설 및 질의회시집(최종).pdf"

@st.cache_resource
def load_pdf_to_gemini():
    """PDF 파일을 구글 서버에 업로드하고 모델에 연결합니다."""
    try:
        if os.path.exists(PDF_PATH):
            # 파일이 이미 업로드되어 있는지 확인 후 업로드
            pdf_file = genai.upload_file(PDF_PATH)
            return pdf_file
        else:
            return None
    except Exception as e:
        return None

# PDF 컨텍스트 준비
pdf_ref = load_pdf_to_gemini()

# 모델 설정 (gemini-1.5-flash)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 대화 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("현장에서 궁금한 자재나 비용 항목을 입력하세요 (예: 안전모, 신호수, 구조적 안전진단)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("해설집 PDF 원문 대조 및 기술사 검토 중..."):
            try:
                # 프롬프트와 함께 PDF 원문 컨텍스트를 모델에 전달
                if pdf_ref:
                    contents = [
                        pdf_ref,
                        f"""너는 20년 경력의 베테랑 건설안전기술사다. 
첨부된 '건설업 산업안전보건관리비 해설 및 질의회시집' PDF 원문을 철저히 참고하여 아래 양식으로만 답변해라.

### [비용 답변 양식]
- 분류: 산안비
- 판정: 구매(채용) 가능 / 구매 불가 / 조건부 가능 중 택일
- 계상 항목: 해설집 원문 기준 정확한 항목명 기재
- 핵심 근거: 해설집 원문 조항 및 질의회시 내용 인용하여 1~2줄 요약

사용자 질문: {prompt}"""
                    ]
                else:
                    contents = f"사용자 질문: {prompt} (주의: PDF 파일을 찾을 수 없습니다.)"

                response = model.generate_content(contents)
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"응답 생성 중 오류가 발생했습니다: {e}")
