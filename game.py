import random
import math
from enum import Enum
cardArr = ['A','2','3','4','5','6','7','8','9','10','J','Q','K',
'A','2','3','4','5','6','7','8','9','10','J','Q','K',
'A','2','3','4','5','6','7','8','9','10','J','Q','K',
'A','2','3','4','5','6','7','8','9','10','J','Q','K']
#moves = Enum('Begin','Hit','Stand')
# Initialise the game object with the number of games you want to play
#class Hand(object):


class BlackJackGame:
	def startRound(self):
		self.playerVsHands = {}
		for x in range(self.numPlayers+1): 
			if x not in self.playerVsHands:
				self.playerVsHands[x] = []
			cards = []
			if x == 0: # this loop is to assign card to the dealer
				self.currDealerHiddenCard = self.currShoeIdx
			cards.append(self.shoe[self.currShoeIdx])
			self.currShoeIdx+=1
			cards.append(self.shoe[self.currShoeIdx])
			self.currShoeIdx+=1
			self.playerVsHands[x].extend(cards)
	def getSumOfCards(self,cards):
		sum1=0
		sum2=0
		for card in cards:
			if card == 'A':
				sum1+=1
				sum1+=11
			elif card == 'J' or card == 'Q' or card == 'K':
				sum1+=10
				sum2+=10
			else:
				sum1+=int(card)
				sum2+=int(card)
		return (sum1,sum2)

	def __init__(self, numPlayers, numGameRounds):
		self.numPlayers = numPlayers
		self.numDecks = math.ceil(numGameRounds * 5 * float(numPlayers+1) / numGameRounds)
		self.shoe = []
		self.currShoeIdx = 0
		self.playIdx = 0 
		self.currDealerHiddenCard = None
		# 0 means player 1, when playIdx is numPlayers it means the dealerr
		# because he plays the last
		self.playerVsHands = None
		for x in range(self.numDecks):
			self.shoe.extend(cardArr)
		self.startRound()


	def getNumberOfCardsLeftInShoe(self):
		return len(self.shoe)-self.currShoeIdx+1
	def getDealerTopCard(self):
		dealerHand = self.playerVsHands[0]
		# dealer will have only 1 hand (he cannot split)
		cardArr =  dealerHand[0]
		return cardArr[-1]
	def getCurrentTurn(self):
		return playIdx
	def getLegalMoves(self):
		# 0 idx is the dealer, 1 .. numPlayers are the players
		nextPlayIdx = self.playIdx
		if nextPlayIdx == (self.numPlayers+1): # curringently the leader is play
			nextPlayIdx = 0
		cards = self.playerVsHands[nextPlayIdx]
		cardSumTuple = self.getSumOfCards(cards)
		if cardSumTuple[0]<17 and cardSumTuple[1]<17:
			return ['Hit']
		elif cardSumTuple[0]>=17 and cardSumTuple[1]>=17:
			return ['Stand']
		else: #  currently  one of the players is playing 
			return ['Hit','Stand']


game = BlackJackGame(4,2)
print(game.playerVsHands)
print(game.getNumberOfCardsLeftInShoe())
print(game.getDealerTopCard())
print(game.getLegalMoves())

		