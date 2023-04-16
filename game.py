import random
import math
import copy
from enum import Enum

cardArr = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
           'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
           'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
           'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


# moves = Enum('Begin','Hit','Stand')
# Initialise the game object with the number of games you want to play
# class Hand(object):


class BlackJackGame:

    def __init__(self, numPlayers, numGameRounds):
        self.numPlayers = numPlayers
        self.numDecks = math.ceil(numGameRounds * 5 * float(numPlayers + 1) / 52)
        #print("numDecks",self.numDecks)
        self.shoe = []
        self.currShoeIdx = 0
        self.playIdx = 1
        self.currDealerHiddenCard = None
        self.currentGameRound = 1
        self.numGameRounds = numGameRounds
        self.gamePlayingHistory = {}
        self.winsVsLosses = [0,0]
        # 0 means player 1, when playIdx is numPlayers it means the dealerr
        # because he plays the last
        self.playerVsHands = None
        for x in range(self.numDecks):
            self.shoe.extend(cardArr)
        random.shuffle(self.shoe)
        self.startRound()

    def playGame(self):
        print("Initial game state:")

        while self.currentGameRound <= self.numGameRounds:
            print(self.playerVsHands, '\n')
            move = self.getMove(game)
            self.makeMove(move)

    def getCard(self):
        card = self.shoe[self.currShoeIdx]
        self.currShoeIdx += 1
        return card

    def startRound(self):
        self.playerVsHands = {}
        for x in range(self.numPlayers + 1):
            if x not in self.playerVsHands:
                self.playerVsHands[x] = []
            cards = []
            if x == 0:  # this loop is to assign card to the dealer
                self.currDealerHiddenCard = self.currShoeIdx
            cards.append(self.getCard())
            cards.append(self.getCard())
            self.playerVsHands[x].extend(cards)

    def getSumOfCards(self, cards):
        sum1 = 0
        sum2 = 0
        for card in cards:
            if card == 'A':
                sum1 += 1
                sum2 += 11
            elif card == 'J' or card == 'Q' or card == 'K':
                sum1 += 10
                sum2 += 10
            else:
                sum1 += int(card)
                sum2 += int(card)
        return sum1, sum2

    def getNumberOfCardsLeftInShoe(self):
        return len(self.shoe) - self.currShoeIdx + 1

    def getDealerVisibleCards(self):
        dealerHand = self.playerVsHands[0]
        return dealerHand[1:]

    def getDealerTopCard(self):
        dealerHand = self.playerVsHands[0]
        return dealerHand[-1]

    def getCurrentTurn(self):
        return self.playIdx

    def getLegalMoves(self):
        # 0 idx is the dealer, 1 .. numPlayers are the players
        nextPlayIdx = self.playIdx
        if nextPlayIdx == (self.numPlayers + 1):  # curringently the leader is play
            nextPlayIdx = 0
        cards = self.playerVsHands[nextPlayIdx]
        cardSumTuple = self.getSumOfCards(cards)
        if cardSumTuple[0] < 17 and cardSumTuple[1] < 17:
            return ['Hit']
        elif cardSumTuple[0] >= 17 and cardSumTuple[1] >= 17:
            return ['Stand']
        else:  # currently  one of the players is playing
            return ['Hit', 'Stand']

    def getOptimalSum(self, cardSumTuple):
        cardOptimalSum = 0
        if cardSumTuple[0] > 21 and cardSumTuple[1] > 21:
            return min(cardSumTuple)
        elif cardSumTuple[0] > cardSumTuple[1]:
            if cardSumTuple[0] <= 21:
                cardOptimalSum = cardSumTuple[0]
            else:
                cardOptimalSum = cardSumTuple[1]
        elif cardSumTuple[0] <= cardSumTuple[1]:
            if cardSumTuple[1] <= 21:
                cardOptimalSum = cardSumTuple[1]
            else:
                cardOptimalSum = cardSumTuple[0]
        return cardOptimalSum

    def findGameWinners(self):

        dealerCardSum = self.getSumOfCards(self.playerVsHands[0])
        dealerCardSum = self.getOptimalSum(dealerCardSum)
        ans = []
        for i in range(1, self.numPlayers + 1):
            playerCardSum = self.getSumOfCards(self.playerVsHands[i])
            playerCardSum = self.getOptimalSum(playerCardSum)
            if playerCardSum > 21 and dealerCardSum>21:
                ans.append('Tied')
            elif playerCardSum > dealerCardSum:
                if playerCardSum <= 21:
                    ans.append('Win')
                    self.winsVsLosses[0]=self.winsVsLosses[0]+1
                else:
                    ans.append('Lost')
                    self.winsVsLosses[1]=self.winsVsLosses[1]+1

            elif playerCardSum < dealerCardSum:
                if dealerCardSum <= 21:
                    ans.append('Lost')
                    self.winsVsLosses[1]=self.winsVsLosses[1]+1
                else:
                    ans.append('Win')
                    self.winsVsLosses[0]=self.winsVsLosses[0]+1
            else:
                ans.append('Tied')
            print("Player ", i, ans[i - 1], playerCardSum, "vs", dealerCardSum)
        print(self.playerVsHands, '\n')
        return ans

    def getGamePlayingHistory(self):
        return self.gamePlayingHistory

    def makeMove(self, move):
        if self.playIdx == 0:
            agentCards = self.playerVsHands[0]
            agentCardsSum = self.getSumOfCards(agentCards)
            while agentCardsSum[0] < 17 and agentCardsSum[1] < 17:
                card = self.getCard()
                self.playerVsHands[0].append(card)
                agentCardsSum = self.getSumOfCards(self.playerVsHands[0])
            self.gamePlayingHistory[self.currentGameRound] = self.findGameWinners()

            self.startRound()
            self.currentGameRound += 1
            self.playIdx = 1
            print("************************ This round is over ************************")
            if self.currentGameRound > self.numGameRounds:
                print("Win percentage is",100.*self.winsVsLosses[0]/(self.winsVsLosses[0]+self.winsVsLosses[1]))
                print("************************     GAME OVER      ************************")

        # if the player is moving 'Stand', do nothing and if he hits just add the card,
        # whether he loses or wins is implicit after the dealer makes the move
        elif move == 'Hit':
            self.playerVsHands[self.playIdx].append(self.getCard())

        # after the current player has played, increment hthe player idx
        else:
            self.playIdx = self.playIdx + 1
            if self.playIdx == (self.numPlayers + 1):
                self.playIdx = 0

    def generateSuccessor(self, card):
        state = BlackJackGame(self.numPlayers, self.numGameRounds)
        state.playerVsHands[state.playIdx].append(card)
        return state

    def generateDealerSuccessor(self, card):
        state = BlackJackGame(self.numPlayers, self.numGameRounds)
        state.playerVsHands[0] = copy.copy(self.playerVsHands[0])
        state.playerVsHands[0].append(card)
        #state.currShoeIdx = self.currShoeIdx
        return state

    def getMove(self, gameState):
        print("The current player is ", self.playIdx)
        print("My current hand is", gameState.playerVsHands[gameState.playIdx])
        action = self.expectimax(gameState)
        print("Chose move", action,"\n")
        return action

    def expectimax(self, gameState):
        currAvailableCards = self.shoe[self.currShoeIdx:]
        availableCardFreqMap = {}
        for card in currAvailableCards:
        	if card in availableCardFreqMap:
        		availableCardFreqMap[card]=availableCardFreqMap[card]+1
        	else:
        		availableCardFreqMap[card]=1

        hit = math.floor(self.expValue(gameState,availableCardFreqMap))
        stand = self.getOptimalSum(self.getSumOfCards(gameState.playerVsHands[gameState.playIdx]))
 
        #print(availableCardFreqMap)
        #print(len(currAvailableCards))

        dealer = math.floor(self.dealerExpValue(gameState, 0,availableCardFreqMap))
        print("Hit:", hit, "stand:", stand, "dealer:", dealer)
        value = self.getOptimalSum((hit, stand))
        if value == hit :
            print("HIT: Hit has better expected value than Stand")
            return "Hit"
        elif stand < dealer and stand < 17:
            print("HIT: Stand is better than Hit, but Dealer's expected value is better than my Stand.")
            return "Hit"
        else:
            print("STAND: Stand is better than Hit and Dealer")
            return "Stand"

    def expValue(self, gameState,availableCardFreqMap):
        expectedValue = 0
        #cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        totalSum=0
        for cardKey in availableCardFreqMap:
            totalSum+=availableCardFreqMap[cardKey]
        for card in availableCardFreqMap:
            successorGameState = gameState.generateSuccessor(card)
            probability = 1.*availableCardFreqMap[card]/totalSum
            nextValue = self.evaluationFunction(successorGameState)
            # expectimax calculation
            expectedValue += probability * nextValue
        return expectedValue + min(gameState.getSumOfCards(gameState.playerVsHands[gameState.playIdx]))

    def dealerExpValue(self, gameState, depth,availableCardFreqMap):
        dealerCardSum = self.getSumOfCards(gameState.getDealerVisibleCards())
        dealerCardSum = self.getOptimalSum(dealerCardSum)
        if dealerCardSum > 21:
        	return -1
        if dealerCardSum >= 17:
            return dealerCardSum
        #cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        expectedValue = 0
        totalSum=0
        for cardKey in availableCardFreqMap:
        	totalSum+=availableCardFreqMap[cardKey]

        for cardKey in availableCardFreqMap:
        	newAvailableCardFreqMap = copy.copy(availableCardFreqMap)
        	newAvailableCardFreqMap[cardKey]=newAvailableCardFreqMap[cardKey]-1
        	if newAvailableCardFreqMap[cardKey] == 0:
        		newAvailableCardFreqMap.pop(cardKey)

        	successorGameState = gameState.generateDealerSuccessor(cardKey)
        	prob = 1.0*availableCardFreqMap[cardKey]/totalSum
        	expectedValue += self.dealerExpValue(successorGameState, depth+1,newAvailableCardFreqMap) * prob

        return expectedValue

    def evaluationFunction(self, gameState):
        sum = max(gameState.getSumOfCards(gameState.playerVsHands[gameState.playIdx]))
        if sum > 21:
            return 0
        return sum


numPlayers = 4
numGames = 2
game = BlackJackGame(numPlayers, numGames)
game.playGame()

