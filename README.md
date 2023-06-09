# OU_ResearchMethods

neighbourhood_LTN is the actual model. It consists of the following functions:
1) make_patches: This makes the initial grid
2) patches_LTN: This deletes the parts of the grid that are part of the LTN, depending of its size
3) carsIni: Randomly places the cars in the grid
4) intersections_LTN: Determines which intersections are part of the LTN, i.e. where cars must change direction
5) run_model: runs the model for a given amount of iterations, with help of the functions described below:
  6) nextpatch: Determines for every car what the next patch is
  7) move_cars: Move cars if the next patch is free, adapt their speed
  8) check_LTN: Check if cars are at intersection of LTN (so that direction and speed might to be adapted)
