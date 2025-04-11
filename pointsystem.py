from datetime import datetime
from typing import Dict, List, Tuple

class FriendshipPair:
    """Tracks friendship points between two users"""
    def __init__(self, user1: str, user2: str):
        # Store the pair names in alphabetical order
        self.pair = tuple(sorted((user1, user2)))
        
        # Monthly points reset every new month
        self.monthly_points = 0
        
        # Tracks points given from user1 to user2
        self.user1_to_user2 = 0
        
        # Tracks points given from user2 to user1
        self.user2_to_user1 = 0
        
        # Last interaction date for point expiry
        self.last_interaction = None

class GlobalFriendshipLeaderboard:
    """Worldwide monthly ranking of strongest friendships"""
    def __init__(self):
        # Stores all friendship pairs: {(user1,user2): FriendshipPair}
        self.all_pairs: Dict[Tuple[str, str], FriendshipPair] = {}
        
        # Current month tracker for auto-resets
        self.current_month = datetime.now().month
        
        # Tiered ranking titles 
        self.rank_titles = [
            "👑 ULTIMATE BESTIES",      # 1st place
            "💎 STRONG CONNECTION",     # 2nd place
            "🌟 ALMOST ACCEPTABLE",     # 3rd place
            "💔 ONE-SIDED FRIENDSHIP",  # 4th place
            "🚮 TRASH TIER PAIR"        # 5th place
        ]

    def record_gift(self, giver: str, receiver: str, points: int):
        """Log friendship points between two users"""
        # Create pair key (alphabetical order)
        pair_key = tuple(sorted((giver, receiver)))
        
        # Initialize new friendship if first interaction
        if pair_key not in self.all_pairs:
            self.all_pairs[pair_key] = FriendshipPair(*pair_key)
        
        # Get the friendship record
        pair = self.all_pairs[pair_key]
        
        # Update monthly totals
        pair.monthly_points += points
        pair.last_interaction = datetime.now()
        
        # Track direction of points
        if giver == pair_key[0]:  # user1 gave to user2
            pair.user1_to_user2 += points
        else:  # user2 gave to user1
            pair.user2_to_user1 += points

    def _reset_monthly_points(self):
        """Reset monthly counts if new month detected"""
        if datetime.now().month != self.current_month:
            print("\n✨ NEW MONTH - Friendship points reset! ✨")
            for pair in self.all_pairs.values():
                pair.monthly_points = 0
            self.current_month = datetime.now().month

    def get_ranked_pairs(self) -> List[Tuple]:
        """Generate monthly rankings with imbalance data"""
        self._reset_monthly_points()
        
        ranked = []
        for pair_key, pair_data in self.all_pairs.items():
            # Calculate imbalance (absolute difference)
            imbalance = abs(pair_data.user1_to_user2 - pair_data.user2_to_user1)
            
            # Package data for sorting
            ranked.append((
                *pair_key,                     # user1, user2
                pair_data.monthly_points,      # total points
                pair_data.user1_to_user2,      # user1's contribution
                pair_data.user2_to_user1,      # user2's contribution
                imbalance                      # relationship imbalance
            ))
        
        # Sort by monthly points (descending)
        return sorted(ranked, key=lambda x: x[2], reverse=True)

    def display_leaderboard(self):
        """Print the monthly global rankings"""
        print(f"\n🌍 GLOBAL FRIENDSHIP LEADERBOARD - {datetime.now().strftime('%B %Y')} 🌍")
        print("💖 Ranked by total friendship points exchanged this month")
        print("-"*60)
        
        # Get sorted rankings
        rankings = self.get_ranked_pairs()
        
        # Display top pairs with savage commentary
        for i, (user1, user2, total, u1_pts, u2_pts, imbalance) in enumerate(rankings[:10], 1):
            # Select appropriate title
            title = self.rank_titles[min(i-1, len(self.rank_titles)-1)]
            
            # Print pair ranking
            print(f"\n{title} #{i}: {user1} & {user2}")
            print(f"   Monthly Points: {total}")
            print(f"   Breakdown: {user1} → {user2}: {u1_pts} pts | {user2} → {user1}: {u2_pts} pts")
            
            # Shame imbalances (>60% difference)
            if imbalance > total * 0.6:
                dominant = user1 if u1_pts > u2_pts else user2
                passive = user2 if dominant == user1 else user1
                print(f"   ⚠️ {dominant} carries {passive} ({imbalance} pt difference)")
            
            # Special insults for weak friendships
            if total < 50:
                print("   💔 Pathetic effort - do they even care?")
            if total < 20:
                print("   🚮 Disgraceful - why are they friends?")

# Example Usage
if __name__ == "__main__":
    # Initialize global leaderboard
    world_leaderboard = GlobalFriendshipLeaderboard()
    
    # Record friendship interactions (1 point = $1 equivalent)
    world_leaderboard.record_gift("Alex", "Jordan", 150)
    world_leaderboard.record_gift("Jordan", "Alex", 50)  # Jordan is less invested
    world_leaderboard.record_gift("Taylor", "Casey", 200)
    world_leaderboard.record_gift("Casey", "Taylor", 180)  # Strong mutual friendship
    world_leaderboard.record_gift("Drew", "Morgan", 10)    # Weak friendship
    
    # Display the brutal truth
    world_leaderboard.display_leaderboard()