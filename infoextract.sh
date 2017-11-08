pip install --user virtualenv
mkdir venv
python -m virtualenv venv
source venv/bin/activate
pip install -U pip
pip install -U spacy
python -m spacy download en
python -m spacy.en.download --force all
python -m spacy.en.download all
pip install nltk
python nltk_download.py
python project.py
./testFinal.sh $1


