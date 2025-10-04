from flask import Flask,request,render_template
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("sleep_disorder_predicting_modal.pkl","rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():

    gender = request.form.get("gender")
    age = request.form.get("age")
    occupation = request.form.get("occupation")
    sleep_duration = request.form.get("sleep_duration")
    quality_of_sleep = request.form.get("quality_of_sleep")
    physical_activity_level = request.form.get("physical_activity_level")
    stress_level = request.form.get("stress_level")
    bmi_category = request.form.get("bmi_category")
    systolic_bp = request.form.get("systolic_bp")
    diastolic_bp = request.form.get("diastolic_bp")
    heart_rate = request.form.get("heart_rate")
    daily_steps = request.form.get("daily_steps")

    occupation_id = {"Software Engineer":1,"Doctor":2,"Sales Representative":3,"Teacher":4,"Nurse":5,"Engineer":6,
                                             "Accountant":7,"Scientist":8,"Lawyer":9,"Salesperson":10,"Manager":11}
    bmi_id = {"Overweight":1,"Normal":2,"Obese":3,"Normal Weight":4}

    data = pd.DataFrame({"Gender":[0 if gender == "Male" else 1],
                        "Age":[int(age)],"Occupation":[occupation_id[occupation]],
                        "Sleep Duration":[int(sleep_duration)],"Quality of Sleep":[int(quality_of_sleep)],
                        "Physical Activity Level":[int(physical_activity_level)],"Stress Level":[int(stress_level)],
                        "BMI Category":[bmi_id[bmi_category]],"Heart Rate":[int(heart_rate)],"Daily Steps":[int(daily_steps)],
                        "Systolic_BP":[int(systolic_bp)],"Diastolic_BP":[int(diastolic_bp)]})

    print(data)

    sleep_disorder = model.predict(data)[0]

    print(sleep_disorder)

    if sleep_disorder == 1:
        sleep_disorder = "Normal"
    elif sleep_disorder == 2:
        sleep_disorder = "Sleep Apnea"
    elif sleep_disorder == 3:
        sleep_disorder = "Insomnia"

    return render_template("index.html", prediction_text=f"The sleep disorder is {sleep_disorder}")

if __name__ == "__main__":
    app.run(debug=True)
