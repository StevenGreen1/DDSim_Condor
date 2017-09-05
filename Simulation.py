from Logic.CondorSupervisorLogic import * 

# Universal Arguments
compactFile = '/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/v01-19-04/lcgeo/v00-13-04/ILD/compact/ILD_l4_v02/ILD_l4_v02.xml'
outputPath = '/r04/lc/sg568/Validation/Simulation/DD4HEP/v01-19-04/ILD_l4_v02/'
useParticleGun = False

# For StdHep Files
stdHepFormat = 'ZudsENERGY_(.*?).stdhep'
stdHepPath = '/r06/lc/sg568/StdHepRepository'
nEvtsPerStdHep = 1000

# Edit for use of Particle Gun
particleForGun = 'kaon0L'
energyOfPartilceForGun = 20
numberOfParticlesFromGun = 10000
numberOfParticlesPerFileFromGun = 1000

CondorSupervisorLogic(compactFile, outputPath, useParticleGun = useParticleGun, particleForGun = particleForGun, energyOfPartilceForGun = energyOfPartilceForGun, numberOfParticlesFromGun = numberOfParticlesFromGun, numberOfParticlesPerFileFromGun = numberOfParticlesPerFileFromGun, stdHepFormat = stdHepFormat, stdHepPath = stdHepPath, nEvtsPerStdHep = nEvtsPerStdHep)

# Particle Gun Particles - http://geant4.cern.ch/UserDocumentation/UsersGuides/ForApplicationDeveloper/html/AllResources/Control/UIcommands/_gun_.html

