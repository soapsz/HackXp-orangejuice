#idea: friendship points
# $1 = 1 pt
# global ranked in terms of pairs and their mutual investments
# shows how individually as users 1 and users 2 spend towards each other in the pair
# refreshes monthly
# friendship is magic! unless ur poor, then  urs = not valid
# shame system intiaties when user spends <50 points
# shame system intiates even if users are on the podium,if the difference between the gift pts is drastic 

from datetime import datetime
from typing import Dict, List, Tuple

class FriendshipPair:
    """Tracks mutual friendship points between two users"""
    def __init__(self, user1: str, user2: str):
        # Store pair names alphabetically to prevent duplicates
        self.pair = tuple(sorted((user1, user2)))
        
        # Current month's total points
        self.monthly_points = 0
        
        # Individual contributions
        self.user1_contribution = 0  # Points from first alphabetical user
        self.user2_contribution = 0  # Points from second alphabetical user
        
        # Last interaction timestamp
        self.last_gift_date = None

class GlobalFriendshipLeaderboard:
    """Worldwide monthly ranking system for friendships"""
    def __init__(self):
        # Database of all friendships: {(user1,user2): FriendshipPair}
        self.friendships: Dict[Tuple[str, str], FriendshipPair] = {}
        
        # Current month tracker
        self.current_month = datetime.now().month
        
        # Ranking titles with increasing sass
        self.rank_titles = [
            "👑 ULTIMATE BESTIES",
            "💎 STRONG BOND",
            "🌟 ALMOST DECENT",
            "💔 ONE-SIDED",
            "🚮 TRASH TIER"
        ]

    def record_gift(self, giver: str, receiver: str, points: int):
        """Log points exchanged between friends"""
        # Create standardized pair key
        pair_key = tuple(sorted((giver, receiver)))
        
        # Initialize new friendship if first interaction
        if pair_key not in self.friendships:
            self.friendships[pair_key] = FriendshipPair(*pair_key)
        
        friendship = self.friendships[pair_key]
        
        # Update points
        friendship.monthly_points += points
        friendship.last_gift_date = datetime.now()
        
        # Track individual contributions
        if giver == pair_key[0]:
            friendship.user1_contribution += points
        else:
            friendship.user2_contribution += points

    def _check_imbalance(self, user1: str, user2: str, 
                       u1_pts: int, u2_pts: int, 
                       total: int) -> List[str]:
        """Generate warnings about friendship imbalances"""
        warnings = []
        
        # Calculate percentage contributions
        higher = max(u1_pts, u2_pts)
        lower = min(u1_pts, u2_pts)
        imbalance = higher - lower
        
        # Extreme imbalance (>80% difference)
        if lower < higher * 0.2:
            cheap_friend = user1 if u1_pts < u2_pts else user2
            dominant = user2 if cheap_friend == user1 else user1
            warnings.append(f"🚨 CHEAP FRIEND ALERT: {cheap_friend} only gave {lower}pts")
            warnings.append(f"⚠️ EXTREME IMBALANCE: {dominant} carries by {imbalance}pts")
        
        # Significant imbalance (>60% difference)
        elif lower < higher * 0.4:
            warnings.append(f"⚖️ WARNING: {imbalance}pt imbalance detected")
        
        return warnings

    def get_monthly_rankings(self) -> List[Tuple]:
        """Generate sorted monthly rankings with imbalance data"""
        ranked = []
        for pair_key, data in self.friendships.items():
            # Calculate metrics
            total = data.monthly_points
            u1_pts = data.user1_contribution
            u2_pts = data.user2_contribution
            
            # Package ranking data
            ranked.append((*pair_key, total, u1_pts, u2_pts))
        
        # Sort by monthly points (descending)
        return sorted(ranked, key=lambda x: x[2], reverse=True)

    def display_leaderboard(self):
        """Print the savage monthly leaderboard"""
        print(f"\n🌍 GLOBAL FRIENDSHIP RANKINGS - {datetime.now().strftime('%B %Y')} 🌍")
        print("💖 Ranked by total points exchanged this month")
        print("-"*60)
        
        rankings = self.get_monthly_rankings()
        
        for i, (user1, user2, total, u1_pts, u2_pts) in enumerate(rankings[:10], 1):
            # Select ranking title
            title = self.rank_titles[min(i-1, len(self.rank_titles)-1)]
            
            # Display pair info
            print(f"\n{title} #{i}: {user1} & {user2}")
            print(f"   Total Points: {total}")
            print(f"   Breakdown: {user1} → {user2}: {u1_pts} pts | {user2} → {user1}: {u2_pts} pts")
            
            # Show imbalance warnings
            for warning in self._check_imbalance(user1, user2, u1_pts, u2_pts, total):
                print(f"   {warning}")
            
            # Special commentary for low-effort friendships
            if total < 50:
                print("   💔 Pathetic effort - do they even care?")

# Example Usage
world = GlobalFriendshipLeaderboard()

# Record friendships (1 point = $1 equivalent)
world.record_gift("Alex", "Jordan", 180)
world.record_gift("Jordan", "Alex", 20)  # Jordan is being cheap
world.record_gift("Taylor", "Casey", 200)
world.record_gift("Casey", "Taylor", 190)  # Healthy friendship
world.record_gift("Drew", "Morgan", 5)    # Embarrassing

# Display rankings
world.display_leaderboard()



#imbalance detection
# 0.8 difference = full warning combo LMAO
# 0.6 difference = gentle warning
# <50 pts = pathethic comment

#thresholds
# cheap friend = <0.2 of higher amt
