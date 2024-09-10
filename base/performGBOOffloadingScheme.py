
from base.Parameters import Parameters
from base.Setting import Setting
from base.Initializer import Initializer
from base.Dijkstra import Dijkstra
from scipy.optimize import linprog

import numpy as np
params = Parameters()
A = params.A
T = params.T
G = params.G
I = params.I

def getTheoreticalOffloadingEfficiency(all_servers, access_servers, x, c, time):
    params = Parameters()
    #calculate total CT size
    sum_CT_original_computation = 0
    for server in access_servers:
        for task in server.tasks:
            sum_CT_original_computation += task["task"][1][time] * task["CT_type"][0] * task["CT_type"][1]

    #calculate total processed CT
    sum_CT_processed_computation = 0
    for i in range(1, params.I + 1, 1):
        # a = np.round((i - 0.01) // (G * T) + 1).astype(int)
        # t = np.round(((i - 0.01) % (G * T)) // G + 1).astype(int)
        # g = np.round((i - 0.01) % G).astype(int)

        sum_CT_processed_computation += x.x[i] * c[i]

    #calculate total offloaded computation
    sum_CT_highlevel_offloaded_computation = 0
    level_2_offloaded_computation = 0
    level_3_offloaded_computation = 0
    for i in range(1, params.I + 1, 1):
        # a = np.round((i - 0.01) // (G * T) + 1).astype(int)
        # t = np.round(((i - 0.01) % (G * T)) // G + 1).astype(int)
        g = np.round((i - 0.01) % G).astype(int)
        if (g > A):
            sum_CT_highlevel_offloaded_computation += x.x[i] * c[i]
            if (all_servers[g - 1].type == "L2"): level_2_offloaded_computation += x.x[i] * c[i]
            if (all_servers[g - 1].type == "L3"): level_3_offloaded_computation += x.x[i] * c[i]


    return sum_CT_original_computation, sum_CT_processed_computation, sum_CT_highlevel_offloaded_computation, level_2_offloaded_computation, level_3_offloaded_computation

def printServersWorkloadMetrics(c, x, all_servers, time):
    params = Parameters()
    print("--------SERVERS' WORKLOAD METRICS---------")
    for server in all_servers:
        print("id: ", server.id, ",name: ", server.name, )

        if (server.type == "AS"):
            available_resource = server.computing_resource * params.tau
            print("- available resource: ", available_resource)
        else:
            available_resource = server.computing_resource * (1 - server.system_load[time] / 100) * params.tau
            print("- available resource: ", available_resource)

        total_offloaded = 0
        for i in range(1, params.I + 1, 1):
            g = np.round((i - 0.01) % params.G).astype(int)
            if (g == server.id):
                total_offloaded += x[i] * c[i]
        print("- total offloaded: ", total_offloaded)

        print("- usage: ", total_offloaded / available_resource * 100, "%")
            

