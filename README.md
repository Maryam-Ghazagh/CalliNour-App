CalliNour


CalliNour is a Python app built with Kivy and KivyMD designed to assist elderly users and visually 
impaired individuals who cannot easily read or see the screen, by enabling offline voice commands for phone calls.


Features

Convert speech to text using Vosk Persian language model.

Simple and accessible UI with a basic menu and a single button.


Technologies Used

Python

Kivy & KivyMD

Vosk Persian language model


Current Status

Work in progress:

Currently, pressing the button displays the spoken words immediately on the screen. 

Full call automation and advanced parsing are still under development.


Setup Instructions

1- Create a virtual environment (venv)

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux


2- Install dependencies

pip install -r requirements.txt


3- Download the Vosk Persian model

Download the vosk-model-small-fa-0.5 folder and place it in the project directory.

Note: This folder is not included in Git due to its large size.


4- Run the app

python main.py


Notes

The venv is used to manage project dependencies.

The Vosk Persian model is large and must be downloaded separately.
