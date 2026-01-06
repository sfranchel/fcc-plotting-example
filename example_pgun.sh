#!/usr/bin/env bash

# Config parameters
COMPACT=$K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml

#COMPACT=$K4GEO/FCCee/IDEA/compact/IDEA_o1_v03/IDEA_o1_v03.xml 
# note that to run with IDEA, you need to use the central steering file from the FCC-Config repo,
# i.e. add the following option to the ddsim command:
# --steeringFile $FCCCONFIG/FullSim/IDEA/IDEA_o1_v03/SteeringFile_IDEA_o1_v03.py


N_EVENTS=100

PARTICLE="mu-"
ENERGY="10*GeV"
THETA_MIN="89.9*deg"
THETA_MAX="90.1*deg"
PHI_MIN="-0.01*rad"
PHI_MAX="0.01*rad"

SAMPLE="mu_10GeV_theta90"

# Extract detector name from the compact file path
DETECTOR=${COMPACT##*/}
DETECTOR=${DETECTOR%.xml}

# Run the simulation

ddsim --enableGun \
      --gun.distribution uniform \
      --gun.energy $ENERGY \
      --gun.particle $PARTICLE \
      --gun.thetaMin=$THETA_MIN \
      --gun.thetaMax=$THETA_MAX \
      --gun.phiMin=$PHI_MIN \
      --gun.phiMax=$PHI_MAX \
      --numberOfEvents $N_EVENTS \
      --random.enableEventSeed \
      --random.seed 42 \
      --compactFile $COMPACT \
      --outputFile ${DETECTOR}_${SAMPLE}.root