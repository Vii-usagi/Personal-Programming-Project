## Personal Programming Project - Vicky. 

import random 
from collections import Counter
import pygame
from colorist import ColorRGB, BgColorRGB, rgb, bg_rgb

starting = True
turn_count = 0
current_combo_type = None

#colors
def bot(string):
    rgb(string,200,10,10)
def botty(string):
    rgb(string,10,80,100)
def cardy(string):
    rgb(string,10,100,120)
def bot1(string):
    rgb(string, 250,0,100)
def bot2(string):
    rgb(string,0,100,250)

# Fixed card decks
all_cards = ['🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂼', '🂽', '🂾', 
             '🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂬', '🂭', '🂮',
             '🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃌', '🃍', '🃎',
             '🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃜', '🃝', '🃞',
             '🃏', '🃟']

all_card_names = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'hJ', 'hQ', 'hK',
                  's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 'sJ', 'sQ', 'sK',
                  'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'dJ', 'dQ', 'dK',
                  'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'cJ', 'cQ', 'cK',
                  'BJ', 'RJ']

# Rank map
rank_map = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15, 'BJ': 16, 'RJ':17}

#combined deck
full_deck = list(zip(all_cards, all_card_names))

#prints rules
def intro():
    bot('''Bot: Hello! Welcome to DouDiZhu aka Landlord
Bot: These are the rules:''')
    bot('''RULES:
3 people a game
Whoever gets the flipped card is the landlord
The landlord gets 3 extra cards that is shown to everyone
Card value in ascending: 3 4 5 6 7 8 9 10 J Q K A 2 BJ RJ
Card combinations: 
Rocket: BJ and RJ, it is the largest combination
Solo chain: number sequence in ascending order (must at least be 5 cards)
Solo: any solo card
Pairs: a pair of the same number
Bomb: a quad of the same number (the value of each bomb depends on the card value)
Trio with single card : a triad of the same number plus a singular card (the value of the 3+1 depends on the triad)
Trio with pair: a triad of the same number plus a pair (the value of the 3+2 depends on the triad)
Pairs chain: at least three consecutive pairs
Airplane: at least two consecutive trios
Airplane with small wings: at least two consecutive trio and the same number of solo cards
Air plane with large wings: at least two consecutive trios and the same number of pairs
Four with two: four of the same card and two solos
Four with a pair: four of the same card and a pair
''')
    
    start_game = int(input("Type 1 to [Continue] \n "))
    if start_game == 1:
        return True
    else:
        print("Guess I'll see you next time!")
        return False

