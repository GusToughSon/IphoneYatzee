def determine_best_score(dice_values, scoreboard_data):
    """AI decision-making for selecting the best scoring category."""
    
    # Remove any 0 values before evaluating
    dice_values = [d for d in dice_values if d > 0]

    score_options = {
        "ones": dice_values.count(1) * 1,
        "twos": dice_values.count(2) * 2,
        "threes": dice_values.count(3) * 3,
        "fours": dice_values.count(4) * 4,
        "fives": dice_values.count(5) * 5,
        "sixes": dice_values.count(6) * 6,
        "three_of_a_kind": sum(dice_values) if any(dice_values.count(d) >= 3 for d in set(dice_values)) else 0,
        "four_of_a_kind": sum(dice_values) if any(dice_values.count(d) >= 4 for d in set(dice_values)) else 0,
        "full_house": 25 if set(dice_values.count(d) for d in set(dice_values)) == {2, 3} else 0,
        "small_straight": 30 if set(dice_values) >= {1, 2, 3, 4} or set(dice_values) >= {2, 3, 4, 5} or set(dice_values) >= {3, 4, 5, 6} else 0,
        "large_straight": 40 if set(dice_values) == {1, 2, 3, 4, 5} or set(dice_values) == {2, 3, 4, 5, 6} else 0,
        "yahtzee": 50 if len(set(dice_values)) == 1 else 0,
        "chance": sum(dice_values),
    }

    # Remove categories that are already filled
    available_scores = {k: v for k, v in score_options.items() if scoreboard_data.get(k) == "empty"}

    if not available_scores:
        return "chance"  # Default to "chance" if no good moves

    best_category = max(available_scores, key=available_scores.get)
    
    print(f"🤖 AI Decision: Select {best_category} for {available_scores[best_category]} points")
    
    return best_category
