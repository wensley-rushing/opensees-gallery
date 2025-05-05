model basic -ndm 2 -ndf 2 
nDMaterial ASDConcrete3D 1 30000.0 0.2 \
  -Te 0.0 9e-05 0.00015 0.00507 0.0250501 0.250501 \
  -Ts 0.0   2.7     3.0     0.6 0.003 0.003 \
  -Td 0.0 0.0 0.0 0.960552268244576 0.9999800399998403 0.9999995660869531 \
  -Ce 0.0 0.0005 0.0006666666666666666 0.0008333333333333333 0.001 0.0011666666666666665 0.0013333333333333333 0.0015 0.0016666666666666666 0.0018333333333333333 0.002 0.18327272727272728 0.18377272727272728 \
  -Cs 0.0 15.0 19.282032302755088 22.459666924148337 24.852813742385703 26.6515138991168 27.979589711327122 28.92304845413264 29.54451150103322 29.891252930760572 30.0 3.0 3.0 \
  -Cd 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -2.220446049250313e-16 0.0 0.0 0.9981618744961699 0.9981786141748574 \
  -autoRegularization 8.97663211186248 

#section PlaneStress 1 1 1.0 

nDMaterial PlaneStress 2 1

node 1   0.0   0.0
node 2 250.0   0.0
node 3   0.0 250.0 

element tri31 1 1 2 3   1.0 PlaneStress 2
fix 1 1 1 
fix 2 0 1 
fix 3 1 0 

timeSeries Linear 1 
constraints Transformation 
numberer Plain 
system FullGeneral 
test NormDispIncr 1e-08 10 0
algorithm Newton 

puts "u  = [nodeDisp 2 ]"
pattern Plain 1 1 {
  sp 2 1 -0.2777777777777778
}
setTime -0.0
integrator LoadControl 0.09090909090909091 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 10
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
puts "u  = [nodeDisp 2 ]"
pattern Plain 1 1 {
  sp 2 1 -0.5555555555555556
}
setTime 0.1092207928837136 
integrator LoadControl 0.046883116164015075 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 18
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 

remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
puts "u = [nodeDisp 2 ]"
pattern Plain 1 1 {
  sp 2 1 -0.8333333333333333
}
setTime 0.4064658887011011 
integrator LoadControl 0.03123863743678415 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
nodeDisp 2 
pattern Plain 1 1 
sp 2 1 -1.1111111111111112 -pattern 1
setTime 0.6866832986178911 
integrator LoadControl 0.024101284721700682 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
nodeDisp 2 
pattern Plain 1 1 
sp 2 1 -1.3888888888888888 -pattern 1
setTime 0.9351711337464219 
integrator LoadControl 0.02160962208452603 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
nodeDisp 2 
pattern Plain 1 1 
sp 2 1 -1.6666666666666665 -pattern 1
setTime 0.795120169687898 
integrator LoadControl 0.01575998694708477 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
nodeDisp 2 
pattern Plain 1 1 
sp 2 1 -1.9444444444444444 -pattern 1
setTime 0.6815315740182022 
integrator LoadControl 0.013269517749241575 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
nodeDisp 2 
pattern Plain 1 1 
sp 2 1 -2.2222222222222223 -pattern 1
setTime 0.5963401272659317 
integrator LoadControl 0.011533139220973381 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1 
analyze 1 
analyze 1 
analyze 1 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
nodeDisp 2 
pattern Plain 1 1 
sp 2 1 -2.5 -pattern 1
setTime 0.5300801131252717 
integrator LoadControl 0.010215649714668007 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
analyze 1
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 
remove pattern 1 
setTime 0.0 
integrator LoadControl 1.0 
analysis Static 
analyze 1 
puts "[eleResponse 1 material 1 strain]" 
puts "[eleResponse 1 material 1 stress]" 

