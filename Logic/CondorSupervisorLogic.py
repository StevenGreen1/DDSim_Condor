#!/usr/bin/python

import os, sys, getopt, re, subprocess, math, dircache, logging, time, random, string

class CondorSupervisorLogic:
    'Common base class for running condor jobs.'

### ----------------------------------------------------------------------------------------------------
### Start of constructor
### ----------------------------------------------------------------------------------------------------

    def __init__(self, compactFile, steeringFile, outputPath, useParticleGun = False, particleForGun = '', energyOfPartilceForGun = 0, numberOfParticlesFromGun = 1, numberOfParticlesPerFileFromGun = 1, stdHepFormat = '', stdHepPath = '', nEvtsPerStdHep = 1000, nEvtsPerStdHepJob = 100):
        cwd = os.getcwd()
        self._CompactFile = compactFile
        self._OutputPath = outputPath
        self._nEvtsPerStdHep = nEvtsPerStdHep
        self._nEvtsPerStdHepJob = nEvtsPerStdHepJob
        self._UseParticleGun = useParticleGun
        self._ParticleForGun = particleForGun
        self._EnergyOfPartilceForGun = energyOfPartilceForGun
        self._NumberOfParticlesPerFileFromGun = numberOfParticlesPerFileFromGun
        self._NumberOfParticlesFromGun = numberOfParticlesFromGun
        self._SteeringFile = steeringFile

        'Logger'
        logFullPath = os.path.join(cwd,'CondorSupervisor.log')
        if os.path.isfile(logFullPath):
            os.remove(logFullPath)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logFullPath)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info('Output path : ' + self._OutputPath)

        'Make Output Path'
        if not os.path.exists(self._OutputPath):
            os.makedirs(self._OutputPath)

        'StdHep Path Information'
        self._StdHepFormat = stdHepFormat
        self._StdHepPath = stdHepPath
        if not useParticleGun:
            self._StdHepFiles = self.getStdHepFiles()

        'Condor'
        self._UseCondor = True
        self._CondorArguments = []
        self._CondorMaxRuns = 500

        'Random String For Job Submission'
        self._RandomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        self._DDSimExecutable = 'DDSim_' + self._RandomString + '.sh'

        os.system('cp Templates/DDSim.sh ' + self._DDSimExecutable)
        if not os.path.isfile(self._DDSimExecutable):
            self.logger.error('DDSim executable missing.  Exiting.')
            self.logger.error('DDSim executable : ' + self._DDSimExecutable)
            sys.exit()

        self.runDDSim()
        os.system('rm ' + self._DDSimExecutable)

### ----------------------------------------------------------------------------------------------------
### End of constructor
### ----------------------------------------------------------------------------------------------------
### Start of getSlcioFiles function
### ----------------------------------------------------------------------------------------------------

    def getStdHepFiles(self):
        fileDirectory = self._StdHepPath
        allFilesInDirectory = dircache.listdir(fileDirectory)
        allFiles = []
        allFiles.extend(allFilesInDirectory)
        allFiles[:] = [ item for item in allFiles if re.match('.*\.stdhep$', item.lower()) ]
        allFiles.sort()
        return allFiles

### ----------------------------------------------------------------------------------------------------
### End of getSlcioFiles function
### ----------------------------------------------------------------------------------------------------
### Start of runDDSim function
### ----------------------------------------------------------------------------------------------------

    def runDDSim(self):
        self.formatArguments()
        #print self._CondorArguments
        self.runCondorJobs()
        #self.checkCondorJobs()

### ----------------------------------------------------------------------------------------------------
### End of runDDSim function
### ----------------------------------------------------------------------------------------------------
### Start of formatArguments function
### ----------------------------------------------------------------------------------------------------

    def formatArguments(self):
        if not self._UseParticleGun:
            for energy in [3000]:
                counter = 0
                jobName = 'Z_uds_' + str(energy) + '_GeV'
                activeStdHepFormat = self._StdHepFormat
                activeStdHepFormat = re.sub('ENERGY',str(energy),activeStdHepFormat)

                stdHepFiles = []
                stdHepFiles = list(self._StdHepFiles)

                if not stdHepFiles:
                    self.logger.debug('No files in input stdhep folder.')
                    self.logger.debug('StdHep Folder : ' + self._StdHepPath)
                    self.logger.debug('StdHep Format : ' + activeStdHepFormat)
                    sys.exit()

                for nfiles in range(len(stdHepFiles)):
                    nextFile = stdHepFiles.pop(0)
                    matchObj = re.match(activeStdHepFormat, nextFile, re.M|re.I)

                    if not matchObj:
                         continue

                    stdHepFileName = os.path.join(self._StdHepPath, nextFile)

                    for startEvent in xrange(0, self._nEvtsPerStdHep, self._nEvtsPerStdHepJob):
                        counter += 1
                        argument = '--compactFile ' + self._CompactFile + ' '
                        argument += '--steeringFile ' + self._SteeringFile + ' '
                        argument += '--numberOfEvents ' + str(self._nEvtsPerStdHepJob) + ' '
                        argument += '--skipNEvents ' + str(startEvent) + ' '
                        argument += '--outputFile ' + os.path.join(self._OutputPath,jobName) + '_' + str(counter) + '.slcio '
                        argument += '--inputFile ' + stdHepFileName + ' '
                        self._CondorArguments.append(argument)
        else:
            jobName = self._ParticleForGun + '_' + str(self._EnergyOfPartilceForGun) + '_GeV'
            counter = 1
            for x in xrange(0, self._NumberOfParticlesFromGun, self._NumberOfParticlesPerFileFromGun):
                counter += 1
                argument = '--compactFile ' + self._CompactFile + ' '
                argument += '--steeringFile ' + self._SteeringFile + ' '
                argument += '--enableGun '
                argument += '--gun.particle ' + self._ParticleForGun + ' '
                argument += '--gun.energy ' + str(self._EnergyOfPartilceForGun) + '*GeV '
                argument += '--gun.distribution uniform '
                argument += '--outputFile ' + os.path.join(self._OutputPath,jobName) + '_' + str(counter) + '.slcio '
                argument += '--numberOfEvents ' + str(self._NumberOfParticlesPerFileFromGun) + ' '
                argument += '--random.seed ' + str(random.randint(1,1000001)) 

                self._CondorArguments.append(argument)

