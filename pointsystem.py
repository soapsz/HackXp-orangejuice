from datetime import datetime, timedelta
from typing import Dict, List

#idea : friendship points . $1 = 1 point
# friendship leaderboard = in pairs
# ranks update every month
# resets to  0 every 60 days


class User:
    def __init__(self, username):
        """Initialize a user with friendship tracking"""
        # Basic user info
        self.username = username
        
        # Point tracking (resets monthly)
        self.monthly_points = 0
        
        # Lifetime points (never resets)
        self.all_time_points = 0
        
        # Tracks points given to each friend
        # Format: {"friend_name": points}
        self.friendships: Dict[str, int] = {}
        
        # Tracks last gift date for each friend
        # Format: {"friend_name": last_gift_date}
        self.last_gifts: Dict[str, datetime] = {}
        
        # Tracks consecutive gifting streaks
        # Format: {"friend_name": streak_days}
        self.streaks: Dict[str, int] = {}

    def send_gift(self, friend: str, money_spent: float):
        """
        Record a gift using money spent (1$ = 1 friendship point)
        - friend: Recipient's name
        - money_spent: Amount spent in dollars
        """
        # Convert dollars to whole points
        points = int(money_spent)
        
        # Update point totals
        self.monthly_points += points
        self.all_time_points += points
        
        # Initialize friendship records if new
        if friend not in self.friendships:
            self.friendships[friend] = 0
            self.streaks[friend] = 0
            self.last_gifts[friend] = datetime.now()
            
        # Update friendship points
        self.friendships[friend] += points
        self.last_gifts[friend] = datetime.now()
        
        # Calculate streak (gifts within 24 hours count)
        days_since = (datetime.now() - self.last_gifts[friend]).days
        self.streaks[friend] = 1 if days_since > 1 else self.streaks[friend] + 1
        
        # Print transaction receipt
        print(f"💸 {self.username} spent ${money_spent} on {friend}")
        print(f"💝 Gained {points} friendship points (Current: {self.monthly_points})")
        
        # Shame cheap gifts
        if money_spent < 20:
            print(f"💔 PS: {friend} must feel unloved...")

    def _check_streak_penalty(self):
        """Apply point deductions for broken streaks (7+ days without gifting)"""
        for friend in list(self.streaks.keys()):
            if (datetime.now() - self.last_gifts[friend]).days > 7:
                # Deduct 10% of points from that friendship (min 50 pts)
                penalty = min(50, self.friendships[friend] // 10)
                self.friendships[friend] -= penalty
                self.monthly_points -= penalty
                print(f"⚠️ {self.username} lost {penalty} pts for neglecting {friend}!")
                self.streaks[friend] = 0  # Reset streak

class MonthlyLeaderboard:
    def __init__(self):
        """Initialize leaderboard with monthly tracking"""
        # Stores all users: {"username": User}
        self.users = {}
        
        # Track current leaderboard month
        self.current_month = datetime.now().month

    def add_user(self, user: User):
        """Register a new user to the leaderboard"""
        self.users[user.username] = user

    def _reset_monthly(self):
        """Reset monthly points if new month detected"""
        if datetime.now().month != self.current_month:
            print("\n💫 NEW MONTH - Leaderboard reset! 💫")
            
            # Process all users
            for user in self.users.values():
                # Apply streak penalties first
                user._check_streak_penalty()
                
                # Reset monthly totals
                user.monthly_points = 0
                
                # Reset individual friendship points
                for friend in user.friendships:
                    user.friendships[friend] = 0
            
            # Update tracking month
            self.current_month = datetime.now().month

    def show_leaderboard(self):
        """Display the monthly rankings with brutal honesty"""
        self._reset_monthly()
        
        # Sort users by monthly points (high to low)
        ranked_users = sorted(self.users.values(), 
                            key=lambda x: x.monthly_points, 
                            reverse=True)
        
        # Leaderboard header
        print("\n🏆 MONTHLY FRIENDSHIP RANKINGS 🏆")
        print(f"--- {datetime.now().strftime('%B %Y')} ---")
        
        # Special titles for top 3
        titles = {
            1: "👑 TRUE BESTIE",
            2: "💎 WORTHY FRIEND", 
            3: "🌟 ALMOST ACCEPTABLE"
        }
        
        # Display each user's status
        for i, user in enumerate(ranked_users, 1):
            # Get appropriate title
            title = titles.get(i, f"💩 #{i} 'FRIEND'")
            print(f"\n{title}: {user.username} - {user.monthly_points} pts")
            
            # Special message for losers
            if user.monthly_points == 0:
                print("   🚮 Who even likes them?")
            else:
                # Show best-treated friend
                top_friend = max(user.friendships.items(), key=lambda x: x[1])
                print(f"   💌 Best treatment: {top_friend[0]} (${top_friend[1]} spent)")
                
                # Shame neglected friends (spent < $50)
                if len(user.friendships) > 1:
                    weakest = min(user.friendships.items(), key=lambda x: x[1])
                    if weakest[1] < 50:
                        print(f"   💔 Neglecting: {weakest[0]} (only ${weakest[1]})")

# Example Usage
if __name__ == "__main__":
    # Initialize leaderboard
    leaderboard = MonthlyLeaderboard()
    
    # Create users
    generous_giver = User("Alex")
    average_friend = User("Jordan")
    cheap_friend = User("Charlie")
    
    # Register users
    leaderboard.add_user(generous_giver)
    leaderboard.add_user(average_friend)
    leaderboard.add_user(cheap_friend)
    
    # Simulate gift exchanges
    generous_giver.send_gift("Jordan", 150)  # Alex → Jordan ($150)
    average_friend.send_gift("Alex", 80)     # Jordan → Alex ($80)
    generous_giver.send_gift("Charlie", 10)  # Alex shames Charlie ($10)
    cheap_friend.send_gift("Alex", 5)        # Charlie tries (and fails)
    
    # Display the savage truth
    leaderboard.show_leaderboard()