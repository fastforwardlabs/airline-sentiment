import umap
import pickle
import joblib
import random
import string
import warnings
warnings.simplefilter('ignore')

import numpy as np
#import holoviews as hv
import pandas as pd

#hv.extension('bokeh')
data_dir = '/home/cdsw/airline-sentiment/data/'
model_dir = '/home/cdsw/airline-sentiment/model/'

with open(data_dir+'../../frontend_data', 'rb') as f:
    data = pickle.load(f)

data.keys()

len(data['prediction'])

data_df = pd.DataFrame(data)
data_df.head()

#data_df.airline.value_counts()

np.shape(data['embedding'][0])

X = np.vstack(data_df['embedding'].values)

np.shape(X)

#get_ipython().run_cell_magic('time', '', "\nembedding = umap.UMAP(n_components=2,\n                      n_neighbors=15,\n                      min_dist=0.1,\n                      metric='cosine').fit_transform(X)")

embedding = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric='cosine').fit_transform(X)

data_df['umap_x'], data_df['umap_y'] = embedding[:, 0], embedding[:, 1]

#get_ipython().run_cell_magic('opts', "Scatter [width=500 height=500] (color='prediction')", 
#                             "hv.Scatter(data_df, kdims=['umap_x', 'umap_y'], vdims=['prediction'])")

#hv.Scatter(data_df, kdims=['umap_x', 'umap_y'], vdims=['prediction'])

#data_df['tweet'] = [''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
#                    for i in range(0, len(data_df))]

data_df.head()

data_df['tweet'] = data_df['tweet'].apply(lambda t: " ".join(t))

joblib.dump(data_df, data_dir+'/umap_embedding.joblib', compress=True)
