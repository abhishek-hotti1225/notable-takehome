Hello Notable Team,

In order to test through the changes requested in the TakeHome Exam. Please go through the following steps to reproduce
steps

1) python3 -m venv venv (creates isolated virtualenv)
2) source venv/bin/activate (activates environment)
3) pip3 install -r requirements.txt (installs dependencies)
4) python3 simple_api.py (starts Flask server)

How to test:

I have added three doctors to test the functionality

```
doctors = [
    {"id": 0, "firstName": "Notable-0", "lastName": "Bob"},
    {"id": 1, "firstName": "Notable-1", "lastName": "Abhi"},
    {"id": 2, "firstName": "Notable-2", "lastName": "John"},
]
```

and appointments for a couple of doctors on `2024/04/17` and `2024/04/19`

So the few endpoints I have created are as follows:

1) /get-all-doctors
    2) Responds with all the doctors available in the system with their ids and names
    3) Ex: `curl -X GET http://127.0.0.1:5005/get-all-doctors`

3) /get-doctor-schedule/\<id\>
    4) Responds with the doctors schedule, takes in a query param of the date in question
        5) If trying to get a schedule for a doctor who does not exist, then get an error
    6) Ex: `curl -X GET 'http://127.0.0.1:5005/get-doctor-schedule/1?date=2024/04/17'`
7) /add_appointment/\<id\>
    8) Adds an appointment to the doctors schedule at the specified time and date
        9) if time is valid ( 15 min interval )
        10) Doctor has availability to take on this appointment (has less than 3 for that time slot)
    11) Ex: ```
        curl -X POST 'http://127.0.0.1:5005/add_appointment/1'
        --header 'Content-Type: application/json'
        --data '{
        "patient_lname": "Sam",
        "patient_fname": "Hubble",
        "time": "9:45",
        "type": "Follow Up",
        "date": "2024/04/17"
        }' ```
12) /delete_appointment/\<id\>
    13) Deletes the specified appointment for the doctor
        14) Returns error if invalid appointment id is passed in
    15) Ex: ``` curl -X  DELETE 'http://127.0.0.1:5005/delete_appointment/1?appt=<appnt-id>'```