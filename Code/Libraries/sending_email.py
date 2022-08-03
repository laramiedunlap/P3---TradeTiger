import smtplib, ssl
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

sub_df = pd.read_csv("sub.csv")

def email_out(message,MailingList):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "fivetradetiger@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email,MailingList, message) 

def new_trade_email(new_trade_event):
    MailingList = sub_df[sub_df["TraderId"]== new_trade_event[0]['args']['TraderId']]["subscriber_email"]
    message = f"""Subject: Your new open trade

                Your subscribed trader, {new_trade_event[0]['args']['TraderId']}, made the following trade:
                Open {new_trade_event[0]['args']['inputSize']} share(s) of {new_trade_event[0]['args']['inputSymbol']} at price ${new_trade_event[0]['args']['inputEntryPriceEntryTime']}, stike is {new_trade_event[0]['args']['inputStrike']}, call is
                {new_trade_event[0]['args']['inputIsCall']}.
                
                """
    email_out(message,MailingList)

def new_close_trade_email(new_close_trade_event):
    MailingList = sub_df[sub_df["TraderId"]== new_close_trade_event[0]['args']['TraderId']]["subscriber_email"]
    message = f"""Subject: Your next close trade

                Your subscribed trader, {new_close_trade_event[0]['args']['TraderId']}, made the following trade:
                Close {new_close_trade_event[0]['args']['inputSize']} share(s) of {new_close_trade_event[0]['args']['inputSymbol']} at price ${new_close_trade_event[0]['args']['inputExitPriceExitTime']}, stike is {new_close_trade_event[0]['args']['inputStrike']}, call is
                {new_close_trade_event[0]['args']['inputIsCall']}.
                
                """
    email_out(message, MailingList)
