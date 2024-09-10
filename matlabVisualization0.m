% Define the path to your data file
% folderPath = './data/systemLoadChange/experiment0/';
% newMethodDataFile = [folderPath, 'GBOMethodEvaluation.txt'];
% ODOmethodDataFile = [folderPath, 'ODOMethodEvaluation.txt'];
% nonOffloadingDataFile = [folderPath, 'NonOffloadingEvaluation.txt'];

% % Read the data from the file
% data = readmatrix(ODOmethodDataFile);

% % Assuming the first column is 'x' and the second column is 'y'
% x = data(:, 6);
% y = data(:, 5);

% plot(x, y, '--*',     'color',[0, 0.4470, 0.7410], 'LineWidth', 1.5, 'MarkerSize', 8);

% ylim([0,1]);
% xlabel('System load at high level server (%)');
% ylabel('Probability of CT processed');

data_directory = {
                  'systemLoadChange/', ...
                      'numberOfTasksChange/', ...
                      'taskSizeChange/', ...
                      'compIntensityChange/', ...
                      'delayRequirementChange/', ...
                      'accuracyChange/'
                  };

changing_factor = {
                   'high level servers'' system load', ...
                       'number of CTs', ...
                       'CT''s size', ...
                       'CT''s CI', ...
                       'CT''s delay requirement', ...
                       'accuracy'
                   };

x_label = {
           'system load (%)', ...
               'number of CTs', ...
               'size (bit)', ...
               'CI (CPU cycles/bit)', ...
               'delay requirement (s)', ...
               'local training accuracy θ'
           };

markerIndices = 1:5:100; % Adjust the step to control marker frequency

figure('Position', [100, 100, 1600, 810]);

for i = 1:5

    for j = 1:3
        data_folder = [data_directory{i}, 'experiment', num2str(j - 1), '/'];

        % Read data from the TSV files
        dataNO = readmatrix(['./data/', data_folder, 'NonOffloadingEvaluation.txt']);
        dataODO = readmatrix(['./data/', data_folder, 'ODOMethodEvaluation.txt']);
        dataGBO = readmatrix(['./data/', data_folder, 'GBOMethodEvaluation.txt']);

        % Plot queueing times
        subplot(5, 3, (i - 1) * 3 + j);
        hold on;
        plot(dataNO(:, 9), dataNO(:, 8), '--*', 'DisplayName', 'Non Offloading', 'Color', 'green', 'LineWidth', 1, 'MarkerIndices', markerIndices, 'MarkerSize', 4);
        plot(dataODO(:, 9), dataODO(:, 8), '--o', 'DisplayName', 'ODO', 'Color', 'red', 'LineWidth', 1, 'MarkerIndices', markerIndices, 'MarkerSize', 4);
        plot(dataGBO(:, 9), dataGBO(:, 8), '--d', 'DisplayName', 'New Method', 'LineWidth', 1, 'MarkerIndices', markerIndices, 'MarkerSize', 4);
        hold off;
        ylim([0, 1.1]);
        xlabel(x_label{i}, 'FontSize', 8);
        ylabel('Probability of tasks processed', 'FontSize', 6);
        title(['Efficiency over range of ', changing_factor{i}], 'FontSize', 8);
        legend('show', 'FontSize', 4);
    end

end

% Show the plots
% tightfig;  % Adjust the figure layout to remove excess white space
