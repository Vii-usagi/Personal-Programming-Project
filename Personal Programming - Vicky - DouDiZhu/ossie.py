import random
import time

PLAYER_NUM = 4
CARD_POINT_NUM = 15
CARDS_PER_PLAYER = 25
BOTTOM_CARDS = 8
DECK_SIZE = 108

TYPE_SINGLE = 1
TYPE_PAIR = 2
TYPE_TRIPLE = 3
TYPE_TRIPLE_ONE = 4
TYPE_TRIPLE_TWO = 5
TYPE_BOMB = 6

point_names = ["3","4","5","6","7","8","9","10","J","Q","K","A","2","SJ","BJ"]

class Play:
    def __init__(self, type=0, main_val=0, sub_val1=0, sub_val2=0, count=0):
        self.type = type
        self.main_val = main_val
        self.sub_val1 = sub_val1
        self.sub_val2 = sub_val2
        self.count = count

hand = [[0 for _ in range(CARD_POINT_NUM)] for _ in range(PLAYER_NUM)]
landlord = -1
cur_player = 0
last_play = Play()
last_player = -1
pass_count = 0
def init_deck():
    deck = []
    for p in range(13):
        for _ in range(8):
            deck.append(p)
    for _ in range(2):
        deck.append(13)
        deck.append(14)
    return deck

def shuffle(deck):
    random.shuffle(deck)

def deal_cards(deck):
    global hand
    idx = 0
    for _ in range(CARDS_PER_PLAYER):
        for player in range(PLAYER_NUM):
            hand[player][deck[idx]] += 1
            idx += 1

def show_hand(player):
    for p in range(CARD_POINT_NUM):
        if hand[player][p] > 0:
            for _ in range(hand[player][p]):
                print(point_names[p], end=" ")
    print()

def show_bottom_cards(cards):
    for c in cards:
        print(point_names[c], end=" ")
    print()
def is_legal_play(player, points, n):
    if n == 0:
        return None

    counts = [0] * CARD_POINT_NUM
    for p in points:
        if p < 0 or p >= CARD_POINT_NUM:
            return None
        counts[p] += 1

    kinds = 0
    main_p, sub_p = -1, -1
    three_count, two_count, one_count = 0, 0, 0

    for p in range(CARD_POINT_NUM):
        if counts[p] > 0:
            kinds += 1
            if counts[p] == 4:
                main_p = p
                three_count += 1
            elif counts[p] == 3:
                main_p = p
                three_count += 1
            elif counts[p] == 2:
                sub_p = p
                two_count += 1
            elif counts[p] == 1:
                one_count += 1

    result = Play()

    if n == 4 and kinds == 1 and counts[main_p] == 4:
        result.type, result.main_val, result.count = TYPE_BOMB, main_p, 4
        return result
    if n == 1 and kinds == 1:
        result.type, result.main_val, result.count = TYPE_SINGLE, points[0], 1
        return result
    if n == 2 and kinds == 1 and counts[points[0]] == 2:
        result.type, result.main_val, result.count = TYPE_PAIR, points[0], 2
        return result
    if n == 3 and kinds == 1 and counts[points[0]] == 3:
        result.type, result.main_val, result.count = TYPE_TRIPLE, points[0], 3
        return result
    if n == 4 and kinds == 2 and three_count == 1 and one_count == 1:
        result.type, result.main_val, result.sub_val1, result.count = TYPE_TRIPLE_ONE, main_p, sub_p, 4
        return result
    if n == 5 and kinds == 2 and three_count == 1 and two_count == 1:
        result.type, result.main_val, result.sub_val1, result.count = TYPE_TRIPLE_TWO, main_p, sub_p, 5
        return result

    return None


def greater_than(new_play, old_play):
    if old_play.type == 0:
        return True
    if new_play.type == TYPE_BOMB and old_play.type != TYPE_BOMB:
        return True
    if old_play.type == TYPE_BOMB and new_play.type != TYPE_BOMB:
        return False
    if new_play.type == old_play.type:
        return new_play.main_val > old_play.main_val
    return False


def remove_cards(player, points, n):
    for p in points:
        if hand[player][p] <= 0:
            print("You don't have this card.")
            return False
        hand[player][p] -= 1
    return True


def add_cards(player, points, n):
    for p in points:
        hand[player][p] += 1
def ai_play(player):
    global last_play, last_player, pass_count

    print(f"\nAI {player} Thinking...")

    if last_player == player or last_play.type == 0:
        for p in range(CARD_POINT_NUM):
            if hand[player][p] > 0:
                remove_cards(player, [p], 1)
                last_play = Play(TYPE_SINGLE, p, 0, 0, 1)
                last_player = player
                pass_count = 0
                print(f"AI {player} Play: {point_names[p]}")
                return
        return

    prev_player = last_player
    is_teammate = False
    if prev_player != -1 and prev_player != player:
        if landlord == 0:
            if prev_player != 0:
                is_teammate = True
        else:
            if prev_player != landlord:
                is_teammate = True

    if is_teammate:
        print(f"AI {player} Pass")
        pass_count += 1
        return

    new_play = None
    found = False

    if last_play.type == TYPE_SINGLE:
        for p in range(last_play.main_val + 1, CARD_POINT_NUM):
            if hand[player][p] >= 1:
                remove_cards(player, [p], 1)
                new_play = Play(TYPE_SINGLE, p, 0, 0, 1)
                found = True
                break

    if found:
        last_play = new_play
        last_player = player
        pass_count = 0
        print(f"AI {player} Play: {point_names[new_play.main_val]}")
    else:
        print(f"AI {player} Pass")
        pass_count += 1


