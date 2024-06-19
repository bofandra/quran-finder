
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask_jsonpify import jsonpify
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, from Flask!'

@app.route('/find')
def find():
    # transform query from user
    q = request.args.get('q')
    model = SentenceTransformer('use-cmlm-multilingual')
    encoded_query_text = model.encode(q)
    print(q)

    # get encoded quran text
    file = open('encoded_quran_cmlm.sav','rb')
    encoded_quran_text = pickle.load(file)
    file.close()

    # compare query to each quran verse
    i = 0
    text_similarity = []
    for encoded_quran_ayat in encoded_quran_text:
      similarity = encoded_query_text @ encoded_quran_ayat.T
      text_similarity.append(similarity)
      i=i+1
      print(i)

    # insert the similarity value to dataframe & sort it
    quran = pd.read_csv('quran-simple-clean.txt', delimiter="|")
    quran['similarity'] = text_similarity
    sorted_quran = quran.sort_values(by='similarity', ascending=False)
    df_list = sorted_quran.values.tolist()
    JSONP_data = jsonpify(df_list)
    return JSONP_data

