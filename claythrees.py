# import numpy as np

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



def canMerge(p1, p2):
  t1 = min(p1, p2)
  if t1 == 0: return True
  t2 = max(p1, p2)
  if p1==p2 and p1 != 1 and p2 != 2: return True
  if t1 == 1 and t2 == 2: return True
  return False

def rightSwipe(board):
  nb = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
  for rowNum, row in enumerate(board):
    for wall in range(3, -1, -1):
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
  if len(changeList) > 0:
    return changeList, nb
  return False

def start(board):
  while (True):
    changeList, board = rightSwipe(board)
    next = int(input('Enter in the next piece'))
    nextPos = int(input('Enter in row of next piece')) - 1
    board[nextPos][0] = next
    print changeList, board

start(parseBoard(raw_input('Enter board on one line: ')))
