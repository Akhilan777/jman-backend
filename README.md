# jman-backend

## How to run

1. Clone the git repository
2. Run ```python -m venv venv```
3. Activate the virtual environment by(for windows)
    ```venv\Scripts\activate```
4. Install the required packages by running
    ```pip install -r requirements.txt```
5. Create a .env file and have a **ELEPHANTSQL_URL** variable which contains the url to sqldatabase
6. If the database does not have the required tables then run
    ```flask db upgrade```
7. Open the ***model.ipynb*** file in the notebooks directory and click run all(If asked to choose a kernel, then   choose the python kernel in venv)
8. Run ```flask run```
    ***Note that it is still in development mode. So don't use this in proudction***
9. In order to get the values from the url ensure that the tables have some data