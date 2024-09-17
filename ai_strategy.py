# ai_strategy.py

def ai_decision(hand):
    """
    Simple AI strategy:
    - Decide which cards to keep or discard based on hand strength.
    - For simplicity, this AI will always keep pairs or higher and discard others.
    """
    from hand_strength.py import evaluate_hand

    evaluation = evaluate_hand(hand)
    if evaluation['rank'] >= 2:  # Pair or better
        return []  # Keep all cards
    else:
        # Discard all cards not part of a pair
        ranks_in_hand = [card.rank for card in hand]
        duplicate_ranks = set([rank for rank in ranks_in_hand if ranks_in_hand.count(rank) > 1])
        cards_to_keep = [card for card in hand if card.rank in duplicate_ranks]
        cards_to_discard = [card for card in hand if card.rank not in duplicate_ranks]
        return cards_to_discard