def performGBOOffloadingScheme(all_servers, time, price_offloading):
    params = Parameters()
    A = params.A
    T = params.T
    G = params.G
    I = params.I

    access_servers = all_servers[0:A]
    high_level_servers = all_servers[A:]

    #find shortest path between servers
    graph = Initializer.createAdjacentListGraph(all_servers)
    distance = np.zeros((A + 1, G + 1))
    for AS in access_servers:
        for OS in all_servers:  #OS = offloading server
            distance[AS.id][OS.id] = Dijkstra(graph, AS.id, OS.id)
        
    # print(distance)

    #Calculate c_i
    c = np.zeros(I + 1)
    for i in range(1,I + 1, 1):
        a = np.round((i - 0.01) // (G * T) + 1).astype(int)
        t = np.round(((i - 0.01) % (G * T)) // G + 1).astype(int)
        g = np.round((i - 0.01) % G).astype(int)

        # print("i:", i, "a: ", a, "t: ", t, "g: ", g)

        CT_Type = Setting.CT_types_list[t - 1]
        S_at = 0
        CI_t = CT_Type[1]

        for CB in access_servers[a-1].tasks: 
            if CB["CT_type"] == CT_Type:
                numb_of_CT = CB["task"][1][time]
                size_of_CT = CT_Type[0]
                S_at = numb_of_CT * size_of_CT
                break
        
        c[i] = S_at * CI_t
        
    
    #find possible offloading high-level servers for ASs
    feasible_offloading_GSs = np.ones((A + 1, T + 1, G + 1))
    for a in range(1, A + 1, 1):
        for t in range(1, T + 1, 1):
            delay_requirement = Setting.CT_types_list[t - 1][2]
            for g in range(1, G + 1, 1):   
                AS = access_servers[a - 1]      #access server
                CT_type = Setting.CT_types_list[t - 1]
                GS = all_servers[g - 1]  #general server

                transmission_delay = 2 * CT_Type[0] * distance[AS.id][GS.id]
                queuing_delay = 0
                if (GS.type != "AS"): queuing_delay = GS.system_load[time] / (GS.service_rate * (100 - GS.system_load[time]))
                computing_delay = CT_type[0] * CT_type[1] / GS.computing_resource

                total_delay = transmission_delay + queuing_delay + computing_delay 

                # print("a: ", a, ",t: ", t, ",g: ", g, "--> total delay:", total_delay)
                # print("trans: ", transmission_delay)
                # print("comp: ", computing_delay)
                # print("queue: ", queuing_delay)
                # if (GS.type != "AS"): 
                #     print("sys_load: ", GS.system_load[time])
                #     print("ser_rate: ", GS.service_rate)

                if (total_delay > delay_requirement): feasible_offloading_GSs[a][t][g] = 0

    #implement objective function
    c_x = np.zeros(I + 1)
    c_x[0] = -999999999

    for a in range (1, A + 1, 1):
        for t in range(1, T + 1, 1):
            for g in range(1, G + 1, 1):
                i = (a - 1) * T * G + (t - 1) * G + g
                if (g <= A): 
                    if (feasible_offloading_GSs[a][t][g] == 0): c_x[i] = -999999999
                    else : c_x[i] = c[i] * params.price_processing
                else:
                    if (feasible_offloading_GSs[a][t][g] == 0): c_x[i] = -999999999
                    # else : c_x[i] = c[i] * params.price_processing
                    else : c_x[i] = c[i] * (params.price_processing - price_offloading)

    c_x = -c_x
    c_x = c_x / 10**10             #scale down the coeficient

    #implement constraints
    A_ub = []
    b_ub = []

    #(12a)
    bounds = (0, 1)

    #(12b)
    for a in range (1, A + 1, 1):
        for t in range(1, T + 1, 1):
            cond = np.zeros(I + 1)
            for g in range(1, G + 1, 1):
                i = (a - 1) * T * G + (t - 1) * G + g
                cond[i] = 1
            A_ub.append(cond)
            b_ub.append(1)
    
    #(12c)
    for g in range (1, A + 1, 1):
        cond = np.zeros(I + 1)
        for a in range(1, A + 1, 1):
            for t in range(1, T + 1, 1):
                i = (a - 1) * T * G + (t - 1) * G + g
                cond[i] = c[i]
        A_ub.append(cond)

        available_resource = access_servers[g-1].getAvailableResources(time)
        b_ub.append(available_resource)

    
    #(12d)
    for g in range (A + 1, G + 1, 1):
        cond = np.zeros(I + 1)
        for a in range(1, A + 1, 1):
            for t in range(1, T + 1, 1):
                i = (a - 1) * T * G + (t - 1) * G + g
                cond[i] = c[i]
        A_ub.append(cond)

        available_resource = all_servers[g-1].getAvailableResources(time)
        b_ub.append(available_resource)


    #get the result
    coeficient = {"c": c, "c_x": c_x, "A_ub": A_ub, "b_ub": b_ub}
    x = linprog(c=c_x, A_ub=A_ub, b_ub=b_ub, bounds=bounds)


    required_computation, processed_computation, high_level_computation, level_2_computation, level_3_computation = getTheoreticalOffloadingEfficiency(all_servers, access_servers, x, coeficient["c"], time)


    return required_computation, processed_computation, high_level_computation, level_2_computation, level_3_computation 



    
