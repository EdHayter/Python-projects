'''
Play blackjack against a dealer! 
Written by Ed Hayter 09/05/20
Play using session()
'''
import numpy as np
import time

#calculate total of blackjack hand. Aces worth most possible while total remains <21
def blackjack_hand_points(hand):
    hand_val = []
    ace_counter = 0
    #Replace str in list with ints. Counts number of aces
    for card in hand:
        hand_val.append(10 if card=='K' or card=='J' or card=='Q' else 11 if card=='A' else int(card))
        ace_counter +=1 if card=='A' else 0
    hand_val = sum(hand_val)
    #If aces present and total over 21, convert aces to be worth 1
    for i in range(ace_counter):
        hand_val -= 10 if hand_val > 21 else 0
  #  if hand_val > 21:
   #     hand_val=0
    return hand_val   

#draw card at random (this does not account for cards already in play!)
def draw():
    t = np.random.randint(1,14)
    return 'A' if t==1 else 'J' if t==11 else 'Q' if t==12 else 'K' if t==13 else str(t)

#function for 1 game
def play_blackjack(bet):
    dealers_hand = [draw()]
    players_hand = [draw(),draw()]
    print('Dealer draws: ', dealers_hand)
    print('You draw: ', players_hand)
    if blackjack_hand_points(players_hand) == 21:
        print('Blackjack! congratz.')
        return bet
    decision = input('Care to stick (s) or draw (d)?\n')
    while not (decision == 's' or decision == 'd'):
        decision = input('Not valid option. Try again...\n')
        #ask player to stick or draw, append to list if draw & abort if bust
    while decision == 'd':
        players_hand.append(draw())
        print('You draw: ', players_hand)
        if blackjack_hand_points(players_hand)>21:
            print('Bust! You lose.\n')
            return -bet
        else:
            decision = input('Care to stick (s) or draw (d)?\n')
            while not (decision == 's' or decision == 'd'):
                decision = input('Not valid option. Try again...\n')
                
    print('Your final hand: ', players_hand)            
    print('Dealers hand: ', dealers_hand)
    #Dealers turn. Adds delay to add suspense! 
    time.sleep(1)
    while blackjack_hand_points(dealers_hand) < 17 and \
        blackjack_hand_points(dealers_hand) < blackjack_hand_points(players_hand):
        dealers_hand.append(draw()) 
        print('Dealer draws: ', dealers_hand)
        time.sleep(1)
    #possible outcomes, return bet if win, lose bet if lose.
    if blackjack_hand_points(dealers_hand)>21:
        print('Dealer goes bust, you win!')
        return bet
    elif blackjack_hand_points(dealers_hand)<blackjack_hand_points(players_hand):
        print('Dealer sticks, you win!')
        return bet
    elif blackjack_hand_points(dealers_hand)==blackjack_hand_points(players_hand):
        print('Draw. Bet returned.')
        return 0
    else:
        print('Dealer sticks, you lose!')
        return -bet
    
#Initialise blackjack session. allow player to bet money starting wiht £100.
def session():
    total = 100 
    highest_total = 100
    print('You start with £100. Win and you double your bet.\n')
    while total > 0:
        #validate bet is a number between 0 and total
        try:
            bet = float(input('How much would you like to bet?\n'))
            bet=round(bet,2) 
            if not (bet>0 and bet<=total):
                print('Not a valid bet. Bet between 0 and your total!\n')
                continue
        except ValueError:
            print("Not a number! Try again.")
            continue
        #update total
        total += play_blackjack(bet)
        highest_total = max(total,highest_total)
        print('Your total is now: £', total,sep='') 
    time.sleep(2)
    print('Thanks for playing, you lost £100. :)')
    time.sleep(2)
    print('You could have walked away with £',highest_total,'!',sep='')

    
        
    
    
        
        
        
            
            