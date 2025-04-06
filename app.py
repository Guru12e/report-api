import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from finalBabyReport import babyReport
from freeReport import freeReport
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

plans = [
    "Starter Parenting",
    "Pro Parenting",
    "Ultimate Parenting",
    "Master Parenting",
]

def AstrokidsBot():
    while True:
        logger.info("Bot is running...")
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
            logger.info(f"Found {len(childDetails)} child records")

            for child in childDetails:
                details = child["childDetails"]
                try:
                    logger.info(f"Processing report for {details['name']}")
                    babyReport(f"{details['dob']} {details['time']}:00", details['place'], details['lat'], details['lon'], os.path.dirname(os.path.abspath(__file__)), details['gender'], details['name'], "5.30", plans.index(details['plan']) + 1)
                    logger.info(f"{details['name']} report generated")

                    collection.update_one(
                        {"childDetails.orderId": details['orderId']},  
                        {"$set": {"childDetails.$.isChecked": True}}  
                    )
                    logger.info(f"{details['name']} isChecked updated to True")
                    
                except Exception as e:
                    logger.error(f"Error processing {details['name']}: {e}")
                    
            client.close()  
            
        except Exception as e:
            logger.error(f"Main Bot Error: {e}")
        
        time.sleep(3600)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    babyReport(data['dob'], data['location'], data['lat'], data['lon'], os.path.dirname(os.path.abspath(__file__)), data['gender'], data['name'], "5.30", data['input'])
    logger.info("Report generated")
    return jsonify({"message": "Success"}), 200

@app.route('/freeReport', methods=['POST'])
def freeReportApi():
    data = request.json
    planets = freeReport(data['dob'], data['location'], data['lat'], data['lon'], app.root_path, data['gender'], data['name'], "5.30")
    return jsonify(planets), 200

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(AstrokidsBot, 'interval', hours=1)  
    scheduler.start()
    logger.info("Scheduler started!")
    logger.info("Bot process started!")
    
    logger.info("Flask app starting...")
    app.run(debug=True)
    logger.info("Flask app started!")
    