This is an ongoing research project supervised by Dr. Amal Khalifa on the topic of applying deep learning to the field of steganography. Because of this, most of the code provided is not the final work because of privacy reasons. Research project started in late 2021 and is expected to be finished by mid 2023.

Development is mostly based on the following publication: http://www.esprockets.com/papers/nips2017.pdf and further exploration will be done to improve the results obtained.

Some of my experience using TensorFlow is highlighted here.

The network has the following topology and is based mostly 2d convolutional layers:

![Alt text](Network_Diagram.png?raw=true "Network Diagram")

And the full functional model is as follows:

![Alt text](Functional_Model.png?raw=true "Functional Model")

Some of the preliminary results can be seen:

![Alt text](Results.png?raw=true "Results")

Here the Cover and Secret Images are "fused" into one single image, the Stego Image. At this stage, the goal is to have the Stego Image as similar to the Cover Image as possible while containing as much information about the secret image within it. We then do the reconstruction of the Recovered Image from the Stego Image trying to obtain an image as close to the original secret image as possible. 
