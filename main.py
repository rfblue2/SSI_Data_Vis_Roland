from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read raw data
file = 'https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/uber-raw-data-apr14.csv'
dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')
raw = pd.read_csv(file, header=0, parse_dates=['Date/Time'], date_parser=dateparse)

np_data = np.array(raw)

hours = pd.DatetimeIndex(raw['Date/Time']).hour

# lats and lons by period of day
morning = np_data[[i for i in range(len(hours)) if hours[i] >= 6 and hours[i] < 13], 1:3]
afternoon = np_data[[i for i in range(len(hours)) if hours[i] >= 13 and hours[i] < 18], 1:3]
evening = np_data[[i for i in range(len(hours)) if hours[i] >= 18 and hours[i] < 21], 1:3]
night = np_data[[i for i in range(len(hours)) if hours[i] >= 21 or hours[i] < 6], 1:3]

print(morning)
print(afternoon)
print(evening)
print(night)

# lats = np_data[:,1]
# lons = np_data[:,2]

map = Basemap(llcrnrlon=-74.255735, llcrnrlat=40.496044, urcrnrlon=-73.700272, urcrnrlat=40.915256,
              resolution='h', projection='merc', lat_0=40.7, lon_0=-74.0)

map.drawmapboundary(fill_color='aqua', linewidth=0.1)
map.fillcontinents(color='coral', lake_color='aqua', zorder=0)
map.drawcoastlines()

# convert lat/lon to plot coors
x1, y1 = map(morning[:,1], morning[:,0])
x2, y2 = map(afternoon[:,1], afternoon[:,0])
x3, y3 = map(evening[:,1], evening[:,0])
x4, y4 = map(night[:,1], night[:,0])

# plot pixels
l4 = map.scatter(x4, y4, marker='o', color='b', s=0.2, alpha=0.1)
l3 = map.scatter(x3, y3, marker='o', color='g', s=0.2, alpha=0.075)
l1 = map.scatter(x1, y1, marker='o', color='r', s=0.2, alpha=0.05)
l2 = map.scatter(x2, y2, marker='o', color='y', s=0.2, alpha=0.025)

plt.legend([l1, l2, l3, l4], ['Morning', 'Afternoon', 'Evening', 'Night'])
plt.title('NYC Uber Pickups Apr 2014')
plt.show()