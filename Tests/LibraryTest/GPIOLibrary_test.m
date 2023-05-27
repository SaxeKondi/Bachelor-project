pigpio = readmatrix("pigpio_Correct_signal.csv", "Range", 3);
large = readmatrix("rpiGPIO Large pulse.csv", "Range", 3);
small = readmatrix("rpiGPIO Small pulse.csv", "Range", 3);
normal = readmatrix("rpiGPIO Standard pulse.csv", "Range", 3);

tpi = pigpio(5001:30000,1).*1000 + 2;
Vpi = pigpio(5001:30000,2);

tsmall = small(5001:30000,1).*1000 + 2;
Vsmall = small(5001:30000,2);

tlarge = large(5001:30000,1).*1000 + 2;
Vlarge = large(5001:30000,2);

tnormal = normal(5001:30000,1).*1000 + 2;
Vnormal = normal(5001:30000,2);

figure(1)
plot(tsmall,Vsmall, 'Color',[0 0.4470 0.7410],'LineWidth',2)
hold on
plot(tnormal,Vnormal, 'Color',[0.8500 0.3250 0.0980],'LineWidth',2)
plot(tlarge,Vlarge, 'Color',[0.6350 0.0780 0.1840],'LineWidth',2)

xlabel('time [ms]') 
ylabel('Voltage [v]') 
grid
hold off

figure(2)
plot(tpi,Vpi, 'Color',[0.4660 0.6740 0.1880],'LineWidth',2)
hold on
xlabel('time [ms]') 
ylabel('Voltage [v]') 
grid
hold off