# the landlord card that the landlord receives
def landlord_cards():
    # copy of the full deck 
    deck = full_deck.copy()
    random.shuffle(deck)
    
    # Pick landlord card
    landlord_card = deck[random.randint(0, len(deck)-1)]
    bot(f"Bot: The flipped card is: {landlord_card}")
    bot("Bot: I will shuffle the cards now...")
    
    # Deal cards - 17 cards each, leave 3 for landlord
    player_cards = deck[0:17]
    bot1_cards = deck[17:34]
    bot2_cards = deck[34:51]
    landlord_extra_cards = deck[51:54]
    
    bot("Bot: The landlord will receive 3 extra cards")
    
    # Show the actual player's cards
    bot("Bot: These are Player 1's cards!")
    show_cards_left(player_cards)
    
    # Seeing who is the landlord
    if landlord_card in player_cards:
        landlord_choice = 1
    elif landlord_card in bot1_cards:
        landlord_choice = 2
    else:
        landlord_choice = 3
    
    # Asking if the player wants to be the landlord
    if landlord_choice == 1:
        landlord = int(input("Bot: Player {} is the landlord! Do you want to be the landlord? Click 1 if yes. ".format(landlord_choice)))
        
        if landlord == 1:
            botty("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
            # Give extra cards to player
            player_cards.extend(landlord_extra_cards)
        else:
            bot("Repicking...")
            landlord_choice = random.randint(1,3)
            botty("New landlord is Player {}".format(landlord_choice))
            # Give extra cards to new landlord
            if landlord_choice == 1:
                player_cards.extend(landlord_extra_cards)
            elif landlord_choice == 2:
                bot1_cards.extend(landlord_extra_cards)
            else:
                bot2_cards.extend(landlord_extra_cards)
                
    # If the landlord is one of the bots
    elif landlord_choice == 2 or landlord_choice == 3:
        botty("Bot: Player {} is the landlord!".format(landlord_choice))
        yes_or_no = random.randint(1,2)
        if yes_or_no != 1:
            bot("Repicking...")
            landlord_choice = random.randint(1,3)
            botty("New landlord is Player {}".format(landlord_choice))
        else:
            botty("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
        
        # Give extra cards to landlord
        if landlord_choice == 1:
            player_cards.extend(landlord_extra_cards)
        elif landlord_choice == 2:
            bot1_cards.extend(landlord_extra_cards)
        elif landlord_choice == 3:
            bot2_cards.extend(landlord_extra_cards)
    
    # Show the landlord cards
    bot("Bot: These are the landlord cards!")
    for card in landlord_extra_cards:
        cardy(card)
    
    return player_cards, bot1_cards, bot2_cards, landlord_choice
#joker
def get_rank(card):
    name = card[1]
    if name in ('BJ','RJ'):
        return rank_map[name]
    rank_part = name[1:]
    if rank_part in rank_map:
        return int(rank_map[rank_part])
    if rank_part == '1':  
        return rank_map['A']
    raise ValueError(f"Unknown rank part: {rank_part} from card name {name}")
        
# Show cards
def show_cards_left(player_cards):  
    sorted_hand = sorted(player_cards, key=get_rank)
    print("Your cards: ", end="")
    for i, card in enumerate(sorted_hand):
        print(f"{i+1}:{card[0]}:{card[1]} ", end="")
    print()
    cardy(f"You currently have: {len(player_cards)} cards")
    return sorted_hand

# Check if landlord is player
def check_landlord_is_player(landlord_choice):
    if landlord_choice == 1:
        player_identity = 1
    else:
        player_identity = 2
    return player_identity


def check_combination(cards_played):
    if not cards_played:
        return "Pass"
        
    values = []
    for card in cards_played:
        print(card)
        print(card[1])
        name = card[1]
        if name == 'BJ':
            values.append(16)
        elif name == 'RJ':
            values.append(17)
        else:
            rank_part = name[1:]
            values.append(rank_map[rank_part])
        
    value_counts = Counter(values)
    num_cards = len(cards_played)
        
    # Rocket (BJ + RJ)
    if set(values) == {16, 17}:
        return "Rocket"
        
    # Solo
    if num_cards == 1:
        return "Solo"
        
    # Pair
    if num_cards == 2 and max(value_counts.values()) == 2:
        return "Pair"
        
    # Bomb
    if num_cards == 4 and max(value_counts.values()) == 4:
        return "Bomb"
        
    # Trio with single
    if num_cards == 4 and max(value_counts.values()) == 3:
        return "Trio with single card"
        
    # Trio with pair
    if num_cards == 5 and sorted(value_counts.values()) == [2, 3]:
        return "Trio with pair"
        
    #placeholder
    #return current_combo_type
    return "Unknown"

def landlord_play(player_identity, player_cards, bot1_cards, bot2_cards, turn_count, current_combo_type):
    if player_identity == 1:
        show_cards_left(player_cards)
        current_combo_type, turn_count = play_combination(turn_count,current_combo_type)

        # Add later 
    elif player_identity == 2:
        #only playing single for now
        current_combo_type, turn_count, cards_played = bot_play_landlord(turn_count,current_combo_type, bot1_cards)
        bot1(f"Player 2 has played {cards_played}")
        botty(f"Player 2 has {len(bot1_cards)} left")
        
    else:
        current_combo_type, turn_count, cards_played = bot_play_landlord(turn_count,current_combo_type, bot2_cards)
        bot2(f"Player 3 has played {cards_played}")
        botty(f"Player 3 has {len(bot2_cards)} left")
    
    return current_combo_type, player_cards, bot1_cards, bot2_cards, turn_count

        # add bot play ***
    #add automatic bots
    #can't incorporate open ai idk why

def bot_play_landlord(turn_count, current_combo_type, bot_cards):
    # bot play... only for single cos idk
    # this doesn't work
    if bot_cards == bot1_cards:
        print(len(bot1_cards))
        for i in bot1_cards:
                chosen_card = random.randint(1,len(bot1_cards)-1)
                cards_played = bot1_cards[chosen_card]
    else:
        for i in bot2_cards:
                chosen_card = random.randint(1,20)
                cards_played = bot2_cards[chosen_card]
    current_combo_type = check_combination(cards_played)
    turn_count += 1
    return current_combo_type, turn_count, cards_played
    


def play_combination(turn_count, current_combo_type):
    # if there is no current combo / reset the game
    if turn_count == 0:
        cards_played = input("*Please play a combination*\n")
        print("You have played:", cards_played)
        
        # add later: check that the cards played are in the player's deck
        # add later: pop the cards played from the player's deck

    else:
        cards_played = input(f"Please play cards that follow the {current_combo_type} combination\n")
        if cards_played == "Skip":
            print("Going back to the previous player...")
            #reset the round so there is no current_combo_type
            turn_count = 0
            return turn_count
            # add on later
        else:
            #check if new matches old
            new_combo_type = check_combination(cards_played) 
            #check if its bigger

            #add later

            if new_combo_type == current_combo_type:
                print("You have played:", cards_played)
                turn_count += 1
            else:
                play_combination(turn_count, current_combo_type)
    return current_combo_type, turn_count

def check_larger_combo():
    pass
    #add later




#---- start of game ---
starting = intro()

if starting:
    cardy("You are Player 1!!!")
    player_cards, bot1_cards, bot2_cards, landlord_choice = landlord_cards()
    player_identity = check_landlord_is_player(landlord_choice)
    sorted_hand = show_cards_left(player_cards)
    current_combo_type, player_cards, bot1_cards, bot2_cards, turn_count = landlord_play(player_identity, player_cards, bot1_cards, bot2_cards, turn_count, current_combo_type)

    # add laterr