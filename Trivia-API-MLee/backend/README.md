# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

MGLEE ADDITION I was unable to use export/set commands in my terminal and successfully run the application from the 'backend' directory. If this happens, an alternative approach to run the server is to navigate to the 'flaskr' directory and execute 'python __init__.py' from there.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...
```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a three keys: success, categories (contains a object of id: category_string key:value pairs), and total_categories (which is the total number of categories)
-Example of categories output:
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches an array of questions and their associated attributes in the trivia bank (table: questions), regardless of category
- Request Arguments: None
- Returns: An object with five keys: success, questions, total_questions, current_category(which will have a value of 'None' in this case), and categories
- Example of questions output:
[{"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"id": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
}]

GET '/categories/<int:category_id>/questions'
- Fetches a dictionary of questions and their associated attributes in the trivia bank (table: questions), filtered to only the selected category
- Request Arguments: category_id
- Returns: An object with five keys: success, questions, total_questions, current_category(as denoted by category_id), and categories
- Example of questions output: Output of questions will be similar to '/questions' endpoint but current_category will be set to the category_id


POST '/questions/create'
- Creates a new record within the trivia bank (questions) with all associated attributes
- Request Arguments: None
- Returns: An object with five keys: success, question, answer, category, and difficulty
- Example of output:
{"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
"success": true
}

POST '/quizzes'
- Creates a quiz consisting of 5 non-redundant, randomly selected questions from the trivia bank, either in total or filtered by category (if specified)
- Request Arguments: None
- Returns: An object with two keys: success, question
- Example of output:
{"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
"success": true
}

DELETE '/questions/<int:question_id>'
- Deletes a question with a specified id and all associated attributes in the trivia bank
- Request Arguments: question_id
- Returns: An object confirming the success of the method and question deleted
- Example of output:
{
"success": true,
"deleted": 16
}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

MGLEE ADDTION: The 'psql trivia_test < trivia.psql' approach did not work in my terminal. However, I was able to both restore a copy of the production and test database using 'psql -d trivia_test -U [user_name] -r -f trivia.psql'
