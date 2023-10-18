from flask import Flask, render_template, request, jsonify
from model_prediction import *

app = Flask(__name__)

text=""
predicted_emotion=""
predicted_emotion_img_url=""

@app.route("/")
def home():
    entries = show_entry()
    return render_template("index.html", entries=entries)
    

@app.route("/predict-emotion", methods=["POST"])
def predict_emotion():
    input_text = request.json.get("text")
    if not input_text:
        return jsonify({
            "status": "error",
            "message": "Please enter some text to predict emotion!"
        }), 400
    else:
        predicted_emotion, predicted_emotion_img_url = predict(input_text)                         
        return jsonify({
            "data": {
                "predicted_emotion": predicted_emotion,
                "predicted_emotion_img_url": predicted_emotion_img_url
            },
            "status": "success"
        }), 200
        
#Write the code for API here
@app.route("/save-entry", methods=["POST"])
def save_entry():
    date = request.json.get("d")
    emotion=request.json.get("e")
    text = request.json.get("t")

    save_text = text.replace('\n', " ")
    entry = f'"{date}", "{save_text}", "{emotion}"'
    with open("./static/assets/data_files/data_entry.csv", "a") as vanya:
        vanya.write(entry)

    return jsonify("success")

                
if __name__ == "__main__":
    app.run(debug=True)

