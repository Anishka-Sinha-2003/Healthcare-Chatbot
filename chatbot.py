# from flask import Flask, request, jsonify, render_template_string
# import pandas as pd

# app = Flask(__name__)

# # Load your dataset
# df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")  # Replace with your actual filename

# # Convert DataFrame to a dictionary for diseases
# disease_db = {}
# for _, row in df.iterrows():
#     disease_name = row["Disease"].lower()  # Ensure column name matches your CSV
#     disease_db[disease_name] = {
#         "fever": row["Fever"],
#         "cough": row["Cough"],
#         "fatigue": row["Fatigue"],
#         "difficulty_breathing": row["Difficulty Breathing"],  # Fixed typo
#         "common_in_age": row["Age"],
#         "common_in_gender": row["Gender"],
#         "blood_pressure_risk": row["Blood Pressure"],
#         "cholesterol_risk": row["Cholesterol Level"],
#         "outcome": row["Outcome Variable"]
#     }

# @app.route("/ask", methods=["GET", "POST"])
# def ask():
#     if request.method == "POST":
#         user_query = request.form.get("query", "").lower()  # For form submissions
#     else:
#         user_query = request.args.get("query", "").lower()  # For direct URLs

#     disclaimer = "⚠️ I'm a healthcare assistant, not a doctor. Consult a professional for medical advice.\n\n"
    
#     # Check for disease queries
#     for disease in disease_db:
#         if disease in user_query:
#             response = f"🔍 {disease.upper()} DETAILS:\n"
#             response += f"• Fever: {disease_db[disease]['fever']}\n"
#             response += f"• Cough: {disease_db[disease]['cough']}\n"
#             response += f"• Fatigue: {disease_db[disease]['fatigue']}\n"
#             response += f"• Difficulty Breathing: {disease_db[disease]['difficulty_breathing']}\n"
#             response += f"• Common in Age: {disease_db[disease]['common_in_age']}\n"
#             response += f"• Common in Gender: {disease_db[disease]['common_in_gender']}\n"
#             response += f"• Blood Pressure Risk: {disease_db[disease]['blood_pressure_risk']}\n"
#             response += f"• Cholesterol Risk: {disease_db[disease]['cholesterol_risk']}\n"
#             response += f"• Outcome: {disease_db[disease]['outcome']}\n"
#             return disclaimer + response

#     return disclaimer + "❌ Sorry, I couldn't find information on that disease."

# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         query = request.form.get("query")
#         reply = ask()
#         return render_template_string('''
#             <h1 style="color: #4CAF50;">Healthcare Chatbot</h1>
#             <form method="POST">
#                 <input type="text" name="query" placeholder="Ask about a disease..." required 
#                        style="padding: 8px; width: 300px;">
#                 <button type="submit" 
#                         style="padding: 8px 15px; background: #4CAF50; color: white; border: none;">
#                     Ask
#                 </button>
#             </form>
#             <pre style="background: #f4f4f4; padding: 15px; border-radius: 5px;">{{ reply }}</pre>
#         ''', reply=reply)
#     return render_template_string('''
#         <h1 style="color: #4CAF50;">Healthcare Chatbot</h1>
#         <form method="POST">
#             <input type="text" name="query" placeholder="Ask about a disease..." required 
#                    style="padding: 8px; width: 300px;">
#             <button type="submit" 
#                     style="padding: 8px 15px; background: #4CAF50; color: white; border: none;">
#                 Ask
#             </button>
#         </form>
#     ''')

# if __name__ == "__main__":
#     app.run(debug=True, port=5001)



from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")  # Replace with your filename

# Prepare disease database
disease_db = {}
for _, row in df.iterrows():
    disease_name = row["Disease"].lower()
    disease_db[disease_name] = {
        "fever": row["Fever"],
        "cough": row["Cough"],
        "fatigue": row["Fatigue"],
        "breathing difficulty": row["Difficulty Breathing"],
        "common age": row["Age"],
        "common gender": row["Gender"],
        "bp risk": row["Blood Pressure"],
        "cholesterol risk": row["Cholesterol Level"],
        "outcome": row["Outcome Variable"]
    }

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.form.get("query", "").lower()
    response = {
        "status": "success",
        "disclaimer": "⚠️ I'm an AI assistant, not a doctor. Always consult a healthcare professional.",
        "data": None
    }

    for disease in disease_db:
        if disease in user_query:
            response["data"] = {
                "name": disease.upper(),
                "details": disease_db[disease]
            }
            break

    if not response["data"]:
        response.update({
            "status": "error",
            "message": "Disease not found in our database"
        })

    return jsonify(response)

