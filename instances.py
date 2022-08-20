# My principal Module
import numpy as np
import pandas as pd
import random
import networkx as nx
import csv
import collections
from collections import defaultdict
#import pylab as plt
from ast import literal_eval
import os
import itertools
from random import randint

seed = 2021

random.seed(seed)

class Instance:
	"""
	This class represents an instance of the IN-Band Network Telemetry
	"""


	def __init__(self, path_data, num_nodes, edges_to_attach, num_flows, num_given_flow, max_route, min_size, max_size, num_items, num_mon_app):
	#def __init__(self, path, max_route, num_items, num_mon_app):
		self.path_data = path_data
		self.num_nodes = num_nodes
		self.num_flows = num_flows
		self.num_given_flow = num_given_flow
		self.num_mon_app = num_mon_app
		#D = [d for d in range(num_nodes)]
		#F = [f for f in range(num_flow)]
		F = list()
		#GF = [i for i in range(num_given_flow)]
		#FF = [f for f in F if f not in GF]
		V = [v for v in range(num_items)]
		M = [m for m in range(num_mon_app)]
		#Size = {0:1,1:2,2:1,3:3,4:1,5:3,6:2,7:1}
		##Size = {0: 3, 1: 1, 2: 5, 3: 3, 4: 5, 5: 3, 6: 3, 7: 2, 8: 4, 9: 3, 10: 2, 11: 4, 12: 1, 13: 2, 14: 5, 15: 2, 16: 1, 17: 5}
		V_d = defaultdict(list)
		
		Size = {}
		#self.GF = GF
		#self.FF = FF
		S = {}
		E = {}
		Kf = {}
		#C = np.zeros((int(np.sqrt(num_nodes)), int(np.sqrt(num_nodes))))
		C = np.zeros(shape=(num_nodes,num_nodes))
		self.max_route = max_route - 1
		#self.D = D
		self.F = F
		self.V = V
		self.M = M
		self.S = S 
		self.E = E
		self.Kf = Kf
		self.path = {}
		self.path_mixte = {}
		self.Size = Size
		self.V_d = V_d
		self.C = C

		#network_csv = open(os.path.join(self.path, "network.csv"), "r")
		##network_csv = open(os.path.join(self.path_data, "Barabasi_" + str(self.num_nodes) + "_" + str(edges_to_attach) + ".csv"), "r")
		network_csv = open(os.path.join(self.path_data, "Int_Network_" + str(self.num_nodes) + ".csv"), "r")
		G = nx.Graph()
		#G.add_nodes_from(D)
		for line in network_csv.readlines():
			#data = line.split(",")
			data = line.strip().split(",")
			G.add_edge(int(data[0]), int(data[1]), weight=int(data[2]))
			#G.add_edge(data[0], data[1], data[2])
			#C[data[0]][data[1]] = data[2]
			C[int(data[0])][int(data[1])] = int(data[2])
		network_csv.close()


		D = list(G.nodes)
		self.D = D
		self.G = G

		# adding items size
		for v in V:
			#self.Size[v] = random.randint(1,5)
			#self.Size[v] = random.randint(min_size,max_size)
			self.Size[v] = random.randrange(min_size,max_size+min_size, min_size)
		# adding atribuate to the nodes
		
		for d in D:
			#t = random.randint(1, num_items)
			t = num_items
			V_d[d] = random.sample(range(num_items), t)
			V_d[d].sort(reverse=False)
			#G.nodes[d]['Items'] = V
		self.V_d = V_d
		#print(V_d)
		

		for d in D:
			G.nodes[d]['Items'] = V_d[d]
		
		#self.G = G
		#print("--------------------")
		#print(G.nodes[5]['Items'])
		#print(V_d[5])

		""" telemetry_items_csv = open(os.path.join(self.path, "items_size.csv"), "r")
		for i, line in enumerate(telemetry_items_csv.readlines()):
			data = line.split(",")
			self.Size[i] = int(data[0]) """

		# adding monitoring application
		lenth_of_monitoring_applications = int(num_items / num_mon_app)
		spatial_requirements = [V[i * lenth_of_monitoring_applications:(i + 1) * lenth_of_monitoring_applications] for i in range((len(V) + lenth_of_monitoring_applications - 1) // lenth_of_monitoring_applications )]
		R = {}
		for m in M:
			R[m] = spatial_requirements[m]

		self.R = R
		self.lenth_of_monitoring_applications = lenth_of_monitoring_applications
		self.spatial_requirements = spatial_requirements

		
		# reading the endpoints
		#network_path_csv = open(os.path.join(self.path, "flow_path.csv"), "r")
		network_path_csv = open(os.path.join(self.path_data, str(self.num_nodes) + "_" + str(self.num_flows) + "_" + str(min_size) + "_" + str(max_size) + ".csv"), "r")
		for line in network_path_csv.readlines():
			data = line.split(",")
			self.F.append(int(data[0]))
			self.S[int(data[0])] = int(data[1])
			self.E[int(data[0])] = int(data[2])
			self.Kf[int(data[0])] = int(data[3])
		network_path_csv.close()

		
		GF = [i for i in range(int((num_given_flow * len(self.F) / 100)))]
		FF = [f for f in F if f not in GF]
		self.GF = GF
		self.FF = FF

		# reading flow path
		#flow_path_txt = open(os.path.join(self.path_data, "flow_short_path.txt"), "r")
		flow_short_path = open(os.path.join(self.path_data, "Short_" + str(self.num_nodes) +  "_" + str(self.num_flows) + "_" + str(min_size) + "_" + str(max_size) + ".txt"), "r" )
		for line in flow_short_path.readlines():
			(key, val) = line.split(":")
			self.path[int(key)] = literal_eval(val)
		flow_short_path.close()

		# reading flow path for the mixte model
		flow_mixte_path = open(os.path.join(self.path_data, "Short_" + str(self.num_nodes) +  "_" + str(self.num_flows) + "_" + str(min_size) + "_" + str(max_size) + ".txt"), "r" )
		for line in flow_mixte_path.readlines():
			(key, val) = line.split(":")
			if int(key) in self.GF:
				self.path_mixte[int(key)] = literal_eval(val)
		flow_mixte_path.close()


	#def ST_Dependency(self):
		PR = {}
		for m in self.M:
			PR[m] = all_subsets(self.R[m])
		#self.PR = PR
		# spatial dependency
		Rs = {}
		for m in self.M:
			Rs[m] = PR[m] 
		# temporal dependency
		Rt = {}
		for m in self.M:
			Rt[m] = PR[m]
		#return PR, Rs, Rt

		Rd = {}
		Rsd = {}
		for m in self.M:
			for d in self.D:
				Rd[m,d] = [t for t in R[m] if t in self.V_d[d]]
				Rsd[m,d] = all_subsets(Rd[m,d])

		#Rsd = {}
		#for m in self.M:
		#	for d in self.D:
		#		Rsd[m,d] = all_subsets(Rd[m,d])


		self.PR = PR
		self.Rs = Rs
		self.Rt = Rt
		self.Rsd = Rsd

		# reading required deadlines
		TT = {}
		for m in self.M:
			for P in range(len(self.Rs[m])):
				TT[P] = randint(0, 20)

		HH = {}
		for m in self.M:
			for P in range(len(self.Rt[m])):
				HH[P] = randint(0, 20)

		self.TT = TT
		self.HH = HH


def all_subsets(ss):
	subsets = itertools.chain(*map(lambda x: itertools.combinations(ss, x), range(0, len(ss) + 1)))
	return [S for S in subsets if len(S) >= 1]
		

"""
#inst = Instance('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/New_Implememntation/INT_Gurobi/INT_Class', 50, 50, 9, 8, 4)
inst = Instance('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/New_Implememntation/INT_Gurobi/INT_Class', 9, 8, 4)


print(inst.G.nodes)
print("-----------------------------------")
print(inst.G.nodes[2]['Items'])
print("-----------------------------------")
#print(inst.S)
print("-----------------------------------")
#print(inst.E)
print("-----------------------------------")
#print(inst.Kf)
print("-----------------------------------")
print(inst.Size)
print("-----------------------------------")
print(inst.R)
print(inst.lenth_of_monitoring_applications)
print("-----------------------------------")
print(all_subsets([1,2,3,4]))
print("-----------------------------------")
#print(inst.ST_Dependency())
print(inst.PR)
print("-----------------------------------")
print(inst.TT)
print("-----------------------------------")
print(inst.HH)
"""
