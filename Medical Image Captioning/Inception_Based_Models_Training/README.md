These folders include all the data and notebooks to create the InceptionV3 based models of medical image captioning.

These models use the InceptionV3 deep convolutional neural networks to extract features from the images and then these features are fed into an LSTM model that generates the captions that will be outputed by the model. 

There are two approaches included here, the first one uses the InceptionV3 model trained on the ImageNet dataset to do the feature extraction. This is problematic because the features available on this dataset are very different from the ones available on our dataset. On the other hand, this is much less computationally expensive because the InceptionV3 model is fairly complex and retraining it takes time.

The second approach retrains does exactly this, however, it retrains the InceptionV3 model based on the CUIs of each image in the dataset. CUIs are medical codes for dianostic and somewhat describe the contents of the image. After the InceptionV3 model is retrained it is used once again to do feature extraction and these features are fed to a similar LSTM model. This approach has the benefit of being able to better identify features on the image based on medical data. However, it is trained on a much smaller dataset since the ROCO dataset contains much less training examples than the ImageNet and this may be problematic because the topology of the network was designed for the latter dataset.

Only a small fraction of the data is available here for a sample of how the model should work. To train the models on the full dataset just upload the full data available at https://github.com/razorx89/roco-dataset under the ROCO folder.

Finally, The notebooks are divided into multiple steps such as the preprocessing of text data, training of the feature extraction network using the ROCO dataset, or simply doing inference using the pretrained InceptionV3 model, building and training the LSTM models used for text generation and more. This is done because some of the notebooks may take hours to run and some of the outputs may be used as input by multiple notebooks.

A better picture of the full workflow between all these notebooks is illustrated in the diagram below.

![Alt text](Notebook Workflow.png?raw=true "Notebook Workflow")

