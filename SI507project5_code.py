## import statements
import requests_oauthlib
import webbrowser
import json
import secretdata
from datetime import datetime

######################## CACHING SETUP ################
##### CATCHING CONSTANT-TIMING #####
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True
CACHE_FNAME = "cache_contents.json"

##### CATCHING CONSTANT-AUTHORIZATION #####
CLIENT_ID = secretdata.CLIENT_ID
CLIENT_SECRET= secretdata.client_secret
AUTHORIZATION_URL = 'https://www.eventbrite.com/oauth/authorize'
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
TOKEN_URL = 'https://www.eventbrite.com/oauth/token'
baseurl= "https://www.eventbriteapi.com/v3/events/search/?token=<token>"


oauth2inst = requests_oauthlib.OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
authorization_url, state = oauth2inst.authorization_url(AUTHORIZATION_URL)
webbrowser.open(authorization_url)
authorization_response = input('Authenticate and then enter the full callback URL: ').strip()
token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, client_secret=CLIENT_SECRET)
r = oauth2inst.get('https://www.eventbriteapi.com/v3/users/me/?token=SESXYS4X3FJ5LHZRWGKQ')
response_diction = json.loads(r.text)
#print(json.dumps(response_diction, indent=2))

###### LOAD CATCHING FILES #####
try:
    with open(CACHE_FNAME, 'r') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}

##### CACHING FUNCTIONS #####
#*** Helper Function
def params_unique_combination(baseurl, params_d, private_keys=["CLIENT_ID"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

#*** fucntion to get data from eventrbite using cathcing pattern/helperfunction
def get_event_data(searchterm):
    baseurl = "https://www.eventbriteapi.com/v3/events/search/?token=<token>"
    params_events = {}
    params_events['q']=searchterm
    params_events['include_all_series_instances']=True
    unique_ident = params_unique_combination(baseurl,params_events)
    #unique_ident = unique_ident.upper()
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        print(unique_ident)
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = oauth2inst.get(baseurl,params=params_events)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        print(unique_ident)
        return CACHE_DICTION[unique_ident]

#*** Fucntion to CHECK DATA IF EXPIRED'
def has_cache_expired(timestamp_str, expire_in_days):
    now = datetime.now()
    cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)
    delta = now - cache_timestamp
    delta_in_days = delta.days
    if delta_in_days > expire_in_days:
        return True
    else:
        return False

#*** Fucntion to CHECK IF DATA ALREADY EXISTED IN FILE AND HAS NOT EXPIRED'
def get_from_cache(identifier, dictionary):
    identifier = identifier.upper()
    if identifier in dictionary:
        data_assoc_dict = dictionary[identifier]
        if 'timestamp' in data_assoc_dict.keys():
            if has_cache_expired(data_assoc_dict['timestamp'],data_assoc_dict["expire_in_days"]):
                if DEBUG:
                    print("Cache has expired for {}".format(identifier))
                    # also remove old copy from cache
                    del dictionary[identifier]
                    data = None
                else:
                    data = dictionary[identifier]['values']
                    print ("Cache has not expired and evertyhing is okay")
        else:
            data = None
    else:
        data = None
        print("I do not know why the program cannot check whether data has expired")
    return data

#'Add identifier and its associated values to the data cache dictionary'
def set_in_data_cache(identifier, data, expire_in_days):
    identifier = identifier.upper()
    CACHE_DICTION[identifier] = {
        'values': data,
        'timestamp': datetime.now().strftime(DATETIME_FORMAT),
        'expire_in_days': expire_in_days
    }

    with open(CACHE_FNAME, 'w') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)
        cache_file.write(cache_json)

TEDx_events=get_event_data("TEDx")
Thanksgiving_events=get_event_data("Thanksgiving")








########################  ADDITIONAL CODE for program should go here...########################
## Perhaps authentication setup, functions to get and process data, a class definition... etc.
#baseurl_organizer="https://www.eventbriteapi.com/v3/:14173279292/?token=<token>"
#params_organierid="14173279292"
#TEDx_Organizer=oauth2inst.get(baseurl)
#print (TEDx_Organizer.text)

####### Get TEDx Events CSV files#######
param_TEDx={'q':"TEDx",'include_all_series_instances':"True"}
TEDx_IDENT=params_unique_combination(baseurl,param_TEDx)
#Capital_TEDx_IDENT=TEDx_IDENT.upper()
#print (Capital_TEDx_IDENT)
Check_TEDx_events=get_from_cache(TEDx_IDENT,CACHE_DICTION)
TEDxfile=open("TEDxinfo.CSV","w")
TEDxfile.write("Name,URL,Timezone,Start_time,organizer_id,venue_id,format_id\n")
for item in CACHE_DICTION[TEDx_IDENT]['events']:
    TEDX_name=item['name']['text']
    TEDX_URL=item['url']
    TEDx_Timezone=item['start']['timezone']
    TEDx_Starttime=item['start']['utc']
    TEDx_OrganizerID=item['organizer_id']
    TEDX_VenueID=item['venue_id']
    TEDx_FormatID=item['format_id']
    #TEDx_Organizer=oauth2inst.get(baseurl,params=params_events)
    #print (TEDx_Timezone)
    TEDxfile.write("{},{},{},{},{},{},{}\n".format(TEDX_name,TEDX_URL,TEDx_Timezone,TEDx_Starttime,TEDx_OrganizerID,TEDX_VenueID,TEDx_FormatID))
TEDxfile.close()

####### Get Thanksgiving Events CSV files#######
param_THXgiving={'q':"Thanksgiving",'include_all_series_instances':"True"}
THXgiving_IDENT=params_unique_combination(baseurl,param_THXgiving)
#Capital_THXgiving_IDENT=THXgiving_IDENT.upper()
#print (Capital_THXgiving_IDENT)
Check_Thanksgiving_events=get_from_cache(THXgiving_IDENT,CACHE_DICTION)
THXgivingfile=open("THXgivinginfo.CSV","w")
THXgivingfile.write("Event_Name,Event_URL,Timezone,Event_Start_time,Event_organizer_id,Venue_ID,Event_Format_id\n")
for elem in CACHE_DICTION[THXgiving_IDENT]['events']:
    THXgiving_name=elem['name']['text']
    THXgivingURL=elem['url']
    THXgiving_Timezone=elem['start']['timezone']
    THXgiving_Starttime=elem['start']['utc']
    THXgiving_OrganizerID=elem['organizer_id']
    THXgiving_VenueID=elem['venue_id']
    THXgiving_FormatID=item['format_id']
    #TEDx_Organizer=oauth2inst.get(baseurl,params=params_events)
    #print (TEDx_Timezone)
    THXgivingfile.write("{},{},{},{},{},{},{}\n".format(THXgiving_name,THXgivingURL,THXgiving_Timezone,THXgiving_Starttime,THXgiving_OrganizerID,THXgiving_VenueID,THXgiving_FormatID))
THXgivingfile.close()

print ("File have been created. It's the end  of The Program")
if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not REDIRECT_URI or not AUTHORIZATION_URL:
        print("You need to fill in this API's specific OAuth2 URLs in this file.")
        exit()
## Make sure to run your code and write CSV files by the end of the program.
