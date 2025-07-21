import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css"; // Custom CSS for styling

export default function ChurnPredictionForm() {
  const [formData, setFormData] = useState({
    query1: "",
    query2: "",
    query3: "",
    query4: "",
    query5: "",
    query6: "",
    query7: "",
    query8: "",
    query9: "",
    query10: "",
    query11: "",
    query12: "",
    query13: "",
    query14: "",
    query15: "",
    query16: "",
    query17: "",
    query18: "",
    query19: "",
  });

  const [output, setOutput] = useState({ output1: "", output2: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Simulate API call to Flask backend
    fetch("http://localhost:5000/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then((res) => res.json())
      .then((data) => setOutput(data))
      .catch((err) => console.error(err));
  };

  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <h2 className="text-center mb-4 text-primary">Churn Prediction Form</h2>

        <form onSubmit={handleSubmit}>
          <div className="row">
            {Object.keys(formData).map((key, index) => (
              <div className="col-md-6 mb-3" key={index}>
                <label className="form-label">{key}:</label>
                <textarea
                  className="form-control"
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  rows="1"
                />
              </div>
            ))}
          </div>

          <div className="text-center mt-3">
            <button type="submit" className="btn btn-primary btn-lg">
              Submit
            </button>
          </div>
        </form>

        {/* ✅ Output Section */}
        <div className="mt-4">
          <h4 className="text-success">Prediction Result:</h4>
          <textarea
            className="form-control mb-2"
            rows="2"
            value={output.output1}
            readOnly
          />
          <textarea
            className="form-control"
            rows="2"
            value={output.output2}
            readOnly
          />
        </div>
      </div>
    </div>
  );
}
