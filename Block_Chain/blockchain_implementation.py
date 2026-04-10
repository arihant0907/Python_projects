import hashlib
import json
# block chian implementaion 
# tutorial link: https://drlee.io/building-your-own-blockchain-in-python-a-step-by-step-guide-ec10ea6c976d

class Block:
    def __init__(self,index,timestamp,data,prior_hash=''):
        self.index=index
        self.timestamp=timestamp
        self.data=data
        self.prior_hash=prior_hash
        self.nonce=0    # # Initialize nonce to zero before creating the hash
        self.curr_hash=self.create_hash()

    def create_hash(self):
        block_string=f"{self.index} {self.timestamp} {self.data} {self.prior_hash} {self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # Loop until the hash begins with the required number of zeros
        while self.curr_hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.curr_hash = self.create_hash()
            print('Block Hash: ' + self.curr_hash)  # Optional: Print each hash attempt


class MyBlockChain:
    def __init__(self):
        self.chain=[self.create_genesis_block()]
        self.difficulty=4

    def create_genesis_block(self):
        return Block(0, '04/3/1977', 'BlockchainTrainingAlliance.com', '0')

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self,new_block):
        print(new_block)
        new_block.prior_hash=self.get_last_block().curr_hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    # this will validate the prior hash code of current block and current hash code previous block
    # hash code of current block and new calculated hash code of current block
    def is_bc_valid(self):
        for i in range(1, len(self.chain)):
            curr_block=self.chain[i]
            prev_block=self.chain[i-1]

            if curr_block.prior_hash !=prev_block.curr_hash:
                return False

            if curr_block.curr_hash != curr_block.create_hash():
                return False

        return True 


if __name__ =="__main__":
    my_block=MyBlockChain()
    my_block.add_block(Block(1, '04/5/1977', 'BlockchainTrainingAlliance.com'))
    my_block.add_block(Block(2, '04/16/1977', 'Blockchain.com'))
    print(json.dumps(my_block.chain, default=lambda o: o.__dict__, indent=4))
    # check your block chain valid or not 
    # print(f"The block chain is {my_block.is_bc_valid()}")
    # check with data tampering 
    # my_block.chain[1].data="hello arihant"
    # print(json.dumps(my_block.chain, default=lambda o: o.__dict__, indent=4))
    # check your block chain valid or not 
    # print(f"The block chain is {my_block.is_bc_valid()}")

