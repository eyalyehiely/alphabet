# AlphaBet Backend Exercise - Events


## Introduction

This project is designed to help students and mentors conduct remote coding sessions. 
by writing and changing the code in real-time. 
The application consists of two main pages:
- The Lobby page.
- The Code Block page.

## Features

### Lobby Page

- The Lobby page displays a list of code blocks.
- Users can choose a code block, which will navigate them to the Code Block page.

### Code Block Page

- The first user to open the Code Block page is considered the mentor, other subsequent users are students.
- The mentor sees the code block in read-only mode.
- Students can edit the code block, changes are displayed in real-time using WebSockets.


### Check Code - Bonus Feature

- Each code block can have a “solution” field. If the student's code matches the solution, a big smiley face is displayed on the screen.


### Architecture Overview and Tech Stack
https://drive.google.com/file/d/11PUG5nbp-kBrYvv6zQMQ_D0fP5pAH9bx/view?usp=drive_link

## Tech 


- **Socket.IO**: For real-time communication between the mentor and student.

### Backend

- **Django**: For the backend server and handling API requests.
- **Django Channels**: For WebSocket support to enable real-time updates.
- **Django Rest Framework**: For building RESTful APIs.

### Database

- **Redis**:


## Quick Start
Follow these steps to set up and run the application using Docker:

## Configure Environment Variables
1.Inspect the settings.py file in each service to identify required environment variables.

2.Create a .env file for each service, supplying the necessary variables. It's crucial to ensure that these variables are correctly set before proceeding.



## Run Containers
Start each service with the following command:
```
docker pull eyalyehiely/backend:latest
(port8000)
```




## Local Development without Docker

1. Clone the backend repository:
    ```bash
    https://github.com/eyalyehiely/alphabet/
    cd learning/backend
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

4. Set up the database (make sure PostgreSQL is installed and running):
    ```bash
    on macOS:
    python3 manage.py makemigrations
    python3 manage.py migrate
    on Windows:
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    daphne -p 8000 backend.asgi:application

6. Run the redis server:
    ```
    redis-server
    ```
    



### API Documentation
---

```
ws/codeblock/${id}/
```
This WebSocket endpoint is used to establish a real-time connection between student to teacher.
- **Path Parameters**:
- ```id ```: The code block id.


---
```
GET /codeblocks/
```
This endpoint fetch all code blocks to the Lobby page.
- **Response**:

- ```id ```: The code block id.
- ```title```: The code block title.
- ```instructions```: The code block instructions.
- ```code```: The code block script.


```
POST /codeblock/${id}/check/
```
This endpoint checks if the user script is correct.

**Request Body**:
- ```code```: The user script.
- ```user_id```: The user unique id.



**Response**:

- ```id ```: The code block id.
- ```title```: The code block title.
- ```instructions```: The code block instructions.
- ```code```: The code block script.

A message indicating if the script is correct.




```
POST /fetchClientUuidToServer/
```
This endpoint send to the server the user unique id.

**Request Body**:
- ```user_id```: The user unique id.



**Response**:

A message indicating if the user_id accepted.



```
POST /codeblock/submission/
```
This endpoint create a new submission if there isnt already one.

**Request Body**:
- ```user_id```: The user unique id.
- ```code_block_id```: The original script id.





**Response**:

A message if submission exist or create a new one.


```
GET,DELETE /codeblock/submission/{id}/?user_id={clientUUID}
```


**GET:**

**Response**:
- Return the current submission or try to create one.


**DELETE:**

**Response**:
DELETE the current submission.





```
PUT /codeblock/submission/{id}/?user_id={clientUUID}
```
This endpoint edit the current submission.

**Request Body**:
- ```code```: The user script.
- ```code_block_id```: The original script id.
- ```user_id```: The user unique id.




**Response**:

Saving the new submission or send an error message.





```
POST /log_visitor/
```
This endpoint check how many users are in the same submission and determine a role.

**Request Body**:
- ```user_id```: The user unique id.
- ```url```: The submission url.




**Response**:

Saving the new role & send data:
- ```user_id```: The user unique id.
- ```url```: The submission url.
- ```role```: The current role.

---
Good luck!




