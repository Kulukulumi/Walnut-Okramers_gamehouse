import streamlit as st

# 1. ページの設定（タイトルなど）
st.set_page_config(page_title="ウェブ版 三目並べ", layout="centered")
st.title("🎮 三目並べ ウェブアプリ")

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
    
    if st.button("もう一度遊ぶ"):
        st.session_state.board = [""] * 9
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.rerun()
else:
    st.info(f"現在は プレイヤー {st.session_state.current_player} の番です")