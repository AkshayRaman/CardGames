#About the game:
#https://en.wikipedia.org/wiki/Sevens_%28card_game%29

from random import shuffle
import sys

suits = ["hearts", "spades", "diamonds", "clubs"]
num_cards = 13

class Card:
	def __init__(self, suit, number):
		self.suit = suit
		self.number = number
	
	def __str__(self):
		if self.number == 1:
			return "%s %s" %("Ace", self.suit.title())
		if self.number <= 10:
			return "%s %s" %(self.number, self.suit.title())
		else:
			return "%s %s" %(["Jack","Queen","King"][self.number-11], self.suit.title())
			
	def __eq__(self, x):
		return (self.suit == x.suit and self.number == x.number)
		
class Deck:
	def __init__(self):
		num = range(1, num_cards + 1)
		
		self.cards = []
		
		for i in num:
			for suit in suits:
				self.cards.append(Card(suit,i))
		
	def shuffle(self):
		shuffle(self.cards)
		
	def __str__(self):
		return ", ".join([str(i) for i in self.cards])
		
	def deal(self, n):
		x = [[] for i in range(n)]
		tot = len(suits) * num_cards
		for i in range(tot):
			x[i%n].append(self.cards[i])
		return x

class Game:
	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.player_count = 4
		self.player_hands = self.deck.deal(self.player_count)
		
		self.played_cards = {}
		for i in suits:
			self.played_cards[i] = []
	
	def __str__(self):
		op = ""
		for player,hand in enumerate(self.player_hands):
			op += "Player %s --> " %(player)
			op += ', '.join([card.__str__() for card in hand])
			op += '\n'
		return op
		
	def get_starter(self):
		starter = Card("hearts", 7)
		for player,hand in enumerate(self.player_hands):
			if starter in hand:
				return player
					
	def display_played_cards(self):
		op = ""
		for suit in self.played_cards:
			if len(self.played_cards[suit])==2:
				min, max = self.played_cards[suit][0:2]
				op += "%s - %s; " %(Card(suit, min), Card(suit, max))
		print "Played cards: %s" %op
	
	def play_card(self, player, card):
		suit = card.suit
		num = card.number
		if not self.played_cards[suit] and num==7:
			print "Player %s played %s." %(player, card)
			self.played_cards[suit].extend([7,7])
			if card in self.player_hands[player]:
				self.player_hands[player].remove(card)
			return card
			
		else:
			if not self.played_cards[suit]:
				return None
			if self.played_cards[suit][0] == num+1:
				self.played_cards[suit][0] = num
				print "Player %s played %s." %(player, card)
				if card in self.player_hands[player]:
					self.player_hands[player].remove(card)
				return card
			elif self.played_cards[suit][1] == num-1:
				self.played_cards[suit][1] = num
				print "Player %s played %s." %(player, card)
				if card in self.player_hands[player]:
					self.player_hands[player].remove(card)
				return card
			else:
				return None
		

if __name__ == "__main__":
	g = Game()
	print g
	cur_player = g.get_starter()
	g.play_card(cur_player,Card("hearts", 7))
	cur_player += 1
	cur_player %= (g.player_count)

	while True:
		print g
		for card in g.player_hands[cur_player]:
			if g.play_card(cur_player, card):
				#g.display_played_cards()
				if len(g.player_hands[cur_player]) == 0:
					print g
					print "Player %s wins!!" %(cur_player)
				
					for player, hand in enumerate(g.player_hands):
						score = sum([i.number for i in hand])
						print "Player: %s -> Score: %s" %(player, score)
					sys.exit(0)
				
				cur_player += 1
				cur_player %= (g.player_count)
				break
				
		print "%s said pass." %(cur_player)
		cur_player += 1
		cur_player %= (g.player_count)