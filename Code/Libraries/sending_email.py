import smtplib, ssl
import os
from dotenv import load_dotenv
import pandas as pd

from misc import string_to_list_end_dateTime

load_dotenv()

def email_out(message,MailingList):
    if (len(MailingList) != 0):
        port = 465  # For SSL
        sender_email = "fivetradetiger@gmail.com"
        password = os.getenv("EMAIL_PASSWORD")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email,MailingList, message)
            print("Email(s) sent!")

def new_trade_email(new_trade_event):
    sub_df = pd.read_csv("sub.csv")
    MailingList = sub_df[sub_df["trade_id"]== new_trade_event[0]['args']['TraderId']]["email_address"]
    price_time = string_to_list_end_dateTime(new_trade_event[0]['args']['inputEntryPriceEntryTime'])
    options_data = string_to_list_end_dateTime(new_trade_event[0]['args']['optionsData'])
    message = f"""Subject: Your new open trade

                Your subscribed trader, {new_trade_event[0]['args']['TraderId']}, made the following trade at {price_time[1]} today:
                Open {new_trade_event[0]['args']['inputSize']} share(s) of {new_trade_event[0]['args']['inputSymbol']} at price ${price_time[0]}
                Options data as follows:
                    Strike: {options_data[0]}
                    Option: {options_data[1]}
                    Expiration Time Stamp: {options_data[2]}
                """
    email_out(message,MailingList)

def new_close_trade_email(new_close_trade_event):
    sub_df = pd.read_csv("sub.csv")
    MailingList = sub_df[sub_df["trade_id"]== new_close_trade_event[0]['args']['TraderId']]["email_address"]
    message = f"""Subject: Your next close trade

                Your subscribed trader, {new_close_trade_event[0]['args']['TraderId']}, closed the following trade:
                Close {new_close_trade_event[0]['args']['tradeNum']} at price ${new_close_trade_event[0]['args']['exitPriceExitTime']}.
                """
    email_out(message, MailingList)