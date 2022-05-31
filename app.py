# Import Python Depenecnies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

# Create SQL engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create new Flask app instance
app = Flask(__name__)

# Create Flask routes
# Welcome route
@app.route('/')
# Welcome function
def welcome():
    return (
    '''
    Welcome to the Climate Analysis API!

    Available Routes:
    
    /api/v1.0/precipitation
    
    /api/v1.0/stations
    
    /api/v1.0/tobs
    
    /api/v1.0/temp/start/end
    ''')

# Precipitation route
@app.route("/api/v1.0/precipitation")
# Precipitation function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations route
@app.route("/api/v1.0/stations")
# Stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature route
@app.route("/api/v1.0/tobs")
# Monthly temperaature function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Start and End statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create stats function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
