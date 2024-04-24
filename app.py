import numpy as np
import matplotlib.pyplot as plt
import ephem
from datetime import datetime, timedelta, timezone
import pytz

# Location of Campinile
latitude = 37.871873
longitude = -122.258347
tz = pytz.timezone('America/Los_Angeles')
start_date = datetime.now(tz)

def plot_sky(latitude, longitude, date_time):

    # Observer's location
    observer = ephem.Observer()
    observer.lat = np.deg2rad(latitude)
    observer.lon = np.deg2rad(longitude)
    observer.date = date_time

    # objects
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)

    # positions
    sun.compute(observer)
    moon.compute(observer)

    # Sun
    sun_azimuth = np.rad2deg(sun.az)
    sun_altitude = 90 - np.rad2deg(sun.alt)

    # Moon
    moon_azimuth = np.rad2deg(moon.az)
    moon_altitude = 90 - np.rad2deg(moon.alt)

    # Polar plot
    plt.subplot(121, projection='polar')
    plt.plot(np.deg2rad(sun_azimuth), sun_altitude, 'o', color='orange', label='Sun')
    plt.plot(np.deg2rad(moon_azimuth), moon_altitude, 'o', color='gray', label='Moon')
    plt.title('Polar Plot')
    plt.gca().set_theta_zero_location('N')
    plt.gca().set_theta_direction(-1)
    plt.grid(True)

    r = np.arange(0, 90, 0.01)
    directions = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270, 'NW': 315}
    for direction, angle in directions.items():
        plt.text(np.deg2rad(angle), 110, direction, horizontalalignment='center', fontsize=8)
        plt.plot([np.deg2rad(angle)] * len(r), r, color='black', alpha=0.3)
    plt.ylim(0, 90)

    # Rectangular plot
    plt.subplot(122)
    plt.plot(sun_azimuth, sun_altitude, 'o', color='orange', label='Sun')
    plt.plot(moon_azimuth, moon_altitude, 'o', color='gray', label='Moon')

    plt.title('Rectangular Plot')
    plt.xlabel('Azimuth (degrees)')
    plt.ylabel('Altitude (degrees)')
    plt.xlim(0, 360)
    plt.ylim(0, 90)
    plt.gca().invert_yaxis()
    plt.legend(loc='upper left')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# plots the sky in its current state
# plot_sky(latitude, longitude, datetime.now(timezone.utc))

def get_altandaz_camp(latitude, longitude, date_time):
    """
    gets the altitude and azmuth of 
    """
    observer = ephem.Observer()
    observer.lat = np.deg2rad(latitude)
    observer.lon = np.deg2rad(longitude)
    observer.date = date_time

    # Objects
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)

    # Positions
    sun.compute(observer)
    moon.compute(observer)

    # Sun
    sun_azimuth = np.rad2deg(sun.az)
    sun_altitude = 90 - np.rad2deg(sun.alt)

    # Moon
    moon_azimuth = np.rad2deg(moon.az)
    moon_altitude = 90 - np.rad2deg(moon.alt)

    return {'Moon': [moon_azimuth, moon_altitude], 'Sun': [sun_azimuth, sun_altitude]}

def plot_object_over_x_days(object, start_date, entries, period=5):
    """
    takes in four parameters
    - object: Which object to track (Sun/ Moon)
    - start_date: the start date and time 
    - entries: how many entries you want 
    - period: starts at 5 days is the amount of days in between each entry
    
    """
    plt.figure(figsize=(12, 6))

    # Polar
    plt.subplot(121, projection='polar')
    plt.title(f'{object} - Polar Plot')
    plt.gca().set_theta_zero_location('N')
    plt.gca().set_theta_direction(-1)
    plt.grid(True)

    # Compass
    r = np.arange(0, 90, 0.01)
    directions = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270, 'NW': 315}
    for direction, angle in directions.items():
        plt.text(np.deg2rad(angle), 110, direction, horizontalalignment='center', fontsize=8)
        plt.plot([np.deg2rad(angle)] * len(r), r, color='black', alpha=0.3)
    plt.ylim(0, 90)  # Set the maximum value on the radial axis
    plt.plot([np.deg2rad(244), np.deg2rad(244)], [0, 90], color='red', linestyle='--', alpha=0.5) # my line of view


    # Cartiesian
    plt.subplot(122)
    plt.title(f'{object} - Rectangular Plot')
    plt.xlabel('Azimuth (degrees)')
    plt.ylabel('Altitude (degrees)')
    plt.xlim(0, 360)
    plt.ylim(0, 90)
    plt.gca().invert_yaxis()
    if entries < 10:
        plt.legend(loc='upper left')
    plt.plot([244, 244], [0, 90], color='red', linestyle='--', alpha=0.5) # my line of view
    plt.grid(True)

    for i in range(entries):
        date_time = start_date + timedelta(days=i*period)
        altandaz = get_altandaz_camp(latitude, longitude, date_time)

        # plotting point in polar
        plt.subplot(121, projection='polar')
        plt.plot(np.deg2rad(altandaz[object][0]), altandaz[object][1], 'o', label=f'{object} - {date_time.strftime("%Y-%m-%d")}')

        # plotting point in cartiesian
        plt.subplot(122)
        plt.plot(altandaz[object][0], altandaz[object][1], 'o', label=f'{object} - {date_time.strftime("%Y-%m-%d")}')
        if entries < 10:
            plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()

# Adjust Start Date And Time
"""
start_date.replace(year=2024, month=2, day=1,hour=17, minute=30, second=0)
==> 2024/02/01 5:30 PM
"""
start_date = start_date.replace(year=2024, month=2, day=1,hour=17, minute=30, second=0)
print(start_date)

"""
plot_object_over_30_days('Sun', start_date, 10, 7)
Make 10 observations of the sun from start_date time every 7 days
"""

plot_object_over_x_days('Sun', start_date, 9, 10)
