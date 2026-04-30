import copy
import json
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

with open('Modern.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

cards = []
for s in data:
    for c in data[s]['cards']:
        cards.append(c)

found = set()
maxp = 0
maxt = 0
counts = {}
minmv = {}
data = []
for c in cards:
    if 'name' not in c or c['name'] in found:
        continue
    found.add(c['name'])
    if ('text' not in c or not c['text']) and 'colors' in c and len(c['colors'])==2 and 'power' in c and 'toughness' in c and c['power'].isdigit() and c['toughness'].isdigit() and 'manaValue' in c:
        p = int(c['power'])
        t = int(c['toughness'])
        maxp = max(maxp,p)
        maxt = max(maxt,t)
        pt = (p,t)
        if pt not in counts:
            counts[pt]=0
        counts[pt]+=1
        mv = int(c['manaValue'])
        if pt not in minmv or mv < minmv[pt]:
            minmv[pt] = mv
        data.append((p,t,mv))

from collections import Counter
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# collapse duplicates
counts = Counter(data)

X = []
z = []
weights = []

for (x, y, val), w in counts.items():
    X.append([x, y])
    z.append(val)
    weights.append(w)

X = np.array(X)
z = np.array(z)
weights = np.array(weights)

# polynomial features
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# weighted regression
model = LinearRegression()
model.fit(X_poly, z, sample_weight=weights)

import numpy as np
import matplotlib.pyplot as plt

x_vals = np.linspace(min(X[:,0]), max(X[:,0]), 50)
y_vals = np.linspace(min(X[:,1]), max(X[:,1]), 50)

X_grid, Y_grid = np.meshgrid(x_vals, y_vals)
Z_grid = model.predict(poly.transform(
    np.c_[X_grid.ravel(), Y_grid.ravel()]
)).reshape(X_grid.shape)

plt.contourf(X_grid, Y_grid, Z_grid)
plt.scatter(X[:,0], X[:,1], c=z)
plt.colorbar()
plt.show()

exit(0)


for p in range(maxp+1):
    for t in range(maxt+1):
        pt = (p,t)
        if pt not in minmv:
            continue
        mv = minmv[pt]
        #if mv < 3:
        #    continue
        print(f"{p}/{t} for {mv-1}")
exit(0)

a = np.zeros((maxp+1, maxt+1))
for p,t in counts:
    a[p,t] = counts[(p,t)]

#plt.imshow(a, cmap='hot', interpolation='nearest')
#plt.show()



masked_data = np.ma.masked_where(a == 0, a)

# Copy an existing colormap and set the 'bad' color
cmap = copy.copy(plt.get_cmap("viridis"))
cmap.set_bad(color='white') # Or 'none' for transparency

plt.imshow(masked_data, cmap=cmap)
plt.colorbar()
plt.show()
