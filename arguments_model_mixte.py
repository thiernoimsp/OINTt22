import os


class Arguments:
	"""
	Let the user enter the argument via command line.
	"""


	def __init__(self, argv, prefix=""):
		if len(argv) != 10:
			usage(argv)
        
		# initializing default values
		self.instance = argv[1]
		self.num_nodes = int(argv[2])
		self.num_flows = int(argv[3])
		self.num_items = int(argv[4])
		self.num_mon_app = int(argv[5])
		self.num_given_flow = int(argv[6])
		self.min_size = int(argv[7]) #1#10
		self.max_size = int(argv[8]) #4#40
		self.edges_to_attach = 2
		self.max_route = int(argv[9]) #17
		#self.num_given_flow = 30
		#self.out_ntk = os.path.join("solutions", "Barabasi_" + prefix + os.path.basename(argv[2])) + "_" + str(self.edges_to_attach)
		#self.out = os.path.join("solutions", "model_mixte_" + prefix + os.path.basename(argv[2])) + "_" + str(self.edges_to_attach)
		self.out = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_out_" + argv[2]) + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]
		#self.out1 = os.path.join("solutions", "mixte" + prefix + os.path.basename(argv[2])) + "_" + str(self.edges_to_attach) + "_" + argv[6] + "_" + argv[4] + "_" + argv[5]
		self.out1 = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_" + argv[2]) + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]
		self.out2 = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_flows_path_" + argv[2]) + "_" + argv[3] + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]
		self.out3 = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_spatial_" + argv[2]) + "_" + argv[3] + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]
		self.out4 = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_temporal_" + argv[2]) + "_" + argv[3] + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]
		self.out5 = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_collect_" + argv[2]) + "_" + argv[3] + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]
		self.out6 = os.path.join("solutions/hybrid/" + os.path.basename(os.path.dirname(argv[1])) + '/' + os.path.basename(argv[1]) + '/' + argv[2] + '_' + argv[4] + '_' + argv[5] + '/' + str(argv[6]) + '_' + str(self.max_route), "mixte_gap_time_" + argv[2]) + "_" + argv[3] + "_" + argv[4] + "_" + argv[5] + "_" + argv[6]



def usage(argv):
    """
    Prints the usage of the software, including all possible arguments.
    :param argv: arguments passed by the user.
    """
    exe = os.path.basename(argv[0])
    print("")
    print("Usage: " + exe + " <instance_file> " + " <|D|> " + " <|F|> " + " <|V|> " + " <|M|> " + " <|GF| " + "<mine_size>" + "<max_size>" + "max_route")
    print("")
    print("Example: " + exe + " data/instances " + " 50 " + " 100 " + " 8 " + " 4 ", + " 30 " + "1" + "4" + "10")
    print("")
    exit(1)
