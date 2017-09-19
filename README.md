# DDSim_Condor
Tools for running DDSim jobs on the Cambridge system using Condor.

Initialise.py  init_ilcsoft.sh  Logic  MakeGearFromCompact.py  README.md  Simulation.py  Templates

1) Run 'python Initialise.py', which edits the RunDDSim.sh script to point to the local init_ilcsoft.sh

2) Edit Simulation.py to decide what you want to simulate.  Point the compact file and steering file strings to the ilcsoft and ILDConfig of interest.

3) Run 'python Simulation.py' to simulate files.

4) Source your local init_ilcsoft.sh.  Edit and run MakeGearFromCompact.py to make a Gear file for the geometry so it is possible to run Marlin recontructions.  Sometimes gear files for detector models are included in ILDConfig, so check there first to see if this step is needed.
