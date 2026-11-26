import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, parents=None, num_parents=0, cpt=None):
        """
        Class representing a node in a Bayesian network
        name: Node name (e.g., "ChestPain", "HeartDisease")
        parents: List of parent nodes
        num_parents: Number of parent nodes
        cpt: Conditional Probability Table (CPT)
        """
        self.name = name
        self.parents = parents if parents is not None else []
        self.num_parents = num_parents
        self.cpt = cpt if cpt is not None else []

def bayes_inference(heart_disease, chest_pain_state, hypertension_state, hypercholesterolemia_state):
    """
    Bayesian inference function: Calculates P(HeartDisease | ChestPain, Hypertension, Hypercholesterolemia)
    heart_disease: Heart disease node
    chest_pain_state: Chest pain state (0=absent, 1=present)
    hypertension_state: Hypertension state (0=absent, 1=present)
    hypercholesterolemia_state: Hypercholesterolemia state (0=absent, 1=present)
    """
    # Prior probability: P(HeartDisease)
    P_HeartDisease = 0.3  # Example value based on referenced paper

    # Likelihood: P(CP, HT, HC | HD)
    # CPT index calculation: Maps state combination to binary (e.g., [CP=1, HT=1, HC=1] -> 111 -> 7)
    state_index = (chest_pain_state << 2) | (hypertension_state << 1) | hypercholesterolemia_state
    P_Evidence_given_HeartDisease = heart_disease.cpt[state_index]  # Evidence probability given HD=1
    P_Evidence_given_NoHeartDisease = (1 - P_Evidence_given_HeartDisease)  # Evidence probability given HD=0 (simplified)

    # Likelihood adjustment (based on paper: simplified independence assumption)
    if chest_pain_state == 1:
        P_Evidence_given_HeartDisease *= 0.9  # CP=1 | HD=1
        P_Evidence_given_NoHeartDisease *= 0.2  # CP=1 | HD=0
    else:
        P_Evidence_given_HeartDisease *= 0.1  # CP=0 | HD=1
        P_Evidence_given_NoHeartDisease *= 0.8  # CP=0 | HD=0

    if hypertension_state == 1:
        P_Evidence_given_HeartDisease *= 0.85  # HT=1 | HD=1 (paper-based)
        P_Evidence_given_NoHeartDisease *= 0.15  # HT=1 | HD=0
    else:
        P_Evidence_given_HeartDisease *= 0.15
        P_Evidence_given_NoHeartDisease *= 0.85

    if hypercholesterolemia_state == 1:
        P_Evidence_given_HeartDisease *= 0.8  # HC=1 | HD=1
        P_Evidence_given_NoHeartDisease *= 0.3  # HC=1 | HD=0
    else:
        P_Evidence_given_HeartDisease *= 0.2
        P_Evidence_given_NoHeartDisease *= 0.7

    # Marginal probability: P(Evidence)
    P_Evidence = (P_Evidence_given_HeartDisease * P_HeartDisease +
                  P_Evidence_given_NoHeartDisease * (1 - P_HeartDisease))

    # Posterior probability: P(HeartDisease | Evidence)
    if P_Evidence == 0:  # Prevent division by zero
        return 0.0
    P_HeartDisease_given_Evidence = (P_Evidence_given_HeartDisease * P_HeartDisease) / P_Evidence
    return P_HeartDisease_given_Evidence

def visualize_results(states, probs):
    """
    Visualize results: Create a bar plot of probabilities using Matplotlib
    states: List of state combinations (e.g., ["CP=1, HT=0, HC=0"])
    probs: List of heart disease probabilities for each state
    """
    plt.figure(figsize=(10, 6))
    plt.bar(states, probs, color='skyblue')
    plt.xlabel("Symptom Condition Combination")
    plt.ylabel("P(HeartDisease=1)")
    plt.title("Heart Disease Probability Visualization")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function: Set up network, handle user input, perform inference, and visualize results
    """
    # 1. Create nodes
    cpt_chest_pain = [0.0]
    chest_pain = Node("ChestPain", None, 0, cpt_chest_pain)

    cpt_hypertension = [0.0]
    hypertension = Node("Hypertension", None, 0, cpt_hypertension)

    cpt_hypercholesterolemia = [0.0]
    hypercholesterolemia = Node("Hypercholesterolemia", None, 0, cpt_hypercholesterolemia)

    # HeartDisease node: 3 parents (CP, HT, HC)
    # CPT: 2^3 = 8 state combinations (e.g., [0,0,0], [0,0,1], ..., [1,1,1])
    cpt_heart_disease = [0.1, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.95]  # Example values based on paper
    heart_disease = Node("HeartDisease", [chest_pain, hypertension, hypercholesterolemia], 3, cpt_heart_disease)

    # 2. User input
    try:
        print("Enter symptom states (0=absent, 1=present)")
        chest_pain_state = int(input("Chest Pain (0/1): "))
        hypertension_state = int(input("Hypertension (0/1): "))
        hypercholesterolemia_state = int(input("Hypercholesterolemia (0/1): "))

        # Input validation
        if not all(state in [0, 1] for state in [chest_pain_state, hypertension_state, hypercholesterolemia_state]):
            raise ValueError("Inputs must be 0 or 1.")
    except ValueError as e:
        print(f"Error: {e}. Running with default values.")
        chest_pain_state, hypertension_state, hypercholesterolemia_state = 1, 0, 0

    # 3. Inference for single input
    prob = bayes_inference(heart_disease, chest_pain_state, hypertension_state, hypercholesterolemia_state)
    print(f"P(HeartDisease | ChestPain={chest_pain_state}, Hypertension={hypertension_state}, Hypercholesterolemia={hypercholesterolemia_state}) = {prob:.2f}")

    # 4. Inference and visualization for all state combinations
    states = []
    probs = []
    for cp in [0, 1]:
        for ht in [0, 1]:
            for hc in [0, 1]:
                state_str = f"CP={cp}, HT={ht}, HC={hc}"
                prob = bayes_inference(heart_disease, cp, ht, hc)
                states.append(state_str)
                probs.append(prob)

    visualize_results(states, probs)

if __name__ == "__main__":
    main()
