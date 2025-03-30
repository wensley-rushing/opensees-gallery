
pragma openseespy

model  -ndm 3 -ndf 6

set off 0 [expr 0.1*5/sqrt(2)]

node 1 0 0 0 
node 2 3.5355339059327373 3.5355339059327373 0 
fix 1 0 1 1 1 1 1 
fix 2 1 0 1 1 0 0 
geomTransf Linear 1 0 0 1 -jntOffset $off $off 0.0   -$off -$off 0.0

section Elastic 1  30 500 -Iy 1 -Iz 1 -G 1 -J 1.5
element forceBeamColumn 1 1 2 -transform 1 -section 1 -shear 0

pattern Plain 1 Linear {load 2 0 1 0 0 0 0}
integrator LoadControl -3.3333333333333335 
analysis Static 
analyze 1 

puts "[expr [nodeDisp 2 2]/5]"
