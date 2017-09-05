#!/usr/bin/python

import os, sys

outputPath = '/r04/lc/sg568/Validation/Simulation/DD4HEP/v01-19-04/ILD_l4_v02/'
compactFile = '/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/v01-19-04/lcgeo/v00-13-04/ILD/compact/ILD_l4_v02/ILD_l4_v02.xml'
detectorName = 'ILD_l4_v02'

os.system('convertToGear GearForILD ' + compactFile + ' ' + os.path.join(outputPath, 'Gear_' + detectorName + '.xml'))
