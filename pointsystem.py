#idea : spend money > earn points > use the points for discounts later as an added benefit
#core idea without any aditional add ons like maybe point expiration etc, soley on conversion and value

#initial user stats 

class User:
    def __init__(self, username):
        #Create a user with a name, 0 points, [empty wishlist]?
        self.username = username
        #start w 0 pts 
        self.points = 0
        

# when user buys item
    def buy_item(self, item_price: float):
        # $1 = 1 point
        points_earned = int(item_price) 
        #adding points to initial state when purchase is made
        self.points += points_earned
        print(f"You earned {points_earned} points! (${item_price:.2f} spent). Total: {self.points} pts")

#point conversion
    def redeem_discount(self) -> float:
        #Convert points to discount, returns discount amount
        if self.points < 100:
            print(f"You need at least 100 points. You have {self.points}.")
            return 0.0
        #amass total of $100 spent for 1 unit of discount = $5 (100 points is the min for 1 discount unit = $5)
        discount_units = self.points // 100  
        #total discount $$ = discount units * $5
        discount = discount_units * 5   
        #keep leftover points     
        self.points %= 100                  
        
        print(f"Redeemed {discount_units * 100} pts → ${discount:.2f} off. Remaining: {self.points} pts")
        return discount

    
#test
user = User("Alex")

#buy items and Earn points
 #earns 120 points (120/100 = 1 full discount unit)
user.buy_item(120.00) 
 #earns 30 points = Total: 150 points
user.buy_item(30.50)  

#redeem discounts
discount = user.redeem_discount()  
#output: "Redeemed 100 pts = $5.00 off. Remaining: 50 pts"

