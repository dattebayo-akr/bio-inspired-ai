import random
import math




class the_core(object):

	def __init__(self, inputs, outputs, population):

		self.inputs = inputs
		self.current_species = 0
		self.current_genome = 0

		self.population = population
		self.outputs = outputs
		self.edges = []
		self.delta_threshold = 3
		self.species = []
		
		self.delta_threshold = 3
		self.generation = 0
		self.max_generations = -1
		


	def generate_the_population(self):

		#returning the list of poulation so that I can monitor the list back in the driver function...else we don't actually need to return it from here

		the_population_register = []

		for i in range(self.population):

			the_genome = generate_the_genome(self.inputs, self.outputs, self.edges)
			the_genome.the_genesis()
			self.check_the_species(the_genome)
			the_population_register.append(the_genome)

		return the_population_register


	def check_the_species(self, the_genome):

		#first up we need to check if this is the first guy in the poulation...we otherwise get an out of range error

		if(len(self.species) == 0):
			self.species.append([the_genome])

		else:

			for each_specie in self.species:

				the_champion = each_specie[0]

				if get_me_the_genomic_distance(the_genome, the_champion) < self.delta_threshold:
					#if the difference is less than the threshold
					each_specie.append(the_genome)
					return


			#this is in case the genome does not match with anyone
			self.species.append([genome])


class generate_the_genome(object):

	def __init__(self, inputs, outputs, innovations):

		self.inputs = inputs
		self.outputs = outputs
		self.no_of_non_internal_nodes = inputs + outputs
		self.max_node = inputs + outputs
		self.activations = []
		self.genes = []
		self.innovations = innovations
		self.fitness = 0
		self.adjusted_fitness = 0


	def the_genesis(self):

		#this is used to generate an individual with si9mple initial structure...for each input node, there is a link made to the output node

		for i in range(self.inputs):
			#print("inside the generate loop while generating the genome")
			for j in range(self.inputs, self.no_of_non_internal_nodes):
				self.generate_the_edge(i + 1,  j + 1)


	def generate_the_edge(self, from_node, to_node):

		#this fella adds a new connection if it is not present

		if(from_node, to_node) in self.check_for_existence():
			#but first we check if it already exists or not
			return


		#adding it to the ultimate edge database
		if (from_node, to_node) not in self.innovations:
			self.innovations.append((from_node, to_node))

		#now for simplicity sake, I am assigning the innovation number as the index of the list in which the edges are stored....i got this idea from a blog I can't find anymore
		the_innovation_number = self.innovations.index((from_node, to_node))

		#next, we need to add this in the set of genes for this individual
		self.genes.append([the_innovation_number, random.uniform(0, 1)*random.choice([-1, 1]), True])



	def check_for_existence(self):

		the_result = []

		for each_gene in self.genes:
			the_result.append(self.innovations[each_gene[0]])

		return the_result




def get_me_the_genomic_distance(the_genome, the_champion):


	#not gettging proper inputs somehow......need to troubleshoot this tomorrow morning

	#printig the inputs to verify

	#print("printig the genome ", the_genome)

	#print("printing the_champion ", the_champion)

	the_innovation_set_of_the_genome = set([i[0] for i in the_genome.genes])

	print("checking the the innovation set of the genome ", the_innovation_set_of_the_genome)

	the_innovation_set_of_the_champion = set([i[0] for i in the_champion.genes])

	print("checking the the innovation set of the champion ", the_innovation_set_of_the_champion)

	#now as stated in the paper, if the innovation numbers are the same, we check the diffreence in weights and if not they contribute to the disjoint



	#the_matching = the_innovation_set_of_the_genome && the_innovation_set_of_the_champion  --> not sure why this didnt work
	the_matching = the_innovation_set_of_the_genome & the_innovation_set_of_the_champion

	print("priniting the matching to verify ", the_matching)

	the_weight_difference = 0

	for i in range(len(the_matching)):
		if the_genome.genes[i][0] in the_matching:
			the_weight_difference = the_weight_difference + abs(the_genome.genes[i][1] - the_champion.genes[i][1])


	print("checking the weight difference ", the_weight_difference)


	the_disjoint = (the_innovation_set_of_the_genome -  the_innovation_set_of_the_champion) | (the_innovation_set_of_the_champion - the_innovation_set_of_the_genome) #getting the right number for the disjoint...it is intially equal to 0

	print("checking the disjoint ", the_disjoint)

	the_disjoint_contribution = len(the_disjoint)/ (len(max(the_innovation_set_of_the_genome, the_innovation_set_of_the_champion, key=len))) 

	the_weight_contribution = the_weight_difference / len(the_matching)

	the_result = the_disjoint_contribution + the_weight_contribution

	print("prinitg the genomic distance result before sending it ", the_result)
	#this returns proper value....then the error is somewhere else.......continuing isolation

	return the_result







#the driver code is here

the_core_object = the_core(3,1, population = 10)

print("printing the core object ", the_core_object)

#generating the population

the_population = the_core_object.generate_the_population()

print(len(the_population))

for i in range(len(the_population)):
	print("printing the fitness of the individual ", the_population[i].fitness)
	print("printig the links ", the_population[i].innovations)
	print("printing the genes ", the_population[i].genes)


