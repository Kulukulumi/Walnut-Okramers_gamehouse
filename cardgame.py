import streamlit as st
import random
import time

# 1. ページの設定（タイトルなど）
st.set_page_config(page_title="ウェブ版 神経衰弱", layout="centered")
st.title("🎮 神経衰弱 ウェブアプリ")

# 1. 準備：カードの中身（絵文字）を決める
# 2枚ずつペアになるようにリストを作成
EMOJIS = ["🍎", "🐱", "🚀", "💎", "👻", "🌈"]
if 'cards' not in st.session_state:
    # 6種類×2枚で12枚のカードを作り、シャッフルする
    card_list = EMOJIS * 2
    random.shuffle(card_list)
    st.session_state.cards = card_list
    # 全カードの状態（False = 裏、True = 表）
    st.session_state.revealed = [False] * 12
    # 現在めくっているカードの番号を記録するリスト
    st.session_state.selection = []

# デザイン設定
st.markdown("""
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        font-size: 40px !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("カードめくりゲーム")

# カードをクリックした時の動き
def flip_card(i):
    # すでに表のカードや、3枚目は選べない
    if st.session_state.revealed[i] or len(st.session_state.selection) >= 2:
        return

    st.session_state.revealed[i] = True
    st.session_state.selection.append(i)

    # 2枚選んだ時の判定
    if len(st.session_state.selection) == 2:
        idx1, idx2 = st.session_state.selection
        if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
            # 一致したらそのまま（表のまま）
            st.session_state.selection = []
        else:
            # 一致しなかったら少し待って裏返す（※ここは後で調整可能）
            pass

# 画面にカードを表示（3列×4行）
cols = st.columns(3)
for i in range(12):
    # カードが表なら絵文字、裏なら「？」を表示
    label = st.session_state.cards[i] if st.session_state.revealed[i] else "❓"
    
    if cols[i % 3].button(label, key=f"card{i}"):
        flip_card(i)
        st.rerun()

# 「？に戻す」ボタン（一致しなかった時用）
if len(st.session_state.selection) == 2:
    if st.button("ハズレ！裏に戻す"):
        idx1, idx2 = st.session_state.selection
        st.session_state.revealed[idx1] = False
        st.session_state.revealed[idx2] = False
        st.session_state.selection = []
        st.rerun()

# 全部めくれたらお祝い
if all(st.session_state.revealed):
    st.balloons()
    st.success("全部見つけたね！おめでとう！")
    if st.button("もう一度あそぶ"):
        del st.session_state.cards
        st.rerun()
