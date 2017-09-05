
from Logic.CondorSupervisorLogic import * 

stdHepFormat = 'ZudsENERGY_(.*?).stdhep'
stdHepPath = '/r06/lc/sg568/StdHepRepository'
outputPath = '/r04/lc/sg568/Validation/Simulation/DD4HEP/v01-19-04/ILD_o1_v05/'
compactFile = '/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/v01-19-04/lcgeo/v00-13-04/ILD/compact/ILD_o1_v05/ILD_o1_v05.xml'
nEvts = 1000

CondorSupervisorLogic(stdHepFormat, stdHepPath, compactFile, nEvts, outputPath)

