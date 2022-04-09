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

### Testing the Admin Panel
AN instance of this server is running on a machin at IIT Dharwad, and it can be accessed by using the 
URl: [**http://farmbook.iitdh.ac.in**](http://farmbook.iitdh.ac.in/)

# API References
1. [**apis/Login/**](#apislogin)
1. [**apis/SignUp/**](#apissignup)
1. [**apis/SetData/**](#apissetdata)
1. [**apis/GetPastData/**](#apisgetpastdata)
1. [**apis/GetSensorValueData/**](#apisgetsensorvaluedata)
1. [**apis/SetVideoFrame/**](#apissetvideoframe)
1. [**apis/SetSensorData/**](#apissetsensordata)
1. [**apis/GetCropRecommendation/**](#apisgetcroprecommendation)
1. [**apis/GetCropRecommendationWithGivenData/**](#apisgetcroprecommendationwithgivendata)


<!-- 3. [**Student APIs**](#student-portal-apis)
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
6. [**Common Errors**](#common-errors) -->


---

# APIs Descriptions

## `apis/Login/`

This Api is used to validate the credentials entered by a user.

### How to Use?

Send a `POST` request to `apis/login/`<br>
### Associated View:
```checkLogin```

### Request_Body:

```json
{
 "user_name":"user1"
 "password":"123"
}
```

### Response

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


<!-- You may see some different errors which can be seen [here](#common-errors) -->

---

## `apis/SignUp/`

This Api is used to create a new user with the given details.

### How to Use?

Send a `POST` request to `apis/SignUp/`<br>

### Associated View:
```newSignup```

### Request_Body:

```json
{
 "user_name":"user1",
 "email":"user1@farmbook.com",
 "password":"123"
}
```

### Response

```json
{
  "message":"User Created"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `User Created`          |
| 400 NOT FOUND| `Bad Request`          | 


<!-- You may see some different errors which can be seen [here](#common-errors) -->

---
## `apis/SetData/`

This Api is used to create a new data object corresponding to the location data and the image.

### How to Use?

Send a `POST` request to `apis/SetData/`<br>
### Associated View:
```setData```

### Request_Body:

```json
{
 "time_stamp":"08/04/2022 16:28:24",
 "latitude":"0.0",
 "longitude":"0.0",
 "probability":"0.95",
 "predicted_class":"healthy",
 "crop_name":"maize",
 "user_name":"user1",
 "image":"image file"
}
```

### Response

```json
{
  "message":"Data Object Created"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Data Object Created`          |
| 404 NOT FOUND| `Predicted class not foundd`          | 
| 404 NOT FOUND| `Crop not found`          | 
| 404 NOT FOUND| `User not found`          | 
| 400 NOT FOUND| `Bad Request - python Exception`          | 


<!-- You may see some different errors which can be seen [here](#common-errors) -->

---
## `apis/GetPastData/`

This Api is used to get the data and the images associated with a user.

### How to Use?

Send a `POST` request to `apis/GetPastData/`<br>

### Associated View:
```getPastData```

### Request_Body:

```json
{
 "user_name":"user1",
 "starting_index":"0"
}
```

### Response

```json
{
  "message":"Data Fetch Successful",
  "data_count":1,
  "data0":{
    "time_stamp":"08/04/2022 16:19:27",
    "latitude":"0.0" ,
    "longitude":"0.0" ,
    "predicted_class":"healthy" ,
    "probability":"0.95",
    "user":"user1",
    "crop_type":"maize",
    "file_name":"user1_maize_08-04-2022_16-19-27.png",
  }

}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Data Fetch Successful`  |
| 400 NOT FOUND| `Bad Request - python Exception`          | 


<!-- You may see some different errors which can be seen [here](#common-errors) -->

---
## `apis/GetSensorValueData/`

This Api is used to get the sensor values associated to a user.

### How to Use?

Send a `POST` request to `apis/GetSensorValueData/`<br>

### Associated View:
```getSensorValuesData```
### Request_Body:

```json
{
 "user_name":"user1"
}
```

### Response

```json
{
  "message":"Sensors Data Fetch Successful",
  "total_count":1,
  "sensor_type":"humidity",
  "latitude":"0.0",
  "longitude":"0.0",
  "user":"user1",
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `User Verified`          |
| 400 NOT FOUND| `Bad Request - python Exception`          | 


<!-- You may see some different errors which can be seen [here](#common-errors) -->

---

## `apis/SetVideoFrame/`

This Api is used to create a video frame object to store in the database.

### How to Use?

Send a `POST` request to `apis/SetVideoFrame/`<br>
### Associated View:
```setVideoFrame```

### Request_Body:

```json
{
"time_stamp":"08/04/2022 16:28:24",
"start_latitude":"0.0",
"end_latitude":"0.0",
"start_latitude":"0.0",
"end_longitude":"0.0",
"probability":"0.95",
"predicted_class":"healthy",
"crop_name":"maize",
"user_name":"user1",
"image":"image file",
}
```

### Response

```json
{
  "message":"Data Object Created"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Data Object Created`          |
| 404 NOT FOUND| `Predicted class not foundd`          | 
| 404 NOT FOUND| `Crop not found`          | 
| 404 NOT FOUND| `User not found`          | 
| 400 NOT FOUND| `Bad Request - python Exception`          | 

## `apis/setSensorData/`

This Api is used to create a sensor value object to store in the database.

### How to Use?

Send a `POST` request to `apis/setSensorData/`<br>
### Associated View:
```setSensorData```

### Request_Body:

```json
{
"time_stamp":"08/04/2022 16:28:24",
"latitude":"0.0",
"longitude":"0.0",
"sensor_type":"humidity",
"value":"100.00"
}
```

### Response

```json
{
  "message":"Value Added to the sensor"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Value Added to the sensor`          |
| 200 OK          | `New sensor added and appended value`          |
| 404 NOT FOUND| `Predicted class not foundd`          | 
| 404 NOT FOUND| `sensor type not found`          | 
| 404 NOT FOUND| `user not found`          | 
| 400 NOT FOUND| `Bad Request`          | 

## `apis/GetCropRecommendation/`

This Api is used to give a recommendation based on the existing data in the database.

### How to Use?

Send a `POST` request to `apis/GetCropRecommendation/`<br>
### Associated View:
```getCropRecommendation```

### Request_Body:

```json
{
"latitude":"0.0",
"longitude":"0.0",
"user_name":"user1",
}
```

### Response

```json
{
  "message":"Data present",
  "full_data":1,
  "predicted_crop":"maize"

}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Data present`          |
| 200 OK          | `Data not present`          |
| 400 NOT FOUND| `Bad Request - python Exception`          | 

## `apis/GetCropRecommendationWithGivenData/`

This Api is used to give a recommendation based on the existing data in the database.

### How to Use?

Send a `POST` request to `apis/GetCropRecommendationWithGivenData/`<br>
### Associated View:
```GetCropRecommendationWithGivenData```

### Request_Body:

```json
{
"latitude":"0.0",
"longitude":"0.0",
"user_name":"user1",
"nitrogen":"0.5",
"phosphorus":"0.5",
"potassium":"0.5",
"pH":"7",
"temperature":"40",
"humidity":"40",



}
```

### Response

```json
{
  "message":"Crop recommended successfully",
  "full_data":1,
  "predicted_crop":"maize"

}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Crop recommended successfully`          |
| 400 NOT FOUND| `Bad Request - python Exception`          | 




<!-- ## `Common Errors`

Some common errors that you may see while accessing the Apis

| Status Codes     | Possible Messages                                        | Possible Reasons                                                                             |
| ---------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 401 UNAUTHORIZED | `Authorization Header Not Found`                         | Check for the authorization header in you request and the prefix( Should use `Bearer`) used. |
| 401 UNAUTHORIZED | `Access Denied. You are not allowed to use this service` | Your may not have required access to those access those Apis.                                |
| 401 UNAUTHORIZED | `Token has wrong audience`                               | You may be using wrong credentials for Google OAuth2.0.                                      |
| 404 NOT FOUND    | `User Not Found. Contact CDC for more details`           | You may not be a user at CDC, IIT Dharwad. Please contact us to get your user account        |
| 400 BAD_REQUEST  | `Error Occurred`                                 | Any random Error which can be seen in the {error} string.                                    |
| 400 BAD_REQUEST  | `Something went wrong`                                 | Any random Error which can be seen in the {error} string.                                    | -->
