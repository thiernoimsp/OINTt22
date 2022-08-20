import networkx as nx
import matplotlib.pyplot as plt
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from collections import defaultdict
import pandas as pd

import csv
import os
import sys
from ast import literal_eval

from arguments_lattice import Arguments

seed = 2022

random.seed(seed)


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        #self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        #self.weights[(to_node, from_node)] = weight


# creating instance of the graph
graph = Graph()


class Int_Generating_Data:
	def __init__(self, path, grid_size, num_nodes, num_flows):
		self.path = path
		self.grid_size = grid_size
		self.num_nodes = num_nodes
		self.num_flows = num_flows
		self.flow_data = list()
		self.G = nx.Graph()
		self.F = list()
		self.S = {}
		self.E = {}
		self.Flows_Short_Path = list()
		self.Flows_Short_Path_Dict = {}








	def Generating_Flows_Data(self, min_size, max_size) :
		i = 0
		while (i<self.num_flows) :
			a = random.randint(0, self.num_nodes - 1)
			b = random.randint(0, self.num_nodes - 1)
			if a!=b :
				#data = [i,a,b,random.randint(min_size,max_size)]
				data = [i,a,b,random.randrange(min_size,max_size+min_size, min_size)]
				self.flow_data.append(data)
				i = i + 1


	def INT_Lattice(self, num_nodes):
		path = os.path.join(self.path, "Int_Network_" + str(self.num_nodes))
		#N = int(num_nodes/4)
		N = self.grid_size
		G=nx.grid_2d_graph(N,N)
		labels = dict( ((i, j), i + (N-1-j) * N ) for i, j in G.nodes() )
		arete = list()        
		for i in G.edges:
			G[i[0]][i[1]]["weight"] = random.randint(5,10)
			arete.append([labels[i[0]], labels[i[1]], G[i[0]][i[1]]["weight"]])
			arete.append([labels[i[1]], labels[i[0]], G[i[1]][i[0]]["weight"]])
		
		with open(path+".csv", 'w', newline='') as ff:
			writer = csv.writer(ff, lineterminator='\n')
			for nnn in arete : 
				writer.writerow(nnn)



	def write(self, min_size, max_size):
		path = os.path.join(self.path, str(self.num_nodes) + "_" + str(self.num_flows) + "_" + str(min_size) + "_" + str(max_size))
		with open(path+".txt", 'w', newline='') as ff: 
			for nnn in self.flow_data : 
				#ff.write(str(line)) 
				res = str(nnn)[1:-1]
				ff.write("%s\n" % res)


		with open(path+".csv", 'w', newline='') as ff:
			writer = csv.writer(ff, lineterminator='\n')
			for nnn in self.flow_data : 
				writer.writerow(nnn)



	def shortest(self, graph, min_size, max_size):
		links = list()
		# loding the network infrastructure
		network_csv = open(os.path.join(self.path, "Int_Network_" + str(self.num_nodes) + ".csv"), "r")
		for line in network_csv.readlines():
			data = line.split(",")
			links.append((int(data[0]), int(data[1]), 1))
		network_csv.close()
		for edge in links:
			graph.add_edge(*edge)

		#loading active network flows data
		network_path_csv = open(os.path.join(self.path, str(self.num_nodes) + "_" + str(self.num_flows) + "_" + str(min_size) + "_" + str(max_size) + ".csv"), "r")
		for line in network_path_csv.readlines():
			#self.F.append(f)
			data = line.split(",")
			self.F.append(int(data[0]))
			self.S[int(data[0])] = int(data[1])
			self.E[int(data[0])] = int(data[2])
		network_path_csv.close()



	def dijsktra(self, graph):
		for f in self.F:
			initial = self.S[f]
			end = self.E[f]

			shortest_paths = {initial: (None, 0)}
			current_node = initial
			visited = set()

			while current_node != end:
				visited.add(current_node)
				destinations = graph.edges[current_node]
				weight_to_current_node = shortest_paths[current_node][1]

				for next_node in destinations:
					weight = graph.weights[(current_node, next_node)] + weight_to_current_node
					if next_node not in shortest_paths:
						shortest_paths[next_node] = (current_node, weight)
					else:
						current_shortest_weight = shortest_paths[next_node][1]
						if current_shortest_weight > weight:
							shortest_paths[next_node] = (current_node, weight)

				next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
				if not next_destinations:
					return "Route Not Possible"
				# next node is the destination with the lowest weight
				current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

			# Work back through destinations in shortest path
			path = []
			while current_node is not None:
				path.append(current_node)
				next_node = shortest_paths[current_node][0]
				current_node = next_node

			# Reverse path
			path = path[::-1]
			self.Flows_Short_Path.append(path)
			self.Flows_Short_Path_Dict[f] = path #appending the dictionary with the short path





	def write_flows_path(self, min_size, max_size) :
		#os.makedirs(os.path.dirname(filename), exist_ok=True)
		path = os.path.join(self.path, "Short_" + str(self.num_nodes) +  "_" + str(self.num_flows) + "_" + str(min_size) + "_" + str(max_size))
		with open(path+".txt", 'w', newline='') as ff:
			for k,v in self.Flows_Short_Path_Dict.items():
				#s = str(k)+" "+ str(v) +"\n"
				s = str(k)+":"+ str(v) +"\n"
				ff.write(s)



if __name__ == "__main__":
	arg = Arguments(sys.argv)

	data = Int_Generating_Data(path = arg.instance, grid_size = arg.grid_size, num_nodes = arg.num_nodes, num_flows = arg.num_flows)

	if not os.path.exists(arg.instance):
		os.makedirs(arg.instance)

	#generating network infrastructure
	#data.INT_Barabasi(arg.num_nodes, arg.edges_to_attach)
	data.INT_Lattice(arg.num_nodes)

	#genrating flows data and saving them 
	data.Generating_Flows_Data(min_size = arg.min_size, max_size = arg.max_size)
	data.write(min_size = arg.min_size, max_size= arg.max_size)

	#generating flows path and saving them
	data.shortest(graph = graph, min_size=arg.min_size, max_size=arg.max_size)
	data.dijsktra(graph)
	data.write_flows_path(min_size=arg.min_size, max_size=arg.max_size)
