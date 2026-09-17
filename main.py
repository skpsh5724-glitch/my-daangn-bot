import time
import random
import re
import urllib.parse
import requests

# 텔레그램 연동 정보
BOT_TOKEN = "8729132658:AAFewkLMLqGtSj6n4XK8Xs7Aj17YcRGeDBM"
CHAT_ID   = "578227533"

# 브랜드별 별칭 사전
BRAND_ALIASES = {
    "루이비통": ["루이비통", "루이비똥", "루이뷔통", "루이비톤", "루이뷔톤", "lv", "louisvuitton"],
    "디올":     ["디올", "크리스찬디올", "크리스챤디올", "dior"],
    "고야드":   ["고야드", "고야뜨", "goyard"]
}

# 감시 대상 80종
WATCH_LIST = [
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "트리오 메신저", "BasePrice": 1950000, "MinPrice": 750000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "디스트릭트 PM", "BasePrice": 1250000, "MinPrice": 450000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "디스트릭트 MM", "BasePrice": 1400000, "MinPrice": 500000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "애비뉴 슬링백", "BasePrice": 1400000, "MinPrice": 500000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "크리스토퍼 백팩", "BasePrice": 2800000, "MinPrice": 1100000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "조쉬 백팩", "BasePrice": 1600000, "MinPrice": 600000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "딘 백팩", "BasePrice": 1900000, "MinPrice": 750000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "마이클 백팩", "BasePrice": 1700000, "MinPrice": 650000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "키폴 45", "BasePrice": 1300000, "MinPrice": 450000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "키폴 50", "BasePrice": 1400000, "MinPrice": 500000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "키폴 55", "BasePrice": 1450000, "MinPrice": 500000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "키폴 반둘리에 25", "BasePrice": 2100000, "MinPrice": 850000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "포쉐트 보야주 MM", "BasePrice": 750000, "MinPrice": 280000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "카스베크", "BasePrice": 850000, "MinPrice": 300000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "포쉐트 볼가", "BasePrice": 1300000, "MinPrice": 500000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "댄디 브리프케이스", "BasePrice": 1500000, "MinPrice": 550000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "포르트 도퀴망", "BasePrice": 1100000, "MinPrice": 400000},
    {"Brand": "루이비통", "Category": "가방", "SearchKw": "데이턴 메신저", "BasePrice": 1050000, "MinPrice": 380000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "포켓 오거나이저", "BasePrice": 420000, "MinPrice": 160000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "멀티플 월릿", "BasePrice": 470000, "MinPrice": 180000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "슬렌더 월릿", "BasePrice": 450000, "MinPrice": 170000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "브라짜 월릿", "BasePrice": 550000, "MinPrice": 200000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "지피 오거나이저", "BasePrice": 650000, "MinPrice": 250000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "지피 월릿 베르티칼", "BasePrice": 580000, "MinPrice": 220000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "네오 카드홀더", "BasePrice": 380000, "MinPrice": 140000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "엔벨로프 카르트", "BasePrice": 320000, "MinPrice": 120000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "마르코 월릿", "BasePrice": 430000, "MinPrice": 150000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "코인 카드 홀더", "BasePrice": 410000, "MinPrice": 150000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "루이비통 롱 월릿", "BasePrice": 480000, "MinPrice": 180000},
    {"Brand": "루이비통", "Category": "지갑", "SearchKw": "키폴 키홀더", "BasePrice": 280000, "MinPrice": 90000},

    {"Brand": "디올", "Category": "가방", "SearchKw": "새들백 옴므", "BasePrice": 2500000, "MinPrice": 950000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "미니 새들백", "BasePrice": 2100000, "MinPrice": 800000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "새들 메신저백", "BasePrice": 1800000, "MinPrice": 700000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "오블리크 롤러백", "BasePrice": 1200000, "MinPrice": 450000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "라이더 백팩", "BasePrice": 1650000, "MinPrice": 600000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "미니 라이더 백팩", "BasePrice": 1400000, "MinPrice": 500000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "갤럽 백팩", "BasePrice": 2200000, "MinPrice": 850000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "갤럽 메신저백", "BasePrice": 1700000, "MinPrice": 650000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "히트 더 로드 백팩", "BasePrice": 2100000, "MinPrice": 800000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "히트 더 로드 메신저", "BasePrice": 1500000, "MinPrice": 550000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "사파리 메신저백", "BasePrice": 1450000, "MinPrice": 550000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "오블리크 버티컬 파우치", "BasePrice": 950000, "MinPrice": 350000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "링 메신저백", "BasePrice": 1300000, "MinPrice": 480000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "오블리크 클러치", "BasePrice": 700000, "MinPrice": 250000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "오블리크 더플백", "BasePrice": 1900000, "MinPrice": 700000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "디올 그래비티 메신저", "BasePrice": 1850000, "MinPrice": 700000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "락 나노 파우치", "BasePrice": 900000, "MinPrice": 320000},
    {"Brand": "디올", "Category": "가방", "SearchKw": "오블리크 토트백", "BasePrice": 1550000, "MinPrice": 550000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "오블리크 카드지갑", "BasePrice": 380000, "MinPrice": 140000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "오블리크 반지갑", "BasePrice": 450000, "MinPrice": 170000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "갤럽 카드홀더", "BasePrice": 350000, "MinPrice": 130000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "디올 지퍼 카드홀더", "BasePrice": 400000, "MinPrice": 150000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "CD 다이아몬드 반지갑", "BasePrice": 460000, "MinPrice": 170000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "CD 다이아몬드 카드홀더", "BasePrice": 370000, "MinPrice": 140000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "새들 플랩 카드홀더", "BasePrice": 410000, "MinPrice": 150000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "디올 3단 지갑 옴므", "BasePrice": 480000, "MinPrice": 180000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "디올 양면 카드지갑", "BasePrice": 360000, "MinPrice": 130000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "오블리크 장지갑", "BasePrice": 580000, "MinPrice": 200000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "디올 그래비티 카드지갑", "BasePrice": 390000, "MinPrice": 140000},
    {"Brand": "디올", "Category": "지갑", "SearchKw": "롤러 파우치 키링", "BasePrice": 320000, "MinPrice": 110000},

    {"Brand": "고야드", "Category": "가방", "SearchKw": "벨베데르 PM", "BasePrice": 2300000, "MinPrice": 950000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "벨베데르 MM", "BasePrice": 2600000, "MinPrice": 1050000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "카피베르", "BasePrice": 1850000, "MinPrice": 750000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "고야드 보잉 45", "BasePrice": 2500000, "MinPrice": 1000000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "고야드 보잉 55", "BasePrice": 2800000, "MinPrice": 1100000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "세나 클러치 MM", "BasePrice": 850000, "MinPrice": 320000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "세나 클러치 GM", "BasePrice": 1050000, "MinPrice": 400000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "알핀 백팩", "BasePrice": 3300000, "MinPrice": 1350000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "앙주 PM", "BasePrice": 2400000, "MinPrice": 950000},
    {"Brand": "고야드", "Category": "가방", "SearchKw": "그랑블루 메신저", "BasePrice": 1900000, "MinPrice": 750000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "생피에르", "BasePrice": 680000, "MinPrice": 280000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "빅투와르", "BasePrice": 780000, "MinPrice": 300000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "생쉴피스", "BasePrice": 430000, "MinPrice": 170000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "말젤브", "BasePrice": 550000, "MinPrice": 220000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "마티뇽 동전지갑", "BasePrice": 650000, "MinPrice": 250000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "리슐리외 장지갑", "BasePrice": 950000, "MinPrice": 380000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "마티뇽 지퍼장지갑", "BasePrice": 1100000, "MinPrice": 420000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "인서트 카드홀더", "BasePrice": 380000, "MinPrice": 150000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "몬테카를로 파우치", "BasePrice": 1300000, "MinPrice": 500000},
    {"Brand": "고야드", "Category": "지갑", "SearchKw": "고야드 여권케이스", "BasePrice": 580000, "MinPrice": 230000}
]

