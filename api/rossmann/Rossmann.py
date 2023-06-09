import pickle
import inflection 
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta

def is_promo(row):
    if row['promo_interval'] == 0:
        return 0
    elif row['month_map'] in row['promo_interval'].split(','):
        return 1
    else:
        return 0

class Rossmann (object):
    
    def __init__(self):
        self.home_path = '/home/mayconr/repos/ComunidadeDS/dsproducao/rossmann_project/'
        
        self.competition_time_month_scaler  = pickle.load(open(self.home_path + 'parameter/competition_time_month_scaler.pkl', 'rb'))
        self.competition_distance_scaler    = pickle.load(open(self.home_path + 'parameter/competition_distance_scaler.pkl', 'rb'))
        self.promo_time_week_scaler         = pickle.load(open(self.home_path + 'parameter/promo_time_week_scaler.pkl', 'rb'))
        self.store_type_scaler              = pickle.load(open(self.home_path + 'parameter/store_type_scaler.pkl', 'rb'))
        self.year_scaler                    = pickle.load(open(self.home_path + 'parameter/year_scaler.pkl', 'rb'))
        
    
    def data_cleaning(self, df1):
     
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment', 'CompetitionDistance',
                    'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))

        #rename
        df1.columns = cols_new

        df1['date'] = pd.to_datetime(df1['date'])
        
        # competition_distance
        df1['competition_distance'].fillna(200000.0, inplace=True)

        # competition_open_since_month
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)

        # competition_open_since_year
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)

        # promo2_since_week
        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)

        # promo2_since_year
        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)

        # promo_interval
        df1['promo_interval'].fillna(0, inplace=True)


        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        df1['month_map'] = df1['date'].dt.month.map(month_map)
        df1['is_promo'] = df1.apply(is_promo, axis=1)

        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(int)
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(int)
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(int)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(int)
        
        return df1
    
    
    def feature_engineering(self, df2):
        #Year
        df2['year'] = df2['date'].dt.year

        #Month
        df2['month'] = df2['date'].dt.month

        #Day
        df2['day'] = df2['date'].dt.day

        #Week of Year
        df2['week_of_year'] = df2['date'].dt.isocalendar().week

        #Year week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')


        #competition since
        df2['competition_since'] = df2.apply(lambda x: datetime(year=x['competition_open_since_year'], month=x['competition_open_since_month'],day=1),axis=1)
        df2['competition_time_month'] = ((df2['date']-df2['competition_since'])/30).apply(lambda x: x.days).astype(int)

        #Promo since
        df2['promo_since'] = df2['promo2_since_year'].astype(str)+'-'+df2['promo2_since_week'].astype(str)
        df2['promo_since'] = df2['promo_since'].apply(lambda x: datetime.strptime(x+'-1','%Y-%W-%w')-timedelta(days=7))
        df2['promo_time_week'] = ((df2['date']-df2['promo_since'])/7).apply(lambda x: x.days).astype(int)

        #assortment
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x=='a' else 'extra' if x=='b' else 'extended')

        #state holiday
        df2['state_holiday'] = df2['state_holiday'].apply(lambda x: 'public_holiday' if x=='a' else 'easter_holiday' if x=='b' else 'christmas' if x == 'c' else 'regular_day')

        ## 3.1 Filtragem das linhas

        df2 = df2[df2['open'] != 0]
        ## 3.2 Seleção das colunas

        cols_drop = ['open', 'promo_interval', 'month_map']
        df2 = df2.drop(cols_drop, axis=1)
        
        return df2
    
    def data_preparation(self,df5):
    

        a = df5.select_dtypes(include=['int32', 'int64', 'float64'])

        df5['competition_distance']= self.competition_distance_scaler.fit_transform(a[['competition_distance']].values)

        df5['competition_time_month']=self.competition_time_month_scaler.fit_transform(a[['competition_time_month']].values)
        
        df5['promo_time_week']=self.promo_time_week_scaler.fit_transform(a[['promo_time_week']].values)

        df5['year']=self.year_scaler.fit_transform(a[['year']].values)


        #state holiday - onehotencoding
        df5 = pd.get_dummies(df5,prefix=['state_holiday'], columns=['state_holiday'],dtype=float)

        df5['store_type'] = self.store_type_scaler.fit_transform(df5['store_type'])


        #store_type  ordinal encoding
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map(assortment_dict)

        df5['month_sin'] = df5['month'].apply(lambda x: np.sin(x*(2*np.pi/12)))
        df5['month_cos'] = df5['month'].apply(lambda x: np.cos(x*(2*np.pi/12)))

        df5['day_sin'] = df5['day'].apply(lambda x: np.sin(x*(2*np.pi/30)))
        df5['day_cos'] = df5['day'].apply(lambda x: np.cos(x*(2*np.pi/30)))

        df5['week_of_year_sin'] = df5['week_of_year'].apply(lambda x: np.sin(x*(2*np.pi/52)))
        df5['week_of_year_cos'] = df5['week_of_year'].apply(lambda x: np.cos(x*(2*np.pi/52)))

        df5['day_of_week_sin'] = df5['day_of_week'].apply(lambda x: np.sin(x*(2*np.pi/7)))
        df5['day_of_week_cos'] = df5['day_of_week'].apply(lambda x: np.cos(x*(2*np.pi/7)))
        
        cols_selected = ['store','promo','store_type','assortment','competition_distance',
                         'competition_open_since_month','competition_open_since_year','promo2',
                         'promo2_since_week','promo2_since_year','competition_time_month',
                         'promo_time_week','month_sin','month_cos','day_sin','day_cos',
                         'day_of_week_sin','day_of_week_cos','week_of_year_cos','week_of_year_sin']

        
        return df5[cols_selected]
    
    def get_prediction(self, model, original_data, test_data):
        pred=model.predict(test_data)
        original_data['prediction'] = np.expm1(pred)
        return original_data.to_json(orient='records', date_format='iso')
    