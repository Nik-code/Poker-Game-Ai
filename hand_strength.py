# hand_strength.py

from collections import Counter

hand_rankings = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

def evaluate_hand(hand):
    ranks = [card.get_value() for card in hand]
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    is_flush = len(suit_counts) == 1
    is_straight = sorted(ranks) == list(range(min(ranks), max(ranks)+1))

    if is_flush and is_straight and max(ranks) == 14:
        hand_type = "Royal Flush"
    elif is_flush and is_straight:
        hand_type = "Straight Flush"
    elif 4 in rank_counts.values():
        hand_type = "Four of a Kind"
    elif sorted(rank_counts.values()) == [2, 3]:
        hand_type = "Full House"
    elif is_flush:
        hand_type = "Flush"
    elif is_straight:
        hand_type = "Straight"
    elif 3 in rank_counts.values():
        hand_type = "Three of a Kind"
    elif list(rank_counts.values()).count(2) == 2:
        hand_type = "Two Pair"
    elif 2 in rank_counts.values():
        hand_type = "One Pair"
    else:
        hand_type = "High Card"

    return {"hand_type": hand_type, "rank": hand_rankings[hand_type]}
