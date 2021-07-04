Casting Agency

# Motivation

Complete this capstone to graduate.

## Deployment Heroku

App is live on :
https://appcap.herokuapp.com/


# Dependencies and local development

To run the app and test it localy:  
- pip install -r requirements.txt 
- source setup.sh
- flask run

To run the unittest run
- python test_app.py

### Endpoints 
you can test endpoint live on heroku or using postman or curl

GET '/actors'
- Fetches all actors 
- Request Arguments: None
- returns all actors 
- Sample Postman Request: http://localhost:5000/actors
{
    "actors": [
        {
            "gender": "male",
            "id": 2,
            "name": "Smith"
        }
    ],
    "success": true
}

```
GET '/actors/<init:id>'
- Fetches an actor 
- Request Arguments: actor - id
- Sample postman request: GET http://localhost:5000/actors/1
{
    "actors": [
        {
            "gender": "male",
            "id": 2,
            "name": "Smith"
        }
    ],
    "success": true
}
```

```
POST '/actors'
- post an actor 
- Request Arguments: id - integer
-sample postman request: POST http://localhost:5000/actors 
{
    'success':'True'
}
```

```
DELETE '/actors/<init:id>'
- Deletes a specified actor using his id
- Request Arguments: id - integer
-sample postman request: DELETE http://localhost:5000/actors/1
{
    'success':'True'
}
```

```
PATCH '/questions'
- Sends a post request in order to patch an actor
- Request Body: 
{
    "name": "Smith",
    "age": "24",
    "gender": "male"
}
- Sample Postman Request: PATCH "http://localhost:5000/actors/1" 
{
    'success':'True'
}

```
### Error Handling
```
Errors are returned as JSON objects in the following format:
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not Allowed
- 500: Internal server error
```

```
AuthError are returned as JSON objects in the following format
{
    "description": "Authorization header is expected.",
    "error": "authorization_header_missing",
    "status_code": 401,
    "sucess": false
}

The API will return 2 error types when requests fail
- 401: unauthorized  
- 404: forbidden

```

## Authors
Baraah
