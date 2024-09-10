
from base.AccessServer import AccessServer
from base.HighLevelServer import HighLevelServer
from base.Parameters import Parameters
from base.Parameters import Experiment
from base.Dijkstra import Dijkstra
from base.Initializer import Initializer
from base.performGBOOffloadingScheme import performGBOOffloadingScheme
from base.performODOoffloadingScheme import performODOoffloadingScheme
from base.performNonOffloadingScheme import performNonOffloadingScheme
from base.Setting import Setting
import numpy as np
import copy
import os
import math

Setting.CT_types_list = []

class DelayEvaluator:

    changing_factor = None
    sigma = 10

    def __init__(self):
        self.params = Parameters()

    def update_metrics_for_experiment(experiment_type, access_servers, time):
        if (experiment_type == Experiment.SYSTEM_LOAD):
            min_load = Parameters.high_level_system_load_range[0]
            max_load = Parameters.high_level_system_load_range[1]
            DelayEvaluator.changing_factor = min_load + time/Parameters.TIME * (max_load - min_load)
        
        if (experiment_type == Experiment.NUM_OF_CT):
            min_num = Parameters.num_of_CTs_range[0]
            max_num = Parameters.num_of_CTs_range[1]
            DelayEvaluator.changing_factor = min_num + time/Parameters.TIME * (max_num - min_num)

        if (experiment_type == Experiment.SIZE):
            min_size = Parameters.size_range[0]
            max_size = Parameters.size_range[1]
            DelayEvaluator.changing_factor = min_size + time/Parameters.TIME * (max_size - min_size)
            for CT in Setting.CT_types_list: CT[0] = DelayEvaluator.changing_factor
            for AS in access_servers:
                for CT in AS.tasks:
                    CT["CT_type"][0] = DelayEvaluator.changing_factor
        if (experiment_type == Experiment.CI):
            min_CI = Parameters.CI_range[0]
            max_CI = Parameters.CI_range[1]
            DelayEvaluator.changing_factor = min_CI + time/Parameters.TIME * (max_CI - min_CI)
            for CT in Setting.CT_types_list: CT[1] = DelayEvaluator.changing_factor
            for AS in access_servers:
                for CT in AS.tasks:
                    CT["CT_type"][1] = DelayEvaluator.changing_factor
        if (experiment_type == Experiment.DELAY_REQUIREMENT):
            min_delay = Parameters.delay_range[0]
            max_delay = Parameters.delay_range[1]
            DelayEvaluator.changing_factor = min_delay + time/Parameters.TIME * (max_delay - min_delay)
            for CT in Setting.CT_types_list: CT[2] = DelayEvaluator.changing_factor
            for AS in access_servers:
                for CT in AS.tasks:
                    CT["CT_type"][2] = DelayEvaluator.changing_factor

        if (experiment_type == Experiment.ACCURACY):
            min_acc = Parameters.accuracy_range[0]
            max_acc = Parameters.accuracy_range[1]
            DelayEvaluator.changing_factor = min_acc + time/Parameters.TIME * (max_acc - min_acc) #calculate acc at fixed time 1->100
            CI_change = DelayEvaluator.sigma*math.log(1/DelayEvaluator.changing_factor)     #computation intensity = sigma*log(1/changing_factor)
            for CT in Setting.CT_types_list: CT[1] = CI_change
            for AS in access_servers:
                for CT in AS.tasks:
                    CT["CT_type"][1] = CI_change
    
    # def printOffloadingScheme(x):
    #     print("--------OFFLOADING SCHEME---------")
    #     params = Parameters()
    #     for i in range (len(x.x)):

    #         if (x.x[i] == 0): continue

    #         a = np.round((i - 0.01) // (params.G * params.T) + 1).astype(int)
    #         t = np.round(((i - 0.01) % (params.G * params.T)) // params.G + 1).astype(int)
    #         g = np.round((i - 0.01) % params.G).astype(int)

    #         print("a: ", a, "t: ", t, "g: ", g,"i: ", i)
    #         print("--> p = ", x.x[i])

    def saveDataToFile(data, filename):
        directory = os.path.dirname(filename)

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        print(filename)
        with open(filename, 'w') as f:
            f.write(f"{'time':<6} {'required_computation':<25} {'processed_computation':<25} {'high_level_computation':<22} {'access_server_computation':<22}  {'level_2_computation':<22} {'level_3_computation':<22} {'efficiency':<15} {'changing_factor':<15}\n")
            for item in data:
                f.write(f"{item['time']:<6} {item['required_computation']:<25.0f} {item['processed_computation']:<25.0f} {item['high_level_computation']:<22.0f} {item['access_server_computation']:<22.0f} {item['level_2_computation']:<22.0f} {item['level_3_computation']:<22.0f} {item['efficiency']:<15f} {item['changing_factor']:<15f}\n")

    def GBOMethodEvalutation(input_all_servers):

        params = Parameters()
        initializer = Initializer()

        #init servers
        all_servers = copy.deepcopy(input_all_servers)
        access_servers = all_servers[0:params.A]

        #initialize offloading scheme tensor
        P = np.zeros((params.A, params.T, params.H))
        # print(P)

        #main iterations
        data = []
        print("\nNEW METHOD EVALUATION")
        for time in range(1, params.TIME + 1, params.tau):
            DelayEvaluator.update_metrics_for_experiment(Parameters.experiment_type, access_servers, time)
            required_computation, processed_computation, high_level_computation, level_2_computation, level_3_computation = performGBOOffloadingScheme(all_servers, time, params.max_price_offloading)

            print("Time: ", time, "Required computation: ", np.round(required_computation), "Processed computation: ", np.round(processed_computation), "Efficiency: ", np.round(processed_computation / required_computation * 100), "%")

            data.append({"time": time, "required_computation": required_computation, "processed_computation": processed_computation, "high_level_computation": high_level_computation, "access_server_computation": processed_computation - high_level_computation ,"level_2_computation": level_2_computation, "level_3_computation": level_3_computation, "efficiency": processed_computation / required_computation, "changing_factor": DelayEvaluator.changing_factor})
        
        DelayEvaluator.saveDataToFile(data, "./data/" + Parameters.saveLocation + "GBOMethodEvaluation.txt")

    def ODOMethodEvaluation(input_all_servers):
        params = Parameters()

        #init servers
        all_servers = copy.deepcopy(input_all_servers)
        access_servers = all_servers[0:params.A]

        #main iterations
        data = []
        print("\nODO METHOD EVALUATION")
        for time in range(1, params.TIME + 1, params.tau):
            DelayEvaluator.update_metrics_for_experiment(Parameters.experiment_type, access_servers, time)
            required_computation, processed_computation, high_level_computation, level_2_computation, level_3_computation = performODOoffloadingScheme(all_servers, time)

            print("Time: ", time, "Required computation: ", np.round(required_computation), "Processed computation: ", np.round(processed_computation), "Efficiency: ", np.round(processed_computation / required_computation * 100), "%")

            data.append({"time": time, "required_computation": required_computation, "processed_computation": processed_computation, "high_level_computation": high_level_computation, "access_server_computation": processed_computation - high_level_computation ,"level_2_computation": level_2_computation, "level_3_computation": level_3_computation, "efficiency": processed_computation / required_computation, "changing_factor": DelayEvaluator.changing_factor})

        DelayEvaluator.saveDataToFile(data, "./data/" + Parameters.saveLocation + "ODOMethodEvaluation.txt")

    def nonOffloadingEvaluation(input_all_servers):
        params = Parameters()

        #init servers
        all_servers = copy.deepcopy(input_all_servers)
        access_servers = all_servers[0:params.A]

        #main iterations
        data = []
        print("\nNON OFFLOADING  EVALUATION")
        for time in range(1, params.TIME + 1, params.tau):
            DelayEvaluator.update_metrics_for_experiment(Parameters.experiment_type, access_servers, time)
            required_computation, processed_computation = performNonOffloadingScheme(all_servers, time)

            
            print("Time: ", time, "Required computation: ", np.round(required_computation), "Processed computation: ", np.round(processed_computation), "Efficiency: ", np.round(processed_computation / required_computation * 100), "%")

            data.append({"time": time, "required_computation": required_computation, "processed_computation": processed_computation, "high_level_computation": 0, "access_server_computation": processed_computation ,"level_2_computation": 0, "level_3_computation": 0, "efficiency": processed_computation / required_computation, "changing_factor": DelayEvaluator.changing_factor})

        DelayEvaluator.saveDataToFile(data, "./data/" + Parameters.saveLocation + "NonOffloadingEvaluation.txt")

    def evaluate():

        initializer = Initializer()

        #init servers
        all_servers, access_servers, level2_servers, level3_servers = initializer.initializeServers()

        DelayEvaluator.GBOMethodEvalutation(all_servers)
        DelayEvaluator.ODOMethodEvaluation(all_servers)
        DelayEvaluator.nonOffloadingEvaluation(all_servers)
        
        