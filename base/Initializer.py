from base.AccessServer import AccessServer
from base.HighLevelServer import HighLevelServer
from base.Parameters import Parameters
from base.Setting import Setting
from Utils.flucPointGenerator import flucPointGenerator
from Utils.linearPointGenerator import linearPointGenerator

class Initializer:
    def __init__(self):
        self.name = "Initialization"
        self.params = Parameters()


    def createServers():

        #get parameters
        params = Parameters()

        #create servers
        accessServers = []
        level2Servers = []
        level3Servers = []

        id = 1
        for i in range(params.A):
            name = "AS-" + str(i + 1)
            accessServers.append(AccessServer(name=name, id=id, type="AS"))
            id += 1
        
        for i in range(params.L2):
            name = "L2-" + str(i + 1)
            level2Servers.append(HighLevelServer(name=name, id=id, type="L2"))
            id += 1
        
        for i in range(params.L3):
            name = "L3-" + str(i + 1)
            level3Servers.append(HighLevelServer(name=name, id=id, type="L3"))
            id += 1

        
        #create connections 
        #add adjacent servers and the bandwidth to them
        for i in range(params.A):
            upperServerNumber = int(i/4)

            for j in range(-1, 2, 1):
                if upperServerNumber + j >= 0 and upperServerNumber + j < 5:
                    accessServers[i].adjacent_servers.append((level2Servers[upperServerNumber + j], params.bandwidth_AS_to_level2))
                    level2Servers[upperServerNumber + j].adjacent_servers.append((accessServers[i], params.bandwidth_AS_to_level2))
                
        for i in range(5):
            for j in range (i + 1, 5, 1):
                level2Servers[i].adjacent_servers.append((level2Servers[j], params.bandwidth_level2_to_level2))
                level2Servers[j].adjacent_servers.append((level2Servers[i], params.bandwidth_level2_to_level2))
            for j in range(3):
                level2Servers[i].adjacent_servers.append((level3Servers[j], params.bandwidth_level2_to_level3))
                level3Servers[j].adjacent_servers.append((level2Servers[i], params.bandwidth_level2_to_level3))

        for i in range(3):
            for j in range(i + 1, 3, 1):
                level3Servers[i].adjacent_servers.append((level3Servers[j], params.bandwidth_level3_to_level3))
                level3Servers[j].adjacent_servers.append((level3Servers[i], params.bandwidth_level3_to_level3))

        all_servers = accessServers + level2Servers + level3Servers
        high_level_servers = level2Servers + level3Servers
        return all_servers, accessServers, level2Servers, level3Servers
    
    #This function only return the graph with weight relative to real weight (1 / bandwidth). Still need to multiply edge weights with data size of the offloaded task to get the real weight
    ## -->  transmission time = data_size / bandwidth
    def createAdjacentListGraph(all_servers):

        graph = {}
        for server in all_servers:
            graph[server.id] = {}
            for adj in server.adjacent_servers:
                graph[server.id][adj[0].id] = 1 / adj[1]

        return graph


    def initializeComputationTask(self, access_server, CT_types_list):
        min_num_CTs = Parameters.num_of_CTs_range[0]
        max_num_CTs = Parameters.num_of_CTs_range[1]
        for CT_type in CT_types_list:
            (arrive_time, numb_of_CTs) = linearPointGenerator(min_num_CTs, max_num_CTs, self.params.TIME)
            access_server.tasks.append({"CT_type": CT_type, "task": (arrive_time, numb_of_CTs)})

    def initializeComputingResource(self, server):
        if server.type == "AS":
            server.computing_resource = self.params.AS_computing_resource
        elif server.type == "L2":
            server.computing_resource = self.params.level2_computing_resource
        elif server.type == "L3":
            server.computing_resource = self.params.level3_computing_resource

    def initializeSystemMetrics(self, highlevel_server):
        
        #system load
        min_load = Parameters.high_level_system_load_range[0]
        max_load = Parameters.high_level_system_load_range[1]
        (time, system_load) = linearPointGenerator(min_load, max_load, self.params.TIME)
        highlevel_server.system_load = system_load

        #total load
        (time, total_load) = flucPointGenerator(20, 50, self.params.TIME)
        highlevel_server.total_load = total_load

        # visualizeXYset(time, system_load)

        #service rate
        highlevel_server.service_rate = highlevel_server.computing_resource / highlevel_server.mean_task_computation

    def initializeServers(self):

        #create servers
        all_servers, access_servers, level2_servers, level3_servers = Initializer.createServers()
        high_level_servers = level2_servers + level3_servers
        #initialize servers' computing resource
        for server in all_servers:
            self.initializeComputingResource(server)

        #initialize system's metrics (system load, arrival rate) for high level servers
        for server in high_level_servers:
            self.initializeSystemMetrics(server)

        #create computational tasks for each access server
        for server in access_servers:
            self.initializeComputationTask(server, Setting.CT_types_list)


        return all_servers, access_servers, level2_servers, level3_servers

        