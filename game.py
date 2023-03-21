import random
from enum import Enum
cardArr = ['A','2','3','4','5','6','7','8','9','10','J','Q','K',
'A','2','3','4','5','6','7','8','9','10','J','Q','K',
'A','2','3','4','5','6','7','8','9','10','J','Q','K',
'A','2','3','4','5','6','7','8','9','10','J','Q','K']
#moves = Enum('Begin','Hitting','Standing','Splitting','DoublingDown')
class Hand(object):
	"""docstring for Hand"""
	def __init__(self, cards, lastMove):
		self.cards = cards
		self.lastMove = lastMove

class BlackJackGame:
	def __init__(self, numPlayers, numDecks):
		self.numPlayers = numPlayers
		self.numDecks = numDecks
		self.shoe = []
		self.currShoeIdx = 0
		self.playIdx = 0 # 0 means player 1, when playIdx is numPlayers it means the dealerr
		# because he plays the last
		self.playerVsHands = {}
		for x in range(numDecks):
			self.shoe.extend(cardArr)
		random.shuffle(self.shoe)
		# assign the dealer who is index 0, and the players starting from index 1
		# upto index `numPlayers` any 2 cards
		for x in range(numPlayers+1): 
			if x not in self.playerVsHands:
				self.playerVsHands[x] = []
			cards = []
			cards.append(self.shoe[self.currShoeIdx])
			self.currShoeIdx+=1
			cards.append(self.shoe[self.currShoeIdx])
			self.currShoeIdx+=1
			self.playerVsHands[x].append(Hand(cards,'Begin'))

	def getNumberOfCardsLeftInShoe(self):
		return len(self.shoe)-self.currShoeIdx+1
	def getDealerTopCard(self):
		dealerHand = self.playerVsHands[0]
		# dealer will have only 1 hand (he cannot split)
		cardArr =  dealerHand[0].cards
		return cardArr[-1]
	def getCurrentTurn(self):
		return playIdx
	def getLegalMoves(self):
		if playIdx == numPlayers: # curringently the leader is play
			hands = playerVsHands[playIdx]
		else: #  currently  one of the players is playing 

game = BlackJackGame(4,2)
print(game.playerVsHands)
print(game.getNumberOfCardsLeftInShoe())
print(game.getDealerTopCard())


		