% ECEN 638 HW8, Coady Lewis, 4/16/2022

% The biggest holdup in runtime comes in part b with 
% b_plot_points (line 118). High values give good plot resolution,
% but you can reduce b_plot_points to speed up the calculation.
% I used 1000 to get the submitted plot.

clc;
clear;
close all;



% Constants
H=0.35;
ns=99;
a=0.001588;
delta=2*H/(ns+1);
gap_voltage=1;
eta=120*pi;
f=300*10^6;
c=3*10^8;
k=(2*pi*f)/c;
% constants for integral approximation
integration_intervals=1000;
integral_delta=delta/integration_intervals;

% PART A*******************************************************************

% Vars
Vm=zeros(ns+2,1);
Z1n=zeros(1,ns);
Z2n=zeros(ns,ns);
Zmn=zeros(ns+2,ns+2);
z=linspace(-H,H,ns+2);


% % Z1n Test Vector
% for i=1:ns
%     Z1n(i)=i;
% end

% Calculate 1st Row vector Z1n here
z1=z(2); %skip point in left side half pulse
for n=1:ns
    z_center=z(n+1);%skip point in left side half pulse
    % use trapezoidal approximation for integral
    lower_limit=z_center-delta/2;
    upper_limit=z_center+delta/2;
    integ=0;
    for m=1:integration_intervals
        lower=lower_limit+(m-1)*integral_delta;
        upper=lower_limit+m*integral_delta;
        % get lower integrand value of interval
        R_r_l=sqrt((z1-lower)^2 + a^2);
        integrand_term1_l=exp(-1i*k*R_r_l)/(4*pi*(R_r_l^5));
        integrand_term2_l=(1+1i*k*R_r_l)*(2*(R_r_l^2)-3*(a^2))+((k*a*R_r_l)^2);
        integrand_c_l=integrand_term1_l*integrand_term2_l;
        % get upper integrand value of interval
        R_r_u=sqrt((z1-upper)^2 + a^2);
        integrand_term1_u=exp(-1i*k*R_r_u)/(4*pi*(R_r_u^5));
        integrand_term2_u=(1+1i*k*R_r_u)*(2*(R_r_u^2)-3*(a^2))+((k*a*R_r_u)^2);
        integrand_c_u=integrand_term1_u*integrand_term2_u;
        % add interval's trapezoidal area to integral
        integ = integ + 0.5*(integrand_c_l+integrand_c_u)*integral_delta;
    end
    Z1n(n)=((1i*eta)/k)*integ;
end

% Get current
Z2n=toeplitz(real(Z1n))+1i*toeplitz(imag(Z1n));
Zmn(1,1)=1;
Zmn(ns+2,ns+2)=1;
Zmn(2:ns+1,2:ns+1)=Z2n;
Vm((ns+3)/2)=gap_voltage/delta;
In=Zmn\Vm;

% plotting
figure(1); % Create a separate first figure window
cr = real(In); % Real part of the current
plot(z,cr);
hold on % Allows another graph to be plotted on the same figure
%figure(2) %Create a separate second figure window
ci = imag(In); %Imaginary part of current
plot(z,ci,':','LineWidth',1.5) % ':' designates a dotted line graph
%figure(3) %plot an axis line at 0 amps
plot(z,zeros(1,ns+2))
xlabel('Position in Wavelengths')
ylabel('Current Amplitude')
hold off % Allows another graph to be plotted on the same figure
legend('Real','Imag') %used when plotting the 2 figs. together

% input impedance check (results are off, but close)
gap_current=In((ns+3)/2);
disp(gap_voltage/gap_current)
















% PART B*******************************************************************
% reduce b_plot_points to speed up calculation

