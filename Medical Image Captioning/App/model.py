#Utility imports
import json
import os, shutil
import random
import streamlit as st
import os
from pathlib import Path
import numpy as np
from PIL import Image

# Inception imports
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Transformer imports
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from tokenizers import ByteLevelBPETokenizer
from transformers import RobertaConfig, RobertaTokenizerFast, RobertaForMaskedLM, TrainingArguments, Trainer
from tokenizers import ByteLevelBPETokenizer
from transformers import VisionEncoderDecoderModel



root = Path(os.getcwd())
aux_pre = root / 'Inception' / 'PretrainedInceptionLSTM'
aux_re = root / 'Inception' / 'RetrainedInceptionLSTM'

model_re_path = root / 'Inception' / 'RetrainedInceptionLSTM' / 'Model'
model_inception_path = root / 'Inception' / 'RetrainedInceptionFeatureExtraction' / 'Model'
model_pre_path = root / 'Inception' / 'PretrainedInceptionLSTM' / 'Model'

transformer_tokenizer = root / 'Transformer' / 'BPE_tokenizerSaved'
transformer_roberta = root / 'Transformer' / 'Image_Cationing_VIT_Roberta_iter2'
transformer_vit = root / 'Transformer' / 'VIT_feature_extractor'

# Must create

def get_pretrained_inceptionV3():
    model = InceptionV3(weights='imagenet')
    model2 = Model(model.input, model.layers[-2].output)
    return model2

def fetch_auxiliary_files(type):
    if type == 'Pretrained Inception':
        word2Index = np.load(aux_pre / "word2Index.npy", allow_pickle=True).item()
        index2Word = np.load(aux_pre / "index2Word.npy", allow_pickle=True).item()
        variable_params = np.load(aux_pre / "variable_params.npy", allow_pickle=True).item()
        return word2Index, index2Word, variable_params
    if type == 'Retrained Inception':
        word2Index = np.load(aux_re / "word2Index.npy", allow_pickle=True).item()
        index2Word = np.load(aux_re / "index2Word.npy", allow_pickle=True).item()
        variable_params = np.load(aux_re / "variable_params.npy", allow_pickle=True).item()
        return word2Index, index2Word, variable_params
    if type == 'Transformer':
        feature_extractor = ViTFeatureExtractor.from_pretrained(transformer_vit)
        tokenizer = RobertaTokenizerFast.from_pretrained(transformer_tokenizer)
        return feature_extractor, tokenizer


@st.cache(allow_output_mutation=True, show_spinner=False)
def fetch_model(type):
    with st.spinner(text="Fetching Model"):
        if type == 'Pretrained Inception':
            model_pre = tf.keras.models.load_model(model_pre_path)
            model_inc = get_pretrained_inceptionV3()
            return model_inc, model_pre
        if type == 'Retrained Inception':
            model_re = tf.keras.models.load_model(model_re_path)
            model_inc = tf.keras.models.load_model(model_inception_path)
            return model_inc, model_re
        if type == 'Transformer':
            visionModel = VisionEncoderDecoderModel.from_pretrained(transformer_roberta)
            return visionModel

def preprocess_image_inception(image):

    x = np.array(image)
    x = np.expand_dims(x, axis = 0)
    x = preprocess_input(x)
    x = x.reshape(1, 299, 299, 3)

    return x

def extract_features(model, image):
    features = model.predict(image, verbose = 0)
    return features

def generate_caption(model, features, max_len, word2Index, index2Word, beam_index = 3):
    caption = beam_search(model, features, max_len, word2Index, index2Word, beam_index)
    return caption

def beam_search(model, features, max_len, word2Index, index2Word, beam_index):
    start = [word2Index["startseq"]]
    start_word = [[start, 1]]

    final_preds = []
    live_seqs = beam_index
    features = np.tile(features, (beam_index,1))
    count = 0
    while len(start_word) > 0:
        #print(count)
        count+=1
        temp = []
        padded_seqs = []
        #Get padded seqs for each of the starting seqs so far, misnamed as start_word
        for s in start_word:
            par_caps = pad_sequences([s[0]], maxlen=max_len, padding='post')
            padded_seqs.append(par_caps)

        #Formatting input so that it can be used for a prediction
        padded_seqs = np.array(padded_seqs).reshape(len(start_word), max_len)

        preds = model.predict([features[:len(start_word)],padded_seqs], verbose=0)

        #Getting the best branches for each of the start seqs that we had
        for index, pred in enumerate(preds):
            word_preds = np.argsort(pred)[-live_seqs:]
            for w in word_preds:
                next_cap, prob = start_word[index][0][:], start_word[index][1]
                next_cap.append(w)
                prob *= pred[w]
                temp.append([next_cap, prob])

        start_word = temp
        # Sorting according to the probabilities
        start_word = sorted(start_word, reverse=False, key=lambda l: l[1])
        # Getting the top words from all branches
        start_word = start_word[-live_seqs:]

        for pair in start_word:
            if index2Word[pair[0][-1]] == 'endseq':
                final_preds.append([pair[0][:-1], pair[1]])
                start_word = start_word[:-1]
                live_seqs -= 1
            if len(pair[0]) == max_len:
                final_preds.append(pair)
                start_word = start_word[:-1]
                live_seqs -= 1

    # Between all the finished sequences (either max len or predicted endseq), decide which is best
    max_prob = 0
    for index, pred in enumerate(final_preds):
        if pred[1] > max_prob:
            best_index = index
            max_prob = pred[1]

    # Convert to readable text
    final_pred = final_preds[best_index]
    final_caption = [index2Word[i] for i in final_pred[0]]
    final_caption = ' '.join(final_caption[1:])
    return final_caption

def _compile():

    image_path = 'samples/ROCO_00929.jpg'
    image = Image.open(image_path)
    #predict(image)
    image.close()


_compile()


sample_dir = './samples/'
sample_image_ids = tuple(["None"] + [int(f.replace('ROCO_', '').replace('.jpg', '')) for f in os.listdir(sample_dir) if f.startswith('ROCO_')])

with open(os.path.join(sample_dir, "Roco-img-ids.json"), "r", encoding="UTF-8") as fp:
    roco_image_ids = json.load(fp)


def get_random_image_id():

    image_id = random.sample(roco_image_ids, k=1)[0]
    return image_id
