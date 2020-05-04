#!/bin/bash
# run MALLET topic modeling on film character dialogue and/or directions

DIALOGUEDIR = ../20sp/DATS599/Film-Screenplay-Analysis/data/topic_modeling/dialogue
DIALOGUEMALLET = ../20sp/DATS599/Film-Screenplay-Analysis/data/topic_modeling/dialogue.mallet
DIRECTIONSDIR = ../20sp/DATS599/Film-Screenplay-Analysis/data/topic_modeling/dirs
DIRECTIONSMALLET = ../20sp/DATS599/Film-Screenplay-Analysis/data/topic_modeling/dirs.mallet

echo $DIALOGUEDIR

# ./bin/mallet import-dir --input $DIALOGUEDIR --output $DIALOGUEMALLET --keep-sequence --remove-stopwords

# ./bin/mallet import-dir --input $DIRECTIONSDIR --output $DIECTIONSMALLET --keep-sequence --remove-stopwords