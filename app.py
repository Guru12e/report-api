from flask import Flask, request, jsonify
from flask_cors import CORS
from finalBabyReport import babyReport
from freeReport import freeReport
from multiprocessing import Process
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from waitress import serve
from apscheduler.schedulers.background import BackgroundScheduler

plans = [
    "Starter Parenting",
    "Pro Parenting",
    "Ultimate Parenting",
    "Master Parenting",
]

def AstrokidsBot():
    while True:
        print("Bot is running...")
        try:
            client = MongoClient(os.getenv("DATABASE_URL")) 
            database = client["AstroKids"]
            collection = database["childDetails"]

            six_hours_ago = datetime.now() - timedelta(hours=6) 
            
            pipeline = [
                {"$unwind": "$childDetails"},
                {"$match": {
                    "childDetails.addedAt": {"$lt": six_hours_ago}, 
                    "childDetails.isChecked": False  
                }},
                {"$project": {"childDetails": 1, "_id": 0}}
            ]
            
            childDetails = list(collection.aggregate(pipeline))
            print(f"Found {len(childDetails)} child records")

            for child in childDetails:
                details = child["childDetails"]
                try:
                    print(f"Processing report for {details['name']}")
                    babyReport(f"{details['dob']} {details['time']}:00" , details['place'], details['lat'], details['lon'], root_path, details['gender'], details['name'], "5.30", plans.index(details['plan']) + 1)
                    print(f"{details['name']} report generated")

                    collection.update_one(
                        {"childDetails.orderId": details['orderId']},  
                        {"$set": {"childDetails.$.isChecked": True}}  
                    )
                    print(f"{details['name']} isChecked updated to True")
                    
                except Exception as e:
                    print(f"Error processing {details['name']}: {e}")
                    
            client.close()  
            
        except Exception as e:
            print(f"Main Bot Error: {e}")
        
        time.sleep(3600)

        
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    babyReport(data['dob'], data['location'], data['lat'], data['lon'], os.path.dirname(os.path.abspath(__file__)), data['gender'], data['name'], "5.30", data['input'])
    print("Report generated")

    return jsonify({
        "message": "Success"
    }), 200

@app.route('/freeReport', methods=['POST'])
def freeReportApi():
    data = request.json
    planets = freeReport(data['dob'], data['location'], data['lat'], data['lon'], app.root_path, data['gender'], data['name'], "5.30")
    return jsonify(planets), 200

if __name__ == '__main__':
    bot_process = Process(target=AstrokidsBot, daemon=True) 
    bot_process.start()
    print("Bot process started!")

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("Shutting down bot...")
    finally:
        bot_process.join()  