import os

class Arguments:
	"""
	Let the user enter the argument via command line.
	"""

	def __init__(self, argv, prefix=""):
		if len(argv) < 1:
			usage(argv)

		# initializing default values
		self.instance = argv[1]
		self.grid_size = int(argv[2])
		self.num_nodes = int(argv[3])
		self.num_flows = int(argv[4])
		self.min_size = int(argv[5])
		self.max_size = int(argv[6])
		
		



def usage(argv):
    """
    Prints the usage of the software, including all possible arguments.
    :param argv: arguments passed by the user.
    """
    exe = os.path.basename(argv[0])
    print("")
    print("Usage: " + exe + " <instance_file> " + " <|N|> " + " <|D|> " + " <|F|> " + " <min size> " + " <max size> ")
    print("")
    print("Example: " + exe + " data/instances " + " 8 " + " 64 " + " 50 " + " 10 " + " 40 ")
    print("")
    exit(1)

    #


