# AlphaBet Backend Exercise - Events


## Introduction

The Events Management API is a backend solution designed for creating, managing, and broadcasting events in real-time. Built with Django and the Django REST framework,and celery.
Django Channels are integrated to provide real-time functionality, enabling live updates and interactions between the server and clients through WebSockets.





## Tech 


- **Django**: For the backend server and handling API requests.
- **Django Channels**: For WebSocket support to enable real-time updates.
- **Django Rest Framework**: For building RESTful APIs.
- **Celery**: For sending email notifications.


### Authentication:
- **JWT**

### Database
- **SQLITE**





### API Documentation
---

```
ws/events/${event_id}/
```
This WebSocket endpoint is used to establish a real-time notifications between backend and frontend.
- **Path Parameters**:
- ```user_id ```: The event id.


---
```
GET /api/events/
```
This endpoint fetch all events.
- **Response**:

- ```id ```: The event id.
- ```name```: The event name.
- ```starting_time```: The event starting_time.
- ```end_time```: The event end time.
- ```location```: The event location.
- ```participants```: The event participants.
- ```created_at```: The event created time.
- ```updated_at```: The event updated time.



```
POST /api/events/
```
This endpoint create event.

- **Request Body**:

- ```id ```: The event id.
- ```name```: The event name.
- ```starting_time```: The event starting_time.
- ```end_time```: The event end time.
- ```location```: The event location.
- ```participants```: The event participants.
- ```created_at```: The event created time.
- ```updated_at```: The event updated time.

- **Response**:
A message that event is created + an email with the event details.



```
GET /api/event/{id}
```
This endpoint get a specific event details.

**Request Body**:
- ```id```: The event unique id.




**Response**:

- ```id ```: The event id.
- ```name```: The event name.
- ```starting_time```: The event starting_time.
- ```end_time```: The event end time.
- ```location```: The event location.
- ```participants```: The event participants.
- ```created_at```: The event created time.
- ```updated_at```: The event updated time.



```
PUT /api/event/{id}
```
This endpoint update a specific event if it is not already happend,
send real time notification to the front and send an email to participants.

**Request Body**:
- user decision according to the properties.



**Response**:

A real time notification to the front and send an email to participants.


```
DELETE /api/event/{id}
```
Delete a specific event.

**Request Body**:
- ```id```: The event unique id.


**Response**:
- A meesage of the event that deleted.




```
GET /api/search_event/{location}
```
Get all events on specific location.

**Request Body**:
- ```location```: The location of the event.


**Response**:
- A list of all events on the location.



```
POST /api/auth/signin/
```
User sign in to app - using JWT.

**Request Body**:
- ```username```: user username.
- ```password```: user password.


**Response**:
- access token.
- refresh token.


```
POST /api/auth/signup/
```
User sign up to app - using JWT.

**Request Body**:
- ```username```: user username.
- ```eamil```: user eamil.
- ```password```: user password.


**Response**:
- access token.
- refresh token.



```
GET /api/user/{user_id}
```
This endpoint get a specific user details.

**Request Body**:
- ```user_id```: user id.



**Response**:
"user": {
        "id": user_id,
        "username": "username",
        "email": "email",
        "created_at": "date and time",
        "updated_at": date and time
    }



```
PUT /api/user/{user_id}
```
This endpoint update a specific user details.

**Request Body**:
- ```user_id```: user id.
- ```email```: email / ```username```: username.



**Response**:
"user": {
        "id": user_id,
        "username": "username",
        "email": "email",
        "created_at": "date and time",
        "updated_at": date and time
    }



```
DELETE /api/user/{user_id}
```
This endpoint delete a specific user.

**Request Body**:
- ```user_id```: user id.



**Response**:
A message that the user has been deleted.





## Quick Start
Follow these steps to set up and run the application using Docker:

## Configure Environment Variables
1.Inspect the settings.py file in each service to identify required environment variables.

2.Create a .env file for each service, supplying the necessary variables. It's crucial to ensure that these variables are correctly set before proceeding.



## Run Containers
Start each service with the following command:
```
docker pull eyalyehiely/alphabet:latest
(port8000)
```




## Local Development without github

1. Clone the backend repository:
    ```bash
    https://github.com/eyalyehiely/alphabet/
    ```

2. Create a virtual environment and activate it:
    ```bash
    on macOS:
    python3 -m venv venv && source venv/bin/activate

    on Windows:
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```



4. Run the development server(server):
    ```bash
    daphne -p 8000 backend.asgi:application

5. Run the redis server(websocket):
    ```
    redis-server
    ```

6.  Run celery(email notifications):
    ```
    celery -A alphabet worker -l info
    celery -A alphabet beat -l info
    ```










