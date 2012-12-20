import numpy as np
from termcolor import colored
from random import random
import sys

# the grid size

GRID_SIZE = 8
# the shapes

SHAPES = [
	('orange',[ 
			[1,1],
			[1,1],
			[1,1],
			[1],
			[1]], True, 'on_white'),
	('light green',[ 
			[1,1,1,1],
			[1,1],
			[1,1]], True, 'on_green'),
	('light purple',[ 
			[1,1],
			[1,1,1,1],
			[1,1]], False, 'on_magenta'),
	('dark green', [ 
			[1],
			[1,1,1],
			[1,1,1],
			[1]], False, 'on_grey'),
	('dark purple', [ 
			[1,1],
			[1,1,1],
			[1,1,1]], False, 'on_red'),
	('yellow', [ 
			[1,1],
			[1,1,1,1],
			[0,0,1,1]], True, 'on_yellow'),
	('pink', [ 
			[1,1,1,1],
			[1,1,1,1]], False, 'on_cyan'),
	('blue', [ 
			[1,1,1],
			[1],
			[1],
			[1,1,1]], False, 'on_blue')
	]

def to_np_array(shape):
	a = np.zeros([GRID_SIZE,GRID_SIZE])
	for y in range(len(shape[1])):
		for x in range(len(shape[1][y])):
			if shape[1][y][x] > 0:
				a[y,x] = 1
	return a
			
def fit(shape, r, grid=None, x=0, y=0, shift=0):
	if grid is None:
		grid = np.zeros([GRID_SIZE,GRID_SIZE])
	s = to_np_array(shape)
	# flip it
	if r > 3:
		# skip if shape is not flipable
		if not shape[2]:
			return False
		s = np.fliplr(s)
		r = r - 4
	# rotate it
	if r > 0:
		s = np.rot90(s, k=r)
	# find the topmost LHS
	tlx,tly = None,None
	for y1 in range(GRID_SIZE):
		for x1 in range(GRID_SIZE):
			if s[y1,x1] > 0:
				if shift == 0:
					tlx,tly = x1,y1
					break
				else:
					# find next topmost LHS
					shift -= 1
		if tlx is not None:
			break
	# no more LHS
	if tlx is None:
		return False
	# roll the elements so that top-left is at x,y
	s = np.roll(s, x-tlx, 1)
	s = np.roll(s, y-tly, 0)
	# ensure that the shape has not rolled off the x-axis
	if np.any( s[0,0:GRID_SIZE] ) and np.any( s[GRID_SIZE-1,0:GRID_SIZE] ):
			return False
	# ensure that the shape has not rolled off the y-axis
	if np.any( s[0:GRID_SIZE,0] ) and np.any( s[0:GRID_SIZE,GRID_SIZE-1] ):
			return False
	# add grids
	g = grid + s
	# sanity
	if g[y,x] < 1:
		raise Exception("Expected grid %s,%s to be filled" % (x,y))
	# if any elements >1 then there was a colision
	if np.max(g) > 1:
		return False
	# else
	return (g,s)

def fill(grid, shapes=None):
	if shapes is None or len(shapes) == 0:
		raise Exception("missing shapes")
	# working from left-to-right on the grid
	# find the next free square
	for y in range(GRID_SIZE):
		for x in range(GRID_SIZE):
			# skip used sq
			if grid[y,x] > 0:
				continue
			# for each shape
			for shape in shapes:
				for r in range(8):
					for shift in range(5):
						fitting = fit(shape, r, x=x, y=y, shift=shift, grid=grid)
						if fitting is not False:
							g,location = fitting
							# create list of remaining shapes
							remaining = [s for s in shapes if s != shape]
							# if there are no shapes left... it's solved!
							if len(remaining) == 0:
								return [(shape, location)];
							# try and fill remaining shapes
							res = fill(g, remaining)
							if res is not False:
								# solved!
								res.append( (shape,location) )
								return res
			return False
	# this should not happen
	raise Exception("no more empty spaces but somehow shapes were left?")

def solve_for(shape,r=0):
	# add the starting shape at angle r onto grid
	res = fit(shape, r)
	if res is False:
		return False
	grid,location = res
	# print the filled grid with the remaining shapes
	res = fill(grid, [s for s in SHAPES if s != shape])
	if res is not False:
		res.append( (s,location) )
	return res

def print_grid(res):
	if res is False:
		return
	# cerate a 2dim list for the output
	sg = []
	for y in range(GRID_SIZE):
		l = []
		for x in range(GRID_SIZE):
			l.append(None)
		sg.append(l)
	# fill the 2dim list with shape objects
	for shape,location in res:
		for y in range(GRID_SIZE):
			for x in range(GRID_SIZE):
				if location[y,x] == 1 and sg[y][x] is None:
					sg[y][x] = shape
	# print the shapegrid
	print "\n"
	for y in range(GRID_SIZE):
		for _ in range(2):
			sys.stdout.write('  ')
			for x in range(GRID_SIZE):
				shape = sg[y][x]
				sys.stdout.write( colored("    ", 'white', shape[3]) )
			sys.stdout.write("\n")
	print "\n"
	
	
def main():
	for n in range(len(SHAPES)):
		for r in range(8):
			res = solve_for(SHAPES[n], r=r)
			print_grid(res)
main()
