# app.py로 저장하여 실행할 수 있는 전체 소스코드입니다.
import streamlit as st

st.set_page_config(page_title="서논술형 자동 채점 시스템", layout="wide")

st.title("🎯 국어과 서·논술형 문항 자동 채점 시스템")
st.caption("다양한 설명 방법과 매체의 복합양식성 (해냄에듀 실습 교사용)")
st.markdown("---")

# 사이드바에서 세트 선택
set_option = st.sidebar.selectbox(
    "📌 채점할 문항 세트를 선택하세요", 
    ["1번 세트 (사회적 촉진/억제)", "2번 세트 (정전기의 특징)", "3번 세트 (삶을 대하는 태도)"]
)

# -------------------------------------------------------------------------
# [Helper Functions] 공통 채점 로직 함수 정의
# -------------------------------------------------------------------------
def check_keywords(text, keywords):
    return any(kw in text.replace(" ", "") for kw in keywords)

def detect_explanation_method(text):
    """문장 내에서 사용된 설명 방법의 특성 표지어와 괄호 표기를 탐지"""
    methods = []
    text_no_space = text.replace(" ", "")
    
    # 1. 정의
    if "란" in text_no_space or "이란" in text_no_space or "말한다" in text_no_space or "정의" in text:
        methods.append("정의")
    # 2. 예시
    if "예를" in text_no_space or "예로는" in text_no_space or "예시" in text:
        methods.append("예시")
    # 3. 인과
    if "때문에" in text_no_space or "해서" in text_no_space or "하므로" in text_no_space or "인과" in text:
        methods.append("인과")
    # 4. 분석
    if "이루어져" in text_no_space or "나누어" in text_no_space or "분석" in text:
        methods.append("분석")
    # 5. 비교/대조
    if "달리" in text_no_space or "반면" in text_no_space or "공통" in text_no_space or "차이" in text_no_space or "비교" in text or "대조" in text:
        methods.append("비교와 대조")
    
    return methods

