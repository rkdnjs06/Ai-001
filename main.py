import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
st.write('안녕하세요, 만나서 반갑습니다!')
name=st.text_input('이름을 입력해주세요!')
if st.button('인사말 생성'):
  st.write(name+'님! 반갑습니다')
  st.balloons()
  import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 🎯", page_icon="🎓")

# 제목
st.title("🎓 MBTI 기반 진로 추천 프로그램")
st.write("당신의 성격 유형(MBTI)을 선택하면 어울리는 진로를 추천해드릴게요! 💡")

# MBTI 목록
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 사용자 선택
user_type = st.selectbox("당신의 MBTI를 선택하세요 😊", mbti_list)

# 진로 데이터 (예시)
career_data = {
    "ISTJ": {
        "careers": ["공무원", "회계사"],
        "majors": ["행정학, 회계학"],
        "traits": "책임감이 강하고 꼼꼼한 성격이에요. 체계적인 일을 좋아하죠. 📋"
    },
    "ISFJ": {
        "careers": ["간호사", "사회복지사"],
        "majors": ["간호학, 사회복지학"],
        "traits": "타인을 배려하고 따뜻한 마음을 가진 사람에게 잘 어울려요. 💖"
    },
    "INFJ": {
        "careers": ["상담사", "작가"],
        "majors": ["심리학, 문예창작"],
        "traits": "깊은 생각과 통찰력이 있어 사람의 마음을 이해하는 데 능숙해요. ✨"
    },
    "INTJ": {
        "careers": ["연구원", "데이터 분석가"],
        "majors": ["컴퓨터공학, 통계학"],
        "traits": "논리적이고 목표 지향적인 타입이에요. 계획 세우는 걸 좋아하죠. 🧠"
    },
    "ISTP": {
        "careers": ["기계공학자", "파일럿"],
        "majors": ["기계공학, 항공학"],
        "traits": "실용적이고 문제 해결 능력이 뛰어나요. 손으로 뭔가 만드는 걸 즐겨요. 🛠️"
    },
    "ISFP": {
        "careers": ["디자이너", "제과제빵사"],
        "majors": ["시각디자인, 제과제빵학"],
        "traits": "감성이 풍부하고 미적 감각이 뛰어나요. 따뜻하고 부드러운 스타일! 🎨🍰"
    },
    "INFP": {
        "careers": ["작가", "예술가"],
        "majors": ["문예창작, 미술"],
        "traits": "상상력이 풍부하고 감수성이 예민해요. 자기만의 세계를 소중히 여겨요. 🌈"
    },
    "INTP": {
        "careers": ["개발자", "연구원"],
        "majors": ["컴퓨터공학, 물리학"],
        "traits": "논리적이고 분석적인 사람으로, 새로운 아이디어를 탐구하길 좋아해요. ⚙️"
    },
    "ESTP": {
        "careers": ["영업사원", "스포츠 코치"],
        "majors": ["경영학, 체육학"],
        "traits": "에너지 넘치고 도전적인 성격! 현실 감각이 뛰어나요. ⚡"
    },
    "ESFP": {
        "careers": ["배우", "이벤트 플래너"],
        "majors": ["연극영화, 호텔경영"],
        "traits": "사교적이고 긍정적인 분위기 메이커예요! 사람들과 어울리는 걸 좋아해요. 🎤🎉"
    },
    "ENFP": {
        "careers": ["크리에이터", "홍보 마케터"],
        "majors": ["미디어커뮤니케이션, 광고홍보"],
        "traits": "열정 넘치고 창의력이 폭발해요! 새로운 아이디어를 떠올리는 걸 좋아해요. 💡🔥"
    },
    "ENTP": {
        "careers": ["창업가", "기획자"],
        "majors": ["경영학, 경제학"],
        "traits": "토론을 좋아하고 유머 감각이 뛰어나요. 변화와 혁신을 즐기죠! 🚀"
    },
    "ESTJ": {
        "careers": ["경영자", "군인"],
        "majors": ["경영학, 국방학"],
        "traits": "리더십이 강하고 현실적인 판단력이 뛰어나요. 조직을 잘 이끌어요. 🏆"
    },
    "ESFJ": {
        "careers": ["교사", "간호사"],
        "majors": ["교육학, 간호학"],
        "traits": "친절하고 책임감이 강한 타입! 다른 사람을 돕는 일에서 빛나요. 🌷"
    },
    "ENFJ": {
        "careers": ["상담가", "홍보전문가"],
        "majors": ["심리학, 커뮤니케이션학"],
        "traits": "사람들의 성장을 도와주는 리더형이에요. 따뜻하면서 추진력도 있어요. 🌟"
    },
    "ENTJ": {
        "careers": ["CEO", "전략 컨설턴트"],
        "majors": ["경영학, 정치외교학"],
        "traits": "야망 있고 리더십이 뛰어나요. 목표를 향해 끊임없이 도전해요. 🦁"
    },
}

# 선택 결과 출력
if user_type:
    info = career_data[user_type]
    st.subheader(f"✨ {user_type} 유형에 어울리는 진로 추천 ✨")
    st.write(f"**추천 진로:** {', '.join(info['careers'])}")
    st.write(f"**추천 학과:** {info['majors']}")
    st.write(f"**성격 특징:** {info['traits']}")
    st.success("당신의 강점을 살릴 수 있는 멋진 길을 찾아보세요! 🌈")

# 푸터
st.markdown("---")
st.caption("Made with ❤️ by 황가원의 AI 도우미")
