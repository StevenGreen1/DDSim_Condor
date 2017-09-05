#!/bin/bash
source /usera/sg568/LC/Validation/Simulation/DD4HEP/v01-19-04/init_ilcsoft.sh
ls $ILCSOFT

ddsim $@
