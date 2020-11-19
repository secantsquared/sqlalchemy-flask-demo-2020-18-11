from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///data/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)


@app.route('/')
def index():
    return {'msg': 'd'}


@app.route('/temps/<start>/<end>')
def calc_temps(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    return jsonify(session.query(func.min(Measurement.tobs),
                                 func.avg(Measurement.tobs),
                                 func.max(Measurement.tobs)).
                   filter(Measurement.date >= start).filter(
        Measurement.date <= end).all())


if __name__ == '__main__':
    app.run(debug=True)
