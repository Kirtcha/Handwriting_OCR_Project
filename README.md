# Handwritten OCR System

## Overview

This project was developed as part of a bachelor's thesis and implements a complete handwritten character recognition pipeline.

The system extracts handwritten characters from scanned documents, generates a structured OCR dataset, trains a neural network model and performs character recognition on previously unseen samples.

## Features

* Image preprocessing
* Thresholding and binarization
* Character contour detection
* Character extraction
* Manual character labeling
* Automatic OCR dataset generation
* Neural network training
* Character classification
* Recognition of handwritten characters

## Technologies

* Python
* OpenCV
* NumPy
* Pandas
* TensorFlow / Keras
* Matplotlib

## Workflow

1. Load a scanned handwritten document
2. Preprocess the image
3. Detect and extract character contours
4. Label extracted characters
5. Generate a structured OCR dataset
6. Train a neural network model
7. Evaluate model performance
8. Recognize characters from new samples

## Results

The trained neural network is capable of recognizing handwritten characters extracted from scanned documents and classifying them into their corresponding character classes.

## Project Goal

The goal of this project is to develop a complete OCR pipeline that automates dataset creation and enables handwritten character recognition using machine learning techniques.
