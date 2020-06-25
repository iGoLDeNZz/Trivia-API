# Trivia Game 
This project is a trivia type game. Players are able to add their questions, give them a category & difficulty rating, and play a 5 question trivia game. As a part of the Fullstack Nanodegree from Udacity, it serves as a final project for lessons from Course 2: API Development and Documentation. By completing this project, students learn and apply their skills structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.

All backend code follows PEP8 style guidelines.

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend
From the backend folder run `pip install -r requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://localhost:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on `localhost:3000`. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 


## API Reference

### Getting Started
#### Base URL:
At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://localhost:5000/`, which is set as a proxy in the frontend configuration.

#### Authentication:
This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "API Resource incorrect"
}
```

The API will return three error types when requests fail:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: request not processable

### Endpoints
#### GET /categories
- **General:**
    - Returns a list of category objects, success value, and total number of categories
    - Returns the total number of categories
- Sample: `curl http://localhost:5000/categories`

``` 
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
    ]  "type": "Sports"
    }],
  "success": true,
  "total_categories": 6
}
```

#### GET /questions
- **General:**
    - Returns a list of question objects, success value, and total number of questions
    - Results are paginated in groups of 10.  Inclue a request argument to choose page number, starting from 1.
- `curl http://localhost:5000/books?page=2`
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
        "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }],
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }],
  "success": true,
  "total_questions": 19
}
```

#### POST /questions
- **General:**
    - Creates a new question using the submitted question, answer, category, and difficulty.  Returns the ide of the created book, success value, total books, and question list.
- `curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"questions":"Did you actually read this?", "answer":"egg","category":5,"difficulty":12}'`
```
{
  "answer": "egg",
  "category": 5,
  "difficulty": 12,
  "id": 24,
  "questions":"Did you actually read this?"
  "success": true
}
```

#### GET /category/{category_id}/questions
- **General:**
    - Returns a list of book objects for the category id specified, success value, current category type, and total number of questions in the category.
    - Results are paginated in groups of 10.  Include a request argument to choose page number, starting from 1.
- Sample: `curl http://localhost:5000/categories/1/questions`
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }],
  "success": true,
  "total_questions": 3
}
```

#### POST /questions/search
- **General:**
    - Returns a list of book objects for the search term provided, success value, and total number of questions returned.
    - Results are paginated in groups of 10.  Include a request argument to choose page number, starting from 1.
- Sample: `curl http://localhost:5000/questions/search -X POST -h "Content-Type: application/json" -d '{"searchTerm":"actor"}'`
```
{
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }],
  "success": true,
  "total_questions": 1
}
```

#### POST /quizzes
- **General:**
    - Picks a random question for the trivia game quiz play using the quiz category and previous questions asked.
    - Returns a question object, success value, previous questions asked, and quiz category.
- Sample: `curl http://1localhost:5000/quizzes -X POST -h "Content-Type: application/json" -d {"quiz_category":1}`
```
{
  "answer": "Alexander Fleming",
  "category": 1,
  "difficulty": 3,
  "id": 21,
  "question": "Who discovered penicillin?"
  "success": true
}
```

## Deployment N/A

## Authors
Yousef Almassad

## Acknowledgements
The awesome team at Udacity and the instructors that have helped me on my way to become a full stack developer and ofcourse you the reader <3

The best is yet to come.