# Snake Game
# By: 	Travis Chang
# Date: Nov. 13 2017
# File: snake.py
# Python version 3.6

from tkinter import *

import random

class Snake():
	score = 0
	#score_label_var = "Score: " + str(score)
	canvasW = 1200	# width of the tkinter canvas
	canvasH = 800	# height of the tkinter canvas
	padding = 30	# padding around the borders of play area
	heading = 50	# extra padding for header to display things; e.g. score
	size = 10 		# size of 1 piece of snake
	the_snek = [] 	# all the pieces of the snake
	move_x = -size	# movement along x-axis; -size to move left initially
	move_y = 0		# movement along y-axis;

	# Boolean used to prevent near simultaneous movement key presses
	# from bugging the movement of the snake. For example, when
	# moving left, if the down and right keys are pressed together,
	# then the snake will end up moving right along the same axis and
	# into itself, causing a body collision and ending the game. The key
	# press events are registered faster than the next update time, which
	# causes this issue. By having the boolean lock the first direction,
	# the issue is fixed. See functions move_test and move_dir.
	direction_decided = False
	
	update_speed = 33		# Time in milliseconds before next update to game state
	game_over = False


	def __init__(self, master):
		# master will be the Tk object	
		self.master = master
		master.title = "Snake"
		
		#self.frame = Frame(master=self.master, width=self.canvasW, height=self.canvasH)
		#self.frame.pack()

		self.canvas = Canvas(self.master, width=self.canvasW, height=self.canvasH, bg="black")
		self.canvas.pack()

		# Display grid to visualize movement through all food spawns
		# self.display_grid()
		
		# Draw and store the walls for the play area
		# [0. TOP, 1. RIGHT, 2. BOTTOM, 3. LEFT]
		self.playArea = [self.canvas.create_line(
							self.padding, self.heading+self.padding,
							self.canvasW-self.padding, self.heading+self.padding,
							fill="white", tags="wall"),
						 self.canvas.create_line(
						 	self.canvasW-self.padding, self.heading+self.padding,
						 	self.canvasW-self.padding, self.canvasH-self.padding,
						 	fill="white", tags="wall"),
						 self.canvas.create_line(
						 	self.padding, self.canvasH-self.padding,
						 	self.canvasW-self.padding, self.canvasH-self.padding,
						 	fill="white", tags="wall"),
						 self.canvas.create_line(
						 	self.padding, self.heading+self.padding,
						 	self.padding, self.canvasH-self.padding,
						 	fill="white", tags="wall")]


		# Draw the snake on the canvas with initial body size
		self.draw_snake(3)
		# Draw the food on the canvas
		self.food = None
		self.draw_food()

		# Display the score
		self.score_label = Label(master=self.canvas, text="Score: {}".format(self.score),
								 fg="white", bg="black", font=("Courier", 20))

		# Create the tkinter canvas
		self.canvas.create_window(self.canvasW//2, self.heading, window=self.score_label)

		# Key Bindings
		self.master.bind("<Up>", self.move_dir)
		self.master.bind("<Down>", self.move_dir)
		self.master.bind("<Left>", self.move_dir)
		self.master.bind("<Right>", self.move_dir)

	# Increase score by 1
	def inc_score(self):
		self.score += 1
		self.score_label.config(text="Score: " + str(self.score))
		# print(self.score)

	# Decrease score by 1
	def def_score(self):
		self.score -= 1
		self.score_label.config(text="Score: " + str(self.score))
		# print(self.score)

	# Move the snake every frame
	def move_test(self):
		# Move the snake as long as the game is not over
		if (not self.game_over):
			self.direction_decided = False
			# Old coordinates of the head of the snake before it moves
			head_coords = self.canvas.coords(self.the_snek[0])
			#print(head_coords)

			# Move snake forward
			self.canvas.move(self.the_snek[0], self.move_x, self.move_y)

			if (self.ate_food()):
				self.the_snek.insert(1, self.canvas.create_rectangle(*head_coords, fill="red"))
			else:
				self.canvas.coords(self.the_snek[-1], head_coords)
				self.the_snek.insert(1, self.the_snek.pop(-1))

			# Body collision check
			self.check_body_collision()

			# Wall collision check
			self.check_wall_collision()

			'''
			overlap = self.canvas.find_overlapping(*self.canvas.coords(self.the_snek[0]))
			if (len(overlap) > 0):
				print(overlap)
			'''
			self.canvas.after(self.update_speed, self.move_test)

	# Change the movement direction of snake based on keypress event
	def move_dir(self, event):
		if not(self.direction_decided):
			if (event.keysym=="Up" and self.move_x != 0):
				self.move_x = 0
				self.move_y = -self.size
			elif (event.keysym=="Down" and self.move_x != 0):
				self.move_x = 0
				self.move_y = self.size
			elif (event.keysym=="Left" and self.move_y != 0):
				self.move_x = -self.size
				self.move_y = 0
			elif (event.keysym=="Right" and self.move_y != 0):
				self.move_x = self.size
				self.move_y = 0
		self.direction_decided = True


	# Check for collisions with the walls of the play area
	def check_wall_collision(self):
		overlapping = self.canvas.find_overlapping(*self.canvas.coords(self.the_snek[0]))
		# Check if any of the walls overlap with the head of the snake
		for wall in self.canvas.find_withtag("wall"):
			# If overlap/collision detected then game over
			if wall in overlapping:
				print("Wall collision detected; wall with tag {} found in tuple of overlaps: {}".format(wall, overlapping))
				self.game_over = True
				break
		return

	# Check for collisions with the body of the snake
	def check_body_collision(self):
		for body in self.the_snek[1:]:
			if self.canvas.coords(self.the_snek[0]) == self.canvas.coords(body):
				self.game_over = True
				print("Body collision at {}".format(str(self.canvas.coords(body))))
				break
		return

	def ate_food(self):
		overlapping = self.canvas.find_overlapping(*self.canvas.coords(self.the_snek[0]))
		if self.canvas.find_withtag("food")[0] in overlapping:
			self.inc_score()
			self.canvas.delete(self.food)
			self.food = None
			self.draw_food()
			return True
		else:
			return False


	def draw_snake(self, snake_length):
		for i in range(snake_length):
			temp_x = (self.canvasW//2) + (i*self.size)
			temp_y = ((self.canvasH+self.heading)//2)
			self.the_snek.append(self.canvas.create_rectangle(
				temp_x,
				temp_y,
				temp_x+self.size, 
				temp_y+self.size, 
				fill="red"))

		return

	def draw_food(self):
		if(self.food == None):
			temp_x = random.randrange(self.padding, self.canvasW-self.padding, self.size)
			temp_y = random.randrange(self.heading+self.padding, self.canvasH-self.padding, self.size)
			#print(temp_x)
			#print(temp_y)

			self.food = self.canvas.create_rectangle(temp_x, temp_y, temp_x+self.size, temp_y+self.size, fill="yellow", tags="food")
		'''
		else:
			self.canvas.delete(self.food)
			self.food = None
		'''
		#self.canvas.after(self.update_speed*10, self.draw_food)


	# Display grid that the snake travels on and where food can appear
	def display_grid(self):
		for i in range(self.padding, self.canvasW-self.padding, self.size):
			for j in range(self.padding+self.heading, self.canvasH-self.padding, self.size):
				self.canvas.create_rectangle(i, j, i+self.size, j+self.size, fill="yellow")

if __name__ == '__main__':
	root = Tk()

	snek = Snake(root)
	snek.move_test()
	#print(snek.canvas.find_withtag("wall"))
	root.mainloop()	 

