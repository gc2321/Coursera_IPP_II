# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = ""; outcome = ""; score = 0; deck=[]
player_hand=[]; dealer_hand=[]; player_value=[]; dealer_value=[]; player_score=0; dealer_score=0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
    def draw2(self, canvas, pos):
        canvas.draw_image(card_back, [36, 48], CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
         
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        s = "" 
        for i in self.hand:
            s += str(i)+" "
        return s    

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        self.value = [0,0]; self.ace = 0
        for i in self.hand:
            self.value[0] += VALUES[i[1]]
            if i[1] == "A":
                self.ace = 1
        if self.ace == 0:
            self.value[1] = self.value[0]
        else:
            self.value[1] = self.value[0]+10        
        return self.value
    
    def draw(self, canvas, hide, loc):
        global in_play
        j = 0
        for i in self.hand:
            card = Card(i[0],i[1])
            if hide == "yes" and in_play == "player" and j==0:
                card.draw2(canvas, [(30+j), loc])
            else:
                card.draw(canvas, [(30+j), loc])
            j += 30         
     
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append([i,j])

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return(self.deck.pop())
    
    def __str__(self):
        s = "" 
        for i in self.deck:
            s += str(i[0])+str(i[1])+" "
        return s     


#define event handlers for buttons
def deal():
    global outcome, in_play, score, deck, player_hand, dealer_hand, player_value, dealer_value, player_score 
    outcome = ""; deck=[]
    
    if in_play == "":
        # initiate new game
        player_hand=Hand(); dealer_hand=Hand(); player_value=[]; dealer_vale=[] 
        player_score=0; dealer_score=0; deck = Deck(); deck.shuffle()

        player_hand.add_card(deck.deal_card()); dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card()); dealer_hand.add_card(deck.deal_card())
        in_play = "player" 

        player_value=player_hand.get_value()
        compute()
    else:
        outcome = "You loss. New deal?"; score -=1; in_play =""
    
def compute():
    # generate hands and scores
    global outcome, score, in_play, player_value, dealer_value, player_score, dealer_score
    
    if in_play == "player":
        if player_value[0]>21 and player_value[1]>21:
            outcome = "You bust. Press Deal to start new game."
            score -= 1; in_play = ""              
        elif player_value[0]==player_value[1]:
            outcome = "You have "+str(player_value[0])+". Hit or stand?"
        elif player_value[1]<=21: 
            outcome = "You have "+str(player_value[0])+" or "+str(player_value[1])+". Hit or stand?"
        else: 
            outcome = "You have "+str(player_value[0])+". Hit or stand?"
   
    elif in_play == "final":
        if dealer_score>21:
            outcome += " Dealer busts. You won! New game?"
            score +=1
        else:
            outcome += " Dealer has "+str(dealer_score)+"."
            if player_score>dealer_score:
                outcome += " You won! New deal?"; score +=1
            else:    
                outcome += " Dealer won. Try again?"; score -=1
        in_play =""
                
def comment():
    global outcome
    return outcome

def cal(cards):
    # calculate the max value of cards
    if cards[0]>21 and cards[1]>21:
        return 22
    else:
        if max(cards)<=21:
            return max(cards)
        else:
            return min(cards)

def hit():
    global in_play, deck, player_hand, player_value	
    if in_play == "player":
        player_hand.add_card(deck.deal_card())
        player_value=player_hand.get_value()
        compute()        
    
def stand():
    global in_play, outcome, dealer_hand, dealer_value, dealer_score, player_hand, player_value, player_score 	 
    in_play = "dealer"
   
    if in_play == "dealer":
        # player_score
        player_score = cal(player_value)
        
        if player_score<=21:
            outcome = "You have "+str(player_score)+"."
        
        # computer dealer_score
        dealer_value=dealer_hand.get_value()
        dealer_score = cal(dealer_value)
        
        if dealer_score>=17:
            in_play = "final"
        else:
            while dealer_score<17:
                dealer_hand.add_card(deck.deal_card())
                dealer_value=dealer_hand.get_value()
                dealer_score = cal(dealer_value)
                #compute()                
            in_play = "final"
        
        compute()
            
# draw handler    
def draw(canvas):
    global score
    
    canvas.draw_text("Blackjack", [160, 80], 30, "Aqua", "sans-serif")
    canvas.draw_text("Score "+str(score), [380, 80], 30, "Black", "sans-serif")
    
    canvas.draw_text("Dealer", [30, 160], 20, "Black", "sans-serif")
    canvas.draw_text("Player", [30, 360], 20, "Black", "sans-serif")
    
    dealer_hand.draw(canvas, "yes", 200)
    player_hand.draw(canvas, "no", 400)
    
    canvas.draw_text(comment(), [130, 360], 20, "Black", "sans-serif")
    
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
