import streamlit as st
import base64

# ---音を読み込む準備---
def play_sound(file_path):
    try:
        with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # javascriptを使ってブラウザに音を鳴らす
        md = f"""
            <audio autoplay="true">
            <source src="data:aaudio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """

        st.markdown(md, unsafe_allow_html=True)

# 1. ページの設定（タイトルなど）
st.set_page_config(page_title="ウェブ版 三目並べ", layout="centered")
st.title("🎮 三目並べ")
# --- デザイン（CSS）の追加 ---
st.markdown("""
    <style>
    /* 1. ボタン全体のデザイン（サイズ・丸み・影・色） */
    div.stButton > button {
        /*adjust sizes*/
        width: 100% !important;     /*横幅いっぱい*/
        height: 120px !important;   /*高さを150pxに変更*/
        /*文字のデザイン*/    
        font-size: 50px !important; /*文字も大きく*/
        font-weight: bold !important;
            
        /* 色と装飾 */
        background-color: #ffffff !important; /* ボタンの背景（白） */
        color: #333333 !important;           /* 文字の色（濃いグレー） */
        border-radius: 15px !important;     /*角を丸く*/
        border: 2px solid #555 !important;  /*枠線太い緑色*/
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2) !important;
        transition: 0.3s !important; /* 動きをなめらかに */
            
        /* 影をつけて立体感を出す */
        box-shadow: 0px 6px 0px #4d5584 !important; 
        transition: 0.1s !important;
    }

    /* 2. ボタンにマウスを乗せた時（ホバー）の色変更 */
    div.stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
        background-color: #f0f2f6 !important;
    }

    /* 3. ボタンを押した時の動き（少し沈む演出） */
    div.stButton > button:active {
        box-shadow: none !important;
        transform: translateY(6px) !important;
    }

    /* 4. 背景全体を少しおしゃれな色に */
    .stApp {
        background-color: #f7dbf9;
    }
    </style>
""", unsafe_allow_html=True)



# 2. ゲームの状態（盤面や手番）を保存する
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
if 'current_player' not in st.session_state:
    st.session_state.current_player = "X"
if 'winner' not in st.session_state:
    st.session_state.winner = None

# 3. 勝利判定の関数
def check_winner():
    b = st.session_state.board
    lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for i, j, k in lines:
        if b[i] == b[j] == b[k] != "":
            return b[i]
    if "" not in b:
        return "Draw"
    return None

# 4. マスをクリックした時の処理
def handle_click(i):
    if st.session_state.board[i] == "" and st.session_state.winner is None:
        st.session_state.board[i] = st.session_state.current_player
        st.session_state.winner = check_winner()
        if st.session_state.winner is None:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# 5. 画面（UI）の作成
# 3x3のボタン配置
cols = st.columns(3)
for i in range(9):
    label = st.session_state.board[i] if st.session_state.board[i] != "" else " "
    if cols[i % 3].button(label, key=f"btn{i}", use_container_width=True):
        handle_click(i)
        st.rerun()

# 6. 結果表示
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.warning("引き分けです！")
    else:
        st.success(f"プレイヤー {st.session_state.winner} の勝ち！")
        play_sound("bictory.mp3")  # ★ここで音を鳴らす！
    
    if st.button("もう一度遊ぶ"):
        st.session_state.board = [""] * 9
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.rerun()
else:
    st.info(f"現在は プレイヤー {st.session_state.current_player} の番です")