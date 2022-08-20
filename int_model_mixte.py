import os
import sys
import time

import docplex.mp

from docplex.mp.model import Model
from docplex.mp.progress import *

from collections import defaultdict

from arguments_model_mixte import Arguments
from instances import Instance
from solutions import Int_Solution



track_progress = list()
class MipGapPrinter(ProgressListener):

	def __init__(self):
		ProgressListener.__init__(self, ProgressClock.Gap)


	def notify_progress(self, pdata):
		gap = pdata.mip_gap
		ms_time = 1000* pdata.time
		obj = pdata.current_objective
		data = [int(pdata.current_objective), round(pdata.mip_gap*100, 2), round(pdata.time, 2)]
		track_progress.append(data)
		#print('-- new gap: {0:.1%}, time: {1:.0f} ms, obj :{2:.2f}'.format(gap, ms_time, obj))
		#print(track_progress)
		return track_progress


class Compact_Formulation_Mixte:
	""" 
	This class implement the new proposed model using gurobi 
	"""
	def __init__(self, inst):
		model = Model('OINT')
		# Variable set
		S_b = [(m,d,P) for m in inst.M for d in inst.D for P in range(len(inst.Rs[m]))]
		T_b = [(m,P) for m in inst.M for P in range(len(inst.Rt[m]))]
		X = [(i, j, f) for i in inst.D for j in inst.D for f in inst.F if i != j]
		Y = [(d,v,f) for d in inst.D for v in inst.V for f in inst.F]
		GG = [(i,f) for i in inst.D for f in inst.F]



		# Variables
		s_b = model.binary_var_dict(S_b, name='s_b')
		t_b = model.binary_var_dict(T_b, name='t_b')
		x = model.binary_var_dict(X, name='x')
		y = model.binary_var_dict(Y, name='y')
		s = model.integer_var_dict(S_b, name='s')
		t = model.integer_var_dict(T_b, name='t')
		gg = model.continuous_var_dict(GG, name='gg')


		# flow do not exceed capacity
		model.add_constraints(model.sum(inst.Size[v] * y[d, v, f] for d in inst.path[f] for v in inst.G.nodes[d]['Items']) <=  inst.Kf[f] for f in inst.GF)
		model.add_constraints(model.sum(y[d,v,f] for d in [j for j in inst.D if j not in inst.path[f]] for v in inst.G.nodes[d]['Items'] ) <= 0 for f in inst.GF)
		#starting
		model.add_constraints(model.sum(x[inst.S[f], j, f] for j in inst.G.neighbors(inst.S[f])) == 1 for f in inst.FF)
		#ending
		model.add_constraints(model.sum(x[i, inst.E[f], f] for i in inst.G.neighbors(inst.E[f])) == 1 for f in inst.FF)
		#flow conservation
		model.add_constraints((model.sum(x[i, p, f] for i in inst.G.neighbors(p)) - model.sum(x[p, j, f] for j in inst.G.neighbors(p))) == 0 for p in inst.D for f in inst.FF if p != inst.S[f] and p != inst.E[f])
		# cycle elimination
		#MTZ
		model.add_constraints(gg[j,f] >= gg[i,f] + 1 - len(inst.D)*(1-x[i,j,f]) for i in inst.D for j in inst.D for f in inst.FF if i!=j)
		# eleminating cycle of size two
		model.add_constraints(x[i,j,f] + x[j,i,f] <= 1 for i in inst.D for j in inst.D for f in inst.FF if i!=j)
		##model.add_constraints(model.sum(x[i, j, f] for j in inst.G.neighbors(i)) <= 1 for i in inst.D for f in inst.FF)
		# limiting route length
		model.add_constraints(model.sum(x[i, j, f] for i in inst.D for j in inst.D if i!=j) <= inst.max_route - 1 for f in inst.FF)
		# collected items must belong to the path of the network flow f
		model.add_constraints(y[d,v,f] <= model.sum(x[i,d,f] for i in inst.G.neighbors(d)) for d in inst.D for v in inst.G.nodes[d]['Items'] for f in inst.FF)
		#single telemetry collected by single flows
		model.add_constraints(model.sum(y[d, v, f] for f in inst.F) <=1 for d in inst.D for v in inst.G.nodes[d]['Items'])
		# flow do not exceed capacity
		model.add_constraints(model.sum(inst.Size[v] * y[d, v, f] for d in inst.D for v in inst.G.nodes[d]['Items']) <=  inst.Kf[f] for f in inst.FF)
		# counting spatial
		model.add_constraints(s[m,d,P] == model.sum(y[d, v, f] for v in inst.Rs[m][P] for f in inst.F) for m in inst.M for d in inst.D for P in range(len(inst.Rs[m])))
		# count temporal
		model.add_constraints(t[m,P] == model.sum(y[d, v, f] for d in inst.D for v in inst.Rs[m][P] for f in inst.F) for m in inst.M for P in range(len(inst.Rt[m])) if inst.HH[P] > inst.TT[P])
			
		# satisfied spatial	
		model.add_constraints(s_b[m,d,P] <= s[m,d,P]/len(inst.Rs[m][P]) for m in inst.M for d in inst.D for P in range(len(inst.Rs[m])))
		# satisfied temporal
		model.add_constraints(t_b[m,P] <= t[m,P]/len(inst.Rt[m][P]) for m in inst.M for P in range(len(inst.Rt[m])))

		# Objective Function
		obj_function = model.sum(s_b[m,d,P] for m,d,P in S_b) + sum(t_b[m,P] for m,P in T_b)
		model.maximize(obj_function)


		# creating class variables
		self.inst = inst
		self.model = model
		self.s_b = s_b
		self.t_b = t_b
		self.x = x
		self.y = y
		self.solution_model = None


	def optimize(self):
		# connect a listener to the model
		self.model.add_progress_listener(MipGapPrinter())
		# setting cplex parameters
		self.model.parameters.timelimit.set(900)
		start_time = time.time()
		solution = self.model.solve(log_output = True)
		#status = self.model.optimize(max_seconds=1000)
		end_time = time.time()
		##status = self.model.solution.solve_status
		##print(status)
		
		
		
		
		Solution_Runtime = round((end_time - start_time),2)
		Gap = round((self.model.solve_details.mip_relative_gap)*100,2)
		UB = int(self.model.solution.solve_details.best_bound)
		Obj_value = int(self.model.solution.objective_value)
		

		# creting the final solution
		self.solution_model = Int_Solution(self.inst, cost=int(self.model.solution.objective_value))


		self.solution_model.add_gap_time(Gap)
		self.solution_model.add_gap_time(Solution_Runtime)
		
		
		
		Flow_Path_dict ={} # initate a dictionary for saving the flow path
		for f in inst.FF:
			ori = inst.S[f]
			tour = [ori]
			while True:
				ori = [i for i in inst.D if ori!=i and self.x[ori, i, f].solution_value == 1][0]
				#print(ori)
				tour.append(ori)
				#print(tour)
				if ori == inst.E[f] :
					break
			
			Flow_Path_dict[f] = tour
		
		#print(Flow_Path_dict)
		
						
		
		# spatial dependencies
		#spa = [ 1 for m in inst.M for d in inst.D for P in range(len(inst.Rs[m])) if s_b[m,d,P].solution_value == 1]
		spa = list()
		if solution != None:
			for m in self.inst.M:
				for d in self.inst.D:
					if len(inst.Rsd[m,d]) > 0:
						for P in range(len(self.inst.Rsd[m,d])):
							if self.s_b[m,d,P].solution_value == 1:
								data = [m,d,P]
								spa.append(data)
								self.solution_model.add_spatial(data)

		# number of spatial					
		Nb_spa = len(spa)

		# temporal dependencies
		#tempo = [ 1 for m in M for P in range(len(Rs[m])) if t_b[m,P].solution_value == 1]
		tempo = list()
		if solution != None:
			for m in self.inst.M:
				for P in range(len(self.inst.Rt[m])):
					if self.t_b[m,P].solution_value == 1:
						data = [m,P]
						tempo.append(data)
						self.solution_model.add_temporal(data)

		# number of temporal					
		Nb_tempo = len(tempo)

		# collected telemtry items
		collect = list()
		if solution != None:
			for d in self.inst.D:
				for v in self.inst.V_d[d]:
					for f in self.inst.F:
						if self.y[d,v,f].solution_value == 1:
							data = [d,v,f]
							collect.append(data)
							self.solution_model.add_telemetry(data)


		# number of items
		Nb_items = len(collect)



		#computing collected item by each flow
		collected_f = defaultdict(list)
		for d in self.inst.D:
			for v in self.inst.V_d[d]:
				for f in self.inst.F:
					if self.y[d,v,f].solution_value == 1:
						data = [v]
						#collected_f[f].append(v)
						collected_f[f].append(inst.Size[v])

		#self.solution.add_flow_items(collected_f)

		flow_collect = {}
		for f in inst.F:
			if f in collected_f.keys():
				flow_collect[f] = sum(collected_f[f])

		self.solution_model.add_flow_items(flow_collect)


		Sol_info = [len(inst.D),len(inst.F), Nb_spa, Nb_tempo, Nb_items, Obj_value, UB, Gap, Solution_Runtime]
		Sol_data = [Flow_Path_dict, spa, tempo, collect] # to update on server
		return Sol_info, Sol_data





