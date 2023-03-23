# Info
This repository contains the deep learning models for time series  which is developed from ZalandoResearch Pytorch-ts but I modified the DeepAR algorithm into RolledDeepAR which aims to reduce errors in inference caused by differences between training and inference data. In the DeepAR model, only actual values from input sequences are used for training, while in inference, sampled predictions are used as past values for future predictions. This can lead to errors if the model encounters an untrained past sequence pattern. Rolled DeepAR addresses this issue by generating rolling predictions during the training phase, feeding sampled predictions to the network for predicting the next day. By using sampled predictions instead of actual values for future values, the training sequences can be more diverse, acting as an augmentation of input sequences. This helps the model generate more robust predictions, particularly in cases where the input value is probabilistic. The major difference between DeepAR and rolled DeepAR is the method of generating the loss during training. Rolled DeepAR uses sampled past values to predict future values, while DeepAR always uses actual values. The loss is calculated only for future predictions instead of using all sequences. The text notes that rolled DeepAR is not necessarily better than DeepAR and depends on the application. For example, if the input sequence is regarded as one sample of a probability distribution, it may be better to train with as many cases as possible rather than using only one set of samples.
   
This model based on this paper [Robust recurrent network for intermittent time-series](https://www.sciencedirect.com/science/article/abs/pii/S0169207021001151)

# Prerequisite
## Libraries
     Python 3.7.4
     CUDA 10.1
     CUDNN 7.6.5
     nvidia drivers 435.21
     PyTorch 1.4

## Install
     * Initialize docker setup for the GPU (pytorch/pytorch:1.4-cuda10.1-cudnn7-devel)
     * run sh ./install.sh
     
# Reference
This model is developed based on [PyTorchTS](https://github.com/zalandoresearch/pytorch-ts).