import streamlit as st
import base64

# --- 音を読み込むための準備（改良版） ---
def play_sound(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # 「controls」を追加して、画面に再生バーを出してみる（テスト用）
            md = f"""
                <audio autoplay="true" controls style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass

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

# --- 6. 結果表示の部分をここから書き換え ---
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.warning("引き分けです！")
    else:
        # 勝った時だけ、もう一度音を鳴らす（または別の豪華な音を指定する）
        # 今ある「bictory.mp3」をもう一度鳴らす場合はこのまま
        play_sound("bictory.mp3") 
        
        st.balloons() # 風船を飛ばす
        st.success(f"🏆 プレイヤー {st.session_state.winner} の勝ち！")

    # リセットボタン
    if st.button("もう一度遊ぶ"):
        st.session_state.board = [""] * 9
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.rerun()