import spacy
import classy_classification
import constants as ct
import pandas as pd
def UpdateSpacyModel():
    nlp = spacy.blank("fr")
    nlp.add_pipe(
        "text_categorizer",
        config={
            "data": ct.factors,
            "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "device": "cpu"
        }
    )
    nlp.to_disk("C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/spacymodel")

def LoadSpacyModel():
    return spacy.load("C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/spacymodel")
# Function to preprocess the news text and detect factors
def news_to_vector(news, nlp , threshold=0.3):
    if pd.isna(news):
        return [0] * len(ct.factors)

    sentences = news.strip('*').split('***')
    list = []
    for sent in sentences:
        result = nlp(sent)._.cats
        list.append([1 if value > threshold else 0 for key, value in result.items()]   )
    factor_presence = [sum(x) for x in zip(*list)]
    return factor_presence

# UpdateSpacyModel()
# nlp= LoadSpacyModel()
# print(news_to_vector("changement de staff" , nlp ))