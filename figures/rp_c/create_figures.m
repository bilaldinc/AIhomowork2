function [ ] = create_figures()
    % execute this script in a directory that contains csv files


    
    files = dir('*.csv');
    files_1 = {};
    for i=1:length(files)
        files_1{i,1} = strcat(files(i).name(1:end-9),'.png');
        files_1{i,2} = dlmread(files(i).name);
    end
    
    x = (0:1:399)';
    fig = figure('visible', 'off');
    plot(x,files_1{1,2},x,files_1{2,2},x,files_1{3,2})
    
    xlabel('Generation');
    ylabel('Average Fitness');
    set(gcf, 'Position', [500, 500, 800, 400]);
    grid on
    legend('repair_0','repair_1','repair_2','Location','southeast')
    
    saveas(fig,files_1{i,1},'png');
    
end


