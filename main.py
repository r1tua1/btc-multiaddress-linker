import requests

class BlockAnalysis:
    def __init__(self):
        self.startAddress = input('[!] > Address to analyze: ')
        print()
        self.linked = [self.startAddress]
        self.linkdetails = {}
        self.processed = []
    
    def getLinked(self, address):
        r = requests.get(f'https://chain.so/api/v2/get_tx_spent/BTC/{address}')

        for tx in r.json()['data']['txs']:
            txr = requests.get(f'https://chain.so/api/v2/get_tx_inputs/BTC/{tx["txid"]}')
            for input in txr.json()['data']['inputs']:
                if input['address'] not in self.linked:
                    vr = requests.get(f'https://chain.so/api/v2/get_address_received/BTC/{input["address"]}')
                    self.linkdetails[input['address']] = {'linkedfrom': address, 'linkedtxid': tx['txid'], 'txidvalue': tx['value'], 'addressvalue': float(vr.json()['data']['confirmed_received_value']) + float(vr.json()['data']['unconfirmed_received_value'])}
                    self.linked.append(input['address'])
                    print(f'[+] > Address {input["address"]} linked with transaction {tx["txid"]} ({tx["value"]})')

        self.processed.append(address)
    
    def start(self):
        self.getLinked(self.startAddress)
        for address in self.linked:
            if address not in self.processed:
                self.getLinked(address)
        
        total = 0

        for address in self.linked[1:]:
            total += self.linkdetails[address]['addressvalue']
            print(f'\n[+] > {address} details')
            print(f'[|] > {address} was linked from {self.linkdetails[address]["linkedfrom"]}')
            print(f'[|] > Linked with TXID {self.linkdetails[address]["linkedtxid"]}')
            print(f'[|] > TXID value of {self.linkdetails[address]["txidvalue"]}')
        
        print(f'\n[+] This portfolio has recieved a total of {total} BTC')
        input()
            

if __name__ == '__main__':
    ba = BlockAnalysis()
    ba.start()
