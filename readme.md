# Leave Request System

Assignment to implement the leave management system where employee can apply for the leave and admin can approve the request

## Requirement
* python3
* Django==3.2.13
* djangorestframework==3.13.1

## Step to run the sytem
```text
* Create a virtual environment in python3 
* install the required packages mentioned in requirement.txt
* create users using manage.py script
* start the server
* create below two groups thought admin panel and assign the respective permission
  * Admin - Can approve the leave request
  * Employees - Can raise the leave request
* create the users and assign the group to each group
```

## endpoints
```yaml
api/v1/leave/request:
  get: to get the leave request for the user
  post: create the new leave request
  patch: cancel the leave request
api/v1/leave/verify:
  get: to get the leave requests
  patch: update the leave request
```
Note: API documentation available in design/swagger

## Project Structure
```yaml
attendance_system: mail django resources
core:
  custom_auth: file contain the custom authentication
  custom_exception: file has the custom exception
  permission_config: config file for the core
design:
  swagger: design document for the apis
src: endpoint app for the project
  models: common model for the project
  services: contain all the endpoints services
    leave:
      config: have all the configuration for the endpoint
      controller: have the endpoint handler
      logic: all the logics for the endpoint
        entity: all the data entity required for the endpoint
        manager: all the manager class to process the request or logics
        utility: all the utility or common function of the endpoints
      models: all the db related stuffs
      serializers: all the serialization logics for the endpoint
```

# NOTE: all the endpoint expecting token in header
```text
Example
--header 'token: 19db1042-a9df-44af-8621-1eb3f413d9f0'
```