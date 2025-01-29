from flask import Flask,request,jsonify
from flask_cors import CORS
from finalBabyReport import babyReport
from waitress import serve

app = Flask(__name__)
CORS(app)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    babyReport(data['dob'],data['location'],data['lat'],data['lon'],app.root_path,data['gender'],data['name'],"5.30",data['input'])
    print("Report generated")

    return jsonify({
        "message" : "Success"
        }), 200
    
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)