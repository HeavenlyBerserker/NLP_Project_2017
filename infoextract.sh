pip install --user virtualenv
mkdir venv
python -m virtualenv venv
source venv/bin/activate
pip install -U pip
pip install -U spacy
python -m spacy download en
#python -m spacy.en.download --force all
#python -m spacy.en.download all
pip install nltk
python project.py
python predict.py $1
cd scoring\ program/
#perl score-ie.pl ../final-predictions.txt ../testset1/testset1-anskeys.txt
