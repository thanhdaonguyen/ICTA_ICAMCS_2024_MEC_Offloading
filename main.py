from base.Parameters import Parameters
from base.Parameters import Experiment
from base.Setting import Setting
from base.Dijkstra import Dijkstra
from base.Initializer import Initializer
from Utils.visualizeDataSet import visualizeDataSet
from Utils.visualizeAllData import visualizeAllData
from Delay_statisfaction_evaluation.DelayEvaluator import DelayEvaluator
from concurrent.futures import ThreadPoolExecutor



def experiment_systemload():
    for i in range(len(Setting.CT_types_sysload_experiment)):
        saveFolder = "systemLoadChange/experiment" + str(i) + "/"
        Parameters.initializeParameter(Experiment.SYSTEM_LOAD, (10, 85), Setting.CT_types_sysload_experiment[i], saveFolder )
        DelayEvaluator.evaluate()
def experiment_numtasks():
    for i in range(len(Setting.CT_types_numtasks_experiment)):
        saveFolder = "numberOfTasksChange/experiment" + str(i) + "/"
        Parameters.initializeParameter(Experiment.NUM_OF_CT, (10, 90), Setting.CT_types_numtasks_experiment[i], saveFolder)
        DelayEvaluator.evaluate()
def experiment_computational_intensity():
    for i in range(len(Setting.CT_types_CI_experiment)):
        saveFolder = "compIntensityChange/experiment" + str(i) + "/"
        Parameters.initializeParameter(Experiment.CI, (10, 100), Setting.CT_types_CI_experiment[i], saveFolder)
        DelayEvaluator.evaluate()
def experiment_CT_size():
    for i in range(len(Setting.CT_types_size_experiment)):
        saveFolder = "taskSizeChange/experiment" + str(i) + "/"
        Parameters.initializeParameter(Experiment.SIZE, (500000,5000000), Setting.CT_types_size_experiment[i], saveFolder)
        DelayEvaluator.evaluate()
def experiment_delay_requirement():
    for i in range(len(Setting.CT_types_delay_experiment)):
        saveFolder = "delayRequirementChange/experiment" + str(i) + "/"
        Parameters.initializeParameter(Experiment.DELAY_REQUIREMENT, (0.001, 0.04), Setting.CT_types_delay_experiment[i], saveFolder)
        DelayEvaluator.evaluate()

def experiment_accuracy():
    for i in range(len(Setting.CT_types_accuracy_experiment)):
        saveFolder = "accuracyChange/experiment" + str(i) + "/"
        Parameters.initializeParameter(Experiment.ACCURACY, (0.001, 0.02), Setting.CT_types_accuracy_experiment[i], saveFolder)
        DelayEvaluator.evaluate()
        
if __name__ == '__main__':



    # experiment_systemload()
    # experiment_numtasks()
    # experiment_computational_intensity()
    # experiment_CT_size()
    # experiment_delay_requirement()
    # experiment_accuracy()

    visualizeAllData()
    



    