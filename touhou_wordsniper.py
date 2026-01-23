import streamlit as st
import random

st.set_page_config(layout="wide")

# --- 1. 初期化 ---
if "deck" not in st.session_state:
    DECK = [
        "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ",
        "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
        "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
        "ま", "み", "む", "め", "も", "や", "ゆ", "よ",
        "ら", "り", "る", "れ", "ろ", "わ", "を", "ん"
    ]
    random.shuffle(DECK)
    st.session_state.deck = DECK
    st.session_state.current_card = "？"

# --- 2. カードを引く ---
def draw_card():
    if st.session_state.deck:
        st.session_state.current_card = st.session_state.deck.pop()
    else:
        st.session_state.current_card = "終"

# --- 3. CSS（最低限・安全） ---
st.markdown("""
<style>
.card {
    width: 300px;
    height: 450px;
    margin: auto;
    background: white;
    border: 8px solid #327e55;
    border-radius: 20px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}

.card-text {
    font-size: 100px;
    font-weight: bold;
}

.upside-down {
    transform: rotate(180deg);
}

.big-button button {
    width: 100%;
    height: 200px;
    font-size: 24px;
}
</style>
""", unsafe_allow_html=True)

# --- 4. 表示 ---
st.title("東方ワードスナイパー Web版")

st.markdown(f"""
<div class="card">
    <div class="card-text">{st.session_state.current_card}</div>
    <div class="card-text upside-down">{st.session_state.current_card}</div>
</div>
""", unsafe_allow_html=True)

st.write("")  
st.write("")  

# --- 5. 下半分クリック用ボタン ---
with st.container():
    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    st.button("カードをめくる", on_click=draw_card)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 補助情報 ---
st.write(f"のこり：{len(st.session_state.deck)} まい")

if st.button("最初からやり直す"):
    st.session_state.clear()
    st.rerun()
