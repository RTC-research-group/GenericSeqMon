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

function logFile(y, fs, fileName, udpPort)
    fprintf(udpPort, ['startlogging ' fileName]); % Send the command
    fprintf('%s', fscanf(udpPort)); % Print the response
    
    pause(0.1);
    sound(y, fs); % Plays the sound
    pause(length(y) / fs); % Wait until it ends
    
    pause(0.1)
    fprintf(udpPort,'stoplogging'); % Send the command
    fprintf('%s', fscanf(udpPort)); % Print the response
end