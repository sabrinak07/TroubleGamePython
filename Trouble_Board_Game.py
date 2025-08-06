# Trouble Board Game
# Authors: Sabrina Kessler, Vanvuong Nguyen, Ramaisa Chowdhury
# Filename: Trouble_Board_Game.py
# Description: A terminal-based multiplayer version of the classic "Trouble" board game using Python and OOP
# Date: May 7, 2025

import random

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = -1  # Start at Home
        self.status = "Home"
        self.lastDieRoll = None

    def __str__(self):
        return f"{self.name}, you are {self.color}, at position {self.position}, status: {self.status}"

    def pop_die(self):
        self.lastDieRoll = random.randint(1, 6)
        print(f"{self.name} rolled a {self.lastDieRoll}")
        return self.lastDieRoll

    def roll_six(self):
        return self.lastDieRoll == 6

    def pop_die_again(self):
        return self.pop_die()

    def move_thepeg(self):
        if self.position == -1:  # Home
            if self.lastDieRoll == 6:
                self.position = 0
                self.status = "Track"
                print(f"{self.name} entered the board at position 0!")
            else:
                print(f"{self.name} needs a 6 to move out of Home.")
        else:
            self.position += self.lastDieRoll
            if self.position >= 27:
                self.position = 28
                self.status = "Safe"
                print(f"{self.name} entered the SAFE ZONE!")
            else:
                print(f"{self.name} moved to position {self.position}")
        return self.position

    def take_turn(self, players):
        command = input(f"\n{self.name}'s turn. Press Enter to roll or type 'quit' to end: ").lower()
        if command == "quit":
            return True

        self.pop_die()
        self.move_thepeg()
        draw_board(players)

        while self.roll_six():
            input(f"{self.name} rolled a 6! Press Enter for a bonus roll...")
            self.pop_die_again()
            self.move_thepeg()
            draw_board(players)

        return False

def is_color_taken(color, players):
    for p in players:
        if p.color.lower() == color.lower():
            return True
    return False

def bump_opponents(current_player, players):
    for p in players:
        if p != current_player and p.position == current_player.position and p.status == "Track":
            print(f"{current_player.name} bumped {p.name}!")
            p.position = -1
            p.status = "Home"

def draw_board(players):
    top_row = list(range(7))
    right_col = [7, 8, 9]
    bottom_row = list(range(10, 17))[::-1]
    left_col = [17, 18, 19]

    def format_space(pos):
        for p in players:
            if p.position == pos:
                return f"[{p.color[0]}]"
        return f"[{pos:2d}]"

    print(" ".join(format_space(i) for i in top_row))
    for l, r in zip(left_col, right_col):
        print(f"{format_space(l)}{' ' * 21}{format_space(r)}")
    print(" ".join(format_space(i) for i in bottom_row))
    for p in players:
        if p.status == "Safe":
            print(f"{p.name} is in the SAFE ZONE!")


def playGame():
    board_limit = 28
    available_colors = ["Red", "Blue", "Green", "Yellow"]
    players = []

    print("Welcome to The Board Game Trouble! Enter player names and pick a color to start.")

    while len(players) < 4:
        name = input("Enter your name: ")
        color = input("Choose a color (Red, Blue, Green, Yellow): ")
        while is_color_taken(color, players) or color.capitalize() not in available_colors:
            print("Invalid or taken color. Try again.")
            color = input("Choose a color: ")
        players.append(Player(name, color.capitalize()))

        if len(players) < 4:
            more = input("Add another player? (yes/no): ").lower()
            if more != "yes":
                break
        else:
            print("Maximum of 4 players reached.")
            break

    print("\nStarting game...\n")
    game_over = False
    turn = 0

    while not game_over:
        player = players[turn % len(players)]
        quit_game = player.take_turn(players)
        if quit_game:
            print(f"\n{player.name} quit the game.")
            break

        bump_opponents(player, players)

        if player.status == "Safe":
            print(f"\n🎉 {player.name} wins the game! 🎉")
            game_over = True
        turn += 1

playGame()
