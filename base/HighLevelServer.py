from base.Parameters import Parameters

class HighLevelServer:

    def getAvailableResources(self, time):

        return self.computing_resource * (1 - self.system_load[time] / 100) * self.params.tau

    def __init__(self, name, id, type):
        self.params = Parameters()
        self.id = id
        self.name = name
        self.type = type
        self.computing_resource = 0
        self.network_bandwidth = 0
        self.mean_task_computation = self.params.mean_task_computation
        self.system_load = []        #the load come from tasks other than offloading tasks from access server
        self.service_rate = 0                       #task/s
        self.queuing_list = 0
        self.adjacent_servers = []