clc
clear all
close all
%% Approxing the tilt.
scope_1 = readmatrix('test_1.csv', 'Range', 'A3:C1572');
scope_2 = readmatrix('test_2.csv', 'Range', 'A3:C1635');
scope_3 = readmatrix('test_3.csv', 'Range', 'A3:C1545');
scope_4 = readmatrix('test_4.csv', 'Range', 'A3:C2002');

scope_time_1 = scope_1(:, 1);
scope_time_1 = scope_time_1 + abs(scope_time_1(1));

scope_voltage_input_1 = scope_1(:, 2);
scope_voltage_output_1 = scope_1(:, 3);
scope_voltage_output_1 = (-1)*(scope_voltage_output_1 - 3.2721);

figure(1)
hold on
plot(scope_time_1, scope_voltage_input_1);
plot(scope_time_1, scope_voltage_output_1)
legend({'Input','Position'})
hold off
grid on
title('Plot of V(t) of the control voltage')
xlabel('time [s]') 
ylabel('Voltage [v]') 

scope_time_2 = scope_2(:, 1);
scope_time_2 = scope_time_2 + abs(scope_time_2(1));

scope_voltage_input_2 = scope_2(:, 2);
scope_voltage_output_2 = scope_2(:, 3);
scope_voltage_output_2 = (-1)*(scope_voltage_output_2 - 3.2721);

figure(2)
hold on
plot(scope_time_2, scope_voltage_input_2);
plot(scope_time_2, scope_voltage_output_2)
legend({'Input','Position'})
hold off
grid on
title('Plot of V(t) of the control voltage')
xlabel('time [s]') 
ylabel('Voltage [v]') 

scope_time_3 = scope_3(:, 1);
scope_time_3 = scope_time_3 + abs(scope_time_3(1));

scope_voltage_input_3 = scope_3(:, 2);
scope_voltage_output_3 = scope_3(:, 3);
scope_voltage_output_3 = (-1)*(scope_voltage_output_3 - 3.2721);

figure(3)
hold on
plot(scope_time_3, scope_voltage_input_3);
plot(scope_time_3, scope_voltage_output_3)
legend({'Input','Position'})
hold off
grid on
title('Plot of V(t) of the control voltage')
xlabel('time [s]') 
ylabel('Voltage [v]') 

scope_time_4 = scope_4(:, 1);
scope_time_4 = scope_time_4 + abs(scope_time_4(1));

scope_voltage_input_4 = scope_4(:, 2);
scope_voltage_output_4 = scope_4(:, 3);
scope_voltage_output_4 = (-1)*(scope_voltage_output_4 - 3.2721);

figure(4)
hold on
plot(scope_time_4, scope_voltage_input_4);
plot(scope_time_4, scope_voltage_output_4)
xline(6.31)
yline(1.70426)
yline(1.42285)
legend({'Input','Position'})
hold off
grid on
title('Plot of V(t) of the control voltage')
xlabel('time [s]') 
ylabel('Voltage [v]') 
