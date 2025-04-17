import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)

def get_location_names():
    return __locations

def save_prediction_history(history):
    with open('./prediction_history.json', 'w') as f:
        json.dump(history, f)

def load_prediction_history():
    try:
        with open('prediction_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_saved_artifacts():
    print("Loading Saved Artifacts.... Starts")
    global __data_columns
    global __locations

    with open("./columns.json",'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    global __model
    with open("./house_prices_model.pickle",'rb') as f:
        __model = pickle.load(f)

    global prediction_history
    prediction_history = load_prediction_history()
    
    print("Loading Saved Artifacts.... Done")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000,3,3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # Other Location
    print(get_estimated_price('Fjipura',1000,2,2)) # Other Location
    # print(__model.feature_names_in_)
