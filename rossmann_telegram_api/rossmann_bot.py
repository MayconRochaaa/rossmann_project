import os
import json
import pandas as pd
import requests
from flask import Flask, request, Response

BASE_DIR = os.path.abspath('')
DATA_DIR = os.path.join(BASE_DIR,'data')

token ='6275503796:AAEXLG2SVq9x69nw3tLO9GwNByT_bUdjp1k'

#https://api.telegram.org/bot6275503796:AAEXLG2SVq9x69nw3tLO9GwNByT_bUdjp1k/getMe
#
#https://api.telegram.org/bot6275503796:AAEXLG2SVq9x69nw3tLO9GwNByT_bUdjp1k/getUpdates
#
#https://api.telegram.org/bot6275503796:AAEXLG2SVq9x69nw3tLO9GwNByT_bUdjp1k/sendMessage?chat_id=918693308&text=

#https://api.telegram.org/bot6275503796:AAEXLG2SVq9x69nw3tLO9GwNByT_bUdjp1k/setWebhook?url=https://53b4c1c1c1d7b3.lhr.life



def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot{}/'.format(token)
    url = url + 'sendMessage?chat_id={}'.format(chat_id) 
    r = requests.post(url, json={'text': text})
    
    print('Status Code {}'.format(r.status_code))
    
    return None

def load_dataset(store_id):
    df10 = pd.read_csv(os.path.join(DATA_DIR,'test.csv'))
    df_store_raw = pd.read_csv(os.path.join(DATA_DIR,'store.csv'))
    


    df_test = pd.merge(df10, df_store_raw, how= 'left', on= 'Store')

    df_test = df_test[df_test['Store']==store_id]
    
    if not df_test.empty:

        df_test = df_test[df_test['Open']!=0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop('Id', axis=1)

        data = json.dumps(df_test.to_dict(orient='records'))
        
    else:
        data='error'
    
    return data

def predict(data):
    
    url = 'https://rossmann-web-app.onrender.com/rossmann/predict'
    header = {'Content-type': 'application/json'} 
    data=data

    r = requests.post(url, data=data, headers=header)
    print('Status Code{}'.format(r.status_code))

    d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())
    
    return d1


def parse_message(message):
    
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    
    store_id = store_id.replace('/','')
    
    try:
        store_id = int(store_id)
        
    except ValueError:
        store_id = 'error'
    
    return chat_id, store_id

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        
        chat_id, store_id = parse_message(message)
        
        if store_id != 'error':
            data = load_dataset(store_id)
            
            if data != 'error':

                d1 = predict(data)
                
                d2 =d1[['store', 'prediction']].groupby('store').sum().reset_index()
                
                msg = 'Store number {} will sell ${:,.2f} in the next 6 weeks'.format(d2['store'].values[0], d2['prediction'].values[0])
                
                send_message(chat_id, msg)
                return Response('Ok', status=200)
                
            else:
                send_message(chat_id, 'Store not available')
                return Response('Ok', status=200)
            
        else:
            send_message(chat_id, 'Store ID is Wrong')
            return Response('Ok', status=200)
        
    else:
        return '<h1> Rossmann Telegram BOT </h1>'
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
