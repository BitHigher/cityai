# 
# File: calc.py
# Author: zhuhanfeng
# Date: 2013.5.6
#

from random import randint, random
import math

def random_point():
	x = randint(0, 1000)
	y = randint(0, 1000)
	return (x, y)

def random_points(n_points):
	return [random_point() for i in xrange(n_points)]
	
def distance(p1, p2):
	return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

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

def costf(sol, groups):
	k = len(sol)
	cost = [[] for i in range(k)]
	for i in range(k):
		for group in groups:
			gsum = 0.0
			for p in group:
				gsum += distance(sol[i], p)
			gsum /= 100000000
			cost[i].append(gsum)

	result = 0.0
	for i in range(k):
		cost[i] = sorted(cost[i])
		for j in range(k):
			result += cost[i][j] * pow(2, k-j-1)
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

	return best_sol, best_cost

def test():
	points = random_points(10000)
	centers, groups = kmeans(points, 8)	
	sol, cost = annealing(groups, centers)
#	print sol, cost

#	from matplotlib import pyplot as plt
#	for group in groups:
#		plt.plot([i for (i,j) in group], [j for (i, j) in group], '2')	

#	plt.plot([i for(i,j) in centers], [j for (i,j) in centers], 'ro')
#	plt.plot([i for(i,j) in sol], [j for (i,j) in sol], '*')
	
#	plt.show()

if __name__ == '__main__':
	test()