L=H*c/f; % length from original run above
% will plot 1 < (pi*L*c)/f < 3.5 to match example 
% (pi*L*c)/3.5 < f < (pi*L*c)/1
b_plot_points = 100;
x_axis = linspace(1,3.5,b_plot_points);
freq_values = (pi*L*c)./x_axis;
admittances = zeros(1,b_plot_points);
for freq_ind=1:b_plot_points
    f=freq_values(freq_ind);
    % Constants
    H=L*f/c;
    ns=99;
    a=0.001588;
    delta=2*H/(ns+1);
    gap_voltage=1;
    eta=120*pi;
    
    c=3*10^8;
    k=(2*pi*f)/c;
    % constants for integral approximation
    integration_intervals=1000;
    integral_delta=delta/integration_intervals;
    
    % Vars
    Vm=zeros(ns+2,1);
    Z1n=zeros(1,ns);
    Z2n=zeros(ns,ns);
    Zmn=zeros(ns+2,ns+2);
    z=linspace(-H,H,ns+2);
    
    
    % % Z1n Test Vector
    % for i=1:ns
    %     Z1n(i)=i;
    % end
    
    % Calculate 1st Row vector Z1n here
    z1=z(2); %skip point in left side half pulse
    for n=1:ns
        z_center=z(n+1);%skip point in left side half pulse
        % use trapezoidal approximation for integral
        lower_limit=z_center-delta/2;
        upper_limit=z_center+delta/2;
        integ=0;
        for m=1:integration_intervals
            lower=lower_limit+(m-1)*integral_delta;
            upper=lower_limit+m*integral_delta;
            % get lower integrand value of interval
            R_r_l=sqrt((z1-lower)^2 + a^2);
            integrand_term1_l=exp(-1i*k*R_r_l)/(4*pi*(R_r_l^5));
            integrand_term2_l=(1+1i*k*R_r_l)*(2*(R_r_l^2)-3*(a^2))+((k*a*R_r_l)^2);
            integrand_c_l=integrand_term1_l*integrand_term2_l;
            % get upper integrand value of interval
            R_r_u=sqrt((z1-upper)^2 + a^2);
            integrand_term1_u=exp(-1i*k*R_r_u)/(4*pi*(R_r_u^5));
            integrand_term2_u=(1+1i*k*R_r_u)*(2*(R_r_u^2)-3*(a^2))+((k*a*R_r_u)^2);
            integrand_c_u=integrand_term1_u*integrand_term2_u;
            % add interval's trapezoidal area to integral
            integ = integ + 0.5*(integrand_c_l+integrand_c_u)*integral_delta;
        end
        Z1n(n)=((1i*eta)/k)*integ;
    end
    
    % Get current
    Z2n=toeplitz(real(Z1n))+1i*toeplitz(imag(Z1n));
    Zmn(1,1)=1;
    Zmn(ns+2,ns+2)=1;
    Zmn(2:ns+1,2:ns+1)=Z2n;
    Vm((ns+3)/2)=gap_voltage/delta;
    In=Zmn\Vm;
    gap_current=In((ns+3)/2);
    admittances(freq_ind)=gap_current/gap_voltage;
end

% plotting
figure(2); % Create a separate first figure window
cr = real(admittances); % Real part of the current
plot(x_axis,cr);
hold on % Allows another graph to be plotted on the same figure
%figure(2) %Create a separate second figure window
ci = imag(admittances); %Imaginary part of current
plot(x_axis,ci,':','LineWidth',1.5) % ':' designates a dotted line graph
%figure(3) %plot an axis line at 0 amps
plot(x_axis,zeros(1,b_plot_points))
xlabel('(beta*L)/2')
ylabel('Input Admittance')
hold off % Allows another graph to be plotted on the same figure
legend('Real','Imag') %used when plotting the 2 figs. together












% PART C*******************************************************************
% We want |E_theta(r_0,theta)/max(E_theta(r_0,theta))|
% so we can drop the r components of E_theta

% 2H=4*lambda/5************************************************************
theta_vals=linspace(0,2*pi,360);

% Constants
H=0.4; % in terms of wavelength
ns=99;
a=0.001588;
delta=2*H/(ns+1);
gap_voltage=1;
eta=120*pi;
f=300*10^6;
c=3*10^8;
k=(2*pi*f)/c;
% constants for integral approximation
integration_intervals=1000;
integral_delta=delta/integration_intervals;


% Vars
Vm=zeros(ns+2,1);
Z1n=zeros(1,ns);
Z2n=zeros(ns,ns);
Zmn=zeros(ns+2,ns+2);
z=linspace(-H,H,ns+2);


% % Z1n Test Vector
% for i=1:ns
%     Z1n(i)=i;
% end

% Calculate 1st Row vector Z1n here
z1=z(2); %skip point in left side half pulse
for n=1:ns
    z_center=z(n+1);%skip point in left side half pulse
    % use trapezoidal approximation for integral
    lower_limit=z_center-delta/2;
    upper_limit=z_center+delta/2;
    integ=0;
    for m=1:integration_intervals
        lower=lower_limit+(m-1)*integral_delta;
        upper=lower_limit+m*integral_delta;
        % get lower integrand value of interval
        R_r_l=sqrt((z1-lower)^2 + a^2);
        integrand_term1_l=exp(-1i*k*R_r_l)/(4*pi*(R_r_l^5));
        integrand_term2_l=(1+1i*k*R_r_l)*(2*(R_r_l^2)-3*(a^2))+((k*a*R_r_l)^2);
        integrand_c_l=integrand_term1_l*integrand_term2_l;
        % get upper integrand value of interval
        R_r_u=sqrt((z1-upper)^2 + a^2);
        integrand_term1_u=exp(-1i*k*R_r_u)/(4*pi*(R_r_u^5));
        integrand_term2_u=(1+1i*k*R_r_u)*(2*(R_r_u^2)-3*(a^2))+((k*a*R_r_u)^2);
        integrand_c_u=integrand_term1_u*integrand_term2_u;
        % add interval's trapezoidal area to integral
        integ = integ + 0.5*(integrand_c_l+integrand_c_u)*integral_delta;
    end
    Z1n(n)=((1i*eta)/k)*integ;
end

% Get current
Z2n=toeplitz(real(Z1n))+1i*toeplitz(imag(Z1n));
Zmn(1,1)=1;
Zmn(ns+2,ns+2)=1;
Zmn(2:ns+1,2:ns+1)=Z2n;
Vm((ns+3)/2)=gap_voltage/delta;
In=Zmn\Vm;

% Get normalized far field
E_theta=zeros(1,360);
for theta_ind=1:360
    summation=0;
    for n=1:ns+2
        summation=summation + In(n)*exp(1i*k*z(n)*cos(theta_vals(theta_ind)));
    end
    E_theta(theta_ind)=abs(sin(theta_vals(theta_ind))*summation);
end
normalization_val = max(E_theta);
for i=1:360
    E_theta(i)=E_theta(i)/normalization_val;
end


    
% plotting
figure(3); % Create a separate first figure window
polarplot(theta_vals,E_theta);
set(gca,'ThetaZeroLocation','top') % put theta=0 at the top to match convention
title('Pattern for 2H=4*lambda/5')



% 2H=lambda************************************************************
theta_vals=linspace(0,2*pi,360);

% Constants
H=0.5; % in terms of wavelength
ns=99;
a=0.001588;
delta=2*H/(ns+1);
gap_voltage=1;
eta=120*pi;
f=300*10^6;
c=3*10^8;
k=(2*pi*f)/c;
% constants for integral approximation
integration_intervals=1000;
integral_delta=delta/integration_intervals;


% Vars
Vm=zeros(ns+2,1);
Z1n=zeros(1,ns);
Z2n=zeros(ns,ns);
Zmn=zeros(ns+2,ns+2);
z=linspace(-H,H,ns+2);


% % Z1n Test Vector
% for i=1:ns
%     Z1n(i)=i;
% end

% Calculate 1st Row vector Z1n here
z1=z(2); %skip point in left side half pulse
for n=1:ns
    z_center=z(n+1);%skip point in left side half pulse
    % use trapezoidal approximation for integral
    lower_limit=z_center-delta/2;
    upper_limit=z_center+delta/2;
    integ=0;
    for m=1:integration_intervals
        lower=lower_limit+(m-1)*integral_delta;
        upper=lower_limit+m*integral_delta;
        % get lower integrand value of interval
        R_r_l=sqrt((z1-lower)^2 + a^2);
        integrand_term1_l=exp(-1i*k*R_r_l)/(4*pi*(R_r_l^5));
        integrand_term2_l=(1+1i*k*R_r_l)*(2*(R_r_l^2)-3*(a^2))+((k*a*R_r_l)^2);
        integrand_c_l=integrand_term1_l*integrand_term2_l;
        % get upper integrand value of interval
        R_r_u=sqrt((z1-upper)^2 + a^2);
        integrand_term1_u=exp(-1i*k*R_r_u)/(4*pi*(R_r_u^5));
        integrand_term2_u=(1+1i*k*R_r_u)*(2*(R_r_u^2)-3*(a^2))+((k*a*R_r_u)^2);
        integrand_c_u=integrand_term1_u*integrand_term2_u;
        % add interval's trapezoidal area to integral
        integ = integ + 0.5*(integrand_c_l+integrand_c_u)*integral_delta;
    end
    Z1n(n)=((1i*eta)/k)*integ;
end

% Get current
Z2n=toeplitz(real(Z1n))+1i*toeplitz(imag(Z1n));
Zmn(1,1)=1;
Zmn(ns+2,ns+2)=1;
Zmn(2:ns+1,2:ns+1)=Z2n;
Vm((ns+3)/2)=gap_voltage/delta;
In=Zmn\Vm;

% Get normalized far field
E_theta=zeros(1,360);
for theta_ind=1:360
    summation=0;
    for n=1:ns+2
        summation=summation + In(n)*exp(1i*k*z(n)*cos(theta_vals(theta_ind)));
    end
    E_theta(theta_ind)=abs(sin(theta_vals(theta_ind))*summation);
end
normalization_val = max(E_theta);
for i=1:360
    E_theta(i)=E_theta(i)/normalization_val;
end


    
% plotting
figure(4); % Create a separate first figure window
polarplot(theta_vals,E_theta);
set(gca,'ThetaZeroLocation','top') % put theta=0 at the top to match convention
title('Pattern for 2H=lambda')