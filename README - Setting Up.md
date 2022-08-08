To run on linux type into the command line:

module add anaconda3
python3 -m venv flask
source flask/bin/activate

To install all necessary modules type 'pip install requirement.text' to command line at this point while in the virtual environment. Continue typing:

export FLASK_APP=run.py
export FLASK_ENV=development
flask run

You will have to install wkhtmltopdf separately at https://wkhtmltopdf.org/downloads.html
After doing so go to views.py and change the variable 'wkh' to the path for yor wkhtmltopdf executable