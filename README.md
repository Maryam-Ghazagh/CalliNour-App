<H1>CalliNour</H1>
CalliNour is a Python app built with Kivy and KivyMD designed to assist elderly users and visually 
impaired individuals who cannot easily read or see the screen, by enabling offline voice commands for phone calls.<br><br>

<H2>Features</H2>
Convert speech to text using Vosk Persian language model.
<br><br>
Simple and accessible UI with a basic menu and a single button.<br><br>

<H2>Technologies Used</H2>

Python

Kivy & KivyMD

Vosk Persian language model <br><br>

<H2>Current Status</H2>

**Work in progress:**

Currently, pressing the button displays the spoken words immediately on the screen. 

Full call automation and advanced parsing are still under development.<br><br><br>

<H2>Setup Instructions</H2>

1- Create a virtual environment (venv)

```python -m venv venv

venv\Scripts\activate      # Windows

source venv/bin/activate   # Mac/Linux
```
<br>
2- Install dependencies <br><br>

```pip install -r requirements.txt```

<br>

3- Download the Vosk Persian model <br><br>

Download the vosk-model-small-fa-0.5 folder and place it in the project directory.

Note: This folder is not included in Git due to its large size.

<br>
4- Run the app
<br><br>

```python main.py```
<br>

<H2>Notes</H2>

The venv is used to manage project dependencies.

The Vosk Persian model is large and must be downloaded separately.
