import random
import time

# Define the board mechanics
LADDERS = {3: 22, 5: 8, 11: 26, 20: 29}
SNAKES = {17: 4, 19: 7, 21: 9, 27: 1}
WINNING_SQUARE = 30

def roll_dice():
    return random.randint(1, 6)

def move_player(player_name, current_position):
    print(f"\n🎲 {player_name}'s turn! Press Enter to roll the dice...")
    input()  # Waits for user input if it's the player, or just an enter hit
    
    roll = roll_dice()
    print(f"🎲 {player_name} rolled a {roll}!")
    
    if current_position + roll > WINNING_SQUARE:
        print(f"⚠️ Over-shoot! {player_name} needs exactly {WINNING_SQUARE - current_position} to win. Staying at square {current_position}.")
        return current_position
        
    new_position = current_position + roll
    print(f"➡️ {player_name} moves to square {new_position}.")
    
    # Check for Ladders
    if new_position in LADDERS:
        up_to = LADDERS[new_position]
        print(f"🚀 BONUS SHIELD! {player_name} found a ladder! Climbing from {new_position} up to {up_to}!")
        new_position = up_to
        
    # Check for Snakes
    elif new_position in SNAKES:
        down_to = SNAKES[new_position]
        print(f"🐍 TAX TRAP! {player_name} stepped on a snake! Sliding down from {new_position} to {down_to}!")
        new_position = down_to
        
    return new_position

def main():
    print("=============================================")
    print(" 🎲 WELCOME TO THE MINI ECOSYSTEM RUNAWAY GAME 🎲")
    print("   First to square 30 wins. Avoid the traps! ")
    print("=============================================")
    
    player_pos = 0
    ai_pos = 0
    
    while player_pos < WINNING_SQUARE and ai_pos < WINNING_SQUARE:
        # Player Turn
        player_pos = move_player("Suraj (You)", player_pos)
        print(f"📊 Current Standing -> You: {player_pos} | Tax Collector: {ai_pos}")
        if player_pos == WINNING_SQUARE:
            print("\n🏆 CONGRATULATIONS! You successfully navigated the board and won!")
            break
            
        time.sleep(0.5)
        
        # AI Turn
        print("\n🤖 Tax Collector is rolling...")
        time.sleep(1)
        ai_pos = move_player("Tax Collector (AI)", ai_pos)
        print(f"📊 Current Standing -> You: {player_pos} | Tax Collector: {ai_pos}")
        if ai_pos == WINNING_SQUARE:
            print("\n📉 OH NO! The Tax Collector beat you to the finish line. Game Over!")
            break
            
if __name__ == "__main__":
    main()