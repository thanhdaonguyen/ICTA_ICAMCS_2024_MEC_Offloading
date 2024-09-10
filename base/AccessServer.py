from Utils.flucPointGenerator import flucPointGenerator
from base.Parameters import Parameters
from base.Setting import Setting

class AccessServer:

    def __init__(self, name, id, type):
        self.params = Parameters()
        self.id = id
        self.name = name
        self.type = type
        self.computing_resource = 0
        self.network_bandwidth = 0
        self.system_load = 0
        self.tasks = []
        self.adjacent_servers = []

    def getComputationTask(self, CT_types_list):
        for type in CT_types_list:
            (numb_of_CTs, arrive_time) = flucPointGenerator(0,50, 200)

    def getAvailableResources(self, time):
        return self.computing_resource * self.params.tau