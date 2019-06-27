from IPython.display import HTML
from urllib.parse import urljoin

HTML("<a href='https://{}.{}'>Airline Sentinment</a>".format(os.environ['CDSW_ENGINE_ID'],os.environ['CDSW_DOMAIN']))

APP_URL = urljoin('https://'+os.environ['CDSW_ENGINE_ID']+'.'+os.environ['CDSW_DOMAIN'],'')

print(APP_URL)

!ipython3 app/dashboard.py