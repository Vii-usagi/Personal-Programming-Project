## Personal Programming Project - Vicky. 
# Copy // trash bin
#WHY IS IT NOT COMMITING

import random 
from collections import Counter

starting = True
turn_count = 0

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
                  'B!', 'R!']

# Rank map
rank_map = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15, 'B!': 16, 'R!':17}

#combined deck
full_deck = list(zip(all_cards, all_card_names))

#prints rules
def intro():
    print('''Bot: Hello! Welcome to DouDiZhu aka Landlord
Bot: These are the rules:''')
    print('''RULES:
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
    print("Bot: The flipped card is:", landlord_card)
    print("Bot: I will shuffle the cards now...")
    
    # Deal cards - 17 cards each, leave 3 for landlord
    player_cards = deck[0:17]
    bot1_cards = deck[17:34]
    bot2_cards = deck[34:51]
    landlord_extra_cards = deck[51:54]
    
    print("Bot: The landlord will receive 3 extra cards")
    
    # Show the actual player's cards
    print("Bot: These are Player 1's cards!")
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
            print("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
            # Give extra cards to player
            player_cards.extend(landlord_extra_cards)
        else:
            print("Repicking...")
            landlord_choice = random.randint(1,3)
            print("New landlord is Player {}".format(landlord_choice))
            # Give extra cards to new landlord
            if landlord_choice == 1:
                player_cards.extend(landlord_extra_cards)
            elif landlord_choice == 2:
                bot1_cards.extend(landlord_extra_cards)
            else:
                bot2_cards.extend(landlord_extra_cards)
                
    # If the landlord is one of the bots
    elif landlord_choice == 2 or landlord_choice == 3:
        print("Bot: Player {} is the landlord!".format(landlord_choice))
        yes_or_no = random.randint(1,2)
        if yes_or_no != 1:
            print("Repicking...")
            landlord_choice = random.randint(1,3)
            print("New landlord is Player {}".format(landlord_choice))
        else:
            print("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
        
        # Give extra cards to landlord
        if landlord_choice == 1:
            player_cards.extend(landlord_extra_cards)
        elif landlord_choice == 2:
            bot1_cards.extend(landlord_extra_cards)
        else:
            bot2_cards.extend(landlord_extra_cards)
    
    # Show the landlord cards
    print("Bot: These are the landlord cards!")
    for card in landlord_extra_cards:
        print(card)
    
    return player_cards, bot1_cards, bot2_cards, landlord_choice

# Show cards
def show_cards_left(player_cards):
    sorted_hand = sorted(player_cards, key=lambda card: rank_map[card[0:]])
    print("Your cards: ", end="")
    for i, card in enumerate(sorted_hand):
        print(f"{i+1}:{card[0]}:{card[1]} ", end="")
    print()
    print(f"You currently have: {len(player_cards)} cards")


# Check if landlord is player
def check_landlord_is_player(landlord_choice):
    if landlord_choice == 1:
        player_identity = 1
    else:
        player_identity = 2
    return player_identity

def check_combination(cards_played):
    # check combo types by seeing how many cards per value is played
    lisssst = []
    for card in cards_played:
        lisssst.append(card[1])
    #counting how many per value
    counting_cards = Counter(lisssst)
    #assigning current_combo (simple)
    if 3 and 2 in counting_cards and len(counting_cards) == 5:
        current_combo_type = "Trio with pair"
    if 4 in counting_cards and len(counting_cards) == 4:
        current_combo_type = "Bomb"
    if 3 and 1 in counting_cards and len(counting_cards) == 5:
        current_combo_type = "Trio with single card"
    if 1 in counting_cards and len(counting_cards) == 1:
        current_combo_type = "Solo"
    if "!" and "!" in counting_cards and len(counting_cards) == 2:
        current_combo_type = "Rocket" 
    if "!" in counting_cards and len(counting_cards) == 1:
        current_combo_type = "Single Joker"
    if 4 and 1 and 1 in counting_cards and len(counting_cards) == 6:
        current_combo_type = "Four with two"
    if 4 and 2 in counting_cards and len(counting_cards) == 6:
        current_combo_type = "Four with a pair"
    
    #assigning current_combo (in ascension)
    #placeholder
    
    pass
    #return current_combo_type
 



def landlord_play(player_identity, player_cards, bot1_cards, bot2_cards):
    if player_identity == 1:
        show_cards_left(player_cards)
        play_combination(turn_count,player_cards,current_combo_type)
        # Add later 

def play_combination(turn_count, cards, current_combo_type):
    if turn_count%3 == 0:
        cards_played = input("*Please play a combination*\n")
        print("You have played:", cards_played)

    else:
        cards_played = input(f"Please play cards that follow the {current_combo_type} combination\n")
    # Add later
    pass

#---- start of game ---
starting = intro()

if starting:
    print("You are Player 1!!!")
    player_cards, bot1_cards, bot2_cards, landlord_choice = landlord_cards()
    player_identity = check_landlord_is_player(landlord_choice)
    # add laterr