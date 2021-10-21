%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Created by Angel Jimenez-Fernandez
% Adapted by Juan Pedro Dominguez-Morales & Daniel Gutierrez-Galan & Alvaro 
% Ayuso Martinez 
% University of Seville 2020
% Last modification: 21/oct/2021
%
% Based on sound2spikes.m
% https://svn.code.sf.net/p/jaer/code/scripts/matlab/cochlea/
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Open connection to jAER:
udpPort = udp('localhost', 8997);
fopen(udpPort);

% Get the current project directory
current_path = pwd;

% Define datasets source and destination folders
folder_name = strcat(current_path,'\..\datasets\audio');
dest_folder_name = strcat(current_path,'\..\datasets\events');

% Get each folder (dataset) in source (audio) folder
classes_folders = dir(folder_name);
classes_folders(1:2) = [];

% For each dataset get all files
for i = 1:length(classes_folders)
    % For each dataset create the associated events folder
    save_folder_name = strcat(classes_folders(i).name, '_aedats');
    mkdir(strcat(dest_folder_name, '\', save_folder_name));
    
    % Get a list of all files in the dataset
    files_in_class = dir(strcat(folder_name, '\', classes_folders(i).name));
    files_in_class(1:2) = [];

    % Read each file and convert audio information into events (through
    % jAER processing) saving it in the new events folder
    for j = 1:length(files_in_class)        
        [y, Fs] = audioread(strcat(strcat(strcat(folder_name,'\',classes_folders(i).name),'\'), files_in_class(j).name));
        logFile(y, Fs, strcat(strcat(dest_folder_name, '\', save_folder_name, '\', files_in_class(j).name)), udpPort);
    end
end

% Clean up the UDP connection to jAER:
fclose(udpPort);
delete(udpPort);
clear udpPort;