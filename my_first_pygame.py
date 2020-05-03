import pygame as pg
import random
import os
import time
import neat

THE_CANVAS_LENGTH = 1000
THE_CANVAS_DEPTH  = 1000

THE_GAP = 200

THE_WIDTH_OF_BAR  = 100
MIN_BAR_HEIGHT  =  100
THE_RADIUS_OF_BALL = 20

THE_VELOCITY_OF_BAR = 10

THE_NUMBER_OF_GENERATIONS  = 50

pg.init()

pg.display.set_caption("The GAME is ON")
THE_WINDOW = pg.display.set_mode((THE_CANVAS_LENGTH, THE_CANVAS_DEPTH))


class the_bar:
	#the bars are created here


	def __init__(self, the_first_x, the_first_y):

		self.the_first_x  = the_first_x
		self.the_first_y  = the_first_y
		#self.the_width  = the_width
		#self.the_height  =  the_height
		self.passed = False  #useful for the phase where we look for collisions
		self.part_1_height = (random.randrange(MIN_BAR_HEIGHT, (THE_CANVAS_DEPTH - (MIN_BAR_HEIGHT + THE_GAP))))
		#self.part_1_height = random.randrange(100, 300)
		self.part_2_height = THE_CANVAS_DEPTH - (self.part_1_height + THE_GAP)
		self.the_old_x = the_first_x

		self.part_1_x = 0
		self.part_1_y = 0
		self.part_2_x = 0
		self.part_2_y = 0

	def draw_the_bar(self):

		self.part_1_x = self.the_first_x 
		self.part_1_y = self.the_first_y

		part_1_width = THE_WIDTH_OF_BAR
		
		self.part_2_x = self.part_1_x
		self.part_2_y = self.part_1_y + self.part_1_height + THE_GAP

		part_2_width = THE_WIDTH_OF_BAR
		


		pg.draw.rect(THE_WINDOW, (0,0,0), (self.the_old_x, self.part_1_y, THE_WIDTH_OF_BAR, self.part_1_height))
		pg.draw.rect(THE_WINDOW, (0,0,0), (self.the_old_x, self.part_2_y, THE_WIDTH_OF_BAR, self.part_2_height))

		pg.draw.rect(THE_WINDOW, (255,255,255), (self.part_1_x, self.part_1_y, part_1_width, self.part_1_height))
		pg.draw.rect(THE_WINDOW, (255,255,255), (self.part_2_x, self.part_2_y, part_2_width, self.part_2_height))
		pg.display.update()


	def move_the_bar(self):
		self.the_old_x = self.the_first_x
		self.the_first_x = self.the_first_x  -  THE_VELOCITY_OF_BAR


	def check_the_collision(self, the_ball_object):

		if((self.the_first_x <= (the_ball_object.x + THE_RADIUS_OF_BALL))   and  ((self.the_first_x + THE_WIDTH_OF_BAR) >= (the_ball_object.x  - THE_RADIUS_OF_BALL))):

			if(((the_ball_object.y - THE_RADIUS_OF_BALL) <= self.part_1_height)  or ((the_ball_object.y + THE_RADIUS_OF_BALL) >=  self.part_2_y)):
				return True


		return False




class the_ball:
	#the ball is created and managed here

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.tick_count = 0
		self.height = self.y
		self.vel = 0
		self.old_y = 0


	def jump(self):
		self.vel = -10.5  #negative velocity so that it gan go upwards from the x position it currently is in
		self.tick_count = 0 #need to reset this to 0 so that we know how much time has passed since we have jumped
		self.height = self.y


	def move(self):
		self.tick_count = self.tick_count + 1

		the_displacement = self.vel * self.tick_count  +  1.5*self.tick_count**2

		#i see a problem with my jumps....on some occasions, the jump is too low so the bird is falling a long way in a single frame...hence i am adding terminal velocity in to the mix

		if the_displacement > 16:
			the_displacement = 16

		if the_displacement < 0:
			the_displacement = the_displacement - 2


		self.old_y = self.y

		self.y = self.y + the_displacement


	def draw_the_ball(self):

		pg.draw.circle(THE_WINDOW, (0, 0, 0), (int(self.x), int(self.old_y)), THE_RADIUS_OF_BALL)
		pg.draw.circle(THE_WINDOW, (255, 0, 0), (int(self.x), int(self.y)), THE_RADIUS_OF_BALL)
		pg.display.update()



def draw_the_stuff(the_bars_list, the_balls_list):
	#the_ball_object.draw_the_ball()

	for each_bar in the_bars_list:
		each_bar.draw_the_bar()

	for each_ball in the_balls_list:
		each_ball.draw_the_ball()

	pg.display.update()




def the_tombstone_drawing(the_ball_object):
	#this function is to eliminate the ball from the screen once it has collided
	pg.draw.circle(THE_WINDOW, (0, 0, 0), (int(the_ball_object.x), int(the_ball_object.y)), THE_RADIUS_OF_BALL)
	pg.display.update()


def the_tombstone_for_bars(the_bars_list):

	for each_bar in the_bars_list:
		pg.draw.rect(THE_WINDOW, (0,0,0), (each_bar.part_1_x, each_bar.part_1_y, THE_WIDTH_OF_BAR, each_bar.part_1_height))
		pg.draw.rect(THE_WINDOW, (0,0,0), (each_bar.part_2_x, each_bar.part_2_y, THE_WIDTH_OF_BAR, each_bar.part_2_height))
		pg.display.update()

#the driver code starts here


