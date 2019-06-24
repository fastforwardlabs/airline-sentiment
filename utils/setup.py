
#Run this only if you are not using a custom docker image
#To build a custom docker image for this project run commands like in build-engine.sh

!mv utils/cdsw-build.sh .
!chmod 755 cdsw-build.sh
!sh ./cdsw-build.sh
