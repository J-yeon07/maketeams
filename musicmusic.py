# app.py
import streamlit as st
import pandas as pd
import random
from typing import List, Dict

st.set_page_config(page_title="MBTI별 노래 추천", layout="centered")

# ----------------------
# 데이터: MBTI -> 곡 목록
# (예시 데이터: 필요하면 직접 바꾸세요)
# 각 항목: {"title":..., "artist":..., "desc":..., "youtube":...}
# ----------------------
MBTI_SONGS: Dict[str, List[Dict]] = {
    "INTJ": [
        {"title":"Space Oddity", "artist":"David Bowie", "desc":"미래지향적이고 사색적인 분위기.", "youtube":"https://www.youtube.com/watch?v=Oy2XQ0r8F9o"},
        {"title":"Breezeblocks", "artist":"alt-J", "desc":"복합적 구조의 리듬과 서사가 매력.", "youtube":"https://www.youtube.com/watch?v=rVeMiVU77wo"},
        {"title":"Runaway", "artist":"Kanye West", "desc":"깊은 자기반성과 드라마틱한 전개.", "youtube":"https://www.youtube.com/watch?v=Pbz7IY1Rk4E"},
    ],
    "INTP": [
        {"title":"Hide and Seek", "artist":"Imogen Heap", "desc":"전자음과 감성의 조합, 사유적 분위기.", "youtube":"https://www.youtube.com/watch?v=UYIAfiVGluk"},
        {"title":"Contact", "artist":"Daft Punk", "desc":"아이디어가 폭발하는 전개.", "youtube":"https://www.youtube.com/watch?v=rYEDA3JcQqw"},
        {"title":"Atlas Hands", "artist":"Benjamin Francis Leftwich", "desc":"잔잔하지만 생각을 자극하는 곡.", "youtube":"https://www.youtube.com/watch?v=bVv7HjXio7E"},
    ],
    "ENTJ": [
        {"title":"My Way", "artist":"Frank Sinatra", "desc":"결단력과 리더십이 느껴지는 클래식.", "youtube":"https://www.youtube.com/watch?v=7Q9dZYm2n6g"},
        {"title":"Power", "artist":"Kanye West", "desc":"목표 지향적이고 에너제틱한 트랙.", "youtube":"https://www.youtube.com/watch?v=L53gjP-TtGE"},
        {"title":"Believer", "artist":"Imagine Dragons", "desc":"강한 추진력과 의지 표현.", "youtube":"https://www.youtube.com/watch?v=7wtfhZwyrcc"},
    ],
    "ENTP": [
        {"title":"Bohemian Rhapsody", "artist":"Queen", "desc":"창의적이고 예측불허의 전개.", "youtube":"https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},
        {"title":"Feel Good Inc.", "artist":"Gorillaz", "desc":"아이디어가 튀는 사운드와 멜로디.", "youtube":"https://www.youtube.com/watch?v=HyHNuVaZJ-k"},
        {"title":"Electric Feel", "artist":"MGMT", "desc":"실험적이면서도 중독성 있는 곡.", "youtube":"https://www.youtube.com/watch?v=MmZexg8sxyk"},
    ],
    "INFJ": [
        {"title":"Fix You", "artist":"Coldplay", "desc":"공감능력과 서정성이 돋보이는 곡.", "youtube":"https://www.youtube.com/watch?v=k4V3Mo61fJM"},
        {"title":"Holocene", "artist":"Bon Iver", "desc":"내면 성찰과 잔잔한 울림.", "youtube":"https://www.youtube.com/watch?v=TWcyIpul8OE"},
        {"title":"Skinny Love", "artist":"Bon Iver", "desc":"감정의 섬세한 표현.", "youtube":"https://www.youtube.com/watch?v=ssdgFoHLwnk"},
    ],
    "INFP": [
        {"title":"Northern Wind", "artist":"City and Colour", "desc":"감수성 풍부한 서정성.", "youtube":"https://www.youtube.com/watch?v=kvbq9H9g0Tg"},
        {"title":"Fast Car", "artist":"Tracy Chapman", "desc":"이야기하는 가사와 감정의 깊이.", "youtube":"https://www.youtube.com/watch?v=uTIB10eQnA0"},
        {"title":"The Night We Met", "artist":"Lord Huron", "desc":"향수와 그리움의 정서.", "youtube":"https://www.youtube.com/watch?v=KtlgYxa6BMU"},
    ],
    "ENFJ": [
        {"title":"Count on Me", "artist":"Bruno Mars", "desc":"타인 배려와 격려의 메시지.", "youtube":"https://www.youtube.com/watch?v=yJYXItns2ik"},
        {"title":"Rise Up", "artist":"Andra Day", "desc":"격려와 연대의 힘.", "youtube":"https://www.youtube.com/watch?v=lwgr_IMeEgA"},
        {"title":"Hall of Fame", "artist":"The Script ft. will.i.am", "desc":"영감을 주는 응원가.", "youtube":"https://www.youtube.com/watch?v=mk48xRzuNvA"},
    ],
    "ENFP": [
        {"title":"Dog Days Are Over", "artist":"Florence + The Machine", "desc":"에너지 넘치고 희망적인 곡.", "youtube":"https://www.youtube.com/watch?v=iWOyfLBYtuU"},
        {"title":"Shake It Out", "artist":"Florence + The Machine", "desc":"감정의 해방과 긍정.", "youtube":"https://www.youtube.com/watch?v=WbN0nX61rIs"},
        {"title":"Home", "artist":"Edward Sharpe & The Magnetic Zeros", "desc":"따뜻하고 자유로운 분위기.", "youtube":"https://www.youtube.com/watch?v=DHEOF_rcND8"},
    ],
    "ISTJ": [
        {"title":"Hotel California", "artist":"Eagles", "desc":"구조적이고 디테일한 스토리텔링.", "youtube":"https://www.youtube.com/watch?v=EqPtz5qN7HM"},
        {"title":"The Logical Song", "artist":"Supertramp", "desc":"이성적이며 회고적인 가사.", "youtube":"https://www.youtube.com/watch?v=FJb0L8g1Y9w"},
        {"title":"Take It Easy", "artist":"Eagles", "desc":"침착하고 현실적인 분위기.", "youtube":"https://www.youtube.com/watch?v=qwG3pZ4d2B0"},
    ],
    "ISFJ": [
        {"title":"Stand by Me", "artist":"Ben E. King", "desc":"헌신적이고 따뜻한 메시지.", "youtube":"https://www.youtube.com/watch?v=hwZNL7QVJjE"},
        {"title":"Landslide", "artist":"Fleetwood Mac", "desc":"돌봄과 추억에 대한 감성.", "youtube":"https://www.youtube.com/watch?v=WM7-PYtXtJM"},
        {"title":"Somewhere Over the Rainbow", "artist":"Israel Kamakawiwoʻole", "desc":"포근하고 안정적인 울림.", "youtube":"https://www.youtube.com/watch?v=V1bFr2SWP1I"},
    ],
    "ESTJ": [
        {"title":"We Will Rock You", "artist":"Queen", "desc":"조직적 리더십과 추진력.", "youtube":"https://www.youtube.com/watch?v=-tJYN-eG1zk"},
        {"title":"Eye of the Tiger", "artist":"Survivor", "desc":"목표달성의 의지.", "youtube":"https://www.youtube.com/watch?v=btPJPFnesV4"},
        {"title":"Don't Stop Me Now", "artist":"Queen", "desc":"분명하고 에너지 넘침.", "youtube":"https://www.youtube.com/watch?v=HgzGwKwLmgM"},
    ],
    "ESFJ": [
        {"title":"Count on Me", "artist":"Bruno Mars", "desc":"따뜻한 배려와 연대.", "youtube":"https://www.youtube.com/watch?v=yJYXItns2ik"},
        {"title":"I'm Yours", "artist":"Jason Mraz", "desc":"친근하고 포근한 가사.", "youtube":"https://www.youtube.com/watch?v=EkHTsc9PU2A"},
        {"title":"Hey Jude", "artist":"The Beatles", "desc":"함께 위로하고 힘이 되는 곡.", "youtube":"https://www.youtube.com/watch?v=A_MjCqQoLLA"},
    ],
    "ISTP": [
        {"title":"After Dark", "artist":"Mr. Kitty", "desc":"냉철하고 쿨한 분위기.", "youtube":"https://www.youtube.com/watch?v=6iQeWfX3RmU"},
        {"title":"Black Skinhead", "artist":"Kanye West", "desc":"직관적이고 강렬한 비트.", "youtube":"https://www.youtube.com/watch?v=YLZ1o8bG1Yw"},
        {"title":"Bad Guy", "artist":"Billie Eilish", "desc":"실험적이고 대담한 톤.", "youtube":"https://www.youtube.com/watch?v=DyDfgMOUjCI"},
    ],
    "ISFP": [
        {"title":"Holocene", "artist":"Bon Iver", "desc":"예술적 감수성과 미학.", "youtube":"https://www.youtube.com/watch?v=TWcyIpul8OE"},
        {"title":"Cherry Wine", "artist":"Hozier", "desc":"감성적이고 섬세한 표현.", "youtube":"https://www.youtube.com/watch?v=EiG0UUc6c2o"},
        {"title":"Sea of Love", "artist":"Cat Power", "desc":"잔잔하고 감미로운 음색.", "youtube":"https://www.youtube.com/watch?v=3Ck3b3O4o5g"},
    ],
    "ESTP": [
        {"title":"Uptown Funk", "artist":"Mark Ronson ft. Bruno Mars", "desc":"즉흥적이고 파티감성.", "youtube":"https://www.youtube.com/watch?v=OPf0YbXqDm0"},
        {"title":"Can't Hold Us", "artist":"Macklemore & Ryan Lewis", "desc":"활동적이고 즉각적인 에너지.", "youtube":"https://www.youtube.com/watch?v=2zNSgSzhBfM"},
        {"title":"Bangarang", "artist":"Skrillex", "desc":"강한 순간적인 자극.", "youtube":"https://www.youtube.com/watch?v=YJVmu6yttiw"},
    ],
    "ESFP": [
        {"title":"Happy", "artist":"Pharrell Williams", "desc":"사교적이고 즐거운 분위기.", "youtube":"https://www.youtube.com/watch?v=ZbZSe6N_BXs"},
        {"title":"Dancing Queen", "artist":"ABBA", "desc":"파티와 무드를 띄우는 클래식.", "youtube":"https://www.youtube.com/watch?v=xFrGuyw1V8s"},
        {"title":"Raise Your Glass", "artist":"P!nk", "desc":"즐겁고 축제 같은 기운.", "youtube":"https://www.youtube.com/watch?v=0J2QdDbelmY"},
    ],
}

# ----------------------
# Helper 함수
# ----------------------
def get_recommendations(mbti: str, n: int, randomize: bool) -> List[Dict]:
    pool = MBTI_SONGS.get(mbti, [])
    if not pool:
        return []
    if randomize:
        return random.sample(pool, k=min(n, len(pool)))
    else:
        return pool[:n]

# ----------------------
# UI: 사이드바
# ----------------------
st.sidebar.title("설정")
mbti_options = sorted(MBTI_SONGS.keys())
selected_mbti = st.sidebar.selectbox("MBTI 선택", mbti_options, index=0)
num_rec = st.sidebar.slider("추천곡 수", min_value=1, max_value=5, value=3)
randomize = st.sidebar.checkbox("무작위 추천", value=True)

# '처음효과' 옵션 (메모리 참고 기능 적용)
st.sidebar.markdown("---")
st.sidebar.write("처음효과")
enable_snow = st.sidebar.checkbox("눈 효과 (st.snow())", value=False)
show_gif = st.sidebar.checkbox("GIF 표시", value=False)
show_animated_text = st.sidebar.checkbox("애니메이션 텍스트", value=False)

# ----------------------
# '처음효과' 적용
# ----------------------
if enable_snow:
    # st.snow() 는 Streamlit 내장 효과
    st.snow()

if show_gif:
    # 간단한 GIF(외부 URL 사용). 환경에 따라 로드가 안 될 수 있음.
    st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", caption="즐거운 음악 추천 🎵")

if show_animated_text:
    # 간단한 CSS 애니메이션 텍스트 (unsafe_allow_html 사용)
    animated_html = """
    <div style="text-align:center; margin: 8px 0 18px 0;">
      <h2 style="font-size:28px; animation: fadeIn 2s infinite alternate;">
        🎧 나의 MBTI에 어울리는 노래를 찾아보세요!
      </h2>
    </div>
    <style>
    @keyframes fadeIn {
      from { opacity: 0.3; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0px); }
    }
    </style>
    """
    st.markdown(animated_html, unsafe_allow_html=True)

# ----------------------
# 메인: 제목/설명
# ----------------------
st.title("MBTI별 노래 추천기")
st.write("MBTI 유형을 선택하면 성격에 어울리는 노래를 추천해 줍니다. (추천 목록은 예시입니다 — 직접 편집/교체 가능)")

# 추천 버튼
if st.button("추천 받기"):
    recs = get_recommendations(selected_mbti, num_rec, randomize)
    if not recs:
        st.warning("선택한 MBTI에 대한 추천곡이 없습니다.")
    else:
        # 보여주기
        rows = []
        for i, song in enumerate(recs, start=1):
            st.subheader(f"{i}. {song['title']} — {song['artist']}")
            st.write(song["desc"])
            # 링크 버튼 (외부 링크 열기)
            st.markdown(f"[유튜브에서 듣기 ▶]({song['youtube']})")
            st.write("")  # 여백
            rows.append({"rank": i, "title": song["title"], "artist": song["artist"], "desc": song["desc"], "youtube": song["youtube"]})

        # DataFrame 및 다운로드
        df = pd.DataFrame(rows)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(label="추천 목록 CSV 다운로드", data=csv, file_name=f"{selected_mbti}_recommendations.csv", mime="text/csv")
else:
    st.info("왼쪽에서 MBTI와 설정을 선택한 뒤 '추천 받기' 버튼을 눌러주세요.")

# ----------------------
# 추가 UI: 전체 MBTI 미리보기
# ----------------------
with st.expander("모든 MBTI의 대표곡 미리보기"):
    for mbti, lst in MBTI_SONGS.items():
        sample = lst[0] if lst else {}
        st.markdown(f"**{mbti}** — {sample.get('title','-')} / {sample.get('artist','-')}")

# ----------------------
# 하단: 사용자 안내
# ----------------------
st.markdown("---")
st.write("앱 사용 팁:")
st.write("- 추천곡은 예시 데이터입니다. `MBTI_SONGS` 딕셔너리를 수정해 원하는 곡으로 바꿀 수 있어요.")
st.write("- 유튜브 링크는 외부 링크입니다. 스트림릿 내에서 바로 재생하려면 오디오 파일을 제공해야 합니다.")
st.write("- 개선하고 싶은 기능(선호 장르 필터, 플레이리스트 저장 등)이 있다면 추가해드릴게요!")

# 끝
