import requests
import datetime as dt

BOVESPA_API_KEY = 1234 #placeholder
INT_EXCHANGE_API_KEY = 1234 #placeholder
CURRENCY_API_KEY = 1234 #placeholder

class data_gathering:

    def __init__(self,currency,int_exchange,
                 bovespa):
        #these are the endpoints from which we request information

        self.currency = currency
        self.int_exchange = int_exchange
        self.bovespa = bovespa

    def get_data(self,company_name):
        #We first try to find the stock on bovespa. If we can't find, we search in international stock markets or crypto.

        endpoint = self.bovespa.format_endpoint(company_name)
        response = requests.get(endpoint).json()
        not_found = response['results'][company_name].get('error')
        if not_found:
            endpoint = self.int_exchange.format_endpoint(company_name)
            response = requests.get(endpoint).json()
            if not response:
                return 'We could not find the tag you inserted :(.'
            else:
                parsed_response = self.int_exchange.parse_response(response)
        else:
            parsed_response = self.bovespa.parse_response(response,
                                                          company_name)
        return parsed_response

    def convert_currency(self,desired_currency,parsed_response):
        #Conversion to the wanted currency.

        actual_currency = parsed_response['currency']
        endpoint = self.currency.format_endpoint(desired_currency,actual_currency)
        response = requests.get(endpoint).json()
        if response:
            currency_conversion = list(response.values())[0]
        else:
            return parsed_response
        parsed_response['price'] = (parsed_response['price'] * 
                                    currency_conversion
                                   )
        
        parsed_response['currency'] = desired_currency

        return parsed_response



class bovespa:

    def __init__(self):
        self.__key = BOVESPA_API_KEY

    def parse_response(self,response,
                       company_name):
        
        #Parse the returned json to a default  determined json.
        result = response['results'][company_name]
        parsed_response = {
            'name': result['company_name'],
            'price' : 'BRL',
            'exchange' : 'Bovespa',
            'currency' : result['currency'],
            'daily_price_fluctuation' : result['change_percent'],
            'last_update' : result['updated_at'],
            'error_message': ''
            #[11:],
        }
        return parsed_response

    def format_endpoint(self,company_name):
        #Inserts the API Key and the Company Name into a URL to make a request correctly.
        endpoint = f'https://api.hgbrasil.com/finance/stock_price?key={self.__key}&symbol={company_name}'
        return endpoint

    

class international_exchange:

    def __init__(self):
        self.__key = INT_EXCHANGE_API_KEY

    def parse_response(self,response):
        result = response[0]
        #now = dt.datetime.now() - dt.timedelta(hours=3)
        now = dt.datetime.now()
        now = now.strftime("%H:%M:%S")
        parsed_response = {
            'name': result['name'],
            'currency' : 'USD',
            'price' : result['price'],
            'exchange' : result['exchange'],
            'daily_price_fluctuation' : result['changesPercentage'],
            'last_update' : now,
            'error_message': ''
        }
        return parsed_response

    def format_endpoint(self,company_name):
        endpoint = f'https://financialmodelingprep.com/api/v3/quote/{company_name}?apikey={self.__key}'
        return endpoint

class currency_price:

    def __init__(self):
        self.__key = CURRENCY_API_KEY

    def format_endpoint(self,currency_to_convert,
                        actual_currency):
        endpoint = f'https://free.currconv.com/api/v7/convert?q={actual_currency}_{currency_to_convert}&compact=ultra&apiKey={self.__key}'
        return endpoint

def parse_entry(message):
    commands = message.split()
    stock = commands[0]
    desired_currency = commands[1]

    return stock,desired_currency

def response_placeholder(stock_name):
    response_placeholder = {
        'name': stock_name,
        'currency': '-',
        'price': '-',
        'exchange': '-',
        'daily_price_fluctuation': '-',
        'last_update': '-',
        'error_message': ','
    }
    
    return response_placeholder

def obtain_values(stock_name,desired_currency=None):
    parsed_data = response_placeholder(stock_name)
    try:
        try:
            parsed_data = data_gatherer.get_data(stock_name)
        except Exception as e:
            message = "Não foi possível encontrar esse ativo na nossa base de dados :( ."
            parsed_data['error_message'] = message
            return parsed_data  
        try:
            if desired_currency == parsed_data['currency'] or not desired_currency:
                pass
            else:
                found_currency = data_gatherer.convert_currency(desired_currency,parsed_data)
                if found_currency:
                    parsed_data = found_currency
        except Exception as e:
            message = "Não foi possível encontrar a moeda selecionada. :("
            parsed_data['error_message'] = message
            return parsed_data
    except Exception as e:
        message = "Ocorreu alguma falha no código. Erro : " + str(e) + "."
        parsed_data['error_message'] = message
        return parsed_data
    return parsed_data

currency_api = currency_price()
int_exchange_api = international_exchange()
bovespa_api = bovespa()
data_gatherer = data_gathering(currency_api,int_exchange_api,
                                bovespa_api)

