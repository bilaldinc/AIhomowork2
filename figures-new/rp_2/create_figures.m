function [ ] = create_figures()
    % execute this script in a directory that contains csv files

    if ~exist('figures', 'dir')
        % Folder does not exist so create it.
        mkdir('figures');
    end
    
    files = dir('*.csv');
    files_1 = {};
    for i=1:length(files)
        files_1{i,1} = strcat(files(i).name(1:end-4),'.png');
        files_1{i,2} = dlmread(files(i).name);
    end
       
    for i=1:length(files)
        fig = figure('visible', 'off');
        plot(files_1{i,2});
        ylim([9 15])
        set(gca,'YTick',9:1:15)
        xlabel('Generation');
        ylabel('Average Fitness');
        set(gcf, 'Position', [500, 500, 800, 400]);
        grid on
        saveas(fig,strcat('figures/',files_1{i,1}),'png');
    end
    
end


