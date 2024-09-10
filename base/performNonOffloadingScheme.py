
from base.Initializer import Initializer
from base.Parameters import Parameters
from base.Dijkstra import Dijkstra
import numpy as np

params = Parameters()
A = params.A
T = params.T
G = params.G
I = params.I



def performNonOffloadingScheme(all_servers, time):
    
    access_servers = all_servers[0:A]
    
    #calculate computation offloaded to servers
    offloaded_computation = np.zeros(G + 1)
    required_resource_at_servers = np.zeros(G + 1)  
    for AS in access_servers:

        #get a set of CTs at AS, sorted by CI (The idea is to process tasks with higher CI first)
        all_CTs_of_AS = []
        for CB in AS.tasks:
            all_CTs_of_AS.append({"type": CB["CT_type"], "num_CT": CB["task"][1][time]})
        all_CTs_of_AS.sort(key=lambda x: x["type"][1], reverse=True) 
            
        
        #process directly at AS if possible
        availableResource = AS.computing_resource * params.tau
        processedWithoutOffloading = 0
        for task in all_CTs_of_AS:
            computing_delay = task["type"][0] * task["type"][1] / AS.computing_resource
            delay_requirement = task["type"][2]
            if computing_delay >= delay_requirement: continue


            #processed task at AS
            neededResource = task["num_CT"] * task["type"][0] * task["type"][1]
            if availableResource > 0:
                if neededResource <= availableResource:
                    processedWithoutOffloading += neededResource
                    required_resource_at_servers[AS.id] += neededResource
                    availableResource -= neededResource
                    task["num_CT"] = 0
                else:
                    processedWithoutOffloading += availableResource
                    required_resource_at_servers[AS.id] += availableResource
                    task["num_CT"] = (1 - availableResource / neededResource) * task["num_CT"]
                    availableResource = 0

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

    return sum_CT_original_computation, sum_CT_processed_computation




    
        


