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
    #Tracks mutual friendship points between two users
    def __init__(self, user1: str, user2: str):
        #Store pair names alphabetically to prevent duplicates
        self.pair = tuple(sorted((user1, user2)))
        
        #Current month's total points
        self.monthly_points = 0
        
        #individual contributions per pair
        #points from first alpabetical user
        self.user1_contribution = 0  
        #points from second alpabetical user
        self.user2_contribution = 0 
        
        #last interaction timestamp
        self.last_gift_date = None

class GlobalFriendshipLeaderboard:
    #worldwide monthly ranking system for friendships
    def __init__(self):
        #database of all friendships: {(user1,user2): FriendshipPair}
        self.friendships: Dict[Tuple[str, str], FriendshipPair] = {}
        
        #current month tracker
        self.current_month = datetime.now().month
        
        #ranking titles lolz
        self.rank_titles = [
            "👑 ULTIMATE BESTIES",
            "💎 STRONG BOND",
            "🌟 ALMOST DECENT",
            "💔 ONE-SIDED",
            "🚮 TRASH TIER"
        ]

    def record_gift(self, giver: str, receiver: str, points: int):
        #log points exchanged between friens
        #create standardized pair key
        pair_key = tuple(sorted((giver, receiver)))
        
        #initialize new friendship if first interaction
        if pair_key not in self.friendships:
            self.friendships[pair_key] = FriendshipPair(*pair_key)
        
        friendship = self.friendships[pair_key]
        
        #uppdate points
        friendship.monthly_points += points
        friendship.last_gift_date = datetime.now()
        
        #track individual contributions
        if giver == pair_key[0]:
            friendship.user1_contribution += points
        else:
            friendship.user2_contribution += points

    def _check_cheap_friends(self, user1: str, user2: str, 
                           u1_pts: int, u2_pts: int) -> List[str]:
        #generate warnings about imbalanced friendships
        warnings = []
        #warning 20% of higher contribution
        threshold = max(u1_pts, u2_pts) * 0.2  
        
        if u1_pts < threshold:
            warnings.append(f"🚨 CHEAP FRIEND ALERT: {user1} only gave {u1_pts}pts")
        if u2_pts < threshold:
            warnings.append(f"🚨 CHEAP FRIEND ALERT: {user2} only gave {u2_pts}pts")
        
        return warnings

    def get_monthly_rankings(self) -> List[Tuple]:
        #generate sorted monthly rankings with imbalance data
        ranked = []
        for pair_key, data in self.friendships.items():
            #calculate imbalance metrics
            total = data.monthly_points
            u1_pts = data.user1_contribution
            u2_pts = data.user2_contribution
            imbalance = abs(u1_pts - u2_pts)
            
            #package ranking data
            ranked.append((*pair_key, total, u1_pts, u2_pts, imbalance))
        
        # Sort by monthly points (descending)
        return sorted(ranked, key=lambda x: x[2], reverse=True)

    def display_leaderboard(self):
        """Print the savage monthly leaderboard"""
        print(f"\n🌍 GLOBAL FRIENDSHIP RANKINGS - {datetime.now().strftime('%B %Y')} 🌍")
        print("💖 Ranked by total points exchanged this month")
        print("-"*60)
        
        rankings = self.get_monthly_rankings()
        
        for i, (user1, user2, total, u1_pts, u2_pts, imbalance) in enumerate(rankings[:10], 1):
            #select ranking title
            title = self.rank_titles[min(i-1, len(self.rank_titles)-1)]
            
            #display pair info
            print(f"\n{title} #{i}: {user1} & {user2}")
            print(f"   Total Points: {total}")
            print(f"   Breakdown: {user1} → {user2}: {u1_pts} pts | {user2} → {user1}: {u2_pts} pts")
            
            #show cheap friend warnings
            for warning in self._check_cheap_friends(user1, user2, u1_pts, u2_pts):
                print(f"   {warning}")
            
            #special commentary
            if total < 50:
                print("   💔 Pathetic effort - do they even care?")
            if imbalance > total * 0.8:
                print(f"   ⚠️ EXTREME IMBALANCE: {max(u1_pts,u2_pts)-min(u1_pts,u2_pts)}pt difference")

#example usage
world = GlobalFriendshipLeaderboard()

#record friendships (1 point = $1 equivalent)
world.record_gift("Alex", "Jordan", 180)
world.record_gift("Jordan", "Alex", 20)  # Jordan is being cheap
world.record_gift("Taylor", "Casey", 150)
world.record_gift("Casey", "Taylor", 140)  # Healthy friendship
world.record_gift("Drew", "Morgan", 5)    # Embarrassing

#display rankings
world.display_leaderboard()