# -------------------------------------------------------------------------
# 1번 세트 채점 로직
# -------------------------------------------------------------------------
if set_option == "1번 세트 (사회적 촉진/억제)":
    st.subheader("🎬 1번 세트: 심리학 용어의 학습 적용")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### ✍️ 학생 답안 입력")
        st.markdown("**[서·논술형 1] 표 빈칸 채우기**")
        q1_1 = st.text_input("(1) 과제의 특성 빈칸", placeholder="예: 비교적 쉬운 취미 생활이나 큰 노력을 들일 필요가 없는 과제")
        q1_2 = st.text_input("(2) 효율적인 환경 및 방법 빈칸", placeholder="예: 충분히 연습하며 익숙해질 때까지 차분하게 혼자 집중하는 시간을 가짐")
        q1_3 = st.text_input("(3) 관련된 심리 현상 빈칸", placeholder="예: 사회적 억제")
        
        st.markdown("**[서·논술형 2] 설명문 이어 쓰기**")
        q2_ans = st.text_area("조건에 맞게 작성한 문장 전체 (1, 2번 문장 통합 입력)", 
                              placeholder="예: 평소 친숙하고 좋아하는 과목은 공부 모임을 만들어 함께 공부하면 효율적이다(인과). 반면 어렵고 복잡한 과제는 혼자 집중해야 한다(대조).")
        
        st.markdown("**[서·논술형 3] 영상 연출 계획**")
        q3_a = st.text_input("시각 요소(Ⓐ) 및 효과", placeholder="예: 혼자 독서실에서 집중하는 모습 / 혼자 집중하는 시간이 필요함을 시각화함")
        q3_b = st.text_input("청각 요소(Ⓑ) 및 효과", placeholder="예: 고요하고 정적 상태 유지 / 차분한 환경임을 체감하게 함")

    with col2:
        st.markdown("### 📊 채점 결과 및 피드백")
        if st.button("💯 1번 세트 채점하기"):
            # 서논술 1 채점
            s1_score = 0
            s1_feedback = []
            if check_keywords(q1_1, ["쉬운", "취미", "노력", "어렵지않은"]): 
                s1_score += 1
            else: s1_feedback.append("(1)번: '쉬운 과제' 맥락이 부족합니다.")
            
            if check_keywords(q1_2, ["혼자", "차분", "집중", "연습"]): 
                s1_score += 1
            else: s1_feedback.append("(2)번: '혼자 집중/연습' 내용이 유실되었습니다.")
                
            if "억제" in q1_3 and "촉진" not in q1_3: 
                s1_score += 1
            else: s1_feedback.append("(3)번: 정확한 심리 현상('사회적 억제')이 아닙니다.")
            
            st.metric("서·논술형 1 점수", f"{s1_score} / 3 점")
            for fb in s1_feedback: st.warning(fb)
            
            # 서논술 2 채점
            s2_score = 0
            s2_feedback = []
            detected_methods = detect_explanation_method(q2_ans)
            
            # 오개념 확인 (촉진과 억제의 대상을 뒤바꿨는지 체크)
            if "촉진" in q2_ans and any(w in q2_ans for w in ["어려운", "복잡한"]):
                st.error("❌ 오개념 감지: '어려운 과제'에 '사회적 촉진'을 연결하여 오답 처리됩니다.")
            else:
                if len(detected_methods) >= 2:
                    s2_score += 1  # 서로 다른 2가지 설명 방법 만족
                    if any(w in q2_ans for w in ["혼자", "함께", "모임", "도서관", "커피숍"]):
                        s2_score += 1 # 본문 내용 활용 수용
                else:
                    s2_feedback.append("설명 방법의 특성(표지 단어)이 2가지 이상 명확히 드러나지 않았습니다.")
            
            st.metric("서·논술형 2 점수", f"{s2_score} / 2 점")
            if s2_feedback: st.info(s2_feedback[0])
            
            # 서논술 3 채점
            s3_score = 0
            if check_keywords(q3_a, ["혼자", "독서실", "방", "집중", "차분"]) and any(w in q3_a for w in ["효과", "전달", "시각"]): s3_score += 1
            if check_keywords(q3_b, ["조용한", "고요", "적막", "소리없는"]) and any(w in q3_b for w in ["효과", "전달", "청각", "체감"]): s3_score += 1
            
            st.metric("서·논술형 3 점수", f"{s3_score} / 2 점")

# -------------------------------------------------------------------------
# 2번 세트 채점 로직
# -------------------------------------------------------------------------
elif set_option == "2번 세트 (정전기의 특징)":
    st.subheader("🎬 2번 세트: 정전기의 특징 설명하기")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### ✍️ 학생 답안 입력")
        st.markdown("**[서·논술형 1] 표 빈칸 채우기**")
        q1_1 = st.text_input("(1) 물의 상태에 비유", placeholder="예: 높은 곳에 고여 있는 물")
        q1_2 = st.text_input("(2) 전하의 상태", placeholder="예: 전하가 이동하지 않고 머물러 있음")
        q1_3 = st.text_input("(3) 위험성", placeholder="예: 위험하지 않음 (또는 감전 위험 없음)")
        
        st.markdown("**[서·논술형 2] 설명문 이어 쓰기**")
        q2_ans = st.text_area("조건에 맞게 작성한 문장 전체", placeholder="예: 정전기란 전하가 정지해 있는 전기다(정의). 우리가 쓰는 전기가 흐르는 물이면 정전기는 고인 물이다(비교).")
        
        st.markdown("**[서·논술형 3] 영상 연출 계획**")
        q3_a = st.text_input("시각 요소(Ⓐ) 및 효과")
        q3_b = st.text_input("청각 요소(Ⓑ) 및 효과")

    with col2:
        st.markdown("### 📊 채점 결과 및 피드백")
        if st.button("💯 2번 세트 채점하기"):
            s1_score = 0
            if "고여" in q1_1 or "고인" in q1_1: s1_score += 1
            if check_keywords(q1_2, ["이동하지", "머무", "정지", "움직이지"]): s1_score += 1
            if check_keywords(q1_3, ["위험하지", "피해없", "안전", "위험없"]): s1_score += 1 
            
            st.metric("서·논술형 1 점수", f"{s1_score} / 3 점")
            
            s2_score = 0
            if "흐르는물" in q2_ans.replace(" ", "") and "정전기" in q2_ans and not ("실생활" in q2_ans or "일반" in q2_ans):
                st.error("❌ 오개념 감지: 정전기를 '흐르는 물'로 잘못 비유하였거나 설명이 꼬였습니다.")
            else:
                detected = detect_explanation_method(q2_ans)
                if len(detected) >= 2: s2_score += 1
                if check_keywords(q2_ans, ["고여", "머물", "정지", "높은"]): s2_score += 1
                
            st.metric("서·논술형 2 점수", f"{s2_score} / 2 점")
            
            s3_score = 0
            if check_keywords(q3_a, ["고인", "멈춘", "웅덩이", "가만히"]) and "효과" in q3_a: s3_score += 1
            if check_keywords(q3_b, ["고요", "조용", "적막", "침묵"]) and "효그" in q3_b or "효과" in q3_b: s3_score += 1
            st.metric("서·논술형 3 점수", f"{s3_score} / 2 점")

