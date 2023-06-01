clc
clear all
close all
%% Approxing the tilt.
scope_1 = readmatrix('test_1.csv', 'Range', 'A3:C1572');
scope_2 = readmatrix('test_2.csv', 'Range', 'A3:C1635');
scope_3 = readmatrix('test_3.csv', 'Range', 'A3:C1545');
scope_4 = readmatrix('test_4.csv', 'Range', 'A3:C2002');
scope_5 = readmatrix('Without filter.csv', 'Range', 'A3:b50002');
scope_6 = readmatrix('With filter.csv', 'Range', 'A3:b50002');

scope_7 = [93.0, 101.1, 103.91, 108.54, 113.05, 117.50, 121.88, 126.95, 131.5, 136.3, 142.6];
scope_7_x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
scope_8 = [93.80, 99.35, 103.91, 108.54, 113.05, 117.50, 121.88, 126.95, 131.5, 136.3, 142.05]

scope_time_1 = scope_1(:, 1);
scope_time_1 = scope_time_1 + abs(scope_time_1(1));

scope_voltage_input_1 = scope_1(:, 2);
scope_voltage_output_1 = scope_1(:, 3);
scope_voltage_output_1 = (-1)*(scope_voltage_output_1 - 3.2721);



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
%title('Plot of V(t) of the control voltage')
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
%title('Plot of V(t) of the control voltage')
xlabel('time [s]') 
ylabel('Voltage [v]') 


scope_time_5 = scope_5(:, 1);
scope_time_5 = scope_time_5 - abs(scope_time_5(1));

scope_voltage_output_5 = scope_5(:, 2);
scope_voltage_output_5 = (-1)*(scope_voltage_output_5 - 3.2721);

figure(5)
hold on
plot(scope_time_5, scope_voltage_output_5);
legend({'Position'})
hold off
grid on
%title('Plot of the position output without filter and P = 10')
xlabel('time [s]') 
ylabel('Voltage [v]') 


scope_time_6 = scope_6(:, 1);
scope_time_6 = scope_time_6 - abs(scope_time_6(1));

scope_voltage_output_6 = scope_6(:, 2);
scope_voltage_output_6 = (-1)*(scope_voltage_output_6 - 3.2721);

figure(6)
hold on
plot(scope_time_6, scope_voltage_output_6);
legend({'Position'})
hold off
grid on
%title('Plot of the position output with filter and P = 10')
xlabel('time [s]') 
ylabel('Voltage [v]') 

scope_7_l =[93, 142.6];
scope_7_l_x = [0,100];
figure(7)
hold on
plot(scope_7_x, scope_7);
plot(scope_7_l_x,scope_7_l);
legend({'Measured','Linear'})
hold off
grid on
%title('Plot of the average measured position vs the theoretical position')
xlabel('duty cylce [%]') 
ylabel('Length [mm]') 


scope_8_l =[93.8, 142.05];
scope_7_l_x = [0,100];
figure(8)
hold on
plot(scope_7_x, scope_8);
plot(scope_7_l_x,scope_8_l);
legend({'Measured','Linear'})
hold off
grid on
%title('Plot of the average measured position vs the theoretical position')
xlabel('duty cylce [%]') 
ylabel('Length [mm]') 


scope_9 = [93.814, 99.329, 103.847, 108.473, 112.969, 117.439, 121.924, 126.974, 131.478, 136.293, 141.948];
scope_10 = [0.11, 0.19, 0.21, 0.15, 0.27, 0.25, 0.17, 0.17, 0.17, 0.08, 0.17];

scope_8_l =[93.8, 142.05];
scope_7_l_x = [0,100];
figure(9)
hold on
plot(scope_7_x, scope_10,'b*','LineWidth',4);
legend({'Max-min'});
hold off
grid on
%title('Plot of the average measured position vs the theoretical position')
xlabel('duty cylce [%]') 
ylabel('Distance [mm]') 


