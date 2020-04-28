import random
import time
from decimal import Decimal
import sys


class Money:
    def __init__(self, bank, bet):
        self._bank = bank
        self._bet = bet

    # Getter/setter for player bank
    @property
    def bank(self):
        return round(Decimal(self._bank), 2)

    @bank.setter
    def bank(self, amount):
        self._bank = amount

    # Getter/setter for bet
    @property
    def bet(self):
        return round(Decimal(self._bet), 2)

    @bet.setter
    def bet(self, amount):
        self._bet = amount

m = Money(100, 0)


class Prob_mode:
    def __init__(self, value):
        self._value = value

    # Getter/setter for probability mode
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, boolean):
        self._value = boolean

p = Prob_mode(False)


class Cards:
    def __init__(self, dealer_total, player_total):
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self._dealer_total = dealer_total
        self._player_total = player_total

    # Getter/setter for dealer_total
    @property
    def dealer_total(self):
        return self._dealer_total

    @dealer_total.setter
    def dealer_total(self, amount):
        self._dealer_total = amount

    # Getter/setter for player_total
    @property
    def player_total(self):
        return self._player_total

    @player_total.setter
    def player_total(self, amount):
        self._player_total = amount
    
c = Cards(0, 0)  


#### Card handling functions ####
def draw_card():
    popped_card = c.deck.pop(random.randint(0, len(c.deck) - 1))
    return popped_card

def initial_deal():
    for _ in range(0, 2):
        c.player_hand.append(draw_card())
    c.dealer_hand.append(draw_card()) # Face up card
    hand_value(c.dealer_hand, 'dealer')
    hand_value(c.player_hand, 'player')

def cardify_full_hand(hand):
    cardified_hand = []
    for i in range(0, (len(hand))):
        card = f"|{hand[i]}|"
        cardified_hand.append(card)
    return ' '.join(cardified_hand)

def cardify_dealer_initial():
    card1 = f"|{c.dealer_hand[0]}|"
    card2 = "|≈|"
    cardified_hand = [card1, card2]
    return ' '.join(cardified_hand)

def hand_value(hand, who=None):
    sum_of_hand = 0
    ace_count = hand.count('A')
    face_count = hand.count('K') + hand.count('Q') + hand.count('J')
    for card in hand:
        if (isinstance(card, int)):
            sum_of_hand += card
    sum_of_hand += 10 * face_count
    if (ace_count > 0):
        if (sum_of_hand >= 11):
            sum_of_hand += ace_count
        else:
            sum_of_hand += (11 + ace_count - 1)
    if who == "dealer":
        c.dealer_total = sum_of_hand
    elif who == "player":
        c.player_total = sum_of_hand
    else:
        return sum_of_hand


#### Display functions ####
def line():
    sleepy_print('-----------------------------------------------')

def sleepy_print(string):
    time.sleep(.5)
    print(string)
    time.sleep(.5)

def error_msg():
    sleepy_print("\n\t!*** Invalid choice, try again ***!\n")
    
def update_total():
    sleepy_print(f"\nNow you have ${m.bank}\n")
    # Bankrupcy test
    if (m.bank < 5):
        input("\n\tYou don't have enough money. Hit ENTER to restart game\n")
        m.bank = 100
        menu()
    else:
        player_choice = input('ENTER for new game or "M" to go back to menu\n').upper()
        if (player_choice == ""):
            start_game()
        elif (player_choice == 'M'):
            time.sleep(.5)
            menu()
        else:
            error_msg()
            update_total()
    
def display_hands_before_flip():
    line()
    dealer_display = f"\nDealer hand = {cardify_dealer_initial()}"
    player_display = f"\nPlayer hand = {cardify_full_hand(c.player_hand)}"
    if p.value:
        dealer_display += f" --------probability--> {blackjack_prob_msg(hand_value([c.dealer_hand[0]]))}"
        player_display += f" --------probability--> {blackjack_prob_msg(c.player_total)}   {bust_prob_msg(c.player_total)}"
    print(dealer_display + '\n')
    print(f"     * The bet is ${m.bet} *")
    print(player_display + '\n')
    line()

def display_hands_after_flip():
    line()
    print("\nDealer's draw...")
    c.dealer_hand.append(draw_card()) # Hidden card
    time.sleep(.5)
    print(f"\nDealer hand = {cardify_full_hand(c.dealer_hand)}")
    print(f"Total = {c.dealer_total}\n")
    print(f"Player hand = {cardify_full_hand(c.player_hand)}")
    print(f"Total = {c.player_total}\n")


#### Probability functions ####
def deck_list_to_nums():
    deck_of_all_nums = []
    for card in c.deck:
        if ((card == 'K') | (card == 'Q') | (card == 'J')):
            deck_of_all_nums.append(10)
        elif (card == 'A'):
            deck_of_all_nums.append(1)
        else:
            deck_of_all_nums.append(card)
    return deck_of_all_nums

def bust_prob_msg(hand_total):
    danger_card_count = 0
    if hand_total >= 12:
        for i in deck_list_to_nums():
            if ((hand_total + i) > 21):
                danger_card_count += 1
    percent = Decimal(danger_card_count/len(c.deck)) * 100
    return f"Bust = %{round(percent, 2)}"

