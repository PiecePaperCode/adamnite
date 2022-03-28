class DPOS:

    def _init_(self):
        self.witnesss_pool = []
        self.GenesisStake()

    def GenesisStake(self):
        genesis_key = hashing(initial_key)
        self.witness_pool[genesis_key] = 1

    def update(self, publicKey, votes_for):
        
