from uniswap_universal_router_decoder import RouterCodec
from web3 import *

uni_comman_value = ['0b08','080c','000c','0a080c','0a000c','0a00','0b00','0b0800','0a08','0a010c','0a090c','0b090c','0b080c','0b000c','Ob09','0a09']  #REFER TO command module for clear understanding of this commands
codec = RouterCodec()

class Decoder:
    def process_trade(self,input_data ):

        codec = RouterCodec()
        decoded_input = codec.decode.function_input(input_data)
        main_input = decoded_input[1]
        command = main_input['commands'].hex()
        #print(command)

        if command == uni_comman_value[0] or command == uni_comman_value[7] or command == uni_comman_value[11] or command == uni_comman_value[12] or command == uni_comman_value[14]:                       
            amount_in,amount_out,swap_in_contract_address,swap_out_contract_address = self.WRAP_ETH_AND_V2_SWAP_EXACT_IN_OUT(main_input)
            
            return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address
            
            

        elif command == uni_comman_value[1]:
            amount_in,amount_out,swap_in_contract_address,swap_out_contract_address = self.V2_SWAP_EXACT_IN_AND_UNWRAP_WETH(main_input)
            return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address
            
            
        elif command == uni_comman_value[2]:
            amount_in,amount_out,swap_in_contract_address,swap_out_contract_address = self.V3_SWAP_EXACT_IN_AND_UNWRAP_WETH(main_input)
            return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address
            
            
        elif command == uni_comman_value[3] or command == uni_comman_value[8] or command == uni_comman_value[10] or command == uni_comman_value[15]:
            amount_in,amount_out,swap_in_contract_address,swap_out_contract_address = self.PERMIT2_PERMIT_V2(main_input)
            return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address
            
            
        elif command == uni_comman_value[4] or command == uni_comman_value[5] or command == uni_comman_value[9]:
            amount_in,amount_out,swap_in_contract_address,swap_out_contract_address = self.PERMIT2_PERMIT_V3(main_input)
            return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address
            
            
        elif command == uni_comman_value[6] or command == uni_comman_value[13]:
            amount_in,amount_out,swap_in_contract_address,swap_out_contract_address = self.WRAP_ETH_AND_V3_SWAP_EXACT_IN_OUT(main_input)
            return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address


        
    def WRAP_ETH_AND_V2_SWAP_EXACT_IN_OUT(self,main_input):
        try:#0b08 for v2 buying
            input_swap_path = main_input['inputs'][1][1]['path']
            amount_in = main_input['inputs'][1][1]['amountIn']
            amount_out = main_input['inputs'][1][1]['amountOutMin']
            swap_in_contract_address = input_swap_path [0]
            swap_out_contract_address = input_swap_path [-1]
        except: #0b090c
            amount_in = main_input['inputs'][1][1]["amountInMax"]
            amount_out = main_input['inputs'][1][1]['amountOut']
            swap_in_contract_address = input_swap_path [0]
            swap_out_contract_address = input_swap_path [-1]
        
        return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address



    def WRAP_ETH_AND_V3_SWAP_EXACT_IN_OUT(self,main_input):
        input_swap_path = main_input['inputs'][1][1]['path']
        fun_name = 'V3_SWAP_EXACT_IN'
        decoded_swap_path = codec.decode.v3_path(fun_name,input_swap_path)
        #print(decoded_swap_path)
        try:
            amount_in = main_input['inputs'][1][1]['amountIn']
            amount_out = main_input['inputs'][1][1]['amountOutMin']
            swap_in_contract_address = decoded_swap_path [0]
            swap_out_contract_address = decoded_swap_path [-1]
        except:
            amount_in = main_input['inputs'][1][1]["amountInMax"]
            amount_out = main_input['inputs'][1][1]['amountOut']
            swap_in_contract_address = decoded_swap_path [-1]
            swap_out_contract_address = decoded_swap_path [0]
        return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address


    def V2_SWAP_EXACT_IN_AND_UNWRAP_WETH(self,main_input):
        input_swap_path =main_input['inputs'][0][1]['path']
        amount_in = main_input['inputs'][0][1]['amountIn']
        amount_out = main_input['inputs'][0][1]['amountOutMin']
        swap_in_contract_address = input_swap_path [0]
        swap_out_contract_address = input_swap_path [-1]
        return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address

    def V3_SWAP_EXACT_IN_AND_UNWRAP_WETH(main_input):
        input_swap_path =main_input['inputs'][0][1]['path']
        fun_name = 'V3_SWAP_EXACT_IN'
        decoded_swap_path = codec.decode.v3_path(fun_name,input_swap_path)
        amount_in = main_input['inputs'][0][1]['amountIn']
        amount_out = main_input['inputs'][0][1]['amountOutMin']
        swap_in_contract_address = decoded_swap_path [0]
        swap_out_contract_address = decoded_swap_path [-1]
        return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address

    def PERMIT2_PERMIT_V2(self,main_input):
        input_swap_path =main_input['inputs'][1][1]['path']
        try:
            amount_in = main_input['inputs'][1][1]["amountIn"]
            amount_out = main_input['inputs'][1][1]['amountOutMin']
            swap_in_contract_address = input_swap_path [0]
            swap_out_contract_address = input_swap_path [-1]
        except:
            amount_in = main_input['inputs'][1][1]["amountInMax"]
            amount_out = main_input['inputs'][1][1]['amountOut']
            swap_in_contract_address = input_swap_path [-1]
            swap_out_contract_address = input_swap_path [0]

        return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address

    def PERMIT2_PERMIT_V3(self,main_input):
        input_swap_path =main_input['inputs'][1][1]['path']
        fun_name = 'V3_SWAP_EXACT_IN'
        decoded_swap_path = codec.decode.v3_path(fun_name,input_swap_path)
        try:
            amount_in = main_input['inputs'][1][1]["amountIn"]
            amount_out = main_input['inputs'][1][1]['amountOutMin']
            swap_in_contract_address = decoded_swap_path [0]
            swap_out_contract_address = decoded_swap_path [-1]
        except:
            amount_in = main_input['inputs'][1][1]["amountInMax"]
            amount_out = main_input['inputs'][1][1]['amountOut']
            swap_in_contract_address = decoded_swap_path [-1]
            swap_out_contract_address = decoded_swap_path [0]
        
        return amount_in,amount_out,swap_in_contract_address,swap_out_contract_address