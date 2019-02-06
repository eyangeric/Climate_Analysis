#Designing a Flask API using Climate Data
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#from flask_sqlalchemy import SQLAlchemy

from flask import Flask, jsonify

#Set up Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create our session (link) from Python to the DB
# session = Session(engine)

#Set up Flask
app = Flask(__name__)

#Set up Flask routes
@app.route("/")
def Welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation data"""
    # Query all precipitation and dates data
    session = Session(engine)
    results = session.query(Measurement).all()

    # Create a dictionary from the row data and append to a list of all precipitation data (precip_data)
    precip_data = []
    for precip in results:
        precip_dict = {}
        precip_dict[precip.date] = precip.prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def stations_all():

    # Query for all stations
    session = Session(engine)
    results = session.query(Station.station).all()
    stations_list = []
    for result in results:
        stations_list.append(result)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tob_pastyear():
    #create list of temperatures in last year of dataset
    #the date was attained from previous analyses
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    temp_list = []
    for result in results:
        temp_list.append(result.tobs)
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
#do not put quotes around the date
#enter dates in the YYYY-MM_DD format
def Temps_fromStart(start=None):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    temp_stats = list(np.ravel(results))
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
#do not put quotes around the date
#enter dates in the YYYY-MM_DD format
def Temps_DateRange(start=None, end=None):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_stats2 = list(np.ravel(results))
    return jsonify(temp_stats2)

if __name__ == '__main__':
    app.run(debug=True)