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
set_number = 16

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

def read_board_from_image():
	global black_figures, white_figures, set_number
	
	set_directory = "D:\\GitHub\\Chessboard Solver\\checkmate_public\\public\\set\\" + str(set_number)
	
	chessboard = Image.open(set_directory + "\\"+ str(set_number) + ".png")
	
	tiles_directory = set_directory + "\\tiles"
	pieces_directory = set_directory + "\\pieces"
	
	black_tile = Image.open(tiles_directory + "\\black.png").convert("RGBA")
	white_tile = Image.open(tiles_directory + "\\white.png").convert("RGBA")
	
	black_figures_directory = pieces_directory + "\\black"
	white_figures_directory = pieces_directory + "\\white"
	
	black_figures = load_images_from_folder(black_figures_directory, black_tile, white_tile)
	
	white_figures = load_images_from_folder(white_figures_directory, black_tile, white_tile)
	
	first, last = find_first_and_last_pixel_in_image(white_tile, chessboard)
	area = (first[1], first[0], last[1] + 1 , last[0] + 1)
	chessboard = chessboard.crop(area)
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
		
		if(i == 1 and j == 0):
			print()
		
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
	
def find_possible_moves(x,y):
	if(board[x,y] == 0):
		return []
	
	moves = []
	
def is_check():
	global board
	for king_color in ['white', 'black']:
		king_pos = find_king(king_color)
		
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
						print(board[x, y][0])
						return True, king_color
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
						print(board[x, y][0])
						return True, king_color
				else:
					break
					
		x, y = king_pos
		for i,j in directions_knight:
			if(is_valid_coord(x + i, y + j) and board[x + i, y + j] != 0):
				if(board[x + i, y + j][0] == 'knight' and board[x + i, y + j][1] != king_color):
					print('knight')
					return True, king_color
				
		x, y = king_pos
		directions_pawn = [
			(-1, 1),
			(-1, -1)
			]
			
		if(king_color == 'black'):
			directions_pawn = [
				(1, 1),
				(1, -1)
			]
			
		for i,j in directions_pawn:
			if(is_valid_coord(x + i, y + j) and board[x + i, y + j] != 0):
				if(board[x + i, y + j][1] != king_color and board[x + i, y + j][0] == 'pawn'):
					print('pawn')
					return True, king_color	

# %%
board = np.array(read_board_from_image())

# %%

print(is_check())





