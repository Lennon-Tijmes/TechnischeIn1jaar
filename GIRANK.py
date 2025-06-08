def girank(family_tree, max_iterations=100, tolerance=0.00001):
    """
    Each parent divides their genetic influence equally among their children.
    Children pass on this influence to their own offspring.
    Parents with more children spread their influence over a larger group, just like
    PageRank does.
    Calculate the "Genetic Influence Rank" (GIRank) with an iterative algorithm
    """
    # Step 1: find the (majom = monkey) people in the tree
    people = set(family_tree.keys())
    for children in family_tree.values():
        people.update(children)

    # Step 2: Find parents
    parents = {person: [] for person in people}
    for parent, children in family_tree.items():
        for child in children:
            parents[child].append(parent)

    # Pagerank but now for the people
    girank = {person: 1 / len(people) for person in people}

    damping = 0.85 # Number from pagerank
    N = len(people)

    # step 3: Go through the iterations
    for apples in range(max_iterations):
        new_girank = {}
        max_change = 0

        # Had to add this in order to make sure if you don't have a parent
        # it still will give you a base influence otherwise all results will be 0 :(
        for person in people:
            propagated = 0
            for parent in parents[person]:
                amount_kids = len(family_tree[parent])
                if amount_kids > 0:
                    propagated += girank[parent] / amount_kids

            # Applying the damping        
            new_score = (1 - damping) / N + damping * propagated
            new_girank[person] = new_score
            max_change = max(max_change, abs(new_girank[person] - girank[person]))
        
        girank = new_girank

        if max_change < tolerance:
            break # IF the changes are small it should be converged
    
    # Step 4: Normalize the values to 1.0 like in pagerank
    total = sum(girank.values())
    if total > 0:
        girank = {person: value / total for person, value in girank.items()}

    return girank

def test_all():
    test_cases = [
        {
            "name": "Cool",
            "tree": {
                "Alice": ["Bob"],
                "Bob": ["Charlie"],
                "Charlie": ["Diana"]
            }
        },
        {
            "name": "Alot from 1",
            "tree": {
                "Alice": ["Bob", "Charlie", "Diana", "Eve"]
            }
        },
        {
            "name": "Family with branches",
            "tree": {
                "Alice": ["Bob", "Charlie"],
                "Bob": ["Diana"],
                "Charlie": ["Eve", "Frank"],
                "Frank": ["George"]
            }
        }
    ]

    for test in test_cases:
        print(f"Test Case: {test['name']}")
        result = girank(test["tree"])
        for person, score in sorted(result.items(), key=lambda x: -x[1]):
            print(f"{person}: {score:.4f}")

if __name__ == "__main__":
    test_all()