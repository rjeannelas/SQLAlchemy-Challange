# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to Climate App API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )
#################################################
# Convert the query results from your precipitation analysis
# Return the JSON representation of your dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Input
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = (dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)).strftime("%Y-%m-%d")

    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()

    all_percip = []
    for date, prcp in precip_data:
        percip_dict = {}
        percip_dict["date"] = date
        percip_dict["prcp"] = prcp
        all_percip.append(percip_dict)
            
    return jsonify(all_percip)

#################################################
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Input
    stations = session.query(Station.station, Station.name).all()

    session.close()

    all_stations = []
    for station, name in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)
        
    return jsonify(all_stations) 
#################################################
# Query the observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Input
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count().desc()).\
        first()[0]

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)


    results = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= year_ago_date).all()

    session.close()

    active_station_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        active_station_tobs.append(tobs_dict)
     
    return jsonify(active_station_tobs)
        
#################################################
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    # Input
    results = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
        ).filter(Measurement.date > start).all()

    session.close()

    start_tobs = []
    for min, max, avg in results:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_tobs.append(start_dict)
                         
    return jsonify(start_tobs)

#################################################
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range
# For a specified start, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    # Input
    results = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
        ).filter(Measurement.date > start).\
        filter(Measurement.date < end).all()
    
    session.close()

    start_end_tobs = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["max"] = max
        start_end_dict["avg"] = avg
        start_end_tobs.append(start_end_dict)
                         
    return jsonify(start_end_tobs)

#################################################
if __name__ == '__main__':
    app.run(debug=True)

