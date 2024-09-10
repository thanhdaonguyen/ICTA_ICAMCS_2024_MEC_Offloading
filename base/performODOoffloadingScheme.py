
from base.Initializer import Initializer
from base.Parameters import Parameters
from base.Dijkstra import Dijkstra
import numpy as np

params = Parameters()
A = params.A
T = params.T
G = params.G
I = params.I



def performODOoffloadingScheme(all_servers, time):
    
    access_servers = all_servers[0:A]
    high_level_servers = all_servers[A:]

    #find shortest paths for offloading tasks to servers
    graph = Initializer.createAdjacentListGraph(all_servers)
    distance = np.zeros((A + 1, G + 1))
    for AS in access_servers:
        for OS in all_servers:  #OS = offloading server
            distance[AS.id][OS.id] = Dijkstra(graph, AS.id, OS.id)
    
    #calculate computation offloaded to servers
    offloaded_computation = np.zeros(G + 1)
    required_resource_at_servers = np.zeros(G + 1)  

    totalCOmp = 0
    for AS in access_servers:

        #get a set of CTs at AS, sorted by CI (The idea is to process tasks with higher CI first)
        all_CTs_of_AS = []
        for CB in AS.tasks:
            all_CTs_of_AS.append({"type": CB["CT_type"], "num_CT": CB["task"][1][time]})
        all_CTs_of_AS.sort(key=lambda x: x["type"][1], reverse=True) 

        

        #find server with shortest offloading delay for each task in all_CTs_of_AS
        offloading_servers = []
        for task in all_CTs_of_AS:
            target_offloading_server = None
            minTimeOffloading = 9999999999
            for OS in all_servers:
                if OS.id == AS.id:
                    continue
                transmission_delay = 2 * task["type"][0] * distance[AS.id][OS.id]
                queuing_delay = 0
                if (OS.type != "AS"): queuing_delay = OS.system_load[time] / (OS.service_rate * (100 - OS.system_load[time]))
                computing_delay = task['type'][0] * task['type'][1] / OS.computing_resource

                total_delay = transmission_delay + queuing_delay + computing_delay

                if total_delay < minTimeOffloading:
                    minTimeOffloading = total_delay
                    target_offloading_server = OS
            offloading_servers.append({"server": target_offloading_server, "delay": minTimeOffloading})

        
        # for task in all_CTs_of_AS: totalCOmp += task["type"][0] * task["type"][1] * task["num_CT"]

        #CTs that are processed directly at AS if possible
        availableResource = AS.getAvailableResources(time)
        for task in all_CTs_of_AS:
            # print(AS.id, ":", availableResource);
            computing_delay = (task["type"][0] * task["type"][1]) / AS.computing_resource
            delay_requirement = task["type"][2]
            if computing_delay > delay_requirement: continue


            #processed task at AS
            neededResource =  task["type"][0] * task["type"][1] * task["num_CT"]
            if availableResource > 0:
                if neededResource <= availableResource:
                    required_resource_at_servers[AS.id] += neededResource
                    availableResource -= neededResource
                    task["num_CT"] = 0
                elif neededResource > availableResource:

                    required_resource_at_servers[AS.id] += availableResource
                    task["num_CT"] = (1 - availableResource / neededResource) * task["num_CT"]
                    availableResource = 0 

    
        #process remaining tasks by offloading to high-level servers   
        
        for i in range(len(all_CTs_of_AS)):
            task = all_CTs_of_AS[i]
            # if (task["num_CT"] != 25 and task["num_CT"] != 0): print(task["num_CT"]) 
            if task["num_CT"] == 0: continue

            total_delay = offloading_servers[i]["delay"]
            if total_delay <= task["type"][2]:
                offloaded_work = task["num_CT"] * task["type"][0] * task["type"][1]
                offloaded_computation[offloading_servers[i]["server"].id] += offloaded_work
                required_resource_at_servers[offloading_servers[i]["server"].id] += offloaded_work
                task["num_CT"] = 0


    #get evaluation of the ODO offloading scheme

    #calculate total tasks' computation 
    sum_CT_original_computation = 0
    for server in access_servers:
        for task in server.tasks:
            sum_CT_original_computation += task["task"][1][time] * task["CT_type"][0] * task["CT_type"][1]

    #total processed computation work
    sum_CT_processed_computation = 0
    for id in range (1, G + 1, 1):
        availableResource = all_servers[id - 1].getAvailableResources(time)
        sum_CT_processed_computation += min(required_resource_at_servers[id], availableResource)



    #total high-level offloaded computation
    sum_CT_highlevel_offloaded_computation = 0
    level_2_offloaded_computation = 0
    level_3_offloaded_computation = 0
    for id in range (A + 1, G + 1, 1):
        availableResource = all_servers[id - 1].getAvailableResources(time)
        processed_offloading_computation = min(offloaded_computation[id], availableResource)
        sum_CT_highlevel_offloaded_computation += processed_offloading_computation
        if (all_servers[id - 1].type == "L2"): level_2_offloaded_computation += processed_offloading_computation
        if (all_servers[id - 1].type == "L3"): level_3_offloaded_computation += processed_offloading_computation

    return sum_CT_original_computation, sum_CT_processed_computation, sum_CT_highlevel_offloaded_computation, level_2_offloaded_computation, level_3_offloaded_computation




    
        