# -------------------------------------------------------------------------
# 3번 세트 채점 로직
# -------------------------------------------------------------------------
else:
    st.subheader("🎬 3번 세트: 삶을 대하는 올바른 태도")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### ✍️ 학생 답안 입력")
        st.markdown("**[서·논술형 1] 표 빈칸 채우기**")
        q1_1 = st.text_input("(1) 세상을 살아가는 일 - 개인적 차이", placeholder="예: 사람마다 같은 경험을 해도 다른 감정으로 받아들임")
        q1_2 = st.text_input("(2) 세상을 살아가는 일 - 필요한 태도", placeholder="예: 모든 사람과 풍경을 천천히 음미해야 함")
        q1_3 = st.text_input("(3) 음식을 맛보는 일 - 태도가 없을 때 결과", placeholder="예: 마구 삼켜서는 맛을 제대로 느낄 수 없음")
        
        st.markdown("**[서·논술형 2] 설명문 이어 쓰기**")
        q2_ans = st.text_area("조건에 맞게 작성한 문장 전체", placeholder="예: 올바른 태도의 예로는 풍경을 천천히 음미하는 것이 있다(예시). 빠르게 달리기만 하는 삶과 달리 다채로움을 준다(대조).")
        
        st.markdown("**[서·논술형 3] 영상 연출 계획**")
        q3_a = st.text_input("시각 요소(Ⓐ) 및 효과")
        q3_b = st.text_input("청각 요소(Ⓑ) 및 효과")

    with col2:
        st.markdown("### 📊 채점 결과 및 피드백")
        if st.button("💯 3번 세트 채점하기"):
            s1_score = 0
            if check_keywords(q1_1, ["다른감정", "다르게", "차이"]): s1_score += 1
            if check_keywords(q1_2, ["천천히", "음미"]): s1_score += 1
            if check_keywords(q1_3, ["제대로", "삼켜", "느낄수없"]): s1_score += 1
            
            st.metric("서·논술형 1 점수", f"{s1_score} / 3 점")
            
            s2_score = 0
            if "빠르게달려야" in q2_ans.replace(" ", "") or "속도" in q2_ans and "천천히" not in q2_ans:
                st.error("❌ 결론 방향 오류: 지문은 '천천히 음미하는 삶'을 지향합니다. 결론이 반대로 작성되었습니다.")
            else:
                detected = detect_explanation_method(q2_ans)
                if len(detected) >= 2: s2_score += 1
                if check_keywords(q2_ans, ["음미", "천천히", "아름다운", "다채로운"]): s2_score += 1
                
            st.metric("서·논술형 2 점수", f"{s2_score} / 2 점")
            
            s3_score = 0
            if check_keywords(q3_a, ["느린", "슬로우", "여유", "공원"]) and "효과" in q3_a: s3_score += 1
            if check_keywords(q3_b, ["잔잔", "평온", "새소리", "클래식"]) and "효과" in q3_b: s3_score += 1
            st.metric("서·논술형 3 점수", f"{s3_score} / 2 점")
