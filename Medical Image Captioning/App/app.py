import streamlit as st
import requests
import io


# Designing the interface
st.title("Medical Image Captioning")

st.sidebar.markdown(
    """
    This project features 3 different Medical image captioning models.
    Two of the use the InceptionV3 architecture to do feature extraction and then generate the captions using an LSTM model.
    The difference between these two is that the first one uses InceptionV3 trained on ImageNet data and outputs 2048 features.
    The second one is based on a retrained version of InceptionV3 that uses the CUI data from the ROCO dataset to extract 745 features from the images.
    The final model is a transformer based on VIT and RoBERTa.
    """
)

with st.spinner('Loading objects ...'):
    from model import *

random_image_id = get_random_image_id()

st.sidebar.title("Select a sample image")
sample_image_id = st.sidebar.selectbox(
    "Please choose a sample image",
    sample_image_ids
)

st.sidebar.title("Select a model Type")
model_type = st.sidebar.selectbox(
    "Please choose a model",
    ['Pretrained Inception', 'Retrained Inception', 'Transformer']
)

if model_type == 'Transformer':
    visionModel = fetch_model(model_type)
    feature_extractor, tokenizer = fetch_auxiliary_files(model_type)
else:
    inception, lstm = fetch_model(model_type)
    word2Index, index2Word, variable_params = fetch_auxiliary_files(model_type)
    max_len = variable_params['max_caption_len']

if st.sidebar.button("Random ROCO (test) images"):
    random_image_id = get_random_image_id()
    sample_image_id = "None"

bytes_data = None
with st.sidebar.form("file-uploader-form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose a file")
    submitted = st.form_submit_button("Upload")
    if submitted and uploaded_file is not None:
        bytes_data = io.BytesIO(uploaded_file.getvalue())

if (bytes_data is None) and submitted:

    st.write("No file is selected to upload")

else:

    image_id = random_image_id
    if sample_image_id != "None":
        assert type(sample_image_id) == int
        image_id = sample_image_id

    sample_name = f"ROCO_{str(image_id).zfill(5)}.jpg"
    sample_path = os.path.join(sample_dir, sample_name)

    if bytes_data is not None:
        image = Image.open(bytes_data)
    elif os.path.isfile(sample_path):
        image = Image.open(sample_path)

    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    width, height = 299, 299
    resized = image.resize(size=(width, height))

    if bytes_data is None:
        st.markdown(f"ROCO_{str(image_id).zfill(5)}.jpg")
    show = st.image(resized)
    show.image(resized, '\n\nSelected Image')

    # For newline
    st.sidebar.write('\n')

    with st.spinner('Generating image caption ...'):
        st.header(f'Predicted caption:\n\n')
        if model_type == 'Transformer':
            caption = tokenizer.decode(visionModel.generate(feature_extractor(image, return_tensors="pt").pixel_values)[0][3:-1])
            #print(tokenizer.decode(visionModel.generate(feature_extractor(Image.open(img).convert("RGB"), return_tensors="pt").pixel_values)[0]))
        else:
            preprocessed_img = preprocess_image_inception(resized)
            features = extract_features(inception, preprocessed_img)
            caption = generate_caption(lstm, features, max_len, word2Index, index2Word)
        st.subheader(caption)

    st.sidebar.header("Model predicts: ")
    st.sidebar.write(f"{caption}")

    image.close()
