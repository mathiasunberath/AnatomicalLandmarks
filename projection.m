% This code is an example for understanding the projection 
% geometry of anatomical landmarks. 
% Copyright Cong Gao, the Johns Hopkins University, email: cgao11@jhu.edu
%% Offset setup 
% The code takes the CT file: ABD_LYMPH_057 as an example
% Dicom Offset
dicom_offset = [-199.61, -380.83, -686.80];
% Origin Offset
origin_offset = [-206, -244, -118];
% 1st Landmark
landmark3D = [30.45, 122.19, -630.07];
% Offset manipulation
landmark3D(1) = -(landmark3D(1) + dicom_offset(1)) + origin_offset(1);
landmark3D(2) = -(landmark3D(2) + dicom_offset(2)) + origin_offset(2);
landmark3D(3) =   landmark3D(3) - dicom_offset(3)  + origin_offset(3) - 25;

%% Projection
% The C-arm intrinsic matrix is
K = [1948.05,        0,   307.5;
           0,  1948.05,   239.5;
           0,        0,       1];
% We randomly generate the rotation matrix R and translation vector T
R = [0.87,  -0.49,   0.0;
    -0.07,  -0.13,  -0.99;
     0.49,   0.86,  -0.15];
T = [0,  0,  639.61]';
% Formulate the 3-by-4 projection matrix P
P = K * [R, T];
% Do projection by making landmark3D as homogeneous coordinate
proj = P * [landmark3D'; 1];
% Save into 2D landmark coordinate
landmark2D(1) = proj(1) / proj(3);
landmark2D(2) = proj(2) / proj(3);

display(landmark2D);

