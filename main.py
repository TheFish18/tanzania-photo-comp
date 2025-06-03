from collections import Counter, defaultdict
import numpy as np


# Ordered from best to worst
GRADE_ORDER = ["Excellent", "Very Good", "Good", "Acceptable", "Poor", "Reject"]
GRADE_TO_INT = {grade: i for i, grade in enumerate(GRADE_ORDER)}
INT_TO_GRADE = {i: grade for i, grade in enumerate(GRADE_ORDER)}

def median_grade(grades):
    """Return the median grade and its index in GRADE_ORDER."""
    numeric = sorted(GRADE_TO_INT[g] for g in grades)
    med_idx = len(numeric) // 2
    median_value = numeric[med_idx] if len(numeric) % 2 else numeric[med_idx - 1]
    return median_value

def majority_judgment(ballots):
    """
    ballots: dict of {photo_title: [list of grades from each voter]}
    Returns: winner and full breakdown
    """
    results = {}
    for title, grades in ballots.items():
        numeric = sorted(GRADE_TO_INT[g] for g in grades)
        median = median_grade(grades)
        results[title] = {
            "grades": numeric,
            "median": median,
        }

    # Get candidates with best (lowest index) median
    best_median = min(r["median"] for r in results.values())
    contenders = [k for k, v in results.items() if v["median"] == best_median]

    # If tie, use tiebreak rule
    while len(contenders) > 1:
        # For each contender, count how many grades are >= median
        tie_scores = {}
        for title in contenders:
            grades = results[title]["grades"]
            count = sum(1 for g in grades if g <= best_median)
            tie_scores[title] = count

        max_support = max(tie_scores.values())
        contenders = [k for k, v in tie_scores.items() if v == max_support]

        # Remove one vote at the median level from each and recalculate
        if len(contenders) > 1:
            for title in contenders:
                grades = results[title]["grades"]
                # Remove one median grade
                for i in range(len(grades)):
                    if grades[i] == best_median:
                        del grades[i]
                        break
                results[title]["median"] = median_grade([INT_TO_GRADE[g] for g in grades])
            best_median = min(results[t]["median"] for t in contenders)

    winner = contenders[0]
    final_result = {
        "winner": winner,
        "median_grade": INT_TO_GRADE[results[winner]["median"]],
        "all_medians": {k: INT_TO_GRADE[v["median"]] for k, v in results.items()},
    }
    return final_result

if __name__ == "__main__":
    from pathlib import Path
    import json

    dir = Path("ballots")
    ballots = defaultdict(list)

    for p in dir.iterdir():
        user_ballot = json.load(p.open())
        for candidate, vote in user_ballot.items():
            ballots[candidate].append(vote)

    bal_set = set(len(bal) for bal in ballots.values())
    if len(bal_set) != 1:
        raise ValueError('Unequal number of votes')

    result = majority_judgment(ballots)
    print("Winner:", result["winner"])
    print("Winner's Median Grade:", result["median_grade"])
    print("All Medians:", result["all_medians"])
