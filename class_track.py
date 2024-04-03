from web3 import *
import time,os,sys
import requests,json
import telegram,asyncio
from telegram.constants import ParseMode
from decoder import Decoder
import address
from uniswap_universal_router_decoder import RouterCodec,FunctionRecipient
from address import ANSEM_WALLET,ROOKIE_WALLET


connect = Web3(Web3.HTTPProvider('https://rpc.ankr.com/base/372f35cacf52b2f1c9074e5190128df78644842d00e5fc4fa354cc12ee7befa4'))
PROCESS_ROUTE = connect.eth.contract(address=connect.to_checksum_address(address.PROCESS_ROUTE),abi=address.PROCESS_ROUTE_ABI)
class Base:

    def __init__(self) -> None:
        self.BASE_KEY = 'FTPKIZK6ARN7C5SNSTD49EXK4EK6EK972G'
        self.influencerWallets = [connect.to_checksum_address(ANSEM_WALLET),connect.to_checksum_address(ROOKIE_WALLET)]
        self.ANSEM_HASHES = []
        self.ANSEM_RECENT_HASH = []
        self.ROOKIE_HASHES = []
        self.ROOKIE_RECENT_HASH = []

    def transaction(self,wallet):
        tracking_url = f'https://api.basescan.org/api?module=account&action=txlist&address={wallet}&sort=desc&apikey={self.BASE_KEY}'
        response = requests.get(tracking_url)
        data = json.loads(response.text)
        transactions = data.get('result',[])
        return transactions
    

    def hash_fetcher(self):
        ANSEM_HASHES = []
        ROOKIE_HASHES = []
        for wallet in self.influencerWallets:
            if wallet == connect.to_checksum_address(ANSEM_WALLET):
                transactions = self.transaction(wallet)
                for transaction in transactions:
                    ANSEM_HASHES.append(transaction['hash'])
            else:
                transactions = self.transaction(wallet)
                for transaction in transactions:
                    ROOKIE_HASHES.append(transaction['hash'])
        self.ANSEM_HASHES = ANSEM_HASHES
        self.ROOKIE_HASHES = ROOKIE_HASHES
        return 'DONE'

    def monitor_transaction(self):
        ANSEM_INPUT = []
        ROOKIE_INPUT = []
        for wallet in self.influencerWallets:
            if wallet == connect.to_checksum_address(ANSEM_WALLET):
                transactions = self.transaction(wallet)
                for transaction in transactions:
                    if transaction['hash'] not in self.ANSEM_HASHES and connect.to_checksum_address(transaction['from']) == connect.to_checksum_address(ANSEM_WALLET) :
                        ANSEM_INPUT.append(transaction['input'])
                        self.ANSEM_HASHES.append(transaction['hash'])
                    else:
                        self.ANSEM_HASHES.append(transaction['hash'])
            elif wallet == connect.to_checksum_address(ROOKIE_WALLET):
                transactions = self.transaction(wallet)
                for transaction in transactions:
                    if transaction['hash'] not in self.ROOKIE_HASHES and connect.to_checksum_address(transaction['from']) == connect.to_checksum_address(ROOKIE_WALLET):
                        ROOKIE_INPUT.append(transaction['input'])
                        self.ROOKIE_HASHES.append(transaction['hash'])
                    else:
                        self.ROOKIE_HASHES.append(transaction['hash'])
        return ANSEM_INPUT,ROOKIE_INPUT

    def process_Route(self,input_data):
        transaction_detail = PROCESS_ROUTE.decode_function_input(input_data)[1]
        amount_in = transaction_detail['amountIn']
        amount_out = transaction_detail['amountOutMin']
        swap_in_token = transaction_detail['tokenIn']
        swap_out_token = transaction_detail['tokenOut']
        return amount_in,amount_out,swap_in_token,swap_out_token
        
    def Input_Decoder(self,input_data):
        processor = Decoder()
        try:
            amount_in,amount_out,swap_in_token,swap_out_token = processor.process_trade(input_data)
            return amount_in,amount_out,swap_in_token,swap_out_token
        except:
            amount_in,amount_out,swap_in_token,swap_out_token = self.process_Route(input_data)
            return amount_in,amount_out,swap_in_token,swap_out_token

    
                
    def Alert(self,name,token,amount_out):
        if name == 'ANSEM':
            wallet = ANSEM_WALLET
        else:
            wallet = ROOKIE_WALLET
        tokenContract = connect.eth.contract(address=token,abi=address.BASIC_TOKEN_ABI)
        symbol = tokenContract.functions.symbol().call()
        amount_out = amount_out/10**tokenContract.functions.decimals().call()
        bot_token = '7077989634:AAESHM9LpnMjJv6j8XDQKFt24d2gcrng6m8'
        tradeInfo = f'INFLUENCER NOTIFICATION  \n\n'\
                    f'NAME: {name}\n\n'\
                    f'{name} WALLET: {wallet}\n\n'\
                    f'AMOUNT_BOUGHT: {amount_out}\n\n'\
                    f'TOKEN {symbol}: {tokenContract.address}\n\n'
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=tradeInfo,parse_mode=ParseMode.HTML,chat_id=963648721)
        if __name__!='__main__':
            asyncio.run(main())

    
    def off_chain(self):
        bot_token = '6344573464:AAF_dIkl-hJ5aFT_f0IbUMCmwtOhIm41tvc'
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=f'INFLUENCERS ARE OFFCHAIN \n\nBOT_STATUS:ACTIVE',
                chat_id=963648721)
        if __name__!='__main__':
            asyncio.run(main())

