# Finance Models Testing with Flask

This repo is for experimenting different ML models and serving them with a rest API

## Setting up and run app

Get sure you have the following compilers and and Python development tools
```shell-script
sudo apt install gcc g++ build-essential python-dev python3-dev
```

Install libraries:
```shell-script
pip3 install -r requirements.txt
```

Run app:
This will expose a flask POST API at port ```5000```

```shell-script
python3 app.py
```

### Usage example

Currently, it just takes a POST request, using the parameters:

- ticker: Name of the ticker, for example: 'GOOG', 'AAPL'.
- n_days: Number of days you want to forecast, starting tomorrow.


### Work in progress

- Switch to a better accuracy model.
- Add support for more variables
- Add exception handling for code.

![example](https://res.cloudinary.com/victor1600/image/upload/v1599241819/markdown/ML/example_noqepc.png)
