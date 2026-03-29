import streamlit as st

RISK_KEYWORDS = ["내부", "투자", "이메일", "고객", "데이터"]
SAFE_KEYWORDS = ["공개", "출처", "리스크"]

def calculate_gap(text):
    risk = sum(1 for k in RISK_KEYWORDS if k in text)
    safe = sum(1 for k in SAFE_KEYWORDS if k in text)
    score = (risk * 0.3) - (safe * 0.1)
    return max(0, min(score, 1))

def decision(score):
    return "BLOCK" if score >= 0.3 else "ALLOW"

st.title("AI Output Risk Control Layer")

text = st.text_area("AI 실행 전 리스크를 판단할 요청을 입력하세요")

if st.button("Run"):
    gap = calculate_gap(text)
    result = decision(gap)

    st.write(f"Gap Score: {gap}")

    if result == "BLOCK":
        st.error("❌ BLOCK")
        st.write("Reason:", "내부 데이터 사용 + 투자 판단 요청 감지")
        
    else:   
        st.success("✅ ALLOWED" \
        "Safe to proceed with AI response.")