def blackjack_prob_msg(hand_total):
    a_count = c.deck.count('A')
    bj_card_count = 0
    if (hand_total == 10):
        bj_card_count = a_count
    elif (hand_total >= 11):
        for i in deck_list_to_nums():
            if ((hand_total + i) == 21):
                bj_card_count += 1
    percent = Decimal(bj_card_count/len(c.deck)) * 100
    return f"Blackjack = %{round(percent, 2)}"


#### Outcomes ####
def player_win():
    if (c.player_total == 21):
        blackjack()
    else:
        if (c.dealer_total > 21):
            print("\t\t Dealer BUSTED...\n")
        m.bank += m.bet * 2
        sleepy_print("                  ++You win!++\n")  
        
def blackjack():
    time.sleep(.5)
    print("                $ $ $ $ $ $ $ $")
    time.sleep(.05)
    print("              $ $  BLACKJACK  $ $")
    time.sleep(.05)
    print("                $ $   1.5x  $ $")
    time.sleep(.05)
    print("                  $   Win!  $")
    time.sleep(.05)
    print("                     $ $ $")
    time.sleep(.05)
    print("                      $ $")
    time.sleep(.05)
    print("                       $")    
    m.bank += (m.bet * Decimal(2.5))
    
def dealer_win():
    sleepy_print("                  --Dealer won--\n")
   
def tie(both_bust=False):
    if both_bust:
        print(("\t   You and the dealer both BUSTED...\n"))
    elif (c.player_total == 21):
        print(("\t You and the dealer both got Blackjack...\n"))
    sleepy_print("                   ~~It's a tie~~\n")
    m.bank += m.bet
    

#### Main gameplay and run functions ####
def ask_for_bet():
    print(f"\nMax bet = ${m.bank}")
    add_bet = input("Hit ENTER to bet the minimum ($5.00) or input higher amount: $")
    if (add_bet == ""):
        m.bank = m.bank - 5
        m.bet = 5
        return
    try:  
        add_bet = round(Decimal(add_bet), 2)
        if (add_bet > m.bank):
            sleepy_print("\n\t!*** You don't have enough money to afford that bet! Try again ***!")
            ask_for_bet()
        elif (add_bet < 5):
            sleepy_print("\n\t!*** Bet is too low. Must meet the minimum ***!")
            ask_for_bet()
        else:
            m.bet += add_bet
            m.bank -= add_bet
    except:
        error_msg()
        ask_for_bet()

def player_hit_stand():
    # If blackjack
    if (c.player_total == 21):
        input("You have 21! Hit ENTER to see what the dealer has...")
        return
    player_choice = input('Do you want to hit ("H") or stand ("S")?\nEnter response: ').upper()
    if (player_choice == 'H'):
        c.player_hand.append(draw_card())
        hand_value(c.player_hand, 'player')
        # If bust
        if (c.player_total > 21):
            display_hands_before_flip()
            input("You BUSTED! Hit ENTER to see what the dealer has...")
            return
        # If still in the game (player total < 21 )    
        else:
            time.sleep(.5)
            display_hands_before_flip()
            player_hit_stand()
    elif (player_choice == 'S'):
        return
    else:
        error_msg()
        player_hit_stand()

def dealer_hit_stand():
    # Dealer hits until 17 or higher is reached
    while (c.dealer_total < 17):
        c.dealer_hand.append(draw_card())
        hand_value(c.dealer_hand, 'dealer')
    
def who_wins():
    difference = c.player_total - c.dealer_total
    # Bust outcomes
    if ((c.player_total > 21) | (c.dealer_total > 21)):
        if ((c.player_total > 21) & (c.dealer_total > 21)):
            tie(both_bust = True)
        elif (c.player_total > 21):
            dealer_win()
        else:
            player_win()
    # All other outcomes
    elif (difference == 0):
        tie()
    elif (difference > 0):
        player_win()
    else:
        dealer_win()

def menu():
    # Probability toggle
    if p.value:
        prob_indicator = 'on'
    else:
        prob_indicator = 'off'
    
    # Options menu
    time.sleep(.05)
    print(f'\n\n\t  Input "P" to toggle probability mode (currently: {prob_indicator})')
    print('\t  Input "X" to exit the game')
    print('\n\t\t--Hit ENTER to deal a new hand--')
    input_var = input().upper()
    if input_var == "":
        start_game()
    elif input_var == 'P':
        time.sleep(.5)
        p.value = not p.value
        menu()
    elif input_var == 'X':
        sleepy_print('\nExiting...\n')
        sys.exit()
    else:    
        error_msg()
        menu()

def start_game():
    # Empty hands, zero bet, and new deck at the start of each hand
    c.dealer_hand = []
    c.player_hand = []
    m.bet = 0
    c.deck = []
    c.deck.extend((2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7,
                    7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A'))
    
    # Main gameplay sequence
    sleepy_print('\n\n****************** New Hand ******************')
    
    # Play action
    ask_for_bet()
    initial_deal()
    display_hands_before_flip()
    player_hit_stand()
    dealer_hit_stand()
    display_hands_after_flip() 
    
    # Ouctomes
    who_wins()
    update_total()

menu()

