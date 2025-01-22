from flask import Flask, request, jsonify  
import requests

# Create an instance of the Flask web application
app = Flask(__name__)

# Define the route for handling POST requests at the root endpoint ('/')
@app.route('/', methods=["POST"])
def index():
    # Get the JSON data sent by Dialogflow
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    # Call the function to fetch the conversion factor between the source and target currencies
    cf = fetch_conversion_factor(source_currency, target_currency)
    
    # Calculate the final converted amount by multiplying the input amount by the conversion factor
    final_amount = amount * cf
    final_amount = round(final_amount, 2)

    # Create the response message to be sent back to Dialogflow, including the conversion result
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }

    # Return the response as a JSON object to Dialogflow
    return jsonify(response)

# Define a function to fetch the conversion factor from the API
def fetch_conversion_factor(source, target):
    url = "https://api.currencyapi.com/v3/latest?apikey=cur_live_d9X5jttNcTw81w0SeCX2IRxZUi1fc1xg66SSiIDr&currencies={}&base_currency={}".format(target, source)

    # Send a GET request to the API to fetch the latest currency conversion rates
    response = requests.get(url)

    # Parse the response into a Python dictionary
    response = response.json()

    # Extract the conversion value for the target currency from the API response
    value = response["data"][target]["value"]

    # Return the conversion factor (the value for the target currency)
    return value

if __name__ == "__main__":
    app.run(debug=True)



#This code listens for POST requests from Dialogflow, processes the user query (currency conversion), calls an external API for the conversion rate, and sends back the conversion result as a response. The function fetch_conversion_factor() interacts with the currency API to fetch the latest conversion rates based on the provided currencies.