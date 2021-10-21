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

function logFile(y, Fs, fileName, udpPort)
    % Create audioplayer object
    player = audioplayer(y, Fs);

    % Start logging
    fprintf(udpPort, ['startlogging ' fileName]); % Send the command
    fprintf('%s', fscanf(udpPort)); % Print the response

    % Play the sound
    play(player);

    while isplaying(player)
        pause(0.005);
    end

    % Stop logging
    fprintf(udpPort,'stoplogging'); % Send the command
    fprintf('%s', fscanf(udpPort)); % Print the response
end