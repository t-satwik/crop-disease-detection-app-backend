# Crop-Disease-Detection-App
 
# Backend Repo

### Setup

1. Download the Repository to your local machine <br>
2. Create a Virtual Environment in the [crop-disease-detection-app-backend](./crop-disease-detection-app-backend) folder with this command below <br>
   `python -m venv venv`
3. Activate the environment with this command <br>
   `.\venv\Scripts\activate`
4. Install the dependencies (like Django, Django-Rest-FrameWork)<br>
   `pip install -r requirements.txt`

### Running the Application

1. Activate the environment with this command. <br>
   `.\venv\Scripts\activate`
2. Start the application by running this command (_Run the command where [manage.py](./crop_disease_detection_app/manage.py) is   located_) or 
     `cd crop_disease_detection_app`  <br>
3.   ` python manage.py runserver`

### Accessing the Admin Panel

1. You can access the admin panel by running the server and opening <http://localhost:8000/admin>
2. Run `python manage.py createsuperuser` to create a user to access the admin panel.
3. Set up the Username and Password
4. You can log in and change the database values anytime.

# API References
1. [**api/login/**](#apilogin)


3. [**Student APIs**](#student-portal-apis)
    1. [**api/student/profile/**](#apistudentprofile)
    2. [**api/student/getDashboard/**](#apistudentgetdashboard)
    3. [**api/student/addResume/**](#apistudentaddresume)
    4. [**api/student/deleteResume/**](#apistudentdeleteresume)
    5. [**api/student/submitApplication/**](#apistudentsubmitapplication)
4. [**Admin APIs**](#admin-portal-apis)
    1. [**api/admin/markStatus/**](#apiadminmarkstatus)
    2. [**api/admin/getDashboard/**](#apiadmingetdashboard)
    3. [**api/admin/updateDeadline/**](#apiadminupdatedeadline)
    4. [**api/admin/updateOfferAccepted**](#apiadminupdateofferaccepted)
    5. [**api/admin/updateEmailVerified**](#apiadminupdateemailverified)
    6. [**api/admin/updateAdditionalInfo**](#apiadminupdateadditionalinfo)
5. [**Company APIs**](#company-portal-apis)
    1. [**api/company/addPlacement/**](#apicompanyaddplacement)
6. [**Common Errors**](#common-errors)


---

# APIs Descriptions

## `api/login/`

This Api is used to validate the credentials entered by a user.

### How to Use?

Send a `POST` request to `api/login/`<br>
Request_Body:

```json
{
"user_name":"user1"
"password":"123"
}
```

### Response

Sample Response Json contains all these fields

```json
{
  "message":"User Verified"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `User Verified`          |
| 401 UNAUTHORIZED| `Wrong Password`         | 
| 401 UNAUTHORIZED| `Enter Password`          | 
| 404 NOT FOUND| `User not found`          | 
| 400 NOT FOUND| `Bad Request`          | 


You may see some different errors which can be seen [here](#common-errors)

---
---

## `Common Errors`

Some common errors that you may see while accessing the Apis

| Status Codes     | Possible Messages                                        | Possible Reasons                                                                             |
| ---------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 401 UNAUTHORIZED | `Authorization Header Not Found`                         | Check for the authorization header in you request and the prefix( Should use `Bearer`) used. |
| 401 UNAUTHORIZED | `Access Denied. You are not allowed to use this service` | Your may not have required access to those access those Apis.                                |
| 401 UNAUTHORIZED | `Token has wrong audience`                               | You may be using wrong credentials for Google OAuth2.0.                                      |
| 404 NOT FOUND    | `User Not Found. Contact CDC for more details`           | You may not be a user at CDC, IIT Dharwad. Please contact us to get your user account        |
| 400 BAD_REQUEST  | `Error Occurred`                                 | Any random Error which can be seen in the {error} string.                                    |
| 400 BAD_REQUEST  | `Something went wrong`                                 | Any random Error which can be seen in the {error} string.                                    |
