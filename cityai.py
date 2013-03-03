#!/usr/bin/python
# -*- coding: UTF-8 -*-
from random import randint, random
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import math

def random_points(num):
	points = []
	for i in range(num):
		points.append((randint(0, 1000), randint(0, 1000)))
	
	return points

def draw_points(points, clusters, centers, bestsol):
	plt.figure(figsize=(20, 20))

	for pindice in clusters:
		plt.plot([points[i][0] for i in pindice], 
				[points[i][1] for i in pindice], 'x--', ms=5.0);

	plt.plot([p[0] for p in centers],
			[p[1] for p in centers], 'bo', markersize=10.0);


	plt.plot([p[0] for p in bestsol],
			[p[1] for p in bestsol], 'ro', markersize=10.0);
	
	plt.savefig('points.png')

def distance(v1, v2):
	length = min(len(v1), len(v2))
	total = 0.0
	for i in range(length):
		total += (v1[i] - v2[i])**2
	return sqrt(total)


def kmeans(points, k, iterations=100):
	# calculate the range of each dimension
	ds = len(points[0])
	ranges = [(min(p[i] for p in points), max(p[i] for p in points))
				for i in range(ds)]
	
	centers = [[random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(ds)]
				for j in range(k)]

	while(iterations > 0):
		iterations -= 1
		clusters = [[] for i in range(k)]
		newcenters = [[0 for i in range(ds)] for j in range(k)]
		for i in range(len(points)):
			minVal = distance(points[i], centers[0])
			minIndex = 0
			for j in range(1,k):
				curVal = distance(points[i], centers[j])
				if curVal < minVal:
					minVal = curVal
					minIndex = j
			clusters[minIndex].append(i)
			newcenters[minIndex] = [newcenters[minIndex][j] + points[i][j] for j in range(ds)]

		for i in range(k):
			length = float(len(clusters[i]))
			if length == 0: length = 1.0
			for j in range(ds):
				newcenters[i][j] /= length

		if(newcenters == centers):
			break
		else:
			centers = newcenters

	print iterations
	return centers, clusters

def cost(points, sol):
	cost = 0.0
	
	for p in points:
		for i in range(len(sol)/2):
			cost += 1 - 1000/distance(p, (sol[2*i], sol[2*i+1]))
	return cost

def annealing(points, sol, costf=cost, step=5, T=10000.0, cool=0.95):
	best = costf(points, sol)
	bestsol = sol

	anneal = []
		
	while T > 0.1:
		# random a index
		index = randint(0, len(sol)-1)
		# random a change
		change = step
		if(random() < 0.5):
			change = -step

		bestsol[index] += change
		curcost = costf(points, bestsol)
        
		if (curcost < best or random() < pow(math.e, -(curcost-best)/T)):
			best = curcost
		else:
			bestsol[index] -= change

		anneal.append((T, best, curcost))
		T *= cool

	return best, bestsol, anneal

def main():
	points = random_points(10000)
	centers, clusters  = kmeans(points, 8)

	sol = []
	for p in centers:
		sol.append(p[0])
		sol.append(p[1])


	best, bestsol, anneal = annealing(points, sol)
	bestsol = [(bestsol[2*i], bestsol[2*i+1]) for i in range(len(bestsol)/2)]
	draw_points(points, clusters, centers, bestsol)

#	print anneal
	#draw anneal trend
	plt.cla()
	plt.figure(figsize=(20, 8))
	plt.plot([i for i in range(len(anneal))],[p[2] for p in anneal],"gx-")
	plt.plot([i for i in range(len(anneal))],[p[1] for p in anneal],"ro-")
	plt.savefig('anneal.png')

main()

