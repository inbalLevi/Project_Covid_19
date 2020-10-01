from flask import Flask, request
import requests

app = Flask(__name__)

response = requests.get("https://disease.sh/v3/covid-19/historical?lastdays=31") # get API
json_data = response.json()

@app.route('/')
def hello():
   return 'Hello, World!'
 

@app.route('/status')
def status():
    if(response.status_code==200):
        return( {"status": "success"})
        
    else:
        return({"status": "fail"})
   
@app.route('/newCasesPeak', methods=["GET"])
def cases():
    country = request.args.get('country')
    return get_info(country, 'cases')


@app.route('/recoveredPeak', methods=["GET"])
def recovered():
   country = request.args.get('country')
   return get_info(country, 'recovered')


@app.route('/deathsPeak', methods=["GET"])
def deaths():
    country = request.args.get('country')
    return get_info(country, 'deaths')
    
@app.errorhandler(404) # error handling, in case user URL input isn't good
def page_not_found(e):
    return {}

def get_info(country, option):
    
    country = country.lower() # compare by lowercase just in case user's input is uppercase

    arr = list(filter(lambda x: (x['country'].lower()==country), json_data)) # find the country

    if(len(arr)): # if a specific country was found
        arr = arr[0]
    else:
        return {} # No such country
    
    final_data = [] # holds the rise of the data (cases/deaths/recovered) every day
    
    data_arr = list(arr['timeline'][option].values())
    for k in range(len(data_arr)-1):
        i = data_arr[k+1]-data_arr[k] # calculate the difference
        final_data.append(i) 
        
    
    maxData=(max(final_data)) # find the max value --> the biggest change
    
    index = final_data.index(maxData)
    m = list(arr['timeline'][option])
    dateOfMaxData = m[index+1] # find the date of maxData
    
    
    if option == 'cases':
        method = 'newCasesPeak'
    elif option == 'recovered':
        method = 'recoveredPeak'
    else:
        method = 'deathsPeak'
        
    return {"country": country, "method": method, "date": dateOfMaxData, "value": maxData}


if __name__ == "__main__":
    app.run()