EXCLUDE_WORDS = ["레플", "미러", "sa급", "자체제작", "st", "스타일", "정품문의", "동대문", "정품아님", "삽니다", "대여", "교환", "오염", "하자", "박스만"]
AUTH_WORDS = ["영수증", "인보이스", "인증서", "보증서", "백화점", "크림", "kream"]
CAPITAL_REGIONS = ["서울", "경기", "인천", "부천", "수원", "성남", "고양", "용인", "안양", "안산", "강남구", "서초구", "송파구", "마포구", "부평구", "남동구"]

seen_ids = set()

def send_alert(target, title, price, region, has_auth, url):
    discount_pct = round((1 - (price / target["BasePrice"])) * 100)
    auth_badge = "🔥 [정품 증빙 키워드 감지]" if has_auth else "⚠️ [진품 직접 확인 필요]"
    
    msg = (
        f"🥕 [당근 급매물 포착: {target['Category']}]\n"
        f"🏷️ 브랜드/품목: {target['Brand']} - {target['SearchKw']}\n"
        f"📦 글제목: {title}\n"
        f"💰 가격: {price:,}원 (시세 대비 -{discount_pct}%)\n"
        f"📍 직거래 동네: {region}\n"
        f"{auth_badge}\n"
        f"🔗 링크: {url}"
    )
    
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(api_url, json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except:
        pass

# 시작 알림
try:
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": "☁️ [클라우드 24시간 감시] 서버가 성공적으로 시작되었습니다!"}, timeout=5)
except:
    pass

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
article_regex = re.compile(r'(?s)<article class="flea-market-article">.*?<a class="flea-market-article-link" href="(?P<Link>/articles/(?P<Id>\d+))".*?<span class="article-title">(?P<Title>.*?)</span>.*?<p class="article-price ">\s*(?P<Price>.*?)\s*</p>.*?<p class="article-region-name">\s*(?P<Region>.*?)\s*</p>')

while True:
    for item in WATCH_LIST:
        encoded_kw = urllib.parse.quote(item["SearchKw"])
        url = f"https://www.daangn.com/search/{encoded_kw}"
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            matches = article_regex.finditer(res.text)
            
            for m in matches:
                item_id = m.group("Id")
                title = m.group("Title").strip()
                raw_price = m.group("Price").strip()
                region = m.group("Region").strip()
                link = "https://www.daangn.com" + m.group("Link")
                
                if item_id in seen_ids:
                    continue
                seen_ids.add(item_id)
                
                clean_title = re.sub(r'\s+', '', title.lower())
                
                # 브랜드 매칭
                if not any(alias in clean_title for alias in BRAND_ALIASES[item["Brand"]]):
                    continue
                
                # 가격 정제
                digits = re.sub(r'[^\d]', '', raw_price)
                if not digits:
                    continue
                price = int(digits)
                
                if price < item["MinPrice"] or price > (item["BasePrice"] * 0.8):
                    continue
                
                # 제외 키워드
                if any(bad in clean_title for bad in EXCLUDE_WORDS):
                    continue
                
                # 수도권 지역 확인
                if not any(reg in region for reg in CAPITAL_REGIONS):
                    continue
                
                has_auth = any(auth in clean_title for auth in AUTH_WORDS)
                send_alert(item, title, price, region, has_auth, link)
                print(f"[알림 발송] {item['Brand']} - {title}")
        except:
            pass
        
        time.sleep(random.uniform(2.0, 3.5))
    
    time.sleep(10)
