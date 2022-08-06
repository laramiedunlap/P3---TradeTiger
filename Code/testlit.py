import yfinance as yf
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def plot_chart(symbol, period, interval):
    df = yf.download(tickers=symbol, period=period, interval=interval)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high = df['High'],
                            low= df['Low'],
                            close = df['Close']              
                                    
                                        
                                        )])
    # fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

st.write("# Showing you a chart")

symbol  = st.text_input("enter a ticker symbol")

interval = st.selectbox("select a bar interval", ["1m","2m","5m","15m","30m","60m","90m","1d","1wk"])

period = st.selectbox("select a bar lookback period",options=["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"])

fig = plot_chart(symbol,period,interval)

st.plotly_chart(fig, use_container_width=False)




###### OPTIONS STUFF BELOW $$$$$4$$

import yfinance as yf
import datetime as dt
def options_chain(symbol):
    """Returns the entire option chain for a symbol to a dataframe"""
    
    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)

    # Get expiration Date
    options['expirationDate'] = pd.to_datetime(options['expirationDate'])
    options['dte'] = (options['expirationDate'] - dt.datetime.today()).dt.days / 365
    options['expirationDate'] = pd.DatetimeIndex(options['expirationDate']).date
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    # Calculate the midpoint of the bid-ask
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 
    
    # Drop unnecessary columns
    options = options.drop(columns = ['contractSize', 'currency', 'lastTradeDate'])

    return options

chain = options_chain(symbol)
expry_list = chain.groupby('expirationDate').count().index.to_list()
strike_list = chain.groupby('strike').count().index.to_list()

st.write("Options: \n")
expry = st.selectbox("Select Expiration:",expry_list)
strike = st.selectbox("Select Strike:",strike_list)
opt_type = st.radio("Select Type:",options = ("Put", "Call"))

def set_current_opt_price(expry,strike,opt_type):
    _slice = chain[chain['expirationDate'] == expry ]
    if opt_type == 'CALL':
            _slice = _slice[_slice['CALL']==True]
    else: 
        _slice = _slice[_slice['CALL']==False]
    
    _slice = _slice[_slice['strike']==strike]['mark'] #round(float(_slice[_slice['strike']==strike]['mark']),2)
    
    return float(_slice.values)

st.write(set_current_opt_price(expry,strike,opt_type))
# st.write(f"price = {set_current_opt_price(expry,strike,opt_type)}")