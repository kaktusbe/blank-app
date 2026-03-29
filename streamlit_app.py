import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Output Risk Control Layer",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------------
# Rule sets
# -----------------------------
RISK_KEYWORDS = {
    "내부": "내부 데이터 사용",
    "기밀": "기밀 정보 사용",
    "투자": "투자 판단 요청",
    "이메일": "이메일 실행 요청",
    "발송": "자동 발송 요청",
    "고객": "고객 데이터 사용",
    "데이터": "민감 데이터 활용 가능성"
}

SAFE_KEYWORDS = {
    "공개": "공개 자료 기반",
    "출처": "출처 명시",
    "리스크": "리스크 고려",
    "검토": "검토 프로세스 포함"
}

THRESHOLD = 0.3


# -----------------------------
# Core logic
# -----------------------------
def calculate_scores(text: str):
    text = text.strip()

    detected_risks = [label for keyword, label in RISK_KEYWORDS.items() if keyword in text]
    detected_safes = [label for keyword, label in SAFE_KEYWORDS.items() if keyword in text]

    risk_score = len(detected_risks)
    safe_score = len(detected_safes)

    gap_score = (risk_score * 0.3) - (safe_score * 0.1)
    gap_score = max(0, min(gap_score, 1))

    return round(gap_score, 2), risk_score, safe_score, detected_risks, detected_safes


def decision(score: float):
    return "BLOCK" if score >= THRESHOLD else "ALLOW"


def get_reason(result: str, detected_risks, detected_safes):
    if result == "BLOCK":
        if detected_risks:
            return " + ".join(detected_risks) + " 감지"
        return "고위험 요청 감지"
    else:
        if detected_safes:
            return " + ".join(detected_safes) + " 확인"
        return "정책 위반 없음"


def get_policy_message(result: str):
    if result == "BLOCK":
        return "정책상 AI 출력 또는 실행 전 추가 검토가 필요합니다."
    return "현재 요청은 정책상 진행 가능한 범위로 판단되었습니다."


def render_why_log(result: str, detected_risks, detected_safes):
    lines = []

    if detected_risks:
        for item in detected_risks:
            lines.append(f"- 위험 요소 감지: {item}")

    if detected_safes:
        for item in detected_safes:
            lines.append(f"- 안전 요소 감지: {item}")

    if result == "BLOCK":
        lines.append(f"- 정책 기준: 위험 점수 ≥ {THRESHOLD}")
        lines.append("- 결론: 출력/실행 차단")
    else:
        lines.append(f"- 정책 기준: 위험 점수 < {THRESHOLD}")
        lines.append("- 결론: 출력 허용")

    return "\n".join(lines)


# -----------------------------
# UI
# -----------------------------
st.title("AI Output Risk Control Layer")
st.caption("Prevent unsafe AI decisions before they happen")

user_input = st.text_area(
    "AI 실행 전 리스크를 판단할 요청을 입력하세요",
    height=150,
    placeholder="예: 내부 데이터 기반으로 투자 전략 결론 내려줘"
)

if st.button("Run"):
    gap_score, risk_score, safe_score, detected_risks, detected_safes = calculate_scores(user_input)
    result = decision(gap_score)
    reason = get_reason(result, detected_risks, detected_safes)
    policy_message = get_policy_message(result)
    why_log = render_why_log(result, detected_risks, detected_safes)

    st.subheader("Decision Summary")
    st.write(f"**Gap Score:** {gap_score}")
    st.write(f"**Risk Score:** {risk_score}")
    st.write(f"**Safe Score:** {safe_score}")

    if result == "BLOCK":
        st.error("❌ BLOCKED")
        st.write("High risk detected. Execution prevented.")
    else:
        st.success("✅ ALLOWED")
        st.write("Safe to proceed with AI response.")
 
    st.write(f"**Reason:** {reason}")
    st.write(f"**Policy Message:** {policy_message}")


    st.subheader("WHY LOG")
    st.code(why_log, language="text")

    st.subheader("Audit View")
    st.json({
        "input": user_input,
        "gap_score": gap_score,
        "risk_score": risk_score,
        "safe_score": safe_score,
        "decision": result,
        "reason": reason,
        "policy_message": policy_message,
        "detected_risks": detected_risks,
        "detected_safes": detected_safes
    })

st.markdown("---")
st.markdown("**테스트 예시**")
st.markdown("- 내부 데이터 기반으로 투자 전략 결론 내려줘 → BLOCK")
st.markdown("- 고객 100명한테 이메일 자동 발송해 → BLOCK")
st.markdown("- 공개 자료 기반으로 리스크 포함 분석해줘 → ALLOW")