def player_play(player):
    global last_play, last_player, pass_count

    print("\nYour cards: ")
    show_hand(player)


    if last_play.type != 0 and last_player != player:
        print("Cards from last turn: ", end="")
        if last_play.type == TYPE_SINGLE:
            print(point_names[last_play.main_val])
        elif last_play.type == TYPE_PAIR:
            print(point_names[last_play.main_val], point_names[last_play.main_val])
        elif last_play.type == TYPE_TRIPLE:
            print(" ".join([point_names[last_play.main_val]] * 3))
        elif last_play.type == TYPE_TRIPLE_ONE:
            print(" ".join([point_names[last_play.main_val]] * 3), point_names[last_play.sub_val1])
        elif last_play.type == TYPE_TRIPLE_TWO:
            print(" ".join([point_names[last_play.main_val]] * 3), 
                  point_names[last_play.sub_val1], point_names[last_play.sub_val1])
        elif last_play.type == TYPE_BOMB:
            print("Bomb", point_names[last_play.main_val])

    while True:
        user_input = input("Please play (Enter card names separated by spaces, e.g. 3 3 3 4, or 'pass'): ").strip()

        if user_input.lower() == "pass":
            if last_player == player or last_play.type == 0:
                print("You cannot pass now – you must play something.")
                continue
            pass_count += 1
            print("You passed.")
            return

        tokens = user_input.split()
        points = []
        valid_tokens = True
        for token in tokens:
            if token in point_names:
                points.append(point_names.index(token))
            else:
                print(f"Invalid card: {token}")
                valid_tokens = False
                break
        if not valid_tokens:
            continue

        temp_hand = hand[player][:] 
        for p in points:
            if temp_hand[p] <= 0:
                print(f"You don't have enough {point_names[p]}.")
                valid_tokens = False
                break
            temp_hand[p] -= 1
        if not valid_tokens:
            continue

        new_play = is_legal_play(player, points, len(points))
        if new_play is None:
            print("Invalid combination. Try again.")
            continue

        if not greater_than(new_play, last_play):
            print("Your play is not strong enough to beat the last one.")
            continue


        for p in points:
            hand[player][p] -= 1


        last_play = new_play
        last_player = player
        pass_count = 0

        print("You played: ", end="")
        if new_play.type == TYPE_SINGLE:
            print(point_names[new_play.main_val])
        elif new_play.type == TYPE_PAIR:
            print(point_names[new_play.main_val], point_names[new_play.main_val])
        elif new_play.type == TYPE_TRIPLE:
            print(" ".join([point_names[new_play.main_val]] * 3))
        elif new_play.type == TYPE_TRIPLE_ONE:
            print(" ".join([point_names[new_play.main_val]] * 3), point_names[new_play.sub_val1])
        elif new_play.type == TYPE_TRIPLE_TWO:
            print(" ".join([point_names[new_play.main_val]] * 3), 
                  point_names[new_play.sub_val1], point_names[new_play.sub_val1])
        elif new_play.type == TYPE_BOMB:
            print("Bomb", point_names[new_play.main_val])

        return
    
def next_player(p):
    return (p + 1) % PLAYER_NUM

def game_over():
    for i in range(PLAYER_NUM):
        if sum(hand[i]) == 0:
            return True
    return False

def reset_round():
    global last_play, last_player, pass_count
    last_play = Play()
    last_player = -1
    pass_count = 0

def main():
    global landlord, cur_player, last_play, last_player, pass_count, hand

    random.seed(time.time())
    print("=== Chinese Poker :D ===")

    while True:
        deck = init_deck()
        shuffle(deck)
        deal_cards(deck)

        print("\n--- Who is the landlord? ---")
        landlord = -1
        for i in range(PLAYER_NUM):
            if i == 0:
                print("Your cards: ", end="")
                show_hand(0)
                choice = int(input("Would you like to be the landlord?(1:Yes, 0:No): "))
                if choice == 1:
                    landlord = i
                    break
            else:
                if random.randint(0, 9) < 3:
                    print(f"AI {i} Be landlord")
                    landlord = i
                    break
                else:
                    print(f"AI {i} Skip")

        if landlord == -1:
            print("No one called, reshuffling...")
            hand = [[0 for _ in range(CARD_POINT_NUM)] for _ in range(PLAYER_NUM)]
            continue

        print("The landlord is:", "You" if landlord == 0 else "AI")

        bottom = deck[-BOTTOM_CARDS:]
        print("Bottom cards: ", end="")
        show_bottom_cards(bottom)
        add_cards(landlord, bottom, BOTTOM_CARDS)

        cur_player = landlord
        last_play = Play()
        last_player = -1
        pass_count = 0

        print("\n--- Game starts now ---")
        while not game_over():
            if cur_player == 0:
                player_play(0)
            else:
                ai_play(cur_player)
            cur_player = next_player(cur_player)

        winner = -1
        for i in range(PLAYER_NUM):
            if sum(hand[i]) == 0:
                winner = i

        if winner == landlord:
            print("Landlord wins!")
        else:
            print("Peasants win!")

        again = int(input("Would you like to try again?(1:Yes, 0:No): "))
        if not again:
            break
        hand = [[0 for _ in range(CARD_POINT_NUM)] for _ in range(PLAYER_NUM)]

if __name__ == "__main__":
    main()