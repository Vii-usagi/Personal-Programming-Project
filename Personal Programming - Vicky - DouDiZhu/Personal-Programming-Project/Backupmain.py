import random 
from collections import Counter
from colorist import ColorRGB, BgColorRGB, rgb, bg_rgb

starting = True
turn_count = 0
current_combo_type = None
#what can I say, Im just dat amazin
all_cards_played = [ ]
skips_in_row = 0

# Fixed card decks
all_cards = [
    ('h', 1, '🂱'), ('h', 2, '🂲'), ('h', 3, '🂳'), ('h', 4, '🂴'),
    ('h', 5, '🂵'), ('h', 6, '🂶'), ('h', 7, '🂷'), ('h', 8, '🂸'),
    ('h', 9, '🂹'), ('h', 10, '🂺'), ('h', 11, '🂻'), ('h', 12, '🂼'),
    ('h', 13, '🂽'), ('h', 14, '🂾'),

    ('s', 1, '🂡'), ('s', 2, '🂢'), ('s', 3, '🂣'), ('s', 4, '🂤'),
    ('s', 5, '🂥'), ('s', 6, '🂦'), ('s', 7, '🂧'), ('s', 8, '🂨'),
    ('s', 9, '🂩'), ('s', 10, '🂪'), ('s', 11, '🂫'), ('s', 12, '🂬'),
    ('s', 13, '🂭'), ('s', 14, '🂮'),

    ('d', 1, '🃁'), ('d', 2, '🃂'), ('d', 3, '🃃'), ('d', 4, '🃄'),
    ('d', 5, '🃅'), ('d', 6, '🃆'), ('d', 7, '🃇'), ('d', 8, '🃈'),
    ('d', 9, '🃉'), ('d', 10, '🃊'), ('d', 11, '🃋'), ('d', 12, '🃌'),
    ('d', 13, '🃍'), ('d', 14, '🃎'),

    ('c', 1, '🃑'), ('c', 2, '🃒'), ('c', 3, '🃓'), ('c', 4, '🃔'),
    ('c', 5, '🃕'), ('c', 6, '🃖'), ('c', 7, '🃗'), ('c', 8, '🃘'),
    ('c', 9, '🃙'), ('c', 10, '🃚'), ('c', 11, '🃛'), ('c', 12, '🃜'),
    ('c', 13, '🃝'), ('c', 14, '🃞'),

    ('BJ', 16, '🃏'),
    ('RJ', 17, '🃟')
]

all_card_names = [
    'h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','hJ','hQ','hK',
    's1','s2','s3','s4','s5','s6','s7','s8','s9','s10','sJ','sQ','sK',
    'd1','d2','d3','d4','d5','d6','d7','d8','d9','d10','dJ','dQ','dK',
    'c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','cJ','cQ','cK',
    'BJ','RJ'
]

#combined deck
full_deck = list(zip([c[2] for c in all_cards], all_card_names, all_cards))

