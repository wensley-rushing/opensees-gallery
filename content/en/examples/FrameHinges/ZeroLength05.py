import veux
from math import cos,sin,sqrt,pi
import xara
# ZeroLength5.tcl
# CE 221 Spring 1999 Midterm Problem
#
#  |A        B
#  |@--------@------------
#  |    4          6     ^
#
def rotSpring2D(model, tag, nodeR, nodeC, matID):
  # Create a rotational spring for a planar problem
  #
  # Arguments
  # eleID - unique element ID for this rotational spring
  # nodeR - node ID which will be retained by the multi-point constraint
  # nodeC - node ID which will be constrained by the multi-point constraint
  # matID - material ID which represents the moment-rotation relationship for the spring
  model.element('ZeroLength', tag, nodeR, nodeC, mat=matID,  dir=6)
  model.equalDOF(nodeR, nodeC, (1, 2))

def create_model():
  # Define the model builder
  model = xara.Model(ndm=2,  ndf=3)
  L = 10
  a =  4
  # Define nodes
  model.node(1, ( 0.0, 0.0))
  model.node(2, ( 0.0, 0.0))
  model.node(3, (  a , 0.0))
  model.node(4, (  a , 0.0))
  model.node(5, (  L , 0.0))

  # Define supports
  model.fix(1, (1, 1, 1))
  model.fix(5, (1, 1, 0))

  # Define moment-rotation relationship for spring A
  model.uniaxialMaterial('ElasticPP', 1, 10, 0.8)

  # Define moment-rotation relationship for spring B
  model.uniaxialMaterial('ElasticPP', 3, 6, 1.0)
  model.uniaxialMaterial('Elastic',   4, 4)
  model.uniaxialMaterial('Parallel',  2, 3, 4)

  # Geometric transformation
  model.geomTransf('Linear', 1)

  # Define beam elements
  model.element('elasticBeamColumn', 3, (2, 3), 100, 1000, 1000, 1)
  model.element('elasticBeamColumn', 4, (4, 5), 100, 1000, 1000, 1)


  rotSpring2D(model, 1 ,   1, 2 ,   1)
  rotSpring2D(model, 2 ,   3, 4 ,   2)

  model.pattern("Plain", 1, "Linear", "{load  3  0.0 -1.0  0.0}")
  return model 

if __name__ == "__main__":
  model = create_model()

  model.integrator("LoadControl", 1, 1, 1, 1)
  model.test("NormDispIncr", 1.0e-8, 10, 1)
  model.numberer("Plain")
  model.algorithm("KrylovNewton", maxDim=3)
  model.constraints("Penalty", 1.0e12, 1.0e12)
  model.system("UmfPack")
  model.analysis("Static")

  model.analyze(1)

  artist = veux.render(model)
  veux.serve(veux.render(model, model.nodeDisp, canvas=artist.canvas))#, ndf=3)) #.canvas.popup()


  model.analyze(9)
  model.print('algorithm')
  model.print('node', 4)


  artist = veux.render(model) #.canvas.popup()
  veux.serve(veux.render(model, model.nodeDisp, canvas=artist.canvas)) #.canvas.popup()

