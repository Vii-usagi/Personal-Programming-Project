## Personal Programming Project - Vicky
import random 
starting = True
turn_count = 0
# these are the card decks blah blah
all_cards = ['🂱 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂼 🂽 🂾 🂡 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂬 🂭 🂮 🃁 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃌 🃍 🃎 🃑 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃜 🃝 🃞 🃏︎ 🃟'.split()]
all_card_names = ['h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 hJ hQ hK s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 sJ sQ sK d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 dJ dQ dK c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 cJ cQ cK Black_Joker Red_Joker'.split()]
all_hearts =    ['🂱 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂼 🂽 🂾'.split(), 'h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 hJ hQ hK'.split()]
all_spades =    ['🂡 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂬 🂭 🂮'.split(), 's1 s2 s3 s4 s5 s6 s7 s8 s9 s10 sJ sQ sK'.split()]
all_diamonds =  ['🃁 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃌 🃍 🃎'.split(), 'd1 d2 d3 d4 d5 d6 d7 d8 d9 d10 dJ dQ dK'.split()]
all_clovers =   ['🃑 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃜 🃝 🃞'.split(), 'c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 cJ cQ cK'.split()]
all_jokers =    ['🃏︎ 🃟'.split(), 'Black_Joker Red_Joker'.split()]

# prints out the rulessss
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
Four with two pairs: four of the same card and two pairs
''')
    
    start_game = int(input("Type 1 to [Continue] \n "))
    if start_game == 1:
        starting == True
    else:
        print("Guess I'll see you next time!")
        starting == False

    return starting

# the landlord card that the landlord recievesss
def landlord_cards():


    landlord_card = random.choice(list(zip(all_cards,all_card_names)))
    print("Bot: The flipped card is:", landlord_card)
    print("Bot: I will shuffle the cards now...")
    print("Bot: These are the cards the landlord will receive: 🂠 🂠 🂠 ")
    print("*They are currently unknown*")

    # each player's card deck
    player_cards = []
    bot1_cards = []
    bot2_cards = []

    # randomly giving each player their cards and card names, each gets 17
    player_cards.append(random.shuffle(list(zip(all_cards,all_card_names))[:16]))
    bot1_cards.append(random.shuffle(list(zip(all_cards,all_card_names))[:16]))
    bot2_cards.append(random.shuffle(list(zip(all_cards,all_card_names))[:16]))

    #show the actual player's cards
    show_cards_left(player_cards)

    #seeing who is the landlord
    if landlord_card in player_cards:
        landlord_choice = 1
    elif landlord_card in bot1_cards:
        landlord_choice = 2
    else:
        landlord_choice = 3

    #asking if the player wants to be the landlord
    if landlord_choice == 1:
        landlord = int(input("Bot: Player {} is the landlord! Player {} Do you want to be the landlord? Click 1 if yes. ".format(landlord_choice)))

        #if player says 1 then player is the landlord
        if landlord == 1:
            print("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))
        #if player doesn't wanna be the landlord the bot randomly chooses someone
        else:
            print("Repicking...")
            landlord_choice = random.randint(1,3)
            print("New landlord is Player {}".format(landlord_choice))
    # if the landlord is one of the bots it randomly chooses
    elif landlord_choice == 2 or landlord_choice == 3:
        print(("Bot: Player {} is the landlord! Player {} Do you want to be the landlord? Click 1 if yes. ".format(landlord_choice)))
        yes_or_no = random.randint(1,2)
        if yes_or_no != 1:
            print("Repicking...")
            landlord_choice = random.randint(1,3)
            print("New landlord is Player {}".format(landlord_choice))
        else:
            print("Player {} is the Landlord! The rest of the players are civilians!".format(landlord_choice))

    #showing the landlord cards
    print("Bot: These are the landlord cards!")
    landlordcards = random.choice(zip(all_cards,all_card_names)[:2])
    print(landlordcards)

    #appending the landlord cards into whoever the landlord is
    if landlord_choice == 1:
        landlordcards.append(player_cards)
    elif landlord_choice == 2:
        landlordcards.append(bot1_cards)
    else:
        landlordcards.append(bot2_cards)

    return player_cards, bot1_cards, bot2_cards, landlord_choice

# this is for the first round only where it checks if the landlord is the player or not
def check_landlord_is_player(landlord_choice):
    if landlord_choice == 1:
        player_identity = 1
    else:
        player_identity = 2
    return player_identity

#used very frequently because I don't think the player is bothered to scroll up to see their cards
def show_cards_left(player_cards):
    print("Bot: These are Player 1's cards! " , player_cards[0])
    print("*You currently have: {} *".format(player_cards[0]))
    print("*You currently have: {} cards*".format(len(list(player_cards[0]))))

def check_combination(placeholder):
    placeholder

#only for the first round/start of the game where a specific person starts the game
def landlord_play(player_identity, player_cards, bot1_cards, bot2_cards):
    if player_identity == 1:
        show_cards_left()
        
def play_combination(turn_count, player_cards, bot1_cards, bot2_cards):
    if turn_count == 0:
        current_combo = input("*Please play a combination*\n")

    else:
        current_combo = input("Please play cards that follow the {} combination".format())




#---- start of game ---
starting = intro()

while starting == True:
    print("You are Player 1!!!")
    landlord_cards()

        
    