# Rank map
rank_map = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15, 'BJ': 16, 'RJ':17}

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
# this works completely fine
def landlord_cards():
    deck = full_deck.copy()
    random.shuffle(deck)
    landlord_card = random.choice(deck)
    print(f"Bot: The flipped card is: {landlord_card}")
    print("Bot: I will shuffle the cards now...")
    player_cards = deck[0:17]
    bot1_cards = deck[17:34]
    bot2_cards = deck[34:51]
    landlord_extra_cards = deck[51:54]
    print("Bot: The landlord will receive 3 extra cards")
    print("Bot: These are Player 1's cards!")
    show_cards_left(player_cards)
    if landlord_card in player_cards:
        landlord_choice = 1
    elif landlord_card in bot1_cards:
        landlord_choice = 2
    else:
        landlord_choice = 3
    if landlord_choice == 1:
        landlord = int(input("Bot: Player {} is the landlord! Do you want to be the landlord? Click 1 if yes. ".format(landlord_choice)))
        if landlord == 1:
            print("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
            player_cards.extend(landlord_extra_cards)
        else:
            print("Repicking...")
            landlord_choice = random.randint(1,3)
            print("New landlord is Player {}".format(landlord_choice))
            if landlord_choice == 1:
                player_cards.extend(landlord_extra_cards)
            elif landlord_choice == 2:
                bot1_cards.extend(landlord_extra_cards)
            else:
                bot2_cards.extend(landlord_extra_cards)
    elif landlord_choice == 2 or landlord_choice == 3:
        print("Bot: Player {} is the landlord!".format(landlord_choice))
        yes_or_no = random.randint(1,2)
        if yes_or_no != 1:
            print("Repicking...")
            landlord_choice = random.randint(1,3)
            print("New landlord is Player {}".format(landlord_choice))
        else:
            print("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
        if landlord_choice == 1:
            player_cards.extend(landlord_extra_cards)
        elif landlord_choice == 2:
            bot1_cards.extend(landlord_extra_cards)
        elif landlord_choice == 3:
            bot2_cards.extend(landlord_extra_cards)
    print("Bot: These are the landlord cards!")
    for card in landlord_extra_cards:
        print(card)
    return player_cards, bot1_cards, bot2_cards, landlord_choice

#joker
def get_rank(card):
    return card[2][1]

# Show cards
def show_cards_left(player_cards):  
    sorted_hand = sorted(player_cards, key=get_rank)
    print("Your cards: ", end="")
    for i, card in enumerate(sorted_hand):
        print(f"{i+1}:{card[0]}:{card[1]} ", end="")
    print()
    print(f"You currently have: {len(player_cards)} cards")
    return sorted_hand

# Check if landlord is player
def check_landlord_is_player(landlord_choice):
    if landlord_choice == 1:
        player_identity = 1
    if landlord_choice == 2:
        player_identity = 2
    if landlord_choice ==3:
        player_identity = 3
    return player_identity

def check_combination(cards_played):
    if not cards_played:
        return "Pass"
    values = [card[2][1] for card in cards_played]
    value_counts = Counter(values)
    num_cards = len(cards_played)
    if set(values) == {16, 17}:
        return "Rocket"
    if num_cards == 1:
        return "Solo"
    if num_cards == 2 and max(value_counts.values()) == 2:
        return "Pair"
    if num_cards == 4 and max(value_counts.values()) == 4:
        return "Bomb"
    if num_cards == 4 and max(value_counts.values()) == 3:
        return "Trio with single card"
    if num_cards == 5 and sorted(value_counts.values()) == [2, 3]:
        return "Trio with pair"
    
    # big ones ykyk
    # Solo chain (at least 5 consecutive singles)
    if num_cards >= 5 and all(v == 1 for v in value_counts.values()):
        sorted_vals = sorted(values)
        if all(sorted_vals[i] + 1 == sorted_vals[i+1] for i in range(len(sorted_vals)-1)):
            return "Solo chain"

    # Pairs chain (at least 3 consecutive pairs)
    if num_cards >= 6 and all(v == 2 for v in value_counts.values()):
        sorted_vals = sorted(set(values))
        if all(sorted_vals[i] + 1 == sorted_vals[i+1] for i in range(len(sorted_vals)-1)):
            return "Pairs chain"

    # Aeroplane (at least 2 consecutive trios)
    if num_cards % 3 == 0 and all(v == 3 for v in value_counts.values()):
        sorted_vals = sorted(set(values))
        if all(sorted_vals[i] + 1 == sorted_vals[i+1] for i in range(len(sorted_vals)-1)):
            return "Aeroplane"

    # Aeroplane with smol wings (trios + same number of solos)
    if num_cards % 4 == 0:
        trio_vals = [v for v, c in value_counts.items() if c == 3]
        if len(trio_vals) >= 2:
            sorted_trios = sorted(trio_vals)
            if all(sorted_trios[i] + 1 == sorted_trios[i+1] for i in range(len(sorted_trios)-1)):
                return "Aeroplane with small wings"

    #Aeroplane with big wings (trios + same number of pairs)
    if num_cards % 5 == 0:
        trio_vals = [v for v, c in value_counts.items() if c == 3]
        pair_vals = [v for v, c in value_counts.items() if c == 2]
        if len(trio_vals) >= 2 and len(pair_vals) >= len(trio_vals):
            sorted_trios = sorted(trio_vals)
            if all(sorted_trios[i] + 1 == sorted_trios[i+1] for i in range(len(sorted_trios)-1)):
                return "Aeroplane with large wings"
    return "Unknown"
'''
def landlord_play(player_identity, player_cards, bot1_cards, bot2_cards, turn_count, current_combo_type):
    if player_identity == 1:
        show_cards_left(player_cards)
        current_combo_type, turn_count = play_combination(turn_count, current_combo_type, player_cards)
    elif player_identity == 2:
        current_combo_type, turn_count, cards_played = bot_play_landlord(turn_count, current_combo_type, bot1_cards)
        print(f"Player 2 has played {cards_played}")
        print(f"Player 2 has {len(bot1_cards)} left")
    else:
        current_combo_type, turn_count, cards_played = bot_play_landlord(turn_count, current_combo_type, bot2_cards)
        print(f"Player 3 has played {cards_played}")
        print(f"Player 3 has {len(bot2_cards)} left")
    return current_combo_type, player_cards, bot1_cards, bot2_cards, turn_count
'''

#### SOOO MANY BUGS
def landlord_play(player_identity, player_cards, bot1_cards, bot2_cards, turn_count, current_combo_type, skips_in_row):
    if player_identity == 1:
        show_cards_left(player_cards)
        current_combo_type, turn_count, skips_in_row = play_combination(turn_count, current_combo_type, player_cards, skips_in_row)
    elif player_identity == 2:
        current_combo_type, turn_count, cards_played, skips_in_row = bot_play_combination(turn_count, current_combo_type, bot1_cards, skips_in_row)
        if cards_played:
            print(f"Player 2 has played {[c[0] for c in cards_played]}")
            print(f"Player 2 has played {[c[1] [2] for c in cards_played]}")
            print(f"Player 2 has {len(bot1_cards)} left")
    
    else:
        current_combo_type, turn_count, cards_played, skips_in_row = bot_play_combination(turn_count, current_combo_type, bot2_cards, skips_in_row)
        if cards_played:
            print(f"Player 3 has played {[c[0] for c in cards_played]}")
            print(f"Player 2 has played {[c[1] [2] for c in cards_played]}")
            print(f"Player 3 has {len(bot2_cards)} left")
    return current_combo_type, player_cards, bot1_cards, bot2_cards, turn_count, skips_in_row

        # add bot play ***
    #add automatic bots
    #can't incorporate open ai idk why

def bot_play_landlord(turn_count, current_combo_type, bot_cards):
    ranks = Counter([c[2][1] for c in bot_cards])
    chosen_cards = []
    if any(count >= 4 for count in ranks.values()):
        bomb_rank = next(r for r, count in ranks.items() if count >= 4)
        chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
    elif any(count >= 2 for count in ranks.values()):
        pair_rank = next(r for r, count in ranks.items() if count >= 2)
        chosen_cards = [c for c in bot_cards if c[2][1] == pair_rank][:2]
    else:
        chosen_cards = [random.choice(bot_cards)]
    for c in chosen_cards:
        bot_cards.remove(c)
    current_combo_type = check_combination(chosen_cards)
    turn_count += 1
    return current_combo_type, turn_count, chosen_cards

def skip_turn(turn_count, current_combo_type, skips_in_row, total_players=3):
    skip_sure = input("Skip? Yes or No? ").strip().lower()
    if skip_sure == "yes":
        skips_in_row += 1
        print("You skipped your turn.")
        if skips_in_row >= total_players - 1:
            current_combo_type = None
            skips_in_row = 0
            print("Round finished. Resetting combo type.")
    else:
        skips_in_row = 0

    #modulo here
    turn_count = (turn_count + 1) % total_players
    return turn_count, current_combo_type, skips_in_row


def play_combination(turn_count, current_combo_type, player_cards, all_cards_played):
    choice = input("*Enter card numbers separated by spaces*\n")
    indicies = choice.split()
    for i in range(len(indicies)):
        indicies[i] = int(indicies[i][1:])

    cards_played = [player_cards[i] for i in indicies]
    combo_type = check_combination(cards_played)
    if turn_count == 0 or combo_type == current_combo_type:
        print("You have played:", cards_played)
        for c in cards_played:
            player_cards.remove(c)
        turn_count += 1
        print(all_cards_played)
        all_cards_played.append(cards_played)
    else:
        print("Invalid combination, try again.")
        return play_combination(turn_count, current_combo_type, player_cards)
    return current_combo_type, turn_count, all_cards_played

# les hope it works gng

def bot_play_combination(turn_count, current_combo_type, bot_cards, skips_in_row):
    ranks = Counter([c[2][1] for c in bot_cards])
    chosen_cards = []
    
    #No current combo type or new round, play anything
    if current_combo_type == 0 or current_combo_type == "Pass":
        if any(count >= 4 for count in ranks.values()):
            bomb_rank = next(r for r, count in ranks.items() if count >= 4)
            chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
        elif any(count >= 2 for count in ranks.values()):
            pair_rank = next(r for r, count in ranks.items() if count >= 2)
            chosen_cards = [c for c in bot_cards if c[2][1] == pair_rank][:2]
        else:
            chosen_cards = [random.choice(bot_cards)]
    else:
        # Match current combo
        if current_combo_type == "Solo":
            sorted_cards = sorted(bot_cards, key=lambda x: x[2][1])
            chosen_cards = [sorted_cards[-1]]
            
        elif current_combo_type == "Pair":
            # Find highest 
            pair_ranks = [r for r, count in ranks.items() if count >= 2]
            if pair_ranks:
                pair_rank = max(pair_ranks)
                chosen_cards = [c for c in bot_cards if c[2][1] == pair_rank][:2]
            else:
                #bomb???
                bomb_ranks = [r for r, count in ranks.items() if count >= 4]
                if bomb_ranks:
                    bomb_rank = max(bomb_ranks)
                    chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
                else:
                    chosen_cards = []
                    
        elif current_combo_type == "Trio with single card":
            trio_ranks = [r for r, count in ranks.items() if count >= 3]
            if trio_ranks:
                trio_rank = max(trio_ranks)
                trio_cards = [c for c in bot_cards if c[2][1] == trio_rank][:3]
                remaining = [c for c in bot_cards if c not in trio_cards]
                if remaining:
                    kicker = [random.choice(remaining)]
                    chosen_cards = trio_cards + kicker
                else:
                    chosen_cards = trio_cards
            else:
                # bomb
                bomb_ranks = [r for r, count in ranks.items() if count >= 4]
                if bomb_ranks:
                    bomb_rank = max(bomb_ranks)
                    chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
                else:
                    chosen_cards = []
                    
        elif current_combo_type == "Trio with pair":
            trio_ranks = [r for r, count in ranks.items() if count >= 3]
            if trio_ranks:
                trio_rank = max(trio_ranks)
                trio_cards = [c for c in bot_cards if c[2][1] == trio_rank][:3]
                remaining = [c for c in bot_cards if c not in trio_cards]
                remaining_ranks = Counter([c[2][1] for c in remaining])
                pair_ranks = [r for r, count in remaining_ranks.items() if count >= 2]
                if pair_ranks:
                    pair_rank = max(pair_ranks)
                    pair_cards = [c for c in remaining if c[2][1] == pair_rank][:2]
                    chosen_cards = trio_cards + pair_cards
                else:
                    chosen_cards = trio_cards
            else:
                bomb_ranks = [r for r, count in ranks.items() if count >= 4]
                if bomb_ranks:
                    bomb_rank = max(bomb_ranks)
                    chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
                else:
                    chosen_cards = []
                    
        elif current_combo_type == "Bomb":
            # Find highest bomb
            bomb_ranks = [r for r, count in ranks.items() if count >= 4]
            if bomb_ranks:
                bomb_rank = max(bomb_ranks)
                chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
            else:
                has_bj = any(c[2][1] == 16 for c in bot_cards)
                has_rj = any(c[2][1] == 17 for c in bot_cards)
                if has_bj and has_rj:
                    chosen_cards = [c for c in bot_cards if c[2][1] in [16, 17]]
                else:
                    chosen_cards = []
                
        elif current_combo_type == "Solo chain":
            bomb_ranks = [r for r, count in ranks.items() if count >= 4]
            if bomb_ranks:
                bomb_rank = max(bomb_ranks)
                chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
            else:
                has_bj = any(c[2][1] == 16 for c in bot_cards)
                has_rj = any(c[2][1] == 17 for c in bot_cards)
                if has_bj and has_rj:
                    chosen_cards = [c for c in bot_cards if c[2][1] in [16, 17]]
                else:
                    chosen_cards = []
                    
        elif current_combo_type == "Pairs chain":
            bomb_ranks = [r for r, count in ranks.items() if count >= 4]
            if bomb_ranks:
                bomb_rank = max(bomb_ranks)
                chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
            else:
                has_bj = any(c[2][1] == 16 for c in bot_cards)
                has_rj = any(c[2][1] == 17 for c in bot_cards)
                if has_bj and has_rj:
                    chosen_cards = [c for c in bot_cards if c[2][1] in [16, 17]]
                else:
                    chosen_cards = []
                    
        elif current_combo_type == "Rocket":
            # Rocket is highest, nothing is higher.
            chosen_cards = []
            
        else:
            # For other, prob bomb or pass
            bomb_ranks = [r for r, count in ranks.items() if count >= 4]
            if bomb_ranks:
                bomb_rank = max(bomb_ranks)
                chosen_cards = [c for c in bot_cards if c[2][1] == bomb_rank][:4]
            else:
                chosen_cards = []
    
    # Remove chosen cards
    if chosen_cards:
        for c in chosen_cards:
            bot_cards.remove(c)
        current_combo_type = check_combination(chosen_cards)
        print(f"Bot played: {[c[0] for c in chosen_cards]}")
        print(f"Bot has {len(bot_cards)} cards left")
    else:
        # Bot skipp
        turn_count, current_combo_type, skips_in_row = skip_turn(turn_count, current_combo_type, skips_in_row)
    
    turn_count += 1
    return current_combo_type, turn_count, chosen_cards, skips_in_row


def check_larger_combo(turn_count, all_cards_played, cards_played):
    #last played combination
    last_played = all_cards_played[turn_count - 1]
    # Compare each card's rank for same combo type
    if len(cards_played) == len(last_played):
        # Compare  highest rank in each combination
        last_max = max([c[2][1] for c in last_played])
        current_max = max([c[2][1] for c in cards_played])
        
        if current_max > last_max:
            return True
        else:
            return False
    else:
        if len(cards_played) == 4 and check_combination(cards_played) == "Bomb":
            return True
        elif len(last_played) == 4 and check_combination(last_played) == "Bomb":
            return False
        else:
            return False
    #add later

#---- start of game ---
starting = intro()

if starting:
    print("You are Player 1!!!")
    player_cards, bot1_cards, bot2_cards, landlord_choice = landlord_cards()
    player_identity = check_landlord_is_player(landlord_choice)
    sorted_hand = show_cards_left(player_cards)
    current_combo_type, player_cards, bot1_cards, bot2_cards, turn_count, skips_in_row = landlord_play(
        player_identity, player_cards, bot1_cards, bot2_cards, turn_count, current_combo_type, skips_in_row
    )
    # add laterr