
import pandas as pd
import matplotlib.pyplot as plt
from base.Parameters import Parameters

data_directory = [
    "systemLoadChange/",
    "numberOfTasksChange/",
    "taskSizeChange/",
    "compIntensityChange/",
    "delayRequirementChange/",
    'accuracyChange/'
]

changing_factor = [
    "high level servers' system load",
    "number of CTs",
    "CT's size",
    "CT's CI ",
    "CT's delay requirement",
    'accuracy'
]

x_label = [
    "system load (%)",
    "number of CTs",
    "size (bit)",
    "CI (CPU cycles/bit)",
    "delay requirement (s)",
    "accuracy of local training"
]

def visualizeAllData():

    # Plotting the data
    plt.figure(figsize=(16, 8.1))
    for i in range(6):
        for j in range(3):
            data_folder = data_directory[i] + "experiment" + str(j) + '/'

            # Read data from the TSV file
            dataNO = pd.read_csv('./data/' + data_folder + 'NonOffloadingEvaluation.txt', delim_whitespace=True)
            dataODO = pd.read_csv('./data/' + data_folder + 'ODOMethodEvaluation.txt', delim_whitespace=True)
            dataGBO = pd.read_csv('./data/' + data_folder + 'GBOMethodEvaluation.txt', delim_whitespace=True)

            # Plot queueing times
            plt.subplot(6, 3, i * 3 + j + 1)
            plt.plot(dataNO['changing_factor'], dataNO['efficiency'], label='Non Offloading', color='green', linewidth=1.5)
            plt.plot(dataODO['changing_factor'], dataODO['efficiency'], label='ODO', color='red', linewidth=1.5)
            plt.plot(dataGBO['changing_factor'], dataGBO['efficiency'], label='New Method', linewidth=1.5)
            plt.ylim(0,1.2)
            plt.xlabel(x_label[i], fontsize=8)
            plt.ylabel('Probability of tasks processed', fontsize=6)
            title = 'Efficiency over range of ' + changing_factor[i]
            plt.title(title, fontsize=8)
            plt.legend(prop={'size': 6})

    # Show the plots
    plt.tight_layout()
    plt.show()
