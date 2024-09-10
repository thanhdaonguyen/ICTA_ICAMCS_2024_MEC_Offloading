
import pandas as pd
import matplotlib.pyplot as plt
from base.Parameters import Parameters

data_directory = [
    "systemLoadChange/",
    "numberOfTasksChange/",
    "taskSizeChange/",
    "compIntensityChange/",
    "delayRequirementChange/",
    "accuracyChange/"
]

changing_factor = [
    "high level servers' system load",
    "number of CTs",
    "CT's size",
    "CT's CI ",
    "CT's delay requirement",
    "accuracy"
]

x_label = [
    "system load (%)",
    "number of CTs",
    "size (bit)",
    "CI (CPU cycles/bit)",
    "delay requirement (s)",
    "accuracy of local training"
]

def visualizeDataSet(folder):

    # Plotting the data
    plt.figure(figsize=(5, 6))
    for i in range(3):
    
        data_folder = folder + "experiment" + str(i) + '/'

        # Read data from the TSV file
        dataGBO = pd.read_csv('./data/' + data_folder + 'GBOMethodEvaluation.txt', delim_whitespace=True)
        dataODO = pd.read_csv('./data/' + data_folder + 'ODOMethodEvaluation.txt', delim_whitespace=True)
        dataNO = pd.read_csv('./data/' + data_folder + 'NonOffloadingEvaluation.txt', delim_whitespace=True)

        # Plot queueing times
        plt.subplot(3, 1, i + 1)
        plt.plot(dataNO['changing_factor'], dataNO['efficiency'], label='Non Offloading', color='green', linewidth=2.5)
        plt.plot(dataODO['changing_factor'], dataODO['efficiency'], label='ODO', color='red', linewidth=2.5)
        plt.plot(dataGBO['changing_factor'], dataGBO['efficiency'], label='New Method', linewidth=2.5)
        plt.ylim(0, 1.2)
        plt.xlabel(folder, fontsize=8)
        plt.ylabel('Probability of tasks processed', fontsize=6)
        title = 'Efficiency over range of ' + folder
        plt.title(title, fontsize=8)
        plt.legend(prop={'size': 6})

    # Show the plots
    plt.tight_layout()
    plt.show()
