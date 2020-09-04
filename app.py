from flask import Flask, jsonify, request

from fbprophet import Prophet
from datetime import datetime
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError


class Model:
    def __init__(self):
        self.data = None
        self.model = None
        self.current_ticker = None
        self.last_date_fetched = None
        self.last_prediction = None
        self.n_days = 0

    def fetch_data(self, ticker='GOOG', start='2015-06-08'):
        """

        :param ticker: name of endpoint ticker to fetch data from
        :param start: Starting date for ticker's training data
        :return:  data for given ticker
        """
        today = datetime.today().strftime('%Y-%m-%d')
        try:
            data = pdr.DataReader(ticker, data_source='yahoo', start=start, end=today)
            self.data = data.reset_index()
            self.current_ticker = ticker
            self.last_date_fetched = today
        except RemoteDataError:
            print('Error in ticker!')

    def fit_model(self):
        """

        :return: model fitted with data

        Currently, this beta model only uses closing price as input.
        """
        data = self.data[["Date", "Close"]]
        data = data.rename(columns={"Date": "ds", "Close": "y"})
        self.model = Prophet(daily_seasonality=True)  # the Prophet class (model)
        self.model.fit(data)  # fit the model using all data

    def get_forecast(self, ticker, n_days=30, date_start_for_data='2015-06-08'):
        """

        :param date_start_for_data: Starting date for ticker's training data
        :param ticker: name of endpoint ticker to fetch data from
        :param n_days: Number of future days to get prediction
        :return: dataframe containing the forecast
        """
        today = datetime.today().strftime(
                '%Y-%m-%d')
        if self.last_date_fetched != today or self.current_ticker != ticker or n_days > self.n_days:
            # Store in attributes last prediction, so we can reuse it.
            self.n_days = n_days
            self.fetch_data(ticker, date_start_for_data)
            self.fit_model()
            future = self.model.make_future_dataframe(periods=n_days)
            self.last_prediction = self.model.predict(future)

        prediction = self.last_prediction.set_index('ds')
        prediction = prediction[str(today):][1:n_days + 1]
        prediction = prediction[['yhat']].to_dict('index')
        prediction = {str(k): round(v['yhat'], 3) for k, v in prediction.items()}

        return jsonify(prediction)


# Creating flask instance
app = Flask(__name__)

# Creating model instance
model = Model()


@app.route('/api', methods=['POST'])
def hello_world():
    data = request.get_json(force=True)
    prediction = model.get_forecast(data['ticker'], n_days=int(data['n_days']))
    return prediction


if __name__ == '__main__':
    app.run()
