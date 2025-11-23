import streamlit as st

st.set_page_config(page_title="🍡 일본 전통 디저트 레시피", page_icon="🍵", layout="centered")

st.title("🍡 일본 전통 디저트 레시피 & 설명")
st.write("일본의 전통 디저트를 선택하면 간단한 설명과 레시피를 보여드려요. 🥢")

# 디저트 리스트
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

# 50개 디저트 상세 설명 + 레시피
dessert_info = {
    "모치 (Mochi)": {"description": "찹쌀로 만든 일본 전통 떡. 쫄깃한 식감이 특징이며 다양한 간식이나 디저트로 활용 가능.", "recipe": "찹쌀 200g, 설탕 50g, 물 180ml\n1. 찹쌀 4시간 불리기\n2. 찜통에 찌기\n3. 절구에 넣고 반죽\n4. 적당한 크기로 나누기\n5. 설탕/콩가루 묻히기"},
    "다이후쿠 (Daifuku)": {"description": "모치 속에 달콤한 팥앙금을 넣은 일본 인기 디저트. 한 입 크기로 귀엽고 달콤.", "recipe": "모치 100g, 단팥앙금 50g\n1. 모치 전자레인지 1분 돌리기\n2. 4등분 후 앙금 넣기\n3. 손에 물 묻혀 모양 잡기\n4. 식혀서 완성"},
    "만주 (Manju)": {"description": "밀가루 반죽 안에 달콤한 팥앙금을 넣어 찐 전통 과자.", "recipe": "밀가루 100g, 설탕 30g, 베이킹파우더 1작은술, 팥앙금 50g\n1. 재료 섞기\n2. 앙금 넣고 둥글게\n3. 찜통 10분 찌기"},
    "양갱 (Yokan)": {"description": "팥과 한천으로 만든 단단한 일본 전통 젤리 과자.", "recipe": "팥앙금 200g, 설탕 50g, 한천 2g, 물 50ml\n1. 한천 녹이기\n2. 팥앙금+설탕 섞기\n3. 한천 넣고 섞기\n4. 틀에 부어 굳히기"},
    "센베이 (Senbei)": {"description": "쌀로 만든 바삭한 일본 전통 과자, 간장 또는 소금으로 맛을 냄.", "recipe": "쌀가루 100g, 간장 1큰술, 설탕 1작은술, 물 50ml\n1. 재료 섞기\n2. 얇게 펴서 팬에 굽기\n3. 앞뒤 노릇하게 굽기"},
    "와라비모치 (Warabi Mochi)": {"description": "고사리 전분으로 만든 쫄깃한 여름 디저트, 콩가루와 시럽 곁들임.", "recipe": "와라비가루 50g, 설탕 30g, 물 250ml, 콩가루\n1. 재료 섞어 약불에서 저으며 끓이기\n2. 반투명해지면 식히기\n3. 콩가루 묻히기"},
    "안미츠 (Anmitsu)": {"description": "젤리, 과일, 팥앙금, 시럽을 함께 담아 먹는 디저트.", "recipe": "젤리 100g, 팥앙금 50g, 과일, 시럽 2큰술\n1. 젤리 깍둑썰기\n2. 과일과 팥앙금 담기\n3. 시럽 뿌리기"},
    "카스테라 (Castella)": {"description": "포르투갈에서 전래된 일본식 스폰지 케이크, 부드럽고 달콤.", "recipe": "계란 4개, 설탕 100g, 밀가루 100g, 꿀 2큰술\n1. 계란+설탕 섞기\n2. 밀가루 체쳐 넣기\n3. 꿀 섞고 160도 오븐 40분"},
    "도라야키 (Dorayaki)": {"description": "두 장의 팬케이크 사이에 달콤한 팥앙금을 넣은 간식.", "recipe": "밀가루 100g, 계란 2개, 설탕 50g, 꿀 1큰술, 팥앙금 100g\n1. 계란+설탕+꿀 섞기\n2. 밀가루 체쳐 섞기\n3. 팬케이크 굽기\n4. 팥앙금 사이에 넣기"},
    "카키고리 (Kakigori)": {"description": "곱게 간 얼음 위에 시럽과 연유 뿌려 먹는 여름 디저트.", "recipe": "얼음 1컵, 시럽, 연유 1큰술\n1. 얼음 곱게 갈기\n2. 컵에 담고 시럽, 연유 뿌리기"},
    "미타라시당고 (Mitarashi Dango)": {"description": "꼬치에 꽂은 떡을 달콤 짭짤한 간장 소스로 구운 간식.", "recipe": "떡 10개, 간장 2큰술, 설탕 1큰술, 물 1큰술\n1. 떡 삶기\n2. 꼬치에 꽂기\n3. 소스 바르고 구워 완성"},
    "킨코모치 (Kinako Mochi)": {"description": "모치 위에 고소한 콩가루(킨코)를 뿌려 먹는 간단 디저트.", "recipe": "모치 100g, 콩가루 2큰술, 설탕 1큰술\n1. 모치 구워서 따뜻하게 유지\n2. 콩가루+설탕 섞어 묻히기"},
    "카나코모치 (Kanako Mochi)": {"description": "볶은 콩가루를 입힌 모치 디저트.", "recipe": "모치 100g, 볶은 콩가루 2큰술\n1. 모치 구워서 준비\n2. 콩가루 입히기"},
    "하가시 (Higashi)": {"description": "단단한 모양과 달콤함이 특징인 일본 전통 과자, 차와 함께 즐김.", "recipe": "밀가루 50g, 설탕 20g, 물 10ml\n1. 재료 섞어 틀에 넣기\n2. 건조 후 완성"},
    "도미코모치 (Domiko Mochi)": {"description": "팥과 함께 만드는 작은 크기의 모치.", "recipe": "모치 100g, 팥앙금 50g\n1. 모치 반죽 준비\n2. 팥앙금 넣고 둥글게 만들기"},
    "고마모치 (Goma Mochi)": {"description": "검은 참깨를 넣어 고소한 맛을 낸 모치.", "recipe": "모치 100g, 검은 참깨 2큰술\n1. 모치 반죽 준비\n2. 참깨 섞기 후 모양 만들기"},
    "아마나 (Amanatto)": {"description": "달콤하게 조린 콩으로 만든 전통 간식.", "recipe": "콩 100g, 설탕 50g, 물 50ml\n1. 콩 삶기\n2. 설탕과 물에 졸이기"},
    "쿠루미모치 (Kurumi Mochi)": {"description": "호두를 넣어 만든 모치로 고소하고 달콤함.", "recipe": "모치 100g, 호두 30g\n1. 모치 반죽 준비\n2. 호두 섞어 모양 만들기"},
    "우지라테모치 (Uji Latte Mochi)": {"description": "말차(우지말차) 맛이 나는 모치 디저트.", "recipe": "모치 100g, 말차 가루 2g, 설탕 1큰술\n1. 모치 준비\n2. 말차+설탕 섞어 반죽에 넣기"},
    "타마고야키 (Tamago Yaki)": {"description": "달걀을 겹겹이 부쳐 만든 달콤한 일본식 계란말이.", "recipe": "계란 3개, 설탕 1큰술, 소금 약간\n1. 계란+설탕+소금 섞기\n2. 팬에 얇게 부쳐 말기"},
    "츠쿠네모치 (Tsukune Mochi)": {"description": "닭고기 반죽을 떡과 함께 꼬치에 구운 일본 간식.", "recipe": "닭고기 100g, 모치 50g, 소금/간장\n1. 닭고기 반죽 준비\n2. 모치와 함께 꼬치에 끼우고 구움"},
    "호타루이카모치 (Hotaruika Mochi)": {"description": "작은 오징어와 떡을 활용한 지역 특산 디저트.", "recipe": "떡 50g, 오징어 30g, 간장 1큰술\n1. 떡 삶기\n2. 오징어 볶아 떡과 섞기"},
    "아즈키모찌 (Azuki Mochi)": {"description": "팥앙금을 넣은 모치, 가장 기본적인 전통 떡 중 하나.", "recipe": "모치 100g, 팥앙금 50g\n1. 모치 준비\n2. 팥앙금 넣어 감싸기"},
    "호지차 푸딩 (Hojicha Pudding)": {"description": "볶은 녹차(호지차)를 넣은 부드러운 푸딩.", "recipe": "우유 200ml, 설탕 30g, 호지차 2g, 젤라틴 2g\n1. 호지차 우려내기\n2. 우유+설탕+호지차 섞기\n3. 젤라틴 넣어 굳히기"},
    "쇼콜라모치 (Chocolat Mochi)": {"description": "초콜릿을 넣어 만든 달콤한 모치.", "recipe": "모치 100g, 초콜릿 30g\n1. 모치 준비\n2. 초콜릿 넣고 반죽 후 모양 만들기"},
    "마차 아이스크림 (Matcha Ice Cream)": {"description": "말차 맛 아이스크림, 쌉쌀하면서 달콤함.", "recipe": "우유 200ml, 생크림 100ml, 설탕 50g, 말차 2g\n1. 재료 섞기\n2. 아이스크림 제조기 또는 냉동"},
    "우메보시 모치 (Umeboshi Mochi)": {"description": "매콤한 매실 절임을 넣은 모치로 상큼한 맛.", "recipe": "모치 100g, 우메보시 1개\n1. 모치 준비\n2. 우메보시 넣고 감싸기"},
    "사쿠라 모치 (Sakura Mochi)": {"description": "벚꽃잎으로 감싼 분홍색 모치, 봄에 즐기는 디저트.", "recipe": "모치 100g, 팥앙금 50g, 벚꽃잎 2장\n1. 모치 준비\n2. 팥앙금 넣고 벚꽃잎으로 감싸기"},
    "쿠루미 안 (Kurumi An)": {"description": "호두 앙금을 넣은 모치로 고소하고 달콤.", "recipe": "모치 100g, 호두앙금 50g\n1. 모치 준비\n2. 호두앙금 넣어 감싸기"},
    "아마자케 푸딩 (Amazake Pudding)": {"description": "달콤한 아마자케로 만든 부드러운 푸딩.", "recipe": "아마자케 150ml, 생크림 50ml, 젤라틴 2g\n1. 재료 섞기\n2. 틀에 붓고 냉장 굳히기"},
    "유바모치 (Yuba Mochi)": {"description": "두유로 만든 얇은 층을 활용한 모치 디저트.", "recipe": "유바 50g, 모치 100g\n1. 모치 준비\n2. 유바 겹쳐서 감싸기"},
    "호쿠호쿠모치 (Hokuhoku Mochi)": {"description": "갓 쪄낸 모치를 따뜻하게 즐기는 일본식 떡.", "recipe": "모치 100g\n1. 모치 찌기\n2. 따뜻하게 제공"},
    "히야시칸모치 (Hiyashikan Mochi)": {"description": "차갑게 즐기는 여름철 모치 디저트.", "recipe": "모치 100g, 얼음물\n1. 모치 찐 후 얼음물에 식히기"},
    "스노우볼 (Snowball Mochi)": {"description": "하얀 가루를 입힌 작은 모치, 눈처럼 예쁨.", "recipe": "모치 100g, 설탕가루 2큰술\n1. 모치 준비\n2. 설탕가루 묻히기"},
    "센자키모치 (Senzaki Mochi)": {"description": "지역 특산 재료를 넣은 모치 디저트.", "recipe": "모치 100g, 특산 재료 30g\n1. 모치 준비\n2. 재료 섞어 모양 만들기"},
    "아즈키 젤리 (Azuki Jelly)": {"description": "팥으로 만든 젤리, 달콤하고 부드럽.", "recipe": "팥앙금 100g, 한천 2g, 물 50ml\n1. 재료 섞고 끓이기\n2. 틀에 부어 굳히기"},
    "하나모치 (Hana Mochi)": {"description": "꽃 모양으로 만든 예쁜 모치.", "recipe": "모치 100g\n1. 모치 반죽 준비\n2. 꽃 모양 만들기"},
    "코히모치 (Kohi Mochi)": {"description": "커피 맛을 첨가한 모치 디저트.", "recipe": "모치 100g, 커피 2g, 설탕 1큰술\n1. 모치 준비\n2. 커피 섞어 반죽"},
    "시로타에모치 (Shirotae Mochi)": {"description": "순백색 모치로 깔끔한 맛이 특징.", "recipe": "모치 100g\n1. 모치 준비"},
    "호지차 모나카 (Hojicha Monaka)": {"description": "호지차 맛을 넣은 모나카, 바삭함과 말차 향 조화.", "recipe": "모나카 2장, 호지차 크림 50g\n1. 크림 모나카 사이 넣기"},
    "카라멜 모치 (Caramel Mochi)": {"description": "카라멜 향과 달콤함이 있는 모치.", "recipe": "모치 100g, 카라멜 30g\n1. 모치 준비\n2. 카라멜 섞어 반죽"},
    "쿠키 모치 (Cookie Mochi)": {"description": "쿠키 조각을 넣은 모치로 식감 재미있음.", "recipe": "모치 100g, 쿠키 조각 20g\n1. 모치 준비\n2. 쿠키 섞기"},
    "우지 모치 (Uji Mochi)": {"description": "우지말차 맛 모치, 쌉쌀한 녹차향 특징.", "recipe": "모치 100g, 말차 2g, 설탕 1큰술\n1. 모치 준비\n2. 말차 섞기"},
    "미소모치 (Miso Mochi)": {"description": "된장 맛을 첨가한 독특한 모치.", "recipe": "모치 100g, 미소 1작은술\n1. 모치 준비\n2. 미소 섞기"},
    "아마모치 (Ama Mochi)": {"description": "달콤하게 맛낸 모치.", "recipe": "모치 100g, 설탕 1큰술\n1. 모치 준비\n2. 설탕 섞기"},
    "호쿠토모치 (Hokuto Mochi)": {"description": "지역 특산 재료를 넣은 모치.", "recipe": "모치 100g, 재료 30g\n1. 모치 준비\n2. 재료 섞기"},
    "카스텔라 롤 (Castella Roll)": {"description": "카스텔라를 말아 만든 롤 케이크.", "recipe": "카스텔라 100g, 생크림 50ml\n1. 카스텔라 굽기\n2. 생크림 바르고 말기"},
    "사쿠라 젤리 (Sakura Jelly)": {"description": "벚꽃 향 젤리로 봄철 인기 디저트.", "recipe": "한천 2g, 물 50ml, 벚꽃잎 2장\n1. 한천 녹이기\n2. 물+벚꽃 섞어 틀에 붓기"},
    "모치 아이스크림 (Mochi Ice Cream)": {"description": "모치 속에 아이스크림을 넣어 먹는 디저트.", "recipe": "모치 50g, 아이스크림 50g\n1. 모치 준비\n2. 아이스크림 넣고 감싸기"},
    "아즈키 아이스크림 (Azuki Ice Cream)": {"description": "팥앙금을 넣은 아이스크림 모치.", "recipe": "모치 50g, 아이스크림 50g, 팥앙금 20g\n1. 모치 준비\n2. 아이스크림+팥앙금 넣기"}
}

# 디저트 선택
dessert_choice = st.selectbox("🍮 디저트를 선택하세요", desserts)

# 선택한 디저트 설명과 레시피 출력
info = dessert_info.get(dessert_choice, {"description": "설명 없음", "recipe": "레시피 없음"})

st.subheader(f"🍴 {dessert_choice} 설명")
st.write(info["description"])

st.subheader(f"🍴 {dessert_choice} 레시피")
st.code(info["recipe"])
