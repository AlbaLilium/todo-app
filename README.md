# todo-app

This is a project task for application.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

Requirements for the software and other tools to build, test and push 

If you run application with Docker:
- [Docker](https://www.docker.com)

If you run application locally:
- Ubuntu 22.04.4 LTS
- PostgresSQL 16 in port 3000 with possibility to connect it remotely.
- Python 3.11
> Note:
> If 3000 port isn't free. You can change port in local.env. 

### Installing

    git clone https://github.com/AlbaLilium/todo-app.git

## Build application

### With Docker

Use this command to build application:

    cd todo-app/
    ./run_with_docker

Then go to this site: http://localhost/docs

### Locally

Use this command to build application:

    cd todo-app/
    ./install_local
    ./run_local

Then go to this site: http://127.0.0.1:8000/docs

-----

# API documentation
## Endpoints
**Note:** 
`credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]`
are needed for authorization. All endpoints with `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]`
return exception, if user not authorized.

There are endpoints in this application:

#### POST users/auth/sign-up
Path parameters
- `user: UserCreateRequestSerializer required`

Create and authorize user. Return HTTP 400 for password smaller than 6 symbols.

Output:
- `token: Token`
#### POST users/auth/sign-in
Path parameters 
- `form_data: OAuth2PasswordRequestForm required`
- 
Authorize user.

Output:
- ` token: Token`
#### GET users/{user-id}/tasks
Path parameters 
- `page_number: int, default 1`
- `page_size: int, default 10`
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)] required`

Get all user's task.

Output:
- `taks_list: TaskListResponseSerializer`
#### GET tasks/
Path parameters
- `page_number: int, default 1`
- `page_size: int, default 10`
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)] required`

Get all task.

- Output:
- `taks_list: TaskListResponseSerializer`
#### GET tasks/{task_id}
Path parameters
- ` task_id: int required`
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)] required`

Get a specific task by id.

Output:
- `task: TaskBase`
#### PATCH tasks/complete/{task_id}
Path parameters
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]`
- `task_id: int required`

Make one task completed.

Output:
- `task: TaskBase`
#### POST tasks/create/{task_id}
Path parameters
- `task: CreateTaskSerializer required,`
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]`

Create task.
 
Output:
- `task_id: int`
#### PATCH tasks/update/{task_id}
Path parameters
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)] required`
- `status: [str, Query()] default None`

Update task by any field: status, description and title.

Output:
- `task: TaskBase`
#### DELETE tasks/delete/{task_id}
Path parameters
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)] required`
- `task: SingleTaskRequestSerializer required`

Delete task by task's id.

Output:
- `response: dict[str:str]`
#### GET tasks/filter/{task_id}

Path parameters
- `credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]`
- `page_number: int, default 1`
- `page_size: int, default 10`
- `status: Annotated[str, Query()] required`
- `user_id: Annotated[int | None, Path(gt=0)], default None`

Filter all task by status and user_id.

Output:
- `taks_list: TaskListResponseSerializer`


### Serializers

#### Token
Attributes:
- `access_token: str`
- `type_token: str`


#### TaskListResponseSerializer
Attributes:
- `taks_list: [TaskBase]`


#### TaskBase
Attributes:
- `id : int`
- `title: str`
- `description: str | None`
- `status: str`
- `user_id: int`
 
   
#### CreateTaskSerializer
Attributes:
- `title: str`
- `description: str | None`
- `status: str`
- `user_id: int`

#### TaskUpdateRequestSerializer

Attributes:
- `id : int`
- `title: str | None`
- `description: str | None`
- `status: str | None`

#### SingleTaskRequestSerializer

Attributes:
- `id : int`

#### TaskStatusRequestSerializer  
Attributes:
   - ` status: str`
   - ` user_id: int | None`

#### DeleteTaskRequestSerializer  

- `id: int` 
- `user_id: int`

----
 #### UserCreateRequestSerializer   
Attributes:
- `first_name: str`
- `last_name: str | None`
- `username: str`
- `password: str`

#### UserCheckRequestSerializer
Attributes:
- `first_name: str`
- `last_name: str | None`
- `username: str`
- `password: str`

#### UserGetRequestSerializer

Attributes:
- `id: int`

---
#### Pagination
Attributes:
- `page_size: int`
- `page_number: int`

---

## Database
### ORM
### Models
#### Task
   - id: int, primary key
   - title: str
   - description: str |  None
   - status: str, not null
   - user_id: foreign key

#### User
- first_name: str
- last_name: str| none
- username: str, unique
- password: str

#### BaseOperation 
 **Note:** support Asynchronous context manager.

**Methods:**

`Pagination`

    Limit response of query.

   - *parameter*: query: Query, page_size: int, page_number: int
   - *return:* Query

#### UserOperation(BaseOperation)
 **Note:** support Asynchronous context manager.

**Methods:**

`insert_user`

Create user in databse.

- *parameter*: user: UserCreateRequestSerializer
- *return:* int

`insert_user`

Create user in database. Raise HTTP 400 if it's in the database.

- *parameter*: user: UserCreateRequestSerializer
- *return:* int

 `get_user_by_id`

Get user by id. Raise HTTP 400 if it's not founded.

 - *parameter*: user: UserGetRequestSerializer) 
 - *return:* UserBase:

 `get_user_by_username`

Get user by username. Raise HTTP 400 if it's not founded.

 - *parameter*: user: UserCheckRequestSerializer) 
 - *return:* UserBase:

 `check_user`

Check if user in database.

 - *parameter*: user: UserCheckRequestSerializer) 
 - *return:* bool:

#### UserOperation(BaseOperation)
 **Note:** support Asynchronous context manager.

**Methods:**

 `get_task`

Get task by id.

 - *parameter*: task_id: int) 
 - *return:* TaskBase:

 `get_all_tasks`

Get all tasks.

 - *parameter*: page_size: int, page_number: int) 
 - *return:* TaskListResponseSerializer:

`update_task_by_field`

Update task on description, title, status. Raise HTTP 400 if it's not founded.

- *parameter*: task: TaskUpdateRequestSerializer
- *return:* TaskBase

`insert_task`

Create task.

- *parameter*: task: CreateTaskSerializer
- *return:* int 


`delete_task`

Delete task by id.

- *parameter*: task: SingleTaskRequestSerializer
- *return:* dict[str:str]

`filter_by_status`

Filter user's task by status and id.

- *parameter*: task: TaskStatusRequestSerializer, page_size, page_number
- *return:*  TaskListResponseSerializer
- 
`get_users_tasks`

Get all user's task. Raise HTTP 400 if it's not founded.

- *parameter*: user_id: int, page_size: int, page_number: int
- *return:* TaskListResponseSerializer

`check_task_owner`

Check the task for user ownership.

- *parameter*: user_id: int, task_id: int
- *return:* bool