def the_fitness_function(the_set_of_genomes, the_configuration):

	the_score = 0

	the_neural_nets_list = []
	the_genomes_list = []
	the_balls_list = []


	for _,each_genome in the_set_of_genomes:
		the_network = neat.nn.FeedForwardNetwork.create(each_genome, the_configuration)

		the_neural_nets_list.append(the_network)
		the_balls_list.append(the_ball(200,200))

		each_genome.fitness = 0  #setting the fitness of each bird 
		the_genomes_list.append(each_genome)



	#the_ball_object = the_ball(200,200) 
	the_bar_list= [the_bar(int(THE_CANVAS_LENGTH),0)]
	#the_bar_list = []
	#the_bar_list.append(the_bar(int(THE_CANVAS_LENGTH),0))


	run = True

	the_clock = pg.time.Clock()


	#print('prinitng random stuff')

	while run:

		#while following the tutorial

		the_clock.tick(30)
		for each_event in pg.event.get():
			if each_event.type == pg.QUIT:
				run = False
				pg.quit()
				quit()


		the_pipe_index = 0

		if(len(the_balls_list) > 0):
			if((len(the_bar_list) > 1) and (the_balls_list[0].x  > (the_bar_list[0].the_first_x + THE_WIDTH_OF_BAR))):
				the_pipe_index = 1  #in the case where there are two pipes on the screen and the first one has crossed the ball, we take into account the co-ordinartes of the second pipe for the neural netwrok stuff

		else:
			the_tombstone_for_bars(the_bar_list)

			run = False
			break


		for the_position, each_ball in enumerate(the_balls_list):
			each_ball.move()
			the_genomes_list[the_position].fitness = the_genomes_list[the_position].fitness + 0.4

			the_output = the_neural_nets_list[the_position].activate((each_ball.y, abs(each_ball.y - the_bar_list[the_pipe_index].part_1_height + the_bar_list[the_pipe_index].part_1_y), abs(each_ball.y - the_bar_list[the_pipe_index].part_2_y)))

			if the_output[0] > 0.5:
				each_ball.jump()



		the_dustbin = []
		add_pipe = False

		for each_bar in the_bar_list:

			the_ball_indexes_to_pop =[]

			for the_position, each_ball in enumerate(the_balls_list):

				if each_bar.check_the_collision(each_ball):
					#the_genomes_list[the_position].fitness  =  the_genomes_list[the_position].fitness - 1 #reducing the fitness of the balls that hit the bar as they should not be favoured in the next generation

					#eliminating the hit ball from all the lists
					#the_neural_nets_list.pop(the_position)
					#the_genomes_list.pop(the_position)
					the_ball_indexes_to_pop.append(the_position)
					the_tombstone_drawing(each_ball)

					#print("collission occured#####")

				#else:
					#print("no collisison ########")


				if (not(each_bar.passed) ) and (each_bar.the_first_x < each_ball.x):
					each_bar.passed = True
					add_pipe  = True

			the_ball_indexes_to_pop.sort(reverse = True)

			for each_index in the_ball_indexes_to_pop:
				#print("prinitng the length of the balls_list ", len(the_balls_list))
				#print("printing  the indexe to be popped ", each_index)
				the_genomes_list[each_index].fitness  =  the_genomes_list[each_index].fitness - 1
				the_neural_nets_list.pop(each_index)
				the_genomes_list.pop(each_index)
				the_balls_list.pop(each_index)
				

			if (each_bar.the_first_x + THE_WIDTH_OF_BAR) < 0:

				#print("prinintg the value of  each_bar.the_first_x + THE_WIDTH_OF_BAR inside the if ", (each_bar.the_first_x + THE_WIDTH_OF_BAR))
				the_dustbin.append(each_bar)
				#the_bar_list.pop(0)


			each_bar.move_the_bar()


		if add_pipe:
			the_score = the_score + 1
			the_bar_list.append(the_bar(THE_CANVAS_LENGTH - 200,0))

			for each_genome in the_genomes_list:
				each_genome.fitness = each_genome.fitness + 5   
				#rewarding the birds that survived a pipe by extra fitness points
			#print("prinitng the score ", the_score)


		for each_bar in the_dustbin:
			#print("inside the loop to remove the bar ")	
			the_bar_list.remove(each_bar)
			#print("printing the length of the bar list after deleting ", len)



		the_second_balls_list_to_pop = []


		for the_position, each_ball in enumerate(the_balls_list):

			if (((each_ball.y + THE_RADIUS_OF_BALL) >= THE_CANVAS_DEPTH)   or  ((each_ball.y - THE_RADIUS_OF_BALL) <= 0)):

				#the_neural_nets_list.pop(the_position)
				#the_genomes_list.pop(the_position)
				the_second_balls_list_to_pop.append(the_position)
				the_tombstone_drawing(each_ball)


		the_second_balls_list_to_pop.sort(reverse = True)

		for each_element in the_second_balls_list_to_pop:
			#print("prinitng the length of the balls_list ", len(the_balls_list))
			#print("printing  the indexe to be popped ", each_element)
			the_balls_list.pop(each_element)
			the_neural_nets_list.pop(each_element)
			the_genomes_list.pop(each_element)


		#print("at the end...prinitg the number of elements in the bar list ", len(the_bar_list))


		draw_the_stuff(the_bar_list, the_balls_list)


	


def the_run_function(the_config_file_path):

	the_configuration = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, the_config_file_path)

	the_population = neat.Population(the_configuration)

	the_population.add_reporter(neat.StdOutReporter(True))
	the_statistics = neat.StatisticsReporter()
	the_population.add_reporter(the_statistics)



	the_greek_god = the_population.run(the_fitness_function, THE_NUMBER_OF_GENERATIONS)


if __name__ == "__main__":
	the_current_dir  = os.path.dirname(__file__)
	the_config_file_path = os.path.join(the_current_dir, "config-feedforward.txt")
	the_run_function(the_config_file_path)

	
