import streamlit as st
import base64

# --- 音を読み込むための準備（ここがエラーの原因でした） ---
def play_sound(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()  # ここは右にスペースが4つ必要
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass # 音がなくてもエラーで止まらないようにする

# --- デザイン（CSS） ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 120px !important;
        font-size: 50px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("三目並べゲーム")

# --- ゲームのロジック ---
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None

def check_winner():
    b = st.session_state.board
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for l in lines:
        if b[l[0]] == b[l[1]] == b[l[2]] != "":
            return b[l[0]]
    if "" not in b:
        return "Draw"
    return None

def handle_click(i):
    if st.session_state.board[i] == "" and st.session_state.winner is None:
        play_sound("bictory.mp3") # 音を鳴らす
        st.session_state.board[i] = st.session_state.current_player
        st.session_state.winner = check_winner()
        if st.session_state.winner is None:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# --- 画面の表示 ---
cols = st.columns(3)
for i in range(9):
    if cols[i % 3].button(st.session_state.board[i] if st.session_state.board[i] else " ", key=f"b{i}"):
        handle_click(i)
        st.rerun()

if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.write("引き分け！")
    else:
        st.balloons()
        st.success(f"勝者: {st.session_state.winner}")
    if st.button("もう一度遊ぶ"):
        st.session_state.board = [""] * 9
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.rerun()