if __name__ == "__main__":
	arg = Arguments(sys.argv)


	start_time = time.time()
	
	# creating folders 'runs', 'logs' and 'solutions' if they don't exist already
	if not os.path.exists('logs/hybrid/' + os.path.basename(os.path.dirname(arg.instance)) + '/' + os.path.basename(arg.instance) + '/' + str(arg.num_nodes) + '_' + str(arg.num_items) + '_' + str(arg.num_mon_app) + '/' + str(arg.num_given_flow) + '_' + str(arg.max_route)):
		os.makedirs('logs/hybrid/' + os.path.basename(os.path.dirname(arg.instance)) + '/' + os.path.basename(arg.instance) + '/' + str(arg.num_nodes) + '_' + str(arg.num_items) + '_' + str(arg.num_mon_app) + '/' + str(arg.num_given_flow) + '_' + str(arg.max_route))
		
	if not os.path.exists('runs/' + os.path.basename(os.path.dirname(arg.instance)) + '/' + os.path.basename(arg.instance) + '/' + str(arg.num_nodes) + '_' + str(arg.num_items) + '_' + str(arg.num_mon_app) + '/' + str(arg.num_given_flow) + '_' + str(arg.max_route)):
		os.makedirs('runs/' + os.path.basename(os.path.dirname(arg.instance)) + '/' + os.path.basename(arg.instance) + '/' + str(arg.num_nodes) + '_' + str(arg.num_items) + '_' + str(arg.num_mon_app) + '/' + str(arg.num_given_flow) + '_' + str(arg.max_route))
	
	#if not os.path.exists('solutions/' + os.path.basename(arg.instance)):
	#	os.makedirs('solutions/' + os.path.basename(arg.instance))
		
	if not os.path.exists('solutions/hybrid/' + os.path.basename(os.path.dirname(arg.instance)) + '/' + os.path.basename(arg.instance) + '/' + str(arg.num_nodes) + '_' + str(arg.num_items) + '_' + str(arg.num_mon_app) + '/' + str(arg.num_given_flow) + '_' + str(arg.max_route)):
		os.makedirs('solutions/hybrid/' + os.path.basename(os.path.dirname(arg.instance)) + '/' + os.path.basename(arg.instance)+ '/' + str(arg.num_nodes) + '_' + str(arg.num_items) + '_' + str(arg.num_mon_app) + '/' + str(arg.num_given_flow) + '_' + str(arg.max_route))




	inst = Instance(path_data = arg.instance, num_nodes = arg.num_nodes, edges_to_attach = arg.edges_to_attach, num_flows = arg.num_flows, num_given_flow = arg.num_given_flow, max_route =arg.max_route, min_size = arg.min_size, max_size = arg.max_size, num_items = arg.num_items, num_mon_app = arg.num_mon_app)
	formulation = Compact_Formulation_Mixte(inst)
	Sol_info, Sol_data = formulation.optimize()


	solution = Int_Solution(inst)
	formulation.solution_model.print_solution()
	formulation.solution_model.write(path = arg.out)

	solution.write_solution(Sol_info, path = arg.out1)
	solution.write_solution_flows_path(Sol_data[0], path = arg.out2)
	solution.write_solution_spatial_temporal_collect(Sol_data[1], path = arg.out3)
	solution.write_solution_spatial_temporal_collect(Sol_data[2], path = arg.out4)
	solution.write_solution_spatial_temporal_collect(Sol_data[3], path = arg.out5)
	solution.write_solution_spatial_temporal_collect(track_progress, path = arg.out6)
	

	print("Total runtime: %.2f seconds" % (time.time() - start_time))
