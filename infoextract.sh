pip install --user virtualenv
mkdir venv
python -m virtualenv venv
source venv/bin/activate 
pip install --user spacy
python -m spacy.en.download all
pip install -user nltk
python nltk_download.py
./testFinal.sh $1


