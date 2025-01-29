from flask import Flask
from flask_cors import CORS
from babyReport import babyReport
from waitress import serve

app = Flask(__name__)
CORS(app)

@app.route('/generate_report', methods=['POST'])
def generate_report(dob,location,lat,lon,path,gender,name,timezone,input):
    babyReport(dob,location,lat,lon,path,gender,name,timezone,input)
    print("Report generated")
    
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)