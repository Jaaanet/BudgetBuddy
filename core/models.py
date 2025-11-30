# %%
class Transaction:
    '''
    Transaction - used for both income and expenses
    '''
    def __init__(self, date, amount, category, description=""):
        #empty string as the description if nothing inputted (makes it optional)
        #date format must be YYYY-MM-DD
        self.date = date
        self.amount = float(amount)
        self.category = category
        self.description = description

    def to_dict(self):
        '''
        Converts transaction into a dictionary
        '''
        data = {"date": self.date, "amount": self.amount, "category": self.category, "description": self.description, "type": self.get_type()}
        return data

    @classmethod
    def from_dict(cls, data):
        '''
        uses the transaction dictionary, determines if it is income or an expense and returns the correct object
        '''
        tx_type = data.get("type", "transaction")
        if tx_type == "income":
            tx_cls = Income
        elif tx_type == "expense":
            tx_cls = Expense
        return tx_cls(date=data["date"], amount=data["amount"], category=data["category"], description=data.get("description", ""))

    def get_type(self):
        '''
        returns the type of transaction as a string (income or expense)
        '''
        return "transaction"

#inherits from Transaction
class Income(Transaction):
    def get_type(self):
        return "income"

#inherits from Transaction
class Expense(Transaction):
    def get_type(self):
        return "expense"

#class for User Profile:
class UserProfile:
    '''
    List of transactions for one user
    '''
    
    def __init__(self, name):
        self.name = name
        self.transactions = []
        
    def add_transactions(self, tx):
        '''
        add transaction to the user's profile
        '''
        self.transactions.append(tx)

    def list_transactions(self, month=None, year=None):
        '''
        Returns all transactions OR only transactions for the month and year the user picks
        '''
        if month is None or year is None:
            return list(self.transactions)

        date_start = f"{year:04d}-{month:02d}-"
        result = []
        for t in self.transactions:
            if t.date.startswith(date_start):
                result.append(t)
        return result

    def delete_transaction(self, tx):
        '''
        We want users to be able to delete transactions. 
        This searches for the transaction they want to delete and if found, it deletes the transaction.
        '''
        if tx in self.transactions:
            self.transactions.remove(tx)

    def to_dict(self):
        '''
        Converts the profile into a dictionary.
        '''
        data = {"name": self.name, "transactions": [t.to_dict() for t in self.transactions]}
        return data

    @classmethod
    def from_dict(cls, data):
        '''
        creates a user profile from a dictionary
        '''
        profile = cls(data["name"])
        for tx_data in data.get("transactions", []):
            tx = Transaction.from_dict(tx_data)
            profile.add_transaction(tx)
        return profile
    
        



# %%
