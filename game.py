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
	def getCard(self):
		card = self.shoe[self.currShoeIdx]
		self.currShoeIdx+=1
		return card

	def startRound(self):
		self.playerVsHands = {}
		for x in range(self.numPlayers+1): 
			if x not in self.playerVsHands:
				self.playerVsHands[x] = []
			cards = []
			if x == 0: # this loop is to assign card to the dealer
				self.currDealerHiddenCard = self.currShoeIdx
			cards.append(self.getCard())
			cards.append(self.getCard())
			self.playerVsHands[x].extend(cards)
	def getSumOfCards(self,cards):
		sum1=0
		sum2=0
		for card in cards:
			if card == 'A':
				sum1+=1
				sum2+=11
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
		self.playIdx = 1
		self.currDealerHiddenCard = None
		self.currentGameRound = 1
		self.numGameRounds = numGameRounds
		self.gamePlayingHistory = {}
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

	def getOptimalSum(self,cardSumTuple):
		cardOptimalSum = 0
		if cardSumTuple[0]>cardSumTuple[1] :
			if cardSumTuple[0]<=21:
				cardOptimalSum = cardSumTuple[0]
			else:
				cardOptimalSum = cardSumTuple[1]
		elif cardSumTuple[0]<=cardSumTuple[1] :
			if cardSumTuple[1]<=21:
				cardOptimalSum = cardSumTuple[1]
			else:
				cardOptimalSum = cardSumTuple[0]
		return cardOptimalSum

	def findGameWinners(self):

		dealerCardSum = self.getSumOfCards(self.playerVsHands[0])
		print("**",dealerCardSum)
		dealerCardSum = self.getOptimalSum(dealerCardSum)
		ans = []
		for i in range(1,self.numPlayers+1):
			playerCardSum = self.getSumOfCards(self.playerVsHands[i])
			playerCardSum = self.getOptimalSum(playerCardSum)
			if playerCardSum > dealerCardSum:
				if playerCardSum <= 21:
					ans.append('Win')
				else:
					ans.append('Lost')

			elif playerCardSum < dealerCardSum:
				if dealerCardSum <= 21:
					ans.append('Lost')
				else:
					ans.append('Win')
			else:
				ans.append('Tied')
			print("Player ",i,ans[i-1], playerCardSum,"vs",dealerCardSum)
		return ans
	def getGamePlayingHistory(self):
		return self.gamePlayingHistory
	def makeMove(self,move):
		print("The current player playing is ",self.playIdx)
		if self.playIdx == 0:
			agentCards = self.playerVsHands[0]
			agentCardsSum = self.getSumOfCards(agentCards)
			while agentCardsSum[0]<17 and agentCardsSum[1]<17:
				card = self.getCard()
				self.playerVsHands[0].append(card)
				agentCardsSum = self.getSumOfCards(self.playerVsHands[0])
			self.gamePlayingHistory[self.currentGameRound]=self.findGameWinners()
			print(game.playerVsHands,'\n')
			self.startRound()
			self.currentGameRound+=1
			if self.currentGameRound > self.numGameRounds:
				print("Game ends !")


		# if the player is moving 'Stand', do nothing and if he hits just add the card,
		# whether he loses or wins is implicit after the dealer makes the move
		elif move=='Hit':
			self.playerVsHands[self.playIdx].append(self.getCard())




		# after the current player has played, increment hthe player idx
		self.playIdx=self.playIdx+1
		if self.playIdx == (self.numPlayers+1):
			self.playIdx = 0




game = BlackJackGame(4,2)
print(game.playerVsHands)
print(game.getNumberOfCardsLeftInShoe())
print(game.getDealerTopCard())
print(game.getLegalMoves())

game.makeMove('Hit')
print(game.playerVsHands,'\n')
game.makeMove('Hit')
print(game.playerVsHands,'\n')
game.makeMove('Hit')
print(game.playerVsHands,'\n')
game.makeMove('Hit')
print(game.playerVsHands,'\n')
game.makeMove('Hit')
print(game.playerVsHands,'\n')
game.makeMove('Hit')

#print(game.playerVsHands,'\n')

print(game.getGamePlayingHistory())

		