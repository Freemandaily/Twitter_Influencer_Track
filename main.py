# This script monitors the influencer ANSEM AND ROOKIE WALLET ADRESS ON BASE

from web3 import *
def main():
    import time,os,sys
    import requests,json
    from class_track import Base

    processor = Base()
    DONE = processor.hash_fetcher()
    offchain = 0
    while True:
        print('Monitoring Influencers transaction')
        ANSEM_INPUT,ROOKIE_INPUT = processor.monitor_transaction()
        if bool(ANSEM_INPUT) or bool(ROOKIE_INPUT):
            
        
            for input_data in ANSEM_INPUT:
                try:
                    amount_in,amount_out,swap_in_token,swap_out_token = processor.Input_Decoder(input_data)
                    name = 'ANSEM'
                    print(f'From Ansem {swap_out_token}')
                    offchain = 0
                    processor.Alert(name,swap_out_token,amount_out)
                except Exception as e:
                    pass
                    #print(f'The issue is from ANSEM is {e}')
            for input_data in ROOKIE_INPUT:
                try:
                    amount_in,amount_out,swap_in_token,swap_out_token = processor.Input_Decoder(input_data)
                    name = 'ROOKIE'
                    print(f'From rookie {swap_out_token}')
                    offchain = 0
                    processor.Alert(name,swap_out_token,amount_out)
                except Exception as e:
                    pass
                    #print(f'The issue from Rookie is {e} ')
        else:
            offchain += 1
            if offchain == 500:
                processor.off_chain()
        time.sleep(5)
        
 
if __name__ == "__main__":
    No_error = True
    while No_error:
        try:
            main()
        except Exception as e:
            print(f'The whole Program Crashed Because Of {e}')
            continue
            
           