@app.route("/", methods=["GET"])
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HealthBot Pro</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {
                --primary: #4361ee;
                --secondary: #3f37c9;
                --light: #f8f9fa;
                --dark: #212529;
            }
            body {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
            }
            .card {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                transition: transform 0.3s;
                border: none;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .btn-primary {
                background-color: var(--primary);
                border: none;
                padding: 10px 25px;
                border-radius: 50px;
            }
            .result-card {
                background: white;
                border-left: 5px solid var(--primary);
            }
            .disease-name {
                color: var(--primary);
                font-weight: 600;
            }
            .feature-icon {
                width: 40px;
                height: 40px;
                background: rgba(67, 97, 238, 0.1);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary);
                margin-right: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card p-4 p-md-5 mb-4">
                        <div class="text-center mb-4">
                            <h1 class="display-4 fw-bold" style="color: var(--primary);">
                                <i class="fas fa-heartbeat me-2"></i> HealthBot Pro
                            </h1>
                            <p class="lead text-muted">
                                Your intelligent healthcare assistant for disease information
                            </p>
                        </div>
                        
                        <form id="queryForm" class="mb-4">
                            <div class="input-group">
                                <input type="text" id="queryInput" class="form-control form-control-lg" 
                                       placeholder="Ask about any disease..." required>
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-search me-2"></i> Search
                                </button>
                            </div>
                        </form>
                        
                        <div id="resultContainer" class="d-none">
                            <div class="card result-card p-4 mb-3">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="feature-icon">
                                        <i class="fas fa-info-circle"></i>
                                    </div>
                                    <h3 id="diseaseTitle" class="disease-name mb-0"></h3>
                                </div>
                                <div id="diseaseDetails" class="row"></div>
                            </div>
                            <div class="alert alert-warning" id="disclaimerAlert">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                <span id="disclaimerText"></span>
                            </div>
                        </div>
                        
                        <div id="errorContainer" class="alert alert-danger d-none">
                            <i class="fas fa-times-circle me-2"></i>
                            <span id="errorText"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            document.getElementById('queryForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const query = document.getElementById('queryInput').value;
                
                // Show loading state
                document.getElementById('resultContainer').classList.add('d-none');
                document.getElementById('errorContainer').classList.add('d-none');
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: `query=${encodeURIComponent(query)}`
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        // Update disclaimer
                        document.getElementById('disclaimerText').textContent = data.disclaimer;
                        
                        if (data.data) {
                            // Update disease info
                            document.getElementById('diseaseTitle').textContent = data.data.name;
                            
                            const detailsContainer = document.getElementById('diseaseDetails');
                            detailsContainer.innerHTML = '';
                            
                            // Add each detail
                            for (const [key, value] of Object.entries(data.data.details)) {
                                const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                                const detailItem = `
                                    <div class="col-md-6 mb-3">
                                        <div class="d-flex align-items-center">
                                            <div class="feature-icon">
                                                <i class="fas fa-${getIconForField(key)}"></i>
                                            </div>
                                            <div>
                                                <h6 class="mb-0 text-muted">${formattedKey}</h6>
                                                <p class="mb-0 fw-bold">${value}</p>
                                            </div>
                                        </div>
                                    </div>
                                `;
                                detailsContainer.innerHTML += detailItem;
                            }
                            
                            document.getElementById('resultContainer').classList.remove('d-none');
                        }
                    } else {
                        document.getElementById('errorText').textContent = data.message;
                        document.getElementById('errorContainer').classList.remove('d-none');
                    }
                } catch (error) {
                    document.getElementById('errorText').textContent = 'Failed to connect to server';
                    document.getElementById('errorContainer').classList.remove('d-none');
                }
            });
            
            function getIconForField(field) {
                const icons = {
                    'fever': 'temperature-high',
                    'cough': 'lungs',
                    'fatigue': 'tired',
                    'breathing': 'wind',
                    'age': 'user-clock',
                    'gender': 'venus-mars',
                    'bp': 'heartbeat',
                    'chol': 'vial',
                    'outcome': 'clipboard-check'
                };
                return icons[field] || 'info-circle';
            }
        </script>
    </body>
    </html>
    ''')

if __name__ == "__main__":
    app.run(debug=True, port=5001)