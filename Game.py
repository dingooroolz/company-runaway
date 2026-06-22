import streamlit as st
import random

# ==========================================
# BOARD CONFIGURATION
# ==========================================
LADDERS = {3: 22, 5: 8, 11: 26, 20: 29}
SNAKES = {17: 4, 19: 7, 21: 9, 27: 1}
WINNING_SQUARE = 30

st.set_page_config(page_title="Ecosystem Runaway Game", page_icon="🎲", layout="centered")

st.title("🎲 The Mini Ecosystem Runaway Game")
st.write("First to square 30 wins. Use the shortcuts, avoid the tax traps!")
st.write("---")

# Initialize game states if they don't exist
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = 0
if 'ai_pos' not in st.session_state:
    st.session_state.ai_pos = 0
if 'game_log' not in st.session_state:
    st.session_state.game_log = ["Game started! Good luck."]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def reset_game():
    st.session_state.player_pos = 0
    st.session_state.ai_pos = 0
    st.session_state.game_log = ["Game restarted! Fresh board."]
    st.session_state.game_over = False

# ==========================================
# VISUAL SCOREBOARD
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.metric(label="👤 Your Position", value=f"Square {st.session_state.player_pos}")
with col2:
    st.metric(label="🤖 Tax Collector Position", value=f"Square {st.session_state.ai_pos}")

# Progress bars to visually show progress toward square 30
st.progress(min(st.session_state.player_pos / WINNING_SQUARE, 1.0), text="Your Progress")
st.progress(min(st.session_state.ai_pos / WINNING_SQUARE, 1.0), text="Tax Collector Progress")

st.write("---")

# ==========================================
# GAME LOGIC TRIGGER
# ==========================================
if not st.session_state.game_over:
    if st.button("🎲 Roll Dice", type="primary", use_container_width=True):
        new_logs = []
        
        # --- PLAYER TURN ---
        p_roll = random.randint(1, 6)
        if st.session_state.player_pos + p_roll > WINNING_SQUARE:
            new_logs.append(f"👤 You rolled a {p_roll} but overshot! Staying at {st.session_state.player_pos}.")
        else:
            st.session_state.player_pos += p_roll
            new_logs.append(f"👤 You rolled a {p_roll} and moved to {st.session_state.player_pos}.")
            
            # Check shortcuts/traps
            if st.session_state.player_pos in LADDERS:
                old = st.session_state.player_pos
                st.session_state.player_pos = LADDERS[old]
                new_logs.append(f"🚀 BONUS SHIELD! Climbed ladder from {old} to {st.session_state.player_pos}!")
            elif st.session_state.player_pos in SNAKES:
                old = st.session_state.player_pos
                st.session_state.player_pos = SNAKES[old]
                new_logs.append(f"🐍 TAX TRAP! Slid down snake from {old} to {st.session_state.player_pos}!")

        # Check Player Win
        if st.session_state.player_pos == WINNING_SQUARE:
            st.session_state.game_over = True
            new_logs.append("🏆 CONGRATULATIONS! You beat the Tax Collector!")
            
        # --- AI TURN (Only if player didn't win yet) ---
        if not st.session_state.game_over:
            ai_roll = random.randint(1, 6)
            if st.session_state.ai_pos + ai_roll > WINNING_SQUARE:
                new_logs.append(f"🤖 Tax Collector rolled a {ai_roll} but overshot.")
            else:
                st.session_state.ai_pos += ai_roll
                new_logs.append(f"🤖 Tax Collector rolled a {ai_roll} and moved to {st.session_state.ai_pos}.")
                
                if st.session_state.ai_pos in LADDERS:
                    old = st.session_state.ai_pos
                    st.session_state.ai_pos = LADDERS[old]
                    new_logs.append(f"🤖 Tax Collector found a ladder to {st.session_state.ai_pos}!")
                elif st.session_state.ai_pos in SNAKES:
                    old = st.session_state.ai_pos
                    st.session_state.ai_pos = SNAKES[old]
                    new_logs.append(f"🤖 Tax Collector hit a trap and fell to {st.session_state.ai_pos}!")

            # Check AI Win
            if st.session_state.ai_pos == WINNING_SQUARE:
                st.session_state.game_over = True
                new_logs.append("📉 GAME OVER! The Tax Collector reached square 30 first.")

        # Save logs
        st.session_state.game_log = new_logs + st.session_state.game_log
        st.rerun()

else:
    st.subheader("🎉 Game Over!")
    if st.button("🔄 Play Again", use_container_width=True):
        reset_game()
        st.rerun()

# ==========================================
# LIVE MATCH FEED
# ==========================================
st.write("### 📋 Live Match Feed")
for log in st.session_state.game_log:
    if "🏆" in log or "🚀" in log:
        st.success(log)
    elif "📉" in log or "🐍" in log:
        st.error(log)
    else:
        st.info(log)
