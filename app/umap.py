import umap
import pickle
import joblib
import random
import string
import warnings
warnings.simplefilter('ignore')

import numpy as np
import holoviews as hv
import pandas as pd

#hv.extension('bokeh')

data_dir = '/home/cdsw/data/'

if os.path.exists('/home/cdsw/frontend_data'):
  frontend_file_path = '/home/cdsw/frontend_data' 
else:
  frontend_file_path = data_dir+'/frontend_data'

with open(frontend_file_path, 'rb') as f:
    data = pickle.load(f)

data.keys()

len(data['prediction'])

data_df = pd.DataFrame(data)
data_df.head()

np.shape(data['embedding'][0])

X = np.vstack(data_df['embedding'].values)

np.shape(X)

embedding = umap.UMAP(n_components=2, n_neighbors=25, min_dist=0.2, metric='cosine').fit_transform(X)

data_df['umap_x'], data_df['umap_y'] = embedding[:, 0], embedding[:, 1]

#hv.Scatter(data_df, kdims=['umap_x', 'umap_y'], vdims=['prediction'])

data_df.head()

data_df['tweet'] = data_df['tweet'].apply(lambda t: " ".join(t))

joblib.dump(data_df, data_dir+'/umap_embedding_2.joblib', compress=True)
