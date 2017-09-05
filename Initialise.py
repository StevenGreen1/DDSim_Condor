import os
import re
import sys

##############
# Update DDSim.sh script to source local init file
##############

cwd = os.getcwd()

newExecutableFile = open("Templates/DDSim.sh", "r")
content = newExecutableFile.read()
newExecutableFile.close()

content = re.sub('/PATH/TO/INIT/init_ilcsoft.sh', os.path.join(cwd, 'init_ilcsoft.sh'), content)

newExecutableFile = open("Templates/DDSim.sh", "w")
newExecutableFile.write(content)
newExecutableFile.close()

os.system('chmod u+x Templates/DDSim.sh')
