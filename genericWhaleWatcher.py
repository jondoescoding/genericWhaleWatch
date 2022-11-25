# Imports
import os
import telegram
import json
from dotenv import load_dotenv
from etherscan import Etherscan
from datetime import datetime

"""
    whaleWatcher.py
    Given an address this script will pull the most recent ERC-20 token transactions and send them to a desired discord  
"""

# GLOBAL VARIABLES
load_dotenv()
#Interactions the ehtereum chain
eth = Etherscan(os.getenv('api_key'))
# Token for the telegram bot
TOKEN = os.getenv('token')
# The group ID for where messages will be sent from the BOT
CHATID = os.getenv('chat_id')

# FUNCTIONS
def send(msg, chat_id, token):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

# MAIN PROCESSING
# loads both variables to have the same information
def erc20TokenTx(userBeingTracked):
    newtransaction = transaction = eth.get_erc20_token_transfer_events_by_address(userBeingTracked,0,999999999, 'asc')[-1]

    while True:
    # updates the newtx variable to check if there is any new erc20 token txs 
        newtransaction = eth.get_erc20_token_transfer_events_by_address(userBeingTracked,0,999999999, 'asc')[-1]
 
    # a comparison between the newtx details against the oldtx details
        if newtransaction['hash'] == transaction['hash']:
            send("No New Tx", CHATID, TOKEN)
        else:
            telegramMsg = f"{newtransaction['from']} moved {int(newtransaction['value'])/10**int(newtransaction['tokenDecimal'])} {newtransaction['tokenName']} to {newtransaction['to']} on {datetime.utcfromtimestamp(int(newtransaction['timeStamp'])).strftime('%d-%m-%Y %H:%M:%S')}EST"
            send(telegramMsg, CHATID, TOKEN)

def normalTx(userBeingTracked):
    newtransaction = transaction = eth.get_normal_txs_by_address(userBeingTracked,0,999999999, 'asc')[-1]

    while True:
    # updates the newtx 
        newtransaction = eth.get_normal_txs_by_address(userBeingTracked,0,999999999, 'asc')[-1]

        if newtransaction == transaction:
            continue
        else:
            msg = f"{newtransaction['from']} moved {int(newtransaction['value'])/10**int(newtransaction['tokenDecimal'])} {newtransaction['tokenName']} to {newtransaction['to']} on {datetime.utcfromtimestamp(int(newtransaction['timeStamp'])).strftime('%d-%m-%Y %H:%M:%S')}EST"
            send(msg,TOKEN,CHATID)


if __name__=="__main__":
    # User that will be tracked
    #useraddress = input('Enter the address of the user you want to track: ')
    useraddress = ('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045')
    # 0x6c8ee01f1f8b62e987b3d18f6f28b22a0ada755f
    # 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 - vitalik
    erc20TokenTx(useraddress)
    #normalTx(useraddress)
