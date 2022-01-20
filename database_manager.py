import API
import fitbit

class DatabaseManager:
    def __init__(self):
        CLIENT_ID, CLIENT_SECRET = API.get_credentials()
        self.client = API.authorize_user(CLIENT_ID, CLIENT_SECRET)

    def query(self, query_type, data_type, date=None, end_date=None, period=None, regen_tokens=True):
        data = []
        try:
            if query_type == 'time_series':
                data = self.client.time_series(
                    'activities/'+data_type,
                    base_date=date,
                    end_date=end_date,
                    period=period)['activities-distance']
            if query_type == 'intraday':
                data = self.client.intraday_time_series(
                    resource='activities/'+data_type,
                    detail_level=period
                )
        except fitbit.exceptions.HTTPUnauthorized:
            if regen_tokens:
                print("tokens expired, regenerating")
                API.clear_tokens()
                self.__init__()
                return self.query(query_type, data_type, date, end_date, regen_tokens=False)
            else:
                raise Exception("Authorization error, could not query data")

        return data