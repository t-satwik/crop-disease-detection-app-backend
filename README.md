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
