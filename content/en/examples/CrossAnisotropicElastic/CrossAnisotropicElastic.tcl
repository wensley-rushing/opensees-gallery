# Cross Anisotropic material model
# For solid model, 8 node brick
# Zhaohui Yang, Yi Bian & Boris Jeremic  March 21, 2003


########################### 
# Create the modelbuilder #
###########################


model BasicBuilder -ndm 3 -ndf 3

# Anisotropic factor
set alpha 1.636

# Young's modulus in vertical direction (kPa)
set Ev    2190
# Young's modulus in any horizontal direction
set Eh    [expr ($Ev)*($alpha)*($alpha)]

# Poisson's ratio for strain in the vertical direction due to a horizontal direct stress.
set nuhv  0.15    

# Poisson's ratio for strain in any horizontal dir. due to a horizontal direct stress.
set nuhh  [expr $nuhv/$alpha]

set Ghv   [expr $alpha*$Ev/(2*(1+$nuhv))]

set p     5.0
set np   -5.0
set NN1   1

###################
# Build the model #
###################

node 1  1.0 1.0 0.0
node 2  0.0 1.0 0.0
node 3  0.0 0.0 0.0
node 4  1.0 0.0 0.0
node 5  1.0 1.0 1.0
node 6  0.0 1.0 1.0
node 7  0.0 0.0 1.0
node 8  1.0 0.0 1.0

#triaxial test boundary
fix 1 0 1 1
fix 2 1 1 1
fix 3 1 0 1
fix 4 0 0 1

# Elastic anisotropic material
#nDMaterial ElasticIsotropic3D 1 $Eh $nuhv 1.8

# Elastic anisotropic material
nDMaterial ElasticCrossAnisotropic 1 $Eh $Ev $nuhv $nuhh $Ghv

# Element
element Brick8N 1  5 6 7 8 1 2 3 4  1  0.0 0.0 -9.81  1.8

#stage 1a
#===========================================================
#isotropic load
pattern Plain 2 "Linear" {
load 1 $np 0   0   -pattern 2
load 3 0   $p  0   -pattern 2
load 4 $np $p  0   -pattern 2
load 5 $np $np $np -pattern 2
load 6 $p  $np $np -pattern 2
load 7 $p  $p  $np -pattern 2
load 8 $np $p  $np -pattern 2
}

#stage 1b
#===========================================================
#Axial compression
#pattern Plain 2 "Linear" {
#load 1 0   0   0   -pattern 2
#load 3 0   0   0   -pattern 2
#load 4 0   0   0   -pattern 2
#load 5 0   0   $np -pattern 2
#load 6 0   0   $np -pattern 2
#load 7 0   0   $np -pattern 2
#load 8 0   0   $np -pattern 2
#}

# Set up recorder
#recorder Element all -time -file AniStrain strain

#recorder Node node_z.out disp -time -node 5 -dof 3
#recorder plot node_z.out "disp load"  10 10 300 300 -columns 2 1


system UmfPack
constraints Plain
test NormDispIncr 1.0e-8 30 0

#integrator DisplacementControl  3   1   $dU  1 $dU $dU
#integrator ArcLength 0.0075 1.0
integrator HSConstraint 0.0075 1.0 1.0 1.0

#integrator LoadControl 1 1 1 1
algorithm Newton
numberer RCM
analysis Static

analyze $NN1
print node 5 8

#stage 2
#===========================================================
#Axial loading
#wipeAnalysis

#equalDOF 5 6 3 3
#equalDOF 5 7 3 3
#equalDOF 5 8 3 3
       	  

#set previous load constant
#loadConst time 0

# Before shifting to disp. control, apply reference load on the top
#pattern Plain 3 "Linear" {
#load 5 0.0 0.0 $np 
#load 6 0.0 0.0 $np
#load 7 0.0 0.0 $np 
#load 8 0.0 0.0 $np
#}
 
#Set up recorder for axial loading stage

#recorder Node node_z.out disp -time -node 5 -dof 3

#recorder Element 1 -file element.out force

#set NN2 10
#set ndz -0.002

#system UmfPack				    
#constraints Plain
#test NormDispIncr 1.0e-08 30  0
#integrator DisplacementControl 5 3 $ndz 1 $ndz $ndz
#algorithm Newton
#numberer RCM
#analysis Static

#analyze $NN2

wipe



