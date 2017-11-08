python predict.py TST1 $1
cd scoring\ program/
perl score-ie.pl predictions.txt ../$1-answers.txt
