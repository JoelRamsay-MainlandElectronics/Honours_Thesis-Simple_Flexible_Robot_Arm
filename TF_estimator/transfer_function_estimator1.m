clc
close all
clear all

%% Load data
ElbowTruePositionRealControllerDisabled = importdata('ElbowTruePositionRealControllerDisabled.csv');
ShoulderTruePositionRealControllerDisabled = importdata('ShoulderTruePositionRealControllerDisabled.csv');
ElbowTruePositionRealControllerEnabled = importdata('ElbowTruePositionRealControllerEnabled.csv');
ShoulderTruePositionRealControllerEnabled = importdata('ShoulderTruePositionRealControllerEnabled.csv');

%% Input Signal Controller Disabled
ElbowInputSignal = importdata('ElbowInputSignalControllerDisabled.csv');
ShoulderInputSignal = importdata('ShoulderInputSignalControllerDisabled.csv');

ElbowInputSignalLongControllerDisabled = [];
number_motions_controller_disabled = length(ElbowTruePositionRealControllerDisabled)/ length(ElbowInputSignal);
for i=1:number_motions_controller_disabled
    ElbowInputSignalLongControllerDisabled = [ElbowInputSignalLongControllerDisabled;ElbowInputSignal];
end

%% Input Signal Controller Enabled
ElbowInputSignal = importdata('ElbowInputSignalControllerEnabled.csv');
ShoulderInputSignal = importdata('ShoulderInputSignalControllerEnabled.csv');

ElbowInputSignalLongControllerEnabled = [];
number_motions_controller_enabled = length(ElbowTruePositionRealControllerEnabled)/ length(ElbowInputSignal);
for i=1:number_motions_controller_enabled
    ElbowInputSignalLongControllerEnabled = [ElbowInputSignalLongControllerEnabled;ElbowInputSignal];
end

%% Estimate Transfer Function Without Controller (input - end effector desired angle, output - end effector true position)
np = 6; %number of poles
fs = 60; %Hz
time_length = length(ElbowInputSignalLongControllerDisabled)/fs/number_motions_controller_disabled;
data = iddata(ElbowTruePositionRealControllerDisabled,ElbowInputSignalLongControllerDisabled, 1/fs);
sys = tfest(data,np)

[num,den] = tfdata(sys);
TF_Elbow_controller_disabled = tf(num,den)

%% Estimate Transfer Function With Controller (input - end effector desired angle, output - end effector true position)
np = 6; %number of poles
fs = 60; %Hz
time_length = length(ElbowInputSignalLongControllerEnabled)/fs/number_motions_controller_enabled;
data = iddata(ElbowTruePositionRealControllerEnabled,ElbowInputSignalLongControllerEnabled, 1/fs);
sys = tfest(data,np)

[num,den] = tfdata(sys);
TF_Elbow_controller_enabled = tf(num,den)

%% Step plot

t = 0:(1/fs):time_length*number_motions_controller_disabled-(1/fs); 
u = ElbowInputSignalLongControllerDisabled;
lsim(TF_Elbow_controller_disabled,u,t)

figure;
t = 0:(1/fs):time_length*number_motions_controller_enabled-(1/fs); 
u = ElbowInputSignalLongControllerEnabled;
lsim(TF_Elbow_controller_enabled,u,t)