import json
from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)
doctors = [
    {"id": 0, "firstName": "Notable-0", "lastName": "Bob"},
    {"id": 1, "firstName": "Notable-1", "lastName": "Abhi"},
    {"id": 2, "firstName": "Notable-2", "lastName": "John"},
]
typesOfAppointments = ["new patient", "follow up"]
appointments = {
    "2024/04/17": [
        {
            "appnt_id": str(uuid.uuid4()),
            "patient_lname": "blob",
            "patient_fname": "char",
            "time": "8:00",
            "doctor": 1,
            "kind": typesOfAppointments[0],
        }
    ],
    "2024/04/19": [
        {
            "appnt_id": str(uuid.uuid4()),
            "patient_lname": "blob",
            "patient_fname": "char",
            "time": "8:00",
            "doctor": 1,
            "kind": typesOfAppointments[1],
        },
        {
            "appnt_id": str(uuid.uuid4()),
            "patient_lname": "blob",
            "patient_fname": "char",
            "time": "8:00",
            "doctor": 2,
            "kind": typesOfAppointments[1],
        },
    ],
}


# TODO: 1) Get list of all doctors - done
# TODO: 2) Get list of all appointments for a doctor on a day
# TODO: 3) Delete an existing appointment for a doctor
# TODO: 4) Add a new appointment to doctor's schedule
#           a) 15 min intervals only ( time.min % 15 == 0)
#           b) max of 3 appointments for same time slot


def format_date(date_in_str):
    return datetime.strptime(date_in_str, "%Y/%m/%d")


def does_doctor_exist(id):
    for doc in doctors:
        if doc.get("id") == id:
            return True
    return False


@app.route("/get-all-doctors", methods=["GET"])
def get_all_doctors():
    return jsonify(doctors)


@app.route("/get-doctor-schedule/<int:id>", methods=["GET"])
def get_doctor_schedule(id: int):
    validity_of_doctor = does_doctor_exist(id)
    if not validity_of_doctor:
        return jsonify({"error": "Invalid Doctor Id"}), 404
    date_to_check = request.args.get("date", None)
    date_in_datetime = None
    if date_to_check:
        try:
            date_in_datetime = format_date(date_to_check)
        except:
            return jsonify(
                {"error": "Please enter date in query params as format: YYYY/MM/DD"}
            )

    if date_in_datetime and date_to_check not in appointments:
        return (
            jsonify(
                f"Doctor {doctors[id].get('firstName')} does not have any appointments for {date_in_datetime.strftime('%b %d %Y')}"
            ),
            200,
        )
    all_appointments_for_day = appointments.get(date_to_check)
    doc_appointments = []
    for appoint in all_appointments_for_day:
        if appoint.get("doctor") == id:
            doc_appointments.append(appoint)
    if doc_appointments:
        return jsonify(doc_appointments)
    else:
        return (
            jsonify(
                f"Doctor {doctors[id].get('firstName')} does not have any appointments for {date_in_datetime.strftime('%b %d %Y')}"
            ),
            200,
        )


@app.route("/add_appointment/<int:id>", methods=["POST"])
def add_appointment(id):
    if not request.data:
        return jsonify({"error": "Request Body is empty"}), 400
    try:
        appointment_data = json.loads(request.data)
    except:
        return (
            jsonify(
                {
                    "error": f"JSON Body is not formatted properly. {request.data} is invalid"
                }
            ),
            400,
        )
    if appointment_data.get("type").lower() not in typesOfAppointments:
        return jsonify(
            "Type of appointments supported at New Patient or Follow Up only. Please pass a valid 'type' in request "
            "body"
        )
    validity_of_doctor = does_doctor_exist(id)
    if not validity_of_doctor:
        return jsonify({"error": "Invalid Doctor Id"}), 404

    date_of_appoint = appointment_data.get("date")
    time_of_appoint = appointment_data.get("time")
    if not time_of_appoint:
        return jsonify(
            {
                "error": "Please enter time for appointment in 24 hr format and 15 min increments (ex: 22:45 or 04:15)"
            }
        )
    else:
        try:
            time = datetime.strptime(time_of_appoint, "%H:%M")
            if time.minute % 15 != 0:
                return jsonify(
                    {
                        "error": "Please enter `time` in request body as 24 hr format and in 15 min increments: (ex: "
                        f"22:45 or 04:15). Appointment time {time_of_appoint} is invalid as it not in 15 min interval"
                    }
                )
        except:
            return jsonify(
                {
                    "error": "Please enter `time` in request body as 24 hr format: (ex: 22:45)"
                }
            )
    try:
        format_date(date_of_appoint)
    except:
        return jsonify(
            {"error": "Please enter `date` in request body as format: YYYY/MM/DD"}
        )
    if date_of_appoint not in appointments:
        appointments[date_of_appoint] = []
    all_appointments_for_day = appointments.get(date_of_appoint)
    doc_appointments_for_time = []
    for appoint in all_appointments_for_day:
        if appoint.get("doctor") == id and appoint.get("time") == time_of_appoint:
            doc_appointments_for_time.append(appoint)
    if len(doc_appointments_for_time) < 3:
        appnt = {
            "appnt_id": str(uuid.uuid4()),
            "patient_lname": appointment_data.get("patient_lname"),
            "patient_fname": appointment_data.get("patient_fname"),
            "time": time_of_appoint,
            "doctor": id,
            "kind": appointment_data.get("type"),
            "date": date_of_appoint,
        }
        appointments.get(date_of_appoint).append(appnt)
        return jsonify(appnt)
    else:
        return jsonify(
            f"Sorry, {doctors[id].get('firstName')} time slot at time {date_of_appoint} {time_of_appoint} is full"
        )


@app.route("/delete_appointment/<int:id>", methods=["DELETE"])
def delete_appointment(id: int):
    validity_of_doctor = does_doctor_exist(id)
    if not validity_of_doctor:
        return jsonify({"error": "Invalid Doctor Id"}), 200
    appointment_id = request.args.get("appt", None)
    if not appointment_id:
        return (
            jsonify(
                {
                    "error": "No appointment id entered. Please pass in query params as 'appt'"
                }
            ),
            200,
        )
    for date, all_appointments_for_day in appointments.items():
        for idx, appoint in enumerate(all_appointments_for_day):
            if (
                appoint.get("doctor") == id
                and appoint.get("appnt_id") == appointment_id
            ):
                appnt = all_appointments_for_day.pop(idx)
                return jsonify(appnt)
    return (
        jsonify(
            {
                "error": f"Invalid Appointment Id for Doctor {doctors[id].get('firstName')}"
            }
        ),
        404,
    )


if __name__ == "__main__":
    app.run(port=5005)
