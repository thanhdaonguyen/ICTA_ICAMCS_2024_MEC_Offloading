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

figure('Position', [100, 100, 1000, 200]);

for i = 1:2
    j = 2;
    data_folder = [data_directory{i}, 'experiment', num2str(j - 1), '/'];

    % Read data from the TSV files
    dataNO = readmatrix(['./data/', data_folder, 'NonOffloadingEvaluation.txt']);
    dataODO = readmatrix(['./data/', data_folder, 'ODOMethodEvaluation.txt']);
    dataGBO = readmatrix(['./data/', data_folder, 'GBOMethodEvaluation.txt']);

    % Plot queueing times
    subplot(1, 2, i);
    hold on;
    plot(dataNO(:, 9), dataNO(:, 8), '--*', 'DisplayName', 'Non Offloading', 'Color', 'green', 'LineWidth', 1, 'MarkerIndices', markerIndices, 'MarkerSize', 4);
    plot(dataODO(:, 9), dataODO(:, 8), '--o', 'DisplayName', 'ODO', 'Color', '#f5b642', 'LineWidth', 1, 'MarkerIndices', markerIndices, 'MarkerSize', 4);
    plot(dataGBO(:, 9), dataGBO(:, 8), '--d', 'DisplayName', 'GBO', 'Color', 'red', 'LineWidth', 1, 'MarkerIndices', markerIndices, 'MarkerSize', 4);
    hold off;
    ylim([0, 1.1]);
    xlabel(x_label{i}, 'FontSize', 12);
    ylabel('Probability of tasks processed', 'FontSize', 10);
    title(['Efficiency over range of ', changing_factor{i}], 'FontSize', 12);

    legend('show', 'FontSize', 6);

end

% Show the plots
% tightfig;  % Adjust the figure layout to remove excess white space
