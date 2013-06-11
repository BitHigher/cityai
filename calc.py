# 
# File: calc.py
# Author: zhuhanfeng
# Date: 2013.5.6
#

from random import randint, random
import math

g_weight_points = None
g_weight = None
g_use_weight = False

def random_point():
	x = randint(0, 1000)
	y = randint(0, 1000)
	return (x, y)

def random_points(n_points):
	return [random_point() for i in xrange(n_points)]
	
def distance(p1, p2):
	return pow((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2, 0.5)

def kmeans(points, k):
	# random k centers
	centers = random_points(k)
	groups = [[] for i in range(k)]

	looping = True
	while(looping):
		for p in points:
			best_group = 0
			best_dist = distance(p, centers[0])
			for i in range(1, k):
				dist = distance(p, centers[i])
				if dist < best_dist:
					best_dist = dist
					best_group = i
			groups[best_group].append(p)

		# choose new centers from each group
		new_centers = [0 for i in range(k)]
		for i in range(k):
			n = len(groups[i])
			x = sum([p[0] for p in groups[i]])
			y = sum([p[1] for p in groups[i]])
			if n == 0:
				new_centers[i] = random_point()
			else:
				new_centers[i] = (x/float(n), y/float(n))

		if centers == new_centers:
			break
		else:
			centers = new_centers
			groups = [[] for i in range(k)]
	
	return centers, groups

def costf_old(sol, groups):
	k = len(sol)
	cost = [[] for i in range(k)]
	for i in range(k):
		for group in groups:
			gsum = 0.0
			for p in group:
				if g_use_weight and p in g_weight_points[i]:
					gsum += distance(sol[i], p)*g_weight
				else:
					gsum += distance(sol[i], p)
					
			gsum /= 100000000
			cost[i].append(gsum)

	result = 0.0
	for i in range(k):
		cost[i] = sorted(cost[i])
		for j in range(1):
			result += cost[i][j] * pow(2, k-j-1)
	return result

def costf(sol, groups):
	k = len(groups)
	result = 0
	for i in range(k):
		gsum = 0
		for p in groups[i]:
			if g_use_weight and p in g_weight_points[i]:
				gsum += distance(sol[i], p)*g_weight
			else:
				gsum += distance(sol[i], p)		
		
		result += gsum / 10000.0
	return result

def random_smooth_sol(current_sol):
	sol = current_sol[:]
	index = randint(0, len(current_sol)-1)
	x = sol[index][0] + random()*20 - 10.0
	y = sol[index][1] + random()*20 - 10.0
	sol[index] = (x, y)
	return sol

def annealing(groups, centers, T=10000.0, cool=0.95):
	best_sol = centers
	best_cost = costf(best_sol, groups)

	while T > 0.1:
		T *= cool
		sol = random_smooth_sol(best_sol)
		cost = costf(sol, groups)

		if cost < best_cost or random() < math.exp(-(cost-best_cost)/T):
			best_cost = cost
			best_sol = sol

	return best_cost, best_sol

def genetic(groups, centers, popsize=50, 
			mutprob=0.2, elite=0.2, maxiter=100):
	
	def mutate(sol):
		new_sol = sol[:]
		i = randint(0, len(sol)-1)
		x = sol[i][0] + random()*20.0 - 10.0
		y = sol[i][1] + random()*20.0 - 10.0
		sol[i] = (x,y)
		return sol
	
	def crossover(sol1, sol2):
		i = randint(1, len(sol1)-2)
		return sol1[0:i] + sol2[i:]

	# build the initial population
	pop = []
	pop.append(centers)
	for i in range(1, popsize):
		pop.append(mutate(pop[i-1]))

	topelite = int(elite*popsize)

	# main loop
	for i in range(maxiter):
		scores = [(costf(v, groups), v) for v in pop]
		scores.sort()
		ranked = [v for (s, v) in scores]	
		
		# start with winners
		pop = ranked[0: topelite]

		# add mutated and crossover of winners
		while len(pop) < popsize:
			if random() < mutprob:
				c = randint(0, topelite)
				pop.append(mutate(ranked[c]))
			else:
				c1 = randint(0, topelite)
				c2 = randint(0, topelite)
				pop.append(crossover(ranked[c1], ranked[c2]))
	
	return scores[0]

def select_weight_points(groups, area=100):
	k = len(groups)
	num = 0
	result = [[] for i in range(k)]
	for i in range(k):
		index = randint(0, len(groups[i])-1)
		x = groups[i][index][0]
		y = groups[i][index][1]

		for (px, py) in groups[i]:
			if px >= (x-area) and px <= (x+area) and \
				py >= (y-area) and py <= (y+area):
				result[i].append((px, py))
				num += 1

	global g_weight_points
	g_weight_points = result
	return num

def get_method_from_input():
	strm = raw_input("\n[Select Optimizator:" 
						"Annealing or Genetic or Quit(A/G/Q)]:")
	strm = strm.strip()

	method = None

	if strm == 'A' or strm == 'a':
		print 'Annealing is selected, computing...'
		method = annealing
	elif strm == 'G' or strm == 'g':
		print 'Genetic is selected, computing...'
		method = genetic
	else:
		print 'Unknown Optimizator, exiting...'
		exit(1)
	return method	

def plot_result(groups, centers, sol, w_sol):	
	from matplotlib import pyplot as plt
	for group in groups:
		plt.plot([i for (i,j) in group], [j for (i, j) in group], 'x')	

	for w in g_weight_points:
		plt.plot([i for (i,j) in w], [j for (i,j) in w], 'b.')
	
	plt.plot([i for(i,j) in centers], [j for (i,j) in centers], 'ro')
	plt.plot([i for(i,j) in sol], [j for (i,j) in sol], 'go')
	plt.plot([i for(i,j) in w_sol], [j for (i,j) in w_sol], 'ko')

	plt.show()

def test():
	num_points = int(raw_input("\n[Number of all points]:"))
	k = int(raw_input("[Number of groups]:"))
	if(k > num_points):
		print "There must be more points than groups"
		exit(1)

	print "Number of points:", num_points
	print "Number of groups:", k

	points = random_points(num_points)
	centers, groups = kmeans(points, k)
	w_num = select_weight_points(groups)
	print "Number of weighted points:", w_num

	while True:
		global g_use_weight
		g_use_weight = False
		method = get_method_from_input()	
		cost, sol = method(groups, centers)
		print "Total Cost:", cost
		print "Weighted Points cost:", costf(sol, g_weight_points)

		global g_weight
		g_weight = int(raw_input("[Please input weight]:"))
		g_use_weight = True
		print "Weight is set to ", g_weight, ", computing..."
		w_cost, w_sol = method(groups, centers)
		
		g_use_weight = False
		weighted_cost = costf(w_sol, g_weight_points)
		print "Total Cost:", w_cost - weighted_cost*(g_weight-1)
		print "Weighted Points cost:", costf(w_sol, g_weight_points)

		strm = raw_input("[Plot the result(y/N)]:")
		if(strm == 'Y' or strm == 'y'):
			print 'Ploting...'
			plot_result(groups, centers, sol, w_sol)

if __name__ == '__main__':
	test()
