from base.Setting import Setting
import math
import numpy as np
from enum import Enum

class Experiment(Enum):
    SYSTEM_LOAD = 1
    CI = 2
    SIZE = 3
    DELAY_REQUIREMENT = 4
    NUM_OF_CT = 5
    ACCURACY = 6

class Parameters:
    A = 20              # number of access servers
    L2 = math.ceil(A / 4)
    L3 = 3
    H = L2 + L3   # number of high-level servers
    G = A + H    # number of all servers
    T = 0
    I = A * T * G
    tau = 1       # \tau period
    TIME = 100   
    mean_task_computation = 0 # CPU cycles

    experiment_type = None
    saveLocation = ""
    changingFactor = ""

    #parameters being changed for the experiments
    high_level_system_load_range = (40,40)
    num_of_CTs_range = (25,25)
    CI_range = (30,30)
    size_range = (500000,5000000)
    delay_range = (0.001, 0.1)
    accuracy_range = (0.001,0.001)

    def __init__(self):
        self.A = 20              # number of access servers
        self.L2 = math.ceil(self.A / 4)
        self.L3 = 3
        self.H = self.L2 +self.L3   # number of high-level servers
        self.G = self.A + self.H    # number of all servers
        self.T = len(Setting.CT_types_list)
        self.I = self.A * self.T * self.G
        self.tau = 1       # \tau period
        self.TIME = 100             # total simulation time

        #computing resource
        self.AS_computing_resource = 6 * 10**9
        self.level2_computing_resource = 12 * 10**9
        self.level3_computing_resource = 30 * 10**9
        
        #bandwidth
        self.bandwidth_AS_to_level2 = 600 * 10**6 # bps
        self.bandwidth_level2_to_level3 = 1000 * 10**6 # bps
        self.bandwidth_level2_to_level2 = 1000 * 10**6 # bps
        self.bandwidth_level3_to_level3 = 1000 * 10**6 # bps

        #mean task computation
        #this is for the initialization of service rate at high-level servers


        #prices 
        self.price_processing = 100             #pr^p
        self.max_price_offloading = 60           #pr^o

    @classmethod
    def initializeParameter(cls, experiment_type, experiement_range, CT_types_list, folder):

        cls.high_level_system_load_range = (40,40)
        cls.num_of_CTs_range = (25,25)
        cls.CI_range = (30,30)
        cls.size_range = (500000,5000000)
        cls.delay_range = (0.001, 0.1)
        cls.accuracy_range = (0.001,0.001)

        if (experiment_type == Experiment.SYSTEM_LOAD):
            cls.experiment_type = Experiment.SYSTEM_LOAD
            Setting.CT_types_list = CT_types_list
            cls.T = len(Setting.CT_types_list)
            cls.mean_task_computation = sum(CT[0] * CT[1] for CT in Setting.CT_types_list) / cls.T 
            
            cls.saveLocation = folder
            cls.changingFactor = "system_load"
            cls.high_level_system_load_range = experiement_range

        if (experiment_type == Experiment.NUM_OF_CT): 
            cls.experiment_type = Experiment.NUM_OF_CT
            Setting.CT_types_list = CT_types_list
            cls.T = len(Setting.CT_types_list) 
            cls.mean_task_computation = sum(CT[0] * CT[1] for CT in Setting.CT_types_list) / cls.T 
            
            cls.saveLocation = folder
            cls.changingFactor = "number_of_tasks"
            cls.num_of_CTs_range = experiement_range

        if (experiment_type == Experiment.CI):
            cls.experiment_type = Experiment.CI
            Setting.CT_types_list = CT_types_list
            cls.T = len(Setting.CT_types_list)
            cls.mean_task_computation = sum(CT[0] * CT[1] for CT in Setting.CT_types_list) / cls.T 
            
            cls.saveLocation = folder
            cls.changingFactor = "CI"
            cls.CI_range = experiement_range

        if (experiment_type == Experiment.SIZE):
            cls.experiment_type = Experiment.SIZE
            Setting.CT_types_list = CT_types_list
            cls.T = len(Setting.CT_types_list)
            cls.mean_task_computation = sum(CT[0] * CT[1] for CT in Setting.CT_types_list) / cls.T 
            
            cls.saveLocation = folder
            cls.changingFactor = "size" 
            cls.size_range = experiement_range

        if (experiment_type == Experiment.DELAY_REQUIREMENT):
            cls.experiment_type = Experiment.DELAY_REQUIREMENT 
            Setting.CT_types_list = CT_types_list
            cls.T = len(Setting.CT_types_list) 
            cls.mean_task_computation = sum(CT[0] * CT[1] for CT in Setting.CT_types_list) / cls.T 
            
            cls.saveLocation = folder
            cls.changingFactor = "delay_requirement"
            cls.delay_range = experiement_range


        if (experiment_type == Experiment.ACCURACY):
            cls.experiment_type = Experiment.ACCURACY
            Setting.CT_types_list = CT_types_list
            cls.T = len(Setting.CT_types_list)
            cls.mean_task_computation = sum(CT[0] * CT[1] for CT in Setting.CT_types_list) / cls.T 
            
            cls.saveLocation = folder
            cls.changingFactor = "accuracy"
            cls.accuracy_range = experiement_range

        

