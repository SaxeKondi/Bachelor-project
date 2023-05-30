Data = readmatrix("Delay test control to video feedback.xlsx", "Range", 'D2:D51');

measurementNumber = 1:length(Data)
sz = 15;

figure(1)
plot(measurementNumber,Data, 'b','LineWidth',1)
hold on
scatter(measurementNumber,Data, sz, "filled", "blue")
ylabel('time [s]') 
xlabel('Measurement number') 
grid
hold off
% 
% figure(2)
% plot(tpi,Vpi, 'Color',[0.4660 0.6740 0.1880],'LineWidth',2)
% hold on
% xlabel('time [ms]') 
% ylabel('Voltage [v]') 
% grid
% hold off



mean(Data)