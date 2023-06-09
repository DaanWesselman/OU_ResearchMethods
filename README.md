# OU_ResearchMethods

neighbourhood_LTN is the actual model. It consists of the following functions:
1) make_patches: This makes the initial grid
2) patches_LTN: This deletes the parts of the grid that are part of the LTN, depending of its size
3) carsIni: Randomly places the cars in the grid
4) intersections_LTN: Determines which intersections are part of the LTN, i.e. where cars must change direction
5) run_model: runs the model for a given amount of iterations, with help of the functions described below:
  6) nextpatch: Determines for every car what the next patch is
  7) move_cars: Move cars if the next patch is free, adapt their speed
  8) check_LTN: Check if cars are at intersection of LTN (so that direction and speed might need to be adapted)

The runs are performed with scripts Research_Question1, Research_Question2 and Research_Question3. In addition, the figures are created here. 

The grid pictures, also used to make animations, are created in make_GRIDplots

The Python model is compared with the NetLogo model in compare_with_NetLogo

Two animations of the model are added: Simulation with LTN.mp4 and Simulation without LTN.mp4
