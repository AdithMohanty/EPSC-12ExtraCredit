from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import ephem
import os
from datetime import datetime, timezone
from threading import Thread
from geopy.geocoders import Nominatim

app = Flask(__name__)

def plot_sky(latitude, longitude, date_time):
    # Observer's location
    observer = ephem.Observer()
    observer.lat = np.deg2rad(latitude)
    observer.lon = np.deg2rad(longitude)
    observer.date = date_time

    # Define celestial objects
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)

    # Compute positions
    sun.compute(observer)
    moon.compute(observer)

    # Plotting the Sun
    plt.plot(np.rad2deg(sun.az), 90 - np.rad2deg(sun.alt), 'o', color='yellow', label='Sun')

    # Plotting the Moon
    plt.plot(np.rad2deg(moon.az), 90 - np.rad2deg(moon.alt), 'o', color='gray', label='Moon')

    # Plotting stars
    for i in range(1, 360, 30):  # 12 constellations
        plt.text(np.random.uniform(0, 360), np.random.uniform(0, 90), "*", fontsize=8)

    # Plot settings
    plt.title('Sky Visualization')
    plt.xlabel('Azimuth (degrees)')
    plt.ylabel('Altitude (degrees)')
    plt.xlim(0, 360)
    plt.ylim(0, 90)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    
    # Save the plot as an image file
    plot_file = os.path.join('static', 'sky_plot.png')
    plt.savefig(plot_file)
    plt.close()

def get_location(ip):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(ip)
    return location.latitude, location.longitude

@app.route('/')
def index():
    # Latitude and Longitude of user's current location
    latitude, longitude = get_location(request.headers.get('X-Forwarded-For', request.remote_addr))
    date_time = datetime.now(timezone.utc)
    
    # Plotting the sky in a separate thread
    Thread(target=plot_sky, args=(float(latitude), float(longitude), date_time)).start()
    
    return render_template('index.html', latitude=latitude, longitude=longitude, date_time=date_time)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
