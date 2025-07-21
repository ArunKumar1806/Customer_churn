import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

df_1 = pd.read_csv("first_telc.csv")  # Load the dataset used for predictions

@app.route("/")
def loadPage():
    return render_template('index.html', query="")

@app.route("/", methods=['POST'])
def predict():
    # Load model and feature columns
    model = pickle.load(open("model.pkl", "rb"))
    train_columns = pickle.load(open("model_columns.pkl", "rb"))  # Load feature names

    # Collect user input from form
    input_data = [[
        int(request.form['query1']),  # SeniorCitizen (int)
        float(request.form['query2']),  # MonthlyCharges (float)
        float(request.form['query3']),  # TotalCharges (float)
        request.form['query4'],  # gender (categorical)
        request.form['query5'],  # Partner (categorical)
        request.form['query6'],  # Dependents (categorical)
        request.form['query7'],  # PhoneService (categorical)
        request.form['query8'],  # MultipleLines (categorical)
        request.form['query9'],  # InternetService (categorical)
        request.form['query10'],  # OnlineSecurity (categorical)
        request.form['query11'],  # OnlineBackup (categorical)
        request.form['query12'],  # DeviceProtection (categorical)
        request.form['query13'],  # TechSupport (categorical)
        request.form['query14'],  # StreamingTV (categorical)
        request.form['query15'],  # StreamingMovies (categorical)
        request.form['query16'],  # Contract (categorical)
        request.form['query17'],  # PaperlessBilling (categorical)
        request.form['query18'],  # PaymentMethod (categorical)
        request.form['query19']   # tenure (int)
    ]]

    # Convert to DataFrame
    new_df = pd.DataFrame(input_data, columns=[
        'SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender', 
        'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
        'PaymentMethod', 'tenure'
    ])

    # Add the new entry to df_1
    df_2 = pd.concat([df_1, new_df], ignore_index=True)

    # Process tenure column into tenure groups
    labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
    df_2['tenure_group'] = pd.cut(df_2.tenure.astype(int), range(1, 80, 12), right=False, labels=labels)
    df_2.drop(columns=['tenure'], axis=1, inplace=True)

    # Convert categorical features to dummy variables
    new_df__dummies = pd.get_dummies(df_2[[
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure_group'
    ]])

    # **Ensure feature alignment**
    new_df__dummies = new_df__dummies.reindex(columns=train_columns, fill_value=0)

    # Make predictions
    single = model.predict(new_df__dummies.tail(1))
    probability = model.predict_proba(new_df__dummies.tail(1))[:, 1]

    # Generate result message
    if single == 1:
        o1 = "This customer is likely to churn!"
        o2 = f"Confidence: {probability[0] * 100:.2f}%"
    else:
        o1 = "This customer is likely to stay!"
        o2 = f"Confidence: {probability[0] * 100:.2f}%"

    return render_template('index.html', output1=o1, output2=o2, **request.form)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
