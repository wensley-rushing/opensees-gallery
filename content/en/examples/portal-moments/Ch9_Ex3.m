%% Script for Example 3 in Chapter 9 of Structural Analysis Theory and Applications
%  displacement method of portal frame

%  =========================================================================================
%  FEDEASLab - Release 5.1, July 2020
%  Matlab Finite Elements for Design, Evaluation and Analysis of Structures
%  Professor Filip C. Filippou (filippou@berkeley.edu)
%  Department of Civil and Environmental Engineering, UC Berkeley
%  Copyright(c) 1998-2020. The Regents of the University of California. All Rights Reserved.
%  =========================================================================================

%% clear memory; close any open windows
CleanStart

%% define structural model (coordinates, connectivity, boundary conditions, element types)
% specify node coordinates (could only specify non-zero terms)
XYZ(1,:) = [  0    0];  % first node
XYZ(2,:) = [  0    8];  % second node, etc
XYZ(3,:) = [ 10    8];  %
XYZ(4,:) = [ 20    8];
XYZ(5,:) = [ 20   -2];

% connectivity array
CON(1,:) = [  1   2];
CON(2,:) = [  2   3];
CON(3,:) = [  3   4];
CON(4,:) = [  4   5];

% boundary conditions (1 = restrained,  0 = free)
BOUN(1,:) = [1 1 1];
BOUN(5,:) = [1 1 1];

% specify element type
[ElemName{1:4}] = deal('Lin2dFrm');    % linear 2d frame element

%% create Model
Model = Create_SimpleModel (XYZ,CON,BOUN,ElemName);

% display model
% plot parameters
% -------------------------------------------------------------------------
WinXr = 0.40;   % X-ratio of plot window to screen size 
WinYr = 0.80;   % Y-ratio of plot window to screen size
% -------------------------------------------------------------------------
NodSF = 3/4;    % relative size for node symbol
AxsSF = 3/4;    % relative size of arrows
HngSF = 3/4;    % relative size of releases
HOfSF = 1;      % relative size of hinge offset from end
% -------------------------------------------------------------------------
Create_Window (WinXr,WinYr);       % open figure window
PlotOpt.PlNod = 'yes';
PlotOpt.PlBnd = 'yes';
PlotOpt.NodSF = NodSF;
Plot_Model (Model,[],PlotOpt);
PlotOpt.AxsSF = AxsSF;
PlotOpt.LOfSF = 1.6.*NodSF;
Label_Model (Model,PlotOpt);

%% specify element properties
ElemData = cell(Model.ne,1);
for el=1:Model.ne
   ElemData{el}.E = 1000;        % elastic modulus
   ElemData{el}.A = 1e6;         % large area for "inextensible" elements a-d
   ElemData{el}.I = 60;          % moment of inertia
end
% insert release at base of element a
ElemData{1}.Release = [0;1;0];

%% 1. Load case: uniformly distributed load in elements a and b
% specify uniformly distributed load in elements a and b
ElemData{1}.w  = [0; -5];
ElemData{2}.w  = [0;-10];
% plot and label distributed element load
Create_Window (WinXr,WinYr);       % open figure window
PlotOpt.PlNod = 'no';
Plot_Model  (Model,[],PlotOpt);    % plot model
PlotOpt.FrcSF = 4;
% PlotOpt.TipSF = 1.25;
Plot_ElemLoading (Model,ElemData,PlotOpt);
Plot_Model (Model,[],PlotOpt);    % plot model

% displacement method of analysis
S_DisplMethod
% display and label bending moment distribution
% -------------------------------------------------------------------------
ScaleM = 1/2;    % scale factor for bending moments
MDigt  = 1;      % number of significant digits for bending moments
% -------------------------------------------------------------------------
Create_Window (WinXr,WinYr);    % open figure window
Plot_Model(Model);
Plot_2dMomntDistr(Model,ElemData,Q,[],ScaleM);
Label_2dMoments(Model,Q,[],MDigt);

% plot deformed shape
MAGF = 30;                     % magnification factor for deformed shape
% display model
Create_Window (WinXr,WinYr);    % open figure window
PlotOpt.MAGF  = MAGF;
PlotOpt.PlNod = 'no';
Plot_Model(Model,[],PlotOpt);
PlotOpt.HngSF = HngSF;
PlotOpt.HOfSF = HOfSF;
PlotOpt.NodSF = NodSF;
Plot_DeformedStructure (Model,ElemData,Uf,Ve,PlotOpt);

%% 2. Load case: thermal deformation of elements a and b
% no nodal forces
% clear equivalent nodal force vector of previous load case
clear Pwf
% clear distributed load from ElemData
ElemData{1}.w  = [0; 0];
ElemData{2}.w  = [0; 0];
% specify initial element deformations in ElemData
ElemData{1}.e0 = [0;0.002];
ElemData{2}.e0 = [0;0.002];
% ElemData{1}.Release = [0;1;0];

% plot and label initial deformations
Create_Window (WinXr,WinYr);       % open figure window
PlotOpt.FrcSF = 5;
PlotOpt.TipSF = 1.25;
Plot_ElemLoading (Model,ElemData,PlotOpt);
Plot_Model  (Model,[],PlotOpt);    % plot model

% displacement method of analysis
S_DisplMethod
% display and label bending moment distribution
Create_Window (WinXr,WinYr);    % open figure window
Plot_Model(Model);
Plot_2dMomntDistr(Model,ElemData,Q,[],ScaleM);
Label_2dMoments(Model,Q,[],MDigt);

% plot curvature distribution
Create_Window (WinXr,WinYr);       % open figure window
Plot_Model(Model);       % original configuration
Plot_2dCurvDistr(Model,ElemData,Q,[],1/2);

% plot deformed shape
MAGF = 50;                     % magnification factor for deformed shape
% display model
Create_Window (WinXr,WinYr);    % open figure window
Plot_Model(Model);
PlotOpt.MAGF  = MAGF;
PlotOpt.PlNod = 'no';
Plot_Model(Model,[],PlotOpt);
PlotOpt.NodSF = NodSF;
Plot_DeformedStructure (Model,ElemData,Uf,Ve,PlotOpt);
