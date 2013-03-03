from random import randint, random
import matplotlib.pyplot as plt
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
	centers = [random_point() for i in range(k)]
	parts = [[] for i in range(k)]

	looping = True
	while looping:
		for p in points:
			best_c = 0
			best_dist = distance(p, centers[0])
			for i in range(1, len(centers)):
				dist = distance(p, centers[i])
				if dist < best_dist:
					best_dist = dist
					best_c = i
			parts[best_c].append(p)

		# choose the new centers according parts
		new_centers = []
		for i in range(k):
			n = len(parts[i])
			x = sum([p[0] for p in parts[i]])
			y = sum([p[1] for p in parts[i]])
			if n == 0:
				new_centers.append(random_point())
			else:
				new_centers.append((x/float(n), y/float(n)))

		if centers == new_centers:
			break;
		else:
			centers = new_centers
			parts = [[] for i in range(k)]
	return centers, parts

# ATTENTION!!! most important
def costf(sol, parts):
	cost = 0.
	for c in sol:
		for points in parts:
			for p in points:
				cost += distance(c, p)
	return cost/10000000

def random_smooth_sol(current_sol):
	sol = current_sol[:]
	index = randint(0, len(current_sol)-1)
	x = sol[index][0] + random()*20 - 10.0
	y = sol[index][1] + random()*20 - 10.0
	sol[index] = (x, y)
	return sol

def anneal(parts, centers, T=10000.0, cool=0.95):	
	best_sol = centers
	best = costf(centers, parts)

	best_array = [best]
	cost_array = [best]
	while T > 0.1:
		sol = random_smooth_sol(best_sol)
		cost = costf(sol, parts)
		if cost < best or random() < math.exp(-(cost-best)/T):
			best = cost
			best_sol = sol

		best_array.append(best)
		cost_array.append(cost)
		T *= cool

	return best_sol, best, best_array, cost_array


def plot_points(parts, centers):
	for points in parts:
		plt.plot([p[0] for p in points], [p[1] for p in points], 'x')
	
	plt.plot([p[0] for p in centers], [p[1] for p in centers], 'ro')
	return plt	

def test(n_points, k):
	points = random_points(n_points)
	centers, parts = kmeans(points, k)
	sol, cost, best_array, cost_array = anneal(parts, centers)

	plt = plot_points(parts, centers)
	plt.plot([p[0] for p in sol], [p[1] for p in sol], 'go')
	plt.savefig('anneal_result.png')

	
	x = [i for i in xrange(len(best_array))]
	plt.clf()
	plt.plot(x, cost_array, 'b')
	plt.plot(x, best_array, 'r')
	plt.savefig('annealing.png')


if __name__ == '__main__':
	test(10000, 5)
