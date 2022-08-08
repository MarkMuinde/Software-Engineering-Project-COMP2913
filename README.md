# Software-Engineering-Project-COMP2913
This project simulates a website that books movie tickets for a cinema. <br>

To run, type into the command line: <br>

<t>module add anaconda3 <br>
<t>python3 -m venv flask <br>
<t>source flask/bin/activate <br>

This will create and run a virtual environment

To install all necessary modules, run: <br>

<t>pip install requirement.text <br>
This should be done whilst in the virtual environment.

To run the website, input:<br>

<t>export FLASK_APP=run.py <br>
<t>export FLASK_ENV=development flask run <br>

You will have to install wkhtmltopdf separately at https://wkhtmltopdf.org/downloads.html After doing so go to views.py and change the variable 'wkh' to the path for yor wkhtmltopdf executable
