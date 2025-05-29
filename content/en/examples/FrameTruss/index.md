---
draft: true
---

A nonlinear truss model (with conventional truss elements and 2-dof nodes) wouldn't be able to capture the failure mode of member buckling. 
Although trusses are designed so that moments are not transmitted at the joints, moments will still develop inside the members due to things like geometric imperfections. 
This is what causes buckling. 
If you don't have reason to believe buckling will occur, you can just create a standard truss model, possibly with an inelastic material as was used in HW 1. Such a model will be accurate as long as no members buckle. However, in order to model a truss in a way that can capture buckling, the individual elements need to be able to capture the internal moments that arise from imperfections, as well as local (p-delta) geometric nonlinearities which exacerbate these moments. Most beam elements are only able to approximate the p-delta effect, and thus we have to subdivide them in order to ensure accuracy. This reminds me of some things I should clarify:The model has be created with ndm=2, ndf=3in the add_member function, you'll have to link the newly generated nodes to the base i/j nodes... use the Model.equalDOF method, eg :

```python
model.equalDOF(i, node_count+1, (1,2,3))
model.equalDOF(j, node_count+2, (1,2,3))
```

This will force the translational DOFs (ie, 1,2 and 3) of the new nodes to be equal to the given nodes. The remaining rotational DOFs (4,5,6) as well as all DOFs of the internal node (node_count+3) should be left free.In the main function that creates the model we'll have to fix the rotation of all original nodes (ie, nodes 1-5). also, make sure to apply the pin and roller reactions to the appropriate original nodes. All of these fixities are done with the Model.fix method. You do not have to fix any of the duplicate nodes, as the fixity will transmit from the equalDOF constraint.
