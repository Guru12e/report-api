import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from finalBabyReport import babyReport
from freeReport import freeReport
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

plans = [
    "Starter Parenting",
    "Pro Parenting",
    "Ultimate Parenting",
    "Master Parenting",
]

def AstrokidsBot():
    logger.info("Bot is running...")
    try:
        with MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=30000) as client:
            logger.info("MongoDB client connected successfully")
            database = client["AstroKids"]
            collection = database["childDetails"]
            six_hours_ago = datetime.now() - timedelta(hours=6)
            
            pipeline = [
                {"$unwind": "$childDetails"},
                {"$match": {
                    "childDetails.addedAt": {"$lt": six_hours_ago}, 
                    "childDetails.isChecked": False  
                }},
                {"$project": {"childDetails": 1, "email": 1, "_id": 0}}
            ]
            
            childDetails = list(collection.aggregate(pipeline))
            logger.info(f"Found {len(childDetails)} child records")

            for child in childDetails:
                details = child["childDetails"]
                try:
                    logger.info(f"Before babyReport for {details['name']}")
                    babyReport(
                        f"{details['dob']} {details['time']}:00", 
                        details['place'], 
                        details['lat'], 
                        details['lon'], 
                        app.root_path, 
                        details['gender'], 
                        details['name'], 
                        "5.30", 
                        plans.index(details['plan']) + 1,
                        email=child['email'],
                    )

                    collection.find_one_and_update(
                        {"childDetails.orderId": details['orderId']},
                        {"$set": {"childDetails.$.isChecked": True}},
                        return_document=True
                    )
                    
                    logger.info(f"{details['name']} isChecked updated to True")
                
                except Exception as e:
                    logger.error(f"Error in loop for {details['name']}: {str(e)}", exc_info=True)
            
            logger.info("All records processed successfully")

        logger.info("MongoDB client connection closed automatically")

    except Exception as e:
        logger.error(f"Main Bot Error: {str(e)}", exc_info=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    babyReport(
        data['dob'], 
        data['location'], 
        data['lat'], 
        data['lon'], 
        os.path.dirname(os.path.abspath(__file__)), 
        data['gender'], 
        data['name'], 
        "5.30", 
        data['input']
    )
    logger.info("Report generated")
    return jsonify({"message": "Success"}), 200

@app.route('/freeReport', methods=['POST'])
def freeReportApi():
    data = request.json
    planets = freeReport(
        data['dob'], 
        data['location'], 
        data['lat'], 
        data['lon'], 
        app.root_path, 
        data['gender'], 
        data['name'], 
        "5.30"
    )
    return jsonify(planets), 200

scheduler = BackgroundScheduler()
scheduler_started = False  

def start_scheduler():
    global scheduler_started
    if not scheduler_started:
        try:
            scheduler.add_job(AstrokidsBot, 'interval', hours=2)  
            scheduler.start()
            logger.info("Scheduler started successfully!")
            scheduler_started = True
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")

start_scheduler()

if __name__ == '__main__':
    logger.info("Running in development mode")
    app.run(debug=True, host="0.0.0.0", port=5000)