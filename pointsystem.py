
#idea : friendship points . $1 = 1 point
# friendship leaderboard = in pairs
# ranks update every month
# resets to  0 every 60 days
# this ranking is global; ranks via mutual investment

#SHAME SYSTEM:
# if you spend less than $20 for your friend, you will get shamed

# NEGLECT EXPOSURE:
# shows who top pairs ignore the most in their list
# special tags for "pathetic friendships" (<$20)

#IMBALANCE DETECTION
# will detect who spends more on who per pair 

from datetime import datetime
from typing import Dict, List, Tuple

class Friendship:
    def __init__(self, user1: str, user2: str):
        #Tracks mutual friendship metrics between two people
        #alpabetically sorted
        self.pair = (user1, user2)
        #pair's combined spending  
        self.total_investment = 0
        #user1's spending minus user's 2    
        self.balance = 0             
        self.last_interaction = None

class GlobalFriendshipRanker:
    def __init__(self):
        #Worldwide friendship comparison system
        self.all_pairs: Dict[Tuple[str, str], Friendship] = {}
        self.user_data: Dict[str, List[str]] = {}  # {"Alex": ["Jordan", "Taylor"]}

    def record_gift(self, giver: str, receiver: str, amount: float):
        """Log a gift between two users"""
        # Create pair key (alphabetical order)
        pair_key = tuple(sorted((giver, receiver)))
        
        # Initialize friendship if new
        if pair_key not in self.all_pairs:
            self.all_pairs[pair_key] = Friendship(*pair_key)
            for user in pair_key:
                if user not in self.user_data:
                    self.user_data[user] = []
                if user == giver:
                    self.user_data[user].append(receiver)
        
        # Update friendship metrics
        friendship = self.all_pairs[pair_key]
        friendship.total_investment += amount
        friendship.last_interaction = datetime.now()
        
        # Adjust balance (positive = first user invested more)
        if giver == pair_key[0]:
            friendship.balance += amount
        else:
            friendship.balance -= amount

    def get_global_rankings(self) -> List[Tuple[str, str, int]]:
        """Rank all friendships worldwide by total investment"""
        ranked = []
        for pair, data in self.all_pairs.items():
            ranked.append((*pair, data.total_investment))
        return sorted(ranked, key=lambda x: x[2], reverse=True)

    def generate_shame_report(self, user: str) -> List[Tuple[str, int]]:
        """List a user's most neglected friends"""
        if user not in self.user_data:
            return []
            
        neglected = []
        for friend in self.user_data[user]:
            pair_key = tuple(sorted((user, friend)))
            investment = self.all_pairs[pair_key].balance if user == pair_key[0] else -self.all_pairs[pair_key].balance
            neglected.append((friend, investment))
        
        return sorted(neglected, key=lambda x: x[1])

    def print_global_leaderboard(self):
        """Display worldwide rankings with brutal honesty"""
        print("\n🌍 GLOBAL BESTIE RANKINGS 🌍")
        print("⚖️ (Combined spending between pairs)")
        print("-"*40)
        
        rankings = self.get_global_rankings()
        
        for i, (user1, user2, total) in enumerate(rankings[:10], 1):
            # Determine relationship status
            pair_data = self.all_pairs[(user1, user2)]
            
            if i == 1:
                title = "👑 ULTIMATE SOULMATES"
            elif i <= 3:
                title = "💎 TRUE FRIENDS"
            elif total < 100:
                title = "💩 CHEAP FRIENDS"
            else:
                title = f"#{i} FRIENDS"
            
            print(f"\n{title}: {user1} & {user2}")
            print(f"   Total spent on each other: ${total}")
            
            # Shame imbalance
            imbalance = abs(pair_data.balance)
            if imbalance > total * 0.7:  # 70%+ imbalance
                richer = user1 if pair_data.balance > 0 else user2
                poorer = user2 if pair_data.balance > 0 else user1
                print(f"   ⚠️ {richer} carries {poorer} (${imbalance} difference)")
            
            # Shame neglect
            if total < 50:
                print("   💔 EMBARRASSING - do they even care?")
            elif total < 20:
                print("   🚮 TRASH TIER - just delete each other")

        # Print shame list for top pairs
        if rankings:
            print("\n🔥 TOP PAIR NEGLECT LISTS 🔥")
            for user in rankings[0][:2]:
                neglected = self.generate_shame_report(user)
                if neglected and neglected[0][1] < 20:
                    print(f"\n{user}'s most neglected friends:")
                    for friend, amount in neglected[:3]:
                        if amount < 20:
                            print(f"   💀 {friend}: ${amount} (PATHETIC)")
                        elif amount < 50:
                            print(f"   🥀 {friend}: ${amount} (Neglected)")

# Example Usage
world_rankings = GlobalFriendshipRanker()

# Record global gifts
world_rankings.record_gift("Alex", "Jordan", 200)
world_rankings.record_gift("Jordan", "Alex", 180)
world_rankings.record_gift("Alex", "Taylor", 50)
world_rankings.record_gift("Jordan", "Taylor", 15)
world_rankings.record_gift("Alex", "Casey", 10)  # Shameful

# Display global truth
world_rankings.print_global_leaderboard()