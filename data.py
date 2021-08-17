

# board = [
# 	['00','00','00','00','00','00','bQ','00'],
# 	['00','00','wP','00','00','00','00','00'],
# 	['00','00','00','00','00','bP','00','00'],
# 	['00','00','00','00','00','00','00','00'],
# 	['00','wQ','00','00','00','00','00','00'],
# 	['00','00','00','00','wP','00','00','00'],
# 	['00','00','00','00','00','wP','bP','00'],
# 	['00','00','00','00','00','00','00','00']
# ]

board = [
	['bR','bN','bB','bK','bQ','bB','bN','bR'],
	['bP','bP','bP','bP','bP','bP','bP','bP'],
	['00','00','00','00','00','00','00','00'],
	['00','00','00','00','00','00','00','00'],
	['00','00','00','00','00','00','00','00'],
	['00','00','00','00','00','00','00','00'],
	['wP','wP','wP','wP','wP','wP','wP','wP'],
	['wR','wN','wB','wK','wQ','wB','wN','wR']
]

# Positional piece square table
pawn_table = [
	[ 80, 80, 80, 80, 80, 80, 80, 80],
	[50, 50, 50, 50, 50, 50, 50, 50],
	[10, 10, 20, 30, 30, 20, 10, 10],
	[ 5,  5, 10, 25, 25, 10,  5,  5],
	[ 0,  0,  0, 20, 20,  0,  0,  0],
	[ 5, -5,-10,  0,  0,-10, -5,  5],
	[ 5, 10, 10,-20,-20, 10, 10,  5],
	[0,  0,  0,  0,  0,  0,  0,  0]
]
knight_table = [
	[-50,-40,-30,-30,-30,-30,-40,-50],
	[-40,-20,  0,  0,  0,  0,-20,-40],
	[-30,  0, 10, 15, 15, 10,  0,-30],
	[-30,  5, 15, 20, 20, 15,  5,-30],
	[-30,  0, 15, 20, 20, 15,  0,-30],
	[-30,  5, 10, 15, 15, 10,  5,-30],
	[-40,-20,  0,  5,  5,  0,-20,-40],
	[-50,-90,-30,-30,-30,-30,-90,-50]
]
bishop_table = [
	[-20,-10,-10,-10,-10,-10,-10,-20],
	[-10,  0,  0,  0,  0,  0,  0,-10],
	[-10,  0,  5, 10, 10,  5,  0,-10],
	[-10,  5,  5, 10, 10,  5,  5,-10],
	[-10,  0, 10, 10, 10, 10,  0,-10],
	[-10, 10, 10, 10, 10, 10, 10,-10],
	[-10,  5,  0,  0,  0,  0,  5,-10],
	[-20,-10,-90,-10,-10,-90,-10,-20]
]
rook_table = [
	[0,  0,  0,  0,  0,  0,  0,  0],
	[5, 10, 10, 10, 10, 10, 10,  5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[ 0,  0,  0,  5,  5,  0,  0,  0]
]
king_table = [
	[-20,-10,-10, -5, -5,-10,-10,-20],
	[-10,  0,  0,  0,  0,  0,  0,-10],
	[-10,  0,  5,  5,  5,  5,  0,-10],
	[-5,  0,  5,  5,  5,  5,  0, -5],
	[ 0,  0,  5,  5,  5,  5,  0, -5],
	[-10,  5,  5,  5,  5,  5,  0,-10],
	[-10,  0,  5,  0,  0,  0,  0,-10],
	[-20,-10,-10, 70, -5,-10,-10,-20]
]
queen_table = [[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-20,-30,-30,-40,-40,-30,-30,-20],
[-10,-20,-20,-20,-20,-20,-20,-10],
[ 20, 20,  0,  0,  0,  0, 20, 20],
[ 20, 30, 10,  0,  0, 10, 30, 20]]

queen_endgame_table = [[-50,-40,-30,-20,-20,-30,-40,-50],
[-30,-20,-10,  0,  0,-10,-20,-30],
[-30,-10, 20, 25, 25, 20,-10,-30],
[-30,-10, 25, 30, 30, 25,-10,-30],
[-30,-10, 25, 30, 30, 25,-10,-30],
[-30,-10, 20, 25, 25, 20,-10,-30],
[-30,-30,  0,  0,  0,  0,-30,-30],
[-50,-30,-30,-30,-30,-30,-30,-50]]


# material evaluation
pawn = 100
knight = 320
bishop = 330
rook = 500
king = 900
queen = 1500
isolated_pawn = -30
doubled_pawn = -30
passed_pawn = 30


def mirror(table):
	mirror_table = []
	for each_row in table:
		mirror_table.insert(0,each_row)

	return mirror_table

def evaluateScore(board,total_move):
	black_score = 0
	white_score = 0
	wdP = count_doubled_pawn(board,"w")
	bdP = count_doubled_pawn(board,"b")

	# print("white doubled: ",wdP)
	# print("Black doubled: ",bdP)

	wiP = count_isolated_pawn(board,"w")
	biP = count_isolated_pawn(board,"b")

	# print("White isolated",wiP)
	# print("black isolated",biP)

	wpP = count_passed_pawn(board,"w")
	bpP = count_passed_pawn(board,"b")

	# print("white passed pawn",wpP)
	# print("black passed pawn",bpP)
	for y in range(8):
		for x in range(8):
			item = board[y][x]
			if item == "bP":
				value = mirror(pawn_table)[y][x]
				black_score += value
				black_score += pawn
			if item == "bR":
				value = mirror(rook_table)[y][x]
				black_score += value
				black_score += rook
			if item == "bN":
				value = mirror(knight_table)[y][x]
				black_score += value
				black_score += knight
			if item == "bB":
				value = mirror(bishop_table)[y][x]
				black_score += value
				black_score += bishop
			if item == "bK":
				value = mirror(king_table)[y][x]
				black_score += value
				black_score += king
			if item == "bQ":
				if total_move > 60:
					value = mirror(queen_endgame_table)[y][x]
				else:
					value = mirror(queen_table)[y][x]
				black_score += value
				black_score += queen

			# white
			if item == "wP":
				value = pawn_table[y][x]
				white_score += value
				white_score += pawn
			if item == "wN":
				value = knight_table[y][x]
				white_score += value
				white_score += knight
			if item == "wR":
				value = rook_table[y][x]
				white_score += value
				white_score += rook
			if item == "wK":
				value = king_table[y][x]
				white_score += value
				white_score += king
			if item == "wB":
				value = bishop_table[y][x]
				white_score += value
				white_score += bishop
			if item == "wQ":
				if total_move>60:
					value = queen_endgame_table[y][x]
				else:
					value = queen_table[y][x]
				white_score += value
				white_score += queen

	black_score += biP*isolated_pawn + bdP*doubled_pawn + bpP*passed_pawn
	white_score += wiP*isolated_pawn + wdP*doubled_pawn + wpP*passed_pawn
	# print("black score: ",black_score)
	# print("white score: ",white_score)
	# print(black_score - white_score)
	return black_score - white_score

def count_doubled_pawn(board,player):
	doubled_pawn = []
	count = 0
	for y in range(8):
		for x in range(8):
			if board[y][x][0] == player and board[y][x][1] == "P":
				if x in doubled_pawn:
					count +=1
				else:
					doubled_pawn.append(x)
	return count

def count_isolated_pawn(board,player):
	isolated_pawn = []
	count = 0

	for y in range(8):
		for x in range(8):
			if board[y][x][0] == player and board[y][x][1] == "P":
				isolated_pawn.append(x)
	for y in range(8):
		for x in range(8):
			if board[y][x][0] == player and board[y][x][1] == "P":
				if x!=0 and x!=7:
					if x-1 in isolated_pawn or x+1 in isolated_pawn:
						pass
					else:
						count +=1
				if x==0:
					if x+1 in isolated_pawn:
						pass
					else:
						count +=1
				if x == 7:
					if x-1 in isolated_pawn:
						pass
					else:
						count +=1
	return count

def count_passed_pawn(board,player):
	count = 0

	if player == "w":
		for y in range(8):
			for x in range(8):
				if board[y][x][0] == player and board[y][x][1] == "P" and y < 4:
					flag = True
					for s in range(8):
						for r in range(8):
							if board[s][r] != player and board[s][r][1] == "P" and s< 4:
								if r==x or r == x -1 or r == x + 1:
									flag = False
									break
					if flag:
						count +=1
	if player =="b":
		for y in range(8):
			for x in range(8):
				if board[y][x][0] == player and board[y][x][1] == "P" and y >= 4:
					flag = True
					for s in range(8):
						for r in range(8):
							if board[s][r] != player and board[s][r][1] == "P" and s >=4:
								if r==x or r == x -1 or r == x + 1:
									flag = False
									break
					if flag:
						count +=1

	return count

def print_board(board):
	for y in range(8):
		for x in range(8):
			print(board[y][x], end=" ")
		print()