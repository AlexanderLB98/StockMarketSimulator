class Company():
    def __init__(self, share_price = 10, option_price = 10):
        self.name = None
        self.share_price = share_price
        self.option_price = option_price
        self.n_shares = 100
        
        
        self.share: Share = Share(name = self.name, price = share_price, quantity = self.n_shares)   
        self.option: Option = Option(name = self.name, price = option_price, expiration_date = None)   
        self.deuda = 0                                          # Deuda inicial de la empresa    
        
    
    
        