# Stress Testing tool for Commodity Prices

### Build

App is currently deployed at https://anise-eyestrain-straw-7wem.onrender.com. To use locally clone this repository, activate a new virtual environment and run <code>pip install -r requirements.txt</code> followed by <code>python src/app.py</code>.

### Usage

The app lets the user choose 3 macroeconomic variables and 1 commodity target variable, displaying their respective plots on the upper sectors of the dashboard. The app will then automatically generate a regression model using the three given macro variables to predict the target variable using the chosen algorithms, and display some results of the calculation in the bottom-left corner. Moreover, it will display a Prophet prediction of the target variable (not using the macro variables) on the bottom right sector.