### ----------------------------------------------------------------------------------------------------
### End of formatArguments
### ----------------------------------------------------------------------------------------------------
### Start of runCondorJobs function
### ----------------------------------------------------------------------------------------------------

    def runCondorJobs(self):
        self.logger.debug('Running condor jobs.')
        nQueued = self.nQueuedCondorJobs()
        condorJobFile = 'Job_' + self._RandomString + '.job'

        while True:
            if nQueued >= self._CondorMaxRuns:
                subprocess.call(["usleep", "500000"])

            else:
                for idx, argument in enumerate(self._CondorArguments):
                    nRemaining = len(self._CondorArguments) - idx - 1
                    nQueued = self.nQueuedCondorJobs()
                    while nQueued >= self._CondorMaxRuns:
                        subprocess.call(["usleep", "500000"])
                        nQueued = self.nQueuedCondorJobs()

                    with open(condorJobFile, 'w') as jobFile:
                        jobString = self.getCondorJobString(idx)
                        jobString += 'arguments = ' + argument + '\n'
                        print argument
                        jobString += 'queue 1 \n'
                        jobFile.write(jobString)

                    subprocess.call(['condor_submit', condorJobFile])
                    print 'Submitted job as there were only ' + str(nQueued) + ' jobs in the queue and ' + str(nRemaining) + ' jobs remaining.'
                    subprocess.call(["usleep", "500000"])
                    os.remove(condorJobFile)

                    if 0 == nRemaining:
                        print 'All condor jobs submitted.'
                        return

### ----------------------------------------------------------------------------------------------------
### End of runCondorJobs function
### ----------------------------------------------------------------------------------------------------
### Start of getCondorJobString function
### ----------------------------------------------------------------------------------------------------

    def getCondorJobString(self, idx):
        jobString  = 'executable              = ' + os.getcwd() + '/' + self._DDSimExecutable + '                    \n'
        jobString += 'initial_dir             = ' + os.getcwd() + '                                                  \n'
        jobString += 'notification            = never                                                                \n'
        jobString += 'Requirements            = (OSTYPE == \"SLC6\")                                                 \n'
        jobString += 'Rank                    = memory                                                               \n'
        jobString += 'output                  = ' + os.environ['HOME'] + '/CondorLogs/DDSim' + str(idx) + '.out                      \n'
        jobString += 'error                   = ' + os.environ['HOME'] + '/CondorLogs/DDSim' + str(idx) + '.err                      \n'
        jobString += 'log                     = ' + os.environ['HOME'] + '/CondorLogs/DDSim' + str(idx) + '.log                      \n'
        jobString += 'environment             = CONDOR_JOB=true                                                      \n'
        jobString += 'Universe                = vanilla                                                              \n'
        jobString += 'getenv                  = false                                                                \n'
        jobString += 'copy_to_spool           = true                                                                 \n'
        jobString += 'should_transfer_files   = yes                                                                  \n'
        jobString += 'when_to_transfer_output = on_exit_or_evict                                                     \n'
        return jobString

### ----------------------------------------------------------------------------------------------------
### End of getCondorJobString function
### ----------------------------------------------------------------------------------------------------
### Start of checkCondorJobs function
### ----------------------------------------------------------------------------------------------------

    def checkCondorJobs(self):
        self.logger.debug('Checking on the running condor jobs.')
        while True: 
            nActiveJobs = self.nQueuedCondorJobs()
            if (nActiveJobs > 0):
                time.sleep(10)
            else:
                self.logger.debug('There are no more active condor jobs.')
                return

### ----------------------------------------------------------------------------------------------------
### End of checkCondorJobs function
### ----------------------------------------------------------------------------------------------------
### Start of checkCondorJobs function
### ----------------------------------------------------------------------------------------------------

    def nQueuedCondorJobs(self):
        self.logger.debug('Checking on the number of running condor jobs.')
        queueProcess = subprocess.Popen(['condor_q'], stdout=subprocess.PIPE)
        queueOutput = queueProcess.communicate()[0]
        runningJobs = queueOutput.split()[-6]
        idleJobs = queueOutput.split()[-8]
        return (int)(runningJobs) + (int)(idleJobs)

### ----------------------------------------------------------------------------------------------------
### End of checkCondorJobs function
### ----------------------------------------------------------------------------------------------------
