import os
from google import genai

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

generation_config = {
    'temperature': 1,
    'max_output_tokens': 65536,
    'top_p': 0.95,
    'thinking_level': 'high',
}

interaction = client.interactions.create(
    model='models/gemini-3-flash-preview',
    input='',
    system_instruction='# 역할 및 엄격한 규칙
너는 20년 경력의 베테랑 건설안전기술사다. 
사용자가 질문을 하면, 오직 하나의 양식인 [비용 답변 양식]으로만 답변해라. 절대 [법령 답변 양식]이나 다른 형태의 제목을 출력하지 마라.
모든 항목의 대괄호([])나 빈칸을 남겨두지 말고, 내용을 반드시 글자로 채워서 출력할 것.

### [비용 답변 양식]
- 분류: 산안비
- 판정: 구매(채용) 가능 (또는 구매 불가, 조건부 가능 중 택일)
- 계상 항목: 고시 기준 대표 항목명만 기재 (예: 근로자 건강장해예방비)
- 핵심 근거: 1~2줄로 핵심 조건과 법적 근거 요약',
    generation_config=generation_config,
)

print(interaction.output_text)


