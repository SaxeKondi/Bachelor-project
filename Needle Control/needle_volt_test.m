clc
clear all
close all
%% Approxing the tilt.
scope = readmatrix('scope_1.csv', 'Range', 'A3:B1803');


scope_time = scope(:, 1);
scope_voltage = scope(:, 2);
scope_time = scope_time + abs(scope_time(1));
figure(1)
plot(scope_time, scope_voltage);
grid on
title('Plot of V(t) of the control voltage')
xlabel('time [s]') 
ylabel('Voltage [v]') 