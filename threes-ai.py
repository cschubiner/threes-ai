# import numpy as np
import random, math, sys, os

def parseBoard(str):
  nums = str.strip().split()
  if len(nums) != 16:
    raise Exception('Board must consist of 16 numbers')
  for i in range(16):
    try:
      nums[i] = int(nums[i])
    except Exception:
      raise Exception('Board must consist of 16 numbers')
  index = 0
  board = [list(),list(),list(),list()]
  pos = 0
  while index < 16:
    for num in nums:
      pos = pos % 4
      board[index//4].append(num)
      index += 1
  return board

def copyArray(arr):
  return [i for i in arr]

def canMerge(p1, p2):
  t1 = min(p1, p2)
  if t1 == 0: return True
  t2 = max(p1, p2)
  if p1==p2 and p1 != 1 and p2 != 2: return True
  if t1 == 1 and t2 == 2: return True
  return False

def mirrorHoriz(board):
  nb = [[],[],[],[]]
  for row in range(4):
    nb[row].append(board[row][3])
    nb[row].append(board[row][2])
    nb[row].append(board[row][1])
    nb[row].append(board[row][0])
  return nb

def leftSwipe(board):
  res = rightSwipe(mirrorHoriz(board))
  return res[0], mirrorHoriz(res[1])


def rightSwipe(board):
  nb = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
  for rowNum, row in enumerate(board):
    for wall in range(3, 0, -1):
      if canMerge(row[wall], row[wall-1]):
        for i in range(wall):
          nb[rowNum][i+1] = row[i]
        nb[rowNum][wall] = row[wall] + row[wall-1]

        for i in range(wall+1, 4):
          nb[rowNum][i] = row[i]
        break

  # nothing happened, copy the row
  for rowNum in range(4):
    rowAllZeroes = True
    for col in range(4):
      if nb[rowNum][col] != 0:
        rowAllZeroes = False
        break
    if rowAllZeroes:
      for col in range(4):
        nb[rowNum][col] = board[rowNum][col]
  # check if change occurred
  changeList = list()
  for row in range(len(board)):
    for col in range(len(board[0])):
      if board[row][col] != nb[row][col]:
        changeList.append(row)
        break
  return changeList, nb

def rotateRight(board):
  return zip(*board[::-1])

def rotateLeft(board):
  return zip(*board)[::-1]

def upSwipe(board):
  rs = rightSwipe(rotateRight(board))
  return rs[0], rotateLeft(rs[1])

def downSwipe(board):
  rs = rightSwipe(rotateLeft(board))
  mod = list()
  for num in rs[0]:
    if num == 0: mod.append(3)
    if num == 1: mod.append(2)
    if num == 2: mod.append(1)
    if num == 3: mod.append(0)
  return mod, rotateRight(rs[1])

def printBoard(board):
  for i in range(4): print board[i]

def copyBoard(board):
  nb = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
  for i in range(4):
    for j in range(4):
      nb[i][j] = board[i][j]
  return nb

def getBestMove(board, next):
  bestMove = 'Game Over'
  bestBoard = board
  bestScore = 0
  bestChanges = list()
  changes, b = rightSwipe(board)
  avScore = 0
  for change in changes:
    nb = copyBoard(b)
    nb[change][0] = next
    avScore += heuristicScore(nb)
  avScore /= float(max(len(changes), 1))
  if avScore > bestScore:
    bestScore = avScore
    bestMove = 'Right Swipe'
    bestBoard = b
    bestChanges = changes
  # if verbose: print 'R score =', avScore, newHScore(b, True), '\n'
  # if verbose: printBoard(b)
  changes, b = leftSwipe(board)
  avScore = 0
  for change in changes:
    nb = copyBoard(b)
    nb[change][3] = next
    avScore += heuristicScore(nb)
  avScore /= float(max(len(changes), 1))
  if avScore > bestScore:
    bestScore = avScore
    bestMove = 'Left Swipe'
    bestBoard = b
    bestChanges = changes
  # if verbose: print 'L score =', avScore, newHScore(b, True), '\n'
  # if verbose: printBoard(b)
  changes, b = upSwipe(board)
  avScore = 0
  for change in changes:
    nb = copyBoard(b)
    nb[3][change] = next
    avScore += heuristicScore(nb)
  avScore /= float(max(len(changes), 1))
  if avScore > bestScore:
    bestScore = avScore
    bestMove = 'Up Swipe'
    bestBoard = b
    bestChanges = changes
  # if verbose: print 'U score =', avScore, newHScore(b, True), '\n'
  # if verbose: printBoard(b)
  changes, b = downSwipe(board)
  avScore = 0
  for change in changes:
    nb = copyBoard(b)
    nb[3][0] = next
    avScore += heuristicScore(nb)
  avScore /= float(max(len(changes), 1))
  if avScore > bestScore:
    bestScore = avScore
    bestMove = 'Down Swipe'
    bestBoard = b
    bestChanges = changes
  # if verbose: print 'D score =', avScore, newHScore(b, True), '\n'
  # if verbose: printBoard(b)
  for i in range(4):
    bestBoard[i] = list(bestBoard[i])
  # print bestChanges
  return bestMove, bestBoard, bestChanges


def pieceValue(piece):
  if piece < 3: return 0
  if piece == 3: return 3
  return 3 * pieceValue(piece // 2)

origDeck = list([1,1,1,1,2,2,2,2,3,3,3,3])
deck = list()
def getPredictedPiece():
  if human:
    return int(input('Enter in the value of the next piece: '))
  global deck
  if len(deck) == 0:
    deck = copyArray(origDeck)
  indchosen = random.randint(0, len(deck) -1 )
  card = deck[indchosen]
  del deck[indchosen]
  return card


def getActualNextPiece(predictedPiece):
  if human and predictedPiece >= 3:
    return int(input('Enter in the value of the new piece: '))
  return predictedPiece

def getNextPos(changes):
  if len(changes) == 1:
    return changes[0]
  if human:
    return int(input('Enter in the row or column of the new piece (A number between 0 and 3): '))
  return changes[random.randint(0, len(changes)-1)]

def getMove(board, next):
  bestMove, newboard, bestChanges = getBestMove(board, next)
  if bestMove != 'Game Over':
    if verbose: print 'Perform', bestMove
  elif verbose: print '\n'
  if human:
    while True:
      move = raw_input('Enter in your move (r, l, u, d): ')
      print move
      if move == 'r': bestChanges, newboard = rightSwipe(board)
      elif move == 'l': bestChanges, newboard = leftSwipe(board)
      elif move == 'u': bestChanges, newboard = upSwipe(board)
      elif move == 'd': bestChanges, newboard = downSwipe(board)
      elif move == '':
        move = bestMove
        break
      else: continue
      break
    for i in range(4):
      newboard[i] = list(newboard[i])
    bestMove = move
  return bestMove, newboard, bestChanges

def start(board):
  while (True):
    next = getPredictedPiece()
    if verbose: printBoard(board)
    bestMove, board, bestChanges = getMove(board, next)
    if bestMove == 'Game Over':
      if verbose: print 'Game over'
      return scoreBoard(board)
    actualNext = getActualNextPiece(next)
    nextPos = getNextPos(bestChanges)
    # if verbose: print 'changed pos:', nextPos
    if bestMove == 'Left Swipe' or bestMove == 'l':
       board[nextPos][3] = actualNext
    elif bestMove == 'Right Swipe' or bestMove == 'r':
       board[nextPos][0] = actualNext
    elif bestMove == 'Down Swipe' or bestMove == 'd':
       board[0][nextPos] = actualNext
    elif bestMove == 'Up Swipe' or bestMove == 'u':
       board[3][nextPos] = actualNext
    if verbose: printBoard(board)
    if verbose: print 'Actual score:', scoreBoard(board), 'Heuristic score:', heuristicScore(board), '\n'

def canMergeNotZero(p1, p2):
  return canMerge(p1,p2) and p1 > 0 and p2 > 0

# def scoreWithChangeList(board)
def newHScore(board, printShit = False):
  if printShit: print

#   +4 points for each empty square
#   +4 points for each pair of adjacent cards that can be merged
#   -1 point for each card which is between two higher cards vertically or horizontally (-2 points if both)
  zeroes = 0
  adjacents = 0
  checkerboards = 0

  for row in board:
    for num in row:
      if num == 0: zeroes += 1

  for i in range(4):
    for j in range(3):
      if canMergeNotZero(board[i][j], board[i][j+1]): adjacents += 1
  for i in range(3):
    for j in range(4):
      if canMergeNotZero(board[i][j], board[i+1][j]): adjacents += 1

  for i in range(4):
    for j in range(2):
      if board[i][j] > board[i][j+1] and board[i][j+1] < board[i][j+2] and board[i][j+1] > 0:
        # print i,j+1, 'piece =', board[i][j+1]
        checkerboards += 1

  for i in range(2):
    for j in range(4):
      if board[i][j] > board[i+1][j] and board[i+1][j] < board[i+2][j] and board[i+1][j] > 0:
        # print i+1, j, 'piece =', board[i+1][j]
        checkerboards += 1

  rss = len(rightSwipe(board)[0])
  lss = len(leftSwipe(board)[0])
  uss = len(upSwipe(board)[0])
  dss = len(downSwipe(board)[0])
  swipeDirs = 0
  if rss > 0: swipeDirs += 1
  if lss > 0: swipeDirs += 1
  if uss > 0: swipeDirs += 1
  if dss > 0: swipeDirs += 1
  options = rss + lss + uss + dss
  # options = 0
  if swipeDirs == 0: swipeDirs = -1000
  else: swipeDirs = 0

  # printShit = True
  if printShit:
    printBoard(board)
    print zeroes, adjacents, checkerboards, options
  return zeroes * weights[1] + adjacents * weights[2] - checkerboards * weights[3] + options * .1 * weights[4] + swipeDirs


def hScoreWithFuture(board):
  hscore = newHScore(board)
  global useFuture
  nextScore = 0
  scoreAfter = 0
  if useFuture and weights[5] >= 3:
    useFuture = False
    nb = getBestMove(board, random.randint(1,3))[1]
    nextScore = newHScore(nb)
    if weights[5] == 8 and True:
      nb = getBestMove(nb, random.randint(1,3))[1]
      scoreAfter = newHScore(nb)
    useFuture = True

  return hscore + weights[0]/5.0 * nextScore + .2 * scoreAfter

def heuristicScore(board):
  return hScoreWithFuture(board)
  return newHScore(board)
  global useFuture

  score = 0
  zeroes = 0
  for row in board:
    for num in row:
      if num == 0: zeroes += 1
  swipeDirs = 0
  rss = len(rightSwipe(board)[0])
  lss = len(leftSwipe(board)[0])
  uss = len(upSwipe(board)[0])
  dss = len(downSwipe(board)[0])
  if rss > 0: swipeDirs += 1
  if lss > 0: swipeDirs += 1
  if uss > 0: swipeDirs += 1
  if dss > 0: swipeDirs += 1
  options = rss + lss + uss + dss
  adjacents = 0
  for i in range(4):
    for j in range(3):
      if canMerge(board[i][j], board[i][j+1]): adjacents += 1
  for i in range(3):
    for j in range(4):
      if canMerge(board[i][j], board[i+1][j]): adjacents += 1
  for i in range(4):
    for j in range(2):
      if canMerge(board[i][j], board[i][j+1]) and canMerge(board[i][j+1], board[i][j+2]): adjacents += 1
  for i in range(2):
    for j in range(4):
      if canMerge(board[i][j], board[i+1][j]) and canMerge(board[i+1][j], board[i+2][j]): adjacents += 1


  nextScore = 0
  if useFuture:
    useFuture = False
    nextScore = heuristicScore(getBestMove(board, random.randint(1,3))[1])/50.0
    useFuture = True

  adjacents *= weights[0]
  zeroes *= weights[1]
  swipeDirs *= weights[2]
  options *= weights[3]
  oldScore = scoreBoard(board)/30 * weights[4]
  nextScore *= weights[5]
  score += adjacents + zeroes + swipeDirs + options + oldScore + nextScore
  # print
  # printBoard(board)
  # print score, adjacents, zeroes, swipeDirs, options
  # print score, newHScore(board)
  return score + newHScore(board) * 28.571428571

def scoreBoard(board):
  score = 0
  for row in board:
    for num in row:
      score += pieceValue(num)
  return score


def testAlgorithm(iters):
  res = 0
  hs = 0
  for i in range(iters):
    score = start(parseBoard('0 2 0 1 3 0 0 3 0 0 0 1 1 3 2 2'))
    res += score
    if score > hs:
      hs = score
  # print 'Highscore: ',hs
  return res/float(iters)
useFuture = True
# human = False

human = raw_input('Do you want to play or have the AI play? (Say "human" or "ai"): ') == 'human'
verbose = False or human

if human:
  # weights = [3, 4, 4, 1, 2, 8]
  weights = [7, 7, 6, 1, 4, 8]
  start(parseBoard(raw_input('Enter in the board (Enter in 16 numbers on one line): ')))
elif True:
  verbose = raw_input('Do you want to watch? (Say "yes" or "no"): ') == 'yes'
  # weights = [7, 7, 6, 1, 4, 6]
  weights = [3, 4, 4, 1, 2, 8]
  print 'Game complete. Scored:', testAlgorithm(1)
  sys.exit()

else:
  numWeights = 6
  bestScore = 0
  iters = 10
  scoreList = list()
  scoreMap = dict()
  while(True):
    weights = [random.randint(0,8) for i in range(numWeights)]
    score = testAlgorithm(20)
    os.system('clear')
    scoreMap[score] = weights
    scoreList.append(score)
    for s in sorted(scoreList):
      print s, scoreMap[s]
  # iters = 1
  # weights = [0 for i in range(numWeights)]
  # greatestEver = 0
  # greatestWeights = weights
  # while True:
  #   for i in range(numWeights):
  #     bestlastval = -8
  #     bestScore = 0
  #     for j in range(-8, 8, 1):
  #       weights[i] = j
  #       # score = testAlgorithm(4)
  #       # if score > bestScore:
  #       score = testAlgorithm(iters)
  #       if score > bestScore:
  #         bestScore = score
  #         bestlastval = j
  #         if score > greatestEver:
  #           greatestEver = score
  #           greatestWeights = copyArray(weights)
  #       print score, weights, ' \t - \t ', greatestEver, greatestWeights
  #     weights[i] = bestlastval



  # 357.428571429 [21, -29, 38, 2, 15, -13]    -    369.257142857 [20, -29, 38, 2, 0, 0]
  # 322.8 [21, -36, 38, 2, 15, -13]    -    369.257142857 [20, -29, 38, 2,

# bd = [[3, 3, 6, 6], [3, 6, 6, 6], [0, 0, 0, 0], [0, 0, 0, 0]]
# printBoard(bd)
# res = upSwipe(bd)
# printBoard(res[1])
# print res[0]

# bd = parseBoard('1 6 2 48 1 1 6 2 6 3 1 24 2 1 1 3')
# printBoard(bd)

# changes, bd = rightSwipe(bd)
# print '\n', changes
# printBoard(bd)

# 3966.9 [2, 8, 6, 1, 0, 7]
# 4146.0 [5, 7, 4, 0, 5, 8]
# 4219.05 [8, 6, 6, 3, 0, 6]
# 4233.9 [1, 7, 7, 2, 2, 8]
# 4582.05 [6, 2, 3, 0, 3, 4]
# 4616.7 [8, 2, 3, 1, 8, 8]
# 4641.45 [8, 5, 5, 1, 4, 5]
# 4919.4 [5, 5, 2, 1, 5, 8]
# 4940.7 [7, 7, 4, 2, 2, 4]
# 4945.8 [7, 8, 6, 1, 1, 5]
# 6782.4 [7, 7, 6, 1, 4, 6]
