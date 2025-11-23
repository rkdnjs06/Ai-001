import streamlit as st

st.set_page_config(page_title="🍡 일본 전통 디저트 레시피", page_icon="🍵", layout="centered")

st.title("🍡 일본 전통 디저트 레시피 추천기")
st.write("안녕하세요! 일본의 전통 디저트 중 하나를 선택하면 레시피를 보여드려요. 🥢")

# 일본 전통 디저트 리스트 (50개)
desserts = [
    "모치 (Mochi)", "다이후쿠 (Daifuku)", "만주 (Manju)", "양갱 (Yokan)", "센베이 (Senbei)",
    "와라비모치 (Warabi Mochi)", "안미츠 (Anmitsu)", "카스테라 (Castella)", "도라야키 (Dorayaki)", "카키고리 (Kakigori)",
    "미타라시당고 (Mitarashi Dango)", "킨코모치 (Kinako Mochi)", "카나코모치 (Kanako Mochi)", "하가시 (Higashi)", "도미코모치 (Domiko Mochi)",
    "고마모치 (Goma Mochi)", "아마나 (Amanatto)", "쿠루미모치 (Kurumi Mochi)", "우지라테모치 (Uji Latte Mochi)", "타마고야키 (Tamago Yaki)",
    "츠쿠네모치 (Tsukune Mochi)", "호타루이카모치 (Hotaruika Mochi)", "아즈키모찌 (Azuki Mochi)", "호지차 푸딩 (Hojicha Pudding)", "쇼콜라모치 (Chocolat Mochi)",
    "마차 아이스크림 (Matcha Ice Cream)", "우메보시 모치 (Umeboshi Mochi)", "사쿠라 모치 (Sakura Mochi)", "쿠루미 안 (Kurumi An)", "아마자케 푸딩 (Amazake Pudding)",
    "유바모치 (Yuba Mochi)", "호쿠호쿠모치 (Hokuhoku Mochi)", "히야시칸모치 (Hiyashikan Mochi)", "스노우볼 (Snowball Mochi)", "센자키모치 (Senzaki Mochi)",
    "아즈키 젤리 (Azuki Jelly)", "하나모치 (Hana Mochi)", "코히모치 (Kohi Mochi)", "시로타에모치 (Shirotae Mochi)", "호지차 모나카 (Hojicha Monaka)",
    "카라멜 모치 (Caramel Mochi)", "쿠키 모치 (Cookie Mochi)", "우지 모치 (Uji Mochi)", "미소모치 (Miso Mochi)", "아마모치 (Ama Mochi)",
    "호쿠토모치 (Hokuto Mochi)", "카스텔라 롤 (Castella Roll)", "사쿠라 젤리 (Sakura Jelly)", "모치 아이스크림 (Mochi Ice Cream)", "아즈키 아이스크림 (Azuki Ice Cream)"
]

# 디저트별 레시피 딕셔너리
recipes = {
    "모치 (Mochi)": "재료: 찹쌀 200g, 설탕 50g, 물 180ml\n\n1. 찹쌀을 4시간 정도 물에 불린다.\n2. 찹쌀을 찜통에 쪄서 익힌다.\n3. 뜨거울 때 절구에 넣고 절구질로 으깨서 반죽을 만든다.\n4. 반죽을 적당한 크기로 나누고 모양을 만든다.\n5. 필요 시 설탕이나 콩가루를 묻혀 완성한다.",
    "다이후쿠 (Daifuku)": "재료: 모치 100g, 단팥앙금 50g\n\n1. 모치를 전자레인지에 1분간 돌려 말랑하게 한다.\n2. 반죽을 4등분하고, 각 부분에 팥앙금을 넣어 감싼다.\n3. 손에 물을 살짝 묻혀 모양을 잡는다.\n4. 완성된 다이후쿠는 식혀서 먹는다.",
    "만주 (Manju)": "재료: 밀가루 100g, 설탕 30g, 베이킹파우더 1작은술, 단팥앙금 50g\n\n1. 밀가루, 설탕, 베이킹파우더를 섞어 반죽을 만든다.\n2. 반죽을 소량 떼어 앙금을 넣고 둥글게 만든다.\n3. 찜통에 10분 정도 쪄서 완성한다.",
    "양갱 (Yokan)": "재료: 팥앙금 200g, 설탕 50g, 한천 2g, 물 50ml\n\n1. 한천을 물에 녹인다.\n2. 냄비에 팥앙금과 설탕을 넣고 중불에서 저어준다.\n3. 한천물을 넣고 잘 섞는다.\n4. 틀에 부어 굳힌 후 썰어서 완성한다.",
    "센베이 (Senbei)": "재료: 쌀가루 100g, 간장 1큰술, 설탕 1작은술, 물 50ml\n\n1. 모든 재료를 섞어 반죽을 만든다.\n2. 반죽을 얇게 펴서 팬에 구워준다.\n3. 앞뒤로 노릇하게 구워 완성한다.",
    "와라비모치 (Warabi Mochi)": "재료: 와라비가루 50g, 설탕 30g, 물 250ml, 콩가루 적당량\n\n1. 와라비가루, 설탕, 물을 냄비에 넣고 잘 섞는다.\n2. 약불에서 계속 저으면서 끓인다.\n3. 반투명해지면 불을 끄고 식힌다.\n4. 콩가루를 묻혀 완성한다.",
    "안미츠 (Anmitsu)": "재료: 젤리 100g, 팥앙금 50g, 과일 적당량, 시럽 2큰술\n\n1. 젤리를 깍둑썰기 한다.\n2. 과일과 팥앙금을 적당히 담는다.\n3. 시럽을 뿌려서 완성한다.",
    "카스테라 (Castella)": "재료: 계란 4개, 설탕 100g, 밀가루 100g, 꿀 2큰술\n\n1. 계란과 설탕을 거품기로 충분히 섞는다.\n2. 밀가루를 체에 내려 섞는다.\n3. 꿀을 넣고 섞은 후 틀에 부어 160도 오븐에서 40분 굽는다.",
    "도라야키 (Dorayaki)": "재료: 밀가루 100g, 계란 2개, 설탕 50g, 꿀 1큰술, 단팥앙금 100g\n\n1. 계란과 설탕, 꿀을 섞고 밀가루를 체쳐 넣는다.\n2. 팬에 동그랗게 부어 양면 노릇하게 굽는다.\n3. 팬케이크 사이에 단팥앙금을 넣어 완성한다.",
    "카키고리 (Kakigori)": "재료: 얼음 1컵, 시럽 적당량, 연유 1큰술\n\n1. 얼음을 곱게 갈아 컵에 담는다.\n2. 시럽과 연유를 뿌려 완성한다.",
    # 나머지 40개도 같은 형식으로 작성
}

# 나머지 디저트 레시피를 간단 예시로 모두 추가
for dessert in desserts:
    if dessert not in recipes:
        recipes[dessert] = f"🍴 {dessert} 레시피 준비 중이에요! 자세한 레시피는 곧 업데이트 됩니다."

# 디저트 선택
selected_dessert = st.selectbox("🍪 디저트를 선택하세요", desserts)

# 선택한 디저트 레시피 표시
st.subheader(f"🍰 {selected_dessert} 레시피")
st.text(recipes[selected_dessert])
