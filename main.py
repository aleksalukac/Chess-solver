# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:43:38 2021

@author: Aleksa
"""
from PIL import Image
from copy import deepcopy
import os
import numpy as np

black_figures = None
white_figures = None
set_number = 3

def find_first_and_last_pixel_in_image(image_color, image):
	img = np.asarray(image)
	height = img.shape[0]
	width = img.shape[1]
	
	img_color = np.asarray(image_color)[0][0]
	
	first_occurance = None
	last_occurance = None
	
	for i in range(height):
		for j in range(width):
			for k in range(3):
				if(img[i][j][k] != img_color[k]):
					break
			else:
				if(first_occurance == None):
					first_occurance = (i,j)
				last_occurance = (i,j)
	
	return first_occurance, last_occurance    
	
def load_images_from_folder(folder, black_tile, white_tile):
	images = {}
	for filename in os.listdir(folder):
		black = deepcopy(black_tile)
		white = deepcopy(white_tile)
		img = Image.open(os.path.join(folder,filename)).convert("RGBA")
		if img is not None:
			black.paste(img, (0, 0), img)
			#black.show()
			images[filename.replace(".png","") + "_black"] = black
			
			white.paste(img, (0,0), img)
			#white.show()
			images[filename.replace(".png","") + "_white"] = white
	return images

def pic_similarity(image1, image2):
	similarity = 0
	for i in range(30):
		for j in range(30):
			for k in range(3):
				similarity += abs(int(image1[i,j,k]) - int(image2[i,j,k]))
	
	return similarity

def find_most_similar_figure(image, color):
	global black_figures, white_figures
	similarity = None
	piece_color = None
	figure = None
	for name, img in black_figures.items():
		if(color in name):
			pic_sim = pic_similarity(image, img)
			if(similarity == None or pic_sim < similarity):
				similarity = pic_sim
				figure = name.split('_')[0]
				piece_color = 'black'
	
	for name, img in white_figures.items():
		if(color in name):
			pic_sim = pic_similarity(image, img)
			if(similarity == None or pic_sim < similarity):
				similarity = pic_sim
				figure = name.split('_')[0]
				piece_color = 'white'	

	return figure, piece_color
# %%

def read_board_from_image(directory_path, show = False):
	global black_figures, white_figures, set_number
	
	set_number = int(directory_path.split('/')[-1])
	set_directory = directory_path
	
	chessboard = Image.open(set_directory + "/"+ str(set_number) + ".png")
	
	tiles_directory = set_directory + "/tiles"
	pieces_directory = set_directory + "/pieces"
	
	black_tile = Image.open(tiles_directory + "/black.png").convert("RGBA")
	white_tile = Image.open(tiles_directory + "/white.png").convert("RGBA")
	
	black_figures_directory = pieces_directory + "/black"
	white_figures_directory = pieces_directory + "/white"
	
	black_figures = load_images_from_folder(black_figures_directory, black_tile, white_tile)
	
	white_figures = load_images_from_folder(white_figures_directory, black_tile, white_tile)
	
	first, last = find_first_and_last_pixel_in_image(white_tile, chessboard)
	print(str(first[0]) + "," + str(first[1]))
	area = (first[1], first[0], last[1] + 1 , last[0] + 1)
	chessboard = chessboard.crop(area)
	
	if(show):
		chessboard.show()
	
	chessboard_shape = np.asarray(chessboard).shape
	
	for name, image in black_figures.items():
		black_figures[name] = image.resize((int(chessboard_shape[0] / 8), int(chessboard_shape[1] / 8)))
		
	
	for name, image in white_figures.items():
		white_figures[name] = image.resize((int(chessboard_shape[0] / 8), int(chessboard_shape[1] / 8)))
		
	for name, image in black_figures.items():
		black_figures[name] = np.asarray(image)
		
	
	for name, image in white_figures.items():
		white_figures[name] = np.asarray(image)
	
	chessboard_tiles = []
		
	chessboard_array = np.asarray(chessboard)
	
	for i in range(8):
		for j in range(8):
			tile = chessboard_array[30 * i : 30 * (i + 1), 30 * j : 30 * (j + 1)]
			#chessboard_tiles.append(Image.fromarray(tile,'RGB'))
			chessboard_tiles.append(tile)
			#chessboard_tiles[-1].show()
			
	white_tile = np.asarray(white_tile)
	black_tile = np.asarray(black_tile)
	
	chessboard_figures = [[0 for x in range(8)] for y in range(8)] 
	
	i, j = 0, -1
	
	for tile in chessboard_tiles:
			
		j += 1
		if(j == 8):
			j = 0
			i += 1
		
		tile_color = 'white'
		if((i + j) % 2 != 0):
			tile_color = 'black'
		
		if(tile_color == 'white' and pic_similarity(tile, white_tile) < 1000):
			continue
		elif(tile_color == 'black' and pic_similarity(tile, black_tile) < 1000):
			continue
			
		chessboard_figures[i][j] = (find_most_similar_figure(tile, tile_color))

	return chessboard_figures

def find_king(color):
	global board
	for i in range(8):
		for j in range(8):
			if(board[i,j] == ('king', color)):
				return i,j

def is_valid_coord(x,y):
	return (x < 8 and y < 8 and x >= 0 and y>= 0)
	
directions_rook = [
	(0, -1),
	(0, 1),
	(-1, 0),
	(1, 0)
]

directions_bishop = [
	(-1, -1),
	(1, -1),
	(1, 1),
	(-1, 1)
]

directions_knight = [
	(-2, -1),
	(-2, 1),
	(2, -1),
	(2, 1),
	(1, 2),
	(1, -2),
	(-1, 2),
	(-1, -2)
]

directions_pawn = [
	(-1, 1),
	(-1, -1)
]

directions_king = [
	(-1, -1),
	(-1, 0),
	(-1, 1),
	(0, -1),
	(0, 1),
	(1, -1),
	(1, 0),
	(1, 1)
]

def is_check(color = None):
	global board, directions_pawn, directions_knight, directions_biship, directions_rook
	
	king_colors = ['white', 'black']
	
	if(color != None):
		king_colors = [color]
	for king_color in king_colors:
		king_pos = find_king(king_color)
		
		checked_from = []
		
		for i,j in directions_rook:
			isChecked = False
			x, y = king_pos
			while True:
				x += i
				y += j
				if(is_valid_coord(x, y)):
					if(board[x, y] == 0):
						continue
					if(board[x, y][1] == king_color):
						break
					if(board[x, y][0] in ['rook','queen']):
						#print(board[x, y][0])
						#checked_from.append((x,y))
						return king_color
				else:
					break
					
		for i,j in directions_bishop:
			isChecked = False
			x, y = king_pos
			while True:
				x += i
				y += j
				if(is_valid_coord(x, y)):
					if(board[x, y] == 0):
						continue
					if(board[x, y][1] == king_color):
						break
					if(board[x, y][0] in ['bishop','queen']):
						#print(board[x, y][0])
						#checked_from.append((x,y))
						return king_color
				else:
					break
					
		x, y = king_pos
		for i,j in directions_knight:
			if(is_valid_coord(x + i, y + j) and board[x + i, y + j] != 0):
				if(board[x + i, y + j][0] == 'knight' and board[x + i, y + j][1] != king_color):
					#print('knight')
					#checked_from.append((x,y))
					return king_color
				
		x, y = king_pos
		
		if(king_color == 'black'):
			directions_pawn = [
				(1, 1),
				(1, -1)
			]
		else:
			directions_pawn = [
				(-1, 1),
				(-1, -1)
			]
			
		for i,j in directions_pawn:
			if(is_valid_coord(x + i, y + j) and board[x + i, y + j] != 0):
				if(board[x + i, y + j][1] != king_color and board[x + i, y + j][0] == 'pawn'):
					#print('pawn')
					#checked_from.append((x,y))
					return king_color	
	
	return None

fen_figures = {
	('queen','white') : 'Q',
	('king', 'white') : 'K',
	('bishop', 'white') : 'B',
	('knight', 'white') : 'N',
	('rook', 'white') : 'R',
	('pawn', 'white') : 'P',
	('queen','black') : 'q',
	('king', 'black') : 'k',
	('bishop', 'black') : 'b',
	('knight', 'black') : 'n',
	('rook', 'black') : 'r',
	('pawn', 'black') : 'p',
	}

def print_fen_notation():
	global board
	notation = ""
	for i in range(8):
		if(i != 0):
			notation += "/"
		s = ""
		k = 0
		for j in range(8):
			if(board[i,j] == 0):
				k += 1
				continue
			if(k != 0):
				s += str(k)
				k = 0
			s += fen_figures[board[i,j]]
		if(k != 0):
			s += str(k)
		
		notation += s
	
	print(notation)

def print_is_checkmate(color):
	global board
	
	for fx in range(8):
		for fy in range(8):
			if(board[fx,fy] != 0 and board[fx,fy][1] == color):
				
				#check if figure can move like rook
				if(board[fx,fy][0] in ['rook','queen']):
					for i,j in directions_rook:
						x, y = fx, fy
						
						#if the figure hits opponent figure, it cannot move after eating it
						haveToStop = False
						while True:
							x += i
							y += j
							if(not is_valid_coord(x, y) or (board[x,y] != 0 and board[x,y][1] == color)):
								break
							
							if(board[x,y] != 0 and board[x,y][1] != color):
								haveToStop = True
							
							prevBoard = deepcopy(board[x,y])
							board[x,y] = deepcopy(board[fx,fy])
							board[fx,fy] = 0
							if(is_check(color) != color):
								print('0')
								return
							board[fx,fy] = deepcopy(board[x,y])
							board[x,y] = deepcopy(prevBoard)
							
							if(haveToStop):
								break
					
				#check if figure can move like bishop		
				if(board[fx,fy][0] in ['bishop','queen']):
					for i,j in directions_bishop:
						x, y = fx, fy
						haveToStop = False
						while True:
							x += i
							y += j
							if(not is_valid_coord(x, y) or (board[x,y] != 0 and board[x,y][1] == color)):
								break
							
							if(board[x,y] != 0 and board[x,y][1] != color):
								haveToStop = True
							
							prevBoard = deepcopy(board[x,y])
							board[x,y] = deepcopy(board[fx,fy])
							board[fx,fy] = 0
							if(is_check(color) != color):
								print('0')
								return
							board[fx,fy] = deepcopy(board[x,y])
							board[x,y] = deepcopy(prevBoard)
							
							if(haveToStop):
								break
							
				#check if figure is pawn
				if(board[fx,fy][0] == 'pawn'):
					start = 1
					
					directions_pawn = [
						(1, 0),
						(1, 1),
						(1, -1)
					]
					
					if(color == 'white'):
						start = 6
						directions_pawn = [
							(-1, 0),
							(-1, 1),
							(-1, -1)
						]
					
					x,y = fx,fy
					for i,j in directions_pawn:
						x += i
						y += j
						if(not is_valid_coord(x, y) or (board[x,y] != 0 and board[x,y][1] == color)):
							continue
						
						prevBoard = deepcopy(board[x,y])
						board[x,y] = deepcopy(board[fx,fy])
						board[fx,fy] = 0
						if(is_check(color) != color):
							print('0')
							return
						board[fx,fy] = deepcopy(board[x,y])
						board[x,y] = deepcopy(prevBoard)
						
						#pawn double move from starting line
						if(j == 0 and fx == start):
							x += i
							if(not is_valid_coord(x, y) or (board[x,y] != 0 and board[x,y][1] == color)):
								continue
						
							prevBoard = deepcopy(board[x,y])
							board[x,y] = deepcopy(board[fx,fy])
							board[fx,fy] = 0
							if(is_check(color) != color):
								print('0')
								return
							board[fx,fy] = deepcopy(board[x,y])
							board[x,y] = deepcopy(prevBoard)
				#end pawn check

				#check if figure is knight
				if(board[fx,fy][0] == 'knight'):
					for i,j in directions_knight:
						x, y = fx, fy
						x += i
						y += j
						if(not is_valid_coord(x, y) or (board[x,y] != 0 and board[x,y][1] == color)):
							continue
												
						prevBoard = deepcopy(board[x,y])
						board[x,y] = deepcopy(board[fx,fy])
						board[fx,fy] = 0
						if(is_check(color) != color):
							print('0')
							return
						board[fx,fy] = deepcopy(board[x,y])
						board[x,y] = deepcopy(prevBoard)
				#end knight check
				
				#check if figure is king
				if(board[fx,fy][0] == 'king'):
					for i,j in directions_king:
						x, y = fx, fy
						x += i
						y += j
						if(not is_valid_coord(x, y) or (board[x,y] != 0 and board[x,y][1] == color)):
							continue
												
						prevBoard = deepcopy(board[x,y])
						board[x,y] = deepcopy(board[fx,fy])
						board[fx,fy] = 0
						if(is_check(color) != color):
							for s,l in directions_king:
								if(not is_valid_coord(x + s, y + l)):
									continue
								if(board[x + s, y + l] != 0 and board[x + s, y + l][0] == 'king' and  board[x + s, y + l][1] != color):
									break
							else:
								print('0')
								return
						board[fx,fy] = deepcopy(board[x,y])
						board[x,y] = deepcopy(prevBoard)
				#end king check
				
	print('1')
	return				
	
# %%
directory_path = input()
#for sss in range(26):
	#print(str(sss) + "**************************************")
	#sss = 17
	#directory_path = "D:/GitHub/Chess-solver/public/set/" + str(sss)

board = np.array(read_board_from_image(directory_path#,True
			  ))
print_fen_notation()

checked_color = is_check()

if(checked_color == None):
	print("-")
	print('0')
else:
	if(checked_color == 'white'):
		print('B')
	else:
		print('W')

	print_is_checkmate(checked_color)
