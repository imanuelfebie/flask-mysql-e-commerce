# Flask E-Commerce sollution

Live preview [here](https://flaskdb-store.herokuapp.com/).

#### Contributors
- Adriel Soengadi
- Ikhsan Maulana
- Imanuel Febie
- Robert Reden

#### Setup instructions
This project is build using [Flask](https://palletsproject.com/p/flask), a lightweight WSGI web application framework. In order to run this web app on your local machine you need to have the following packages installed on your system:

- Python 3.8
- [Pipenv](https://pipenv.readthedocs.io/en/latest) (it's always advised to create your python projects inside virtual environments)

If your on MacOS, you can install Pipenv easily with Homebrew. You can also use Linuxbrew on Linux using the same command:

```bash
$ brew install pipenv
```

If your have a working installation of pip, you can install Pipenv using pip. To install:

```bash
$ pip install --user pipenv
```

Make sure that python 3.8 is set as your default python interpreter and that `pipenv` is added to your `$PATH`. If both of these are installed and are working correctly on you system you can simply clone the project `git clone https://github.com/imanuelfebie/flask-mysql-e-commerce.git`. Change into the project directory and run `pipenv install`. This will install all the python packages that are required for this to be able to run:

- flask
- flask-mysqldb

In order to activate the virtual environment run `pipenv shell` inside the project directory. Run the development server with `python run.py`, if there are no errors displayed you can view the web app on `localhost:5000`
