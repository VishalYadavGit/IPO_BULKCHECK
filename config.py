import os
from dotenv import load_dotenv

load_dotenv()

KFINTECH = "https://ipostatus.kfintech.com/"

# coming soon 
Linkintime = "https://in.mpms.mufg.com/Initial_Offer/public-issues.html"

IPO_NAME = "MEESHO"
PAN_NUMBER = os.environ.get("PAN_NUMBERS","").split(",")