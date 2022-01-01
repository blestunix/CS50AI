import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    
    Parameters:
        - `people` is a dictionary of people as described in the “Understanding” section. The keys represent names, 
          and the values are dictionaries that contain mother and father keys. You may assume that either mother
          and father are both blank (no parental information in the data set), or mother and father will both refer
          to other people in the people dictionary.
        - `one_gene` is a set of all people for whom we want to compute the probability that they have one copy of the gene.
        - `two_genes` is a set of all people for whom we want to compute the probability that they have two copies of the gene.
        - `have_trait` is a set of all people for whom we want to compute the probability that they have the trait.
        
    """
    # Probability of `person` haven 2, 1 or 0 genes
    gene_count = lambda person: 1 if  person in one_gene else 2 if person in two_genes else 0

    probability = 0
    for (person, info) in zip(people.keys(), people.values()):
        genes = gene_count(person)
    
        # Check if a `person` has parents not listed in the `info` dictionary
        if info["mother"] is None and info["father"] is None:
            probability = PROBS["gene"][genes]
        # Parents are indeed listed
        else:
            mother = abs(gene_count(info["mother"]) / 2 - PROBS["mutation"])
            father = abs(gene_count(info["father"]) / 2 - PROBS["mutation"])
            if genes == 2:
                # The person got 2 genes i.e. 1 from each parent i.e. A.B
                probability = mother * father
            elif genes == 1:
                # The person got 1 genes; either from mother of from father i.e. A.~B + B.~A 
                probability = mother * (1 - father) + father * (1 - mother)
            else:
                # The person has no such gene i.e. none from any of the parent; mathematically: ~A.~B
                probability = (1 - mother) * (1 - father)
        
        # Get the state of the 'person' of having the trait
        has_trait = person in have_trait
        # compute the probability that a person does or does not have a particular trait.
        probability *= PROBS["trait"][genes][has_trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    
    Parameter:
        - `probabilities` is a dictionary of people as described in the “Understanding” section. 
           Each person is mapped to a "gene" distribution and a "trait" distribution.
        - `one_gene` is a set of people with one copy of the gene in the current joint distribution.
        - `two_genes` is a set of people with two copies of the gene in the current joint distribution.
        - `have_trait` is a set of people with the trait in the current joint distribution.
        - `p` is the probability of the joint distribution.
    """
     # Probability of `person` haven 2, 1 or 0 genes
    gene_count = lambda person: 1 if  person in one_gene else 2 if person in two_genes else 0

    for person in probabilities:
        # update the probabilities[person]["gene"] distribution by adding p to the corresponding gene
        genes = gene_count(person)
        probabilities[person]["gene"][genes] += p
        
        # update the probabilities[person]["trait"] distribution by adding p to the corresponding trait state
        trait = person in have_trait
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    
    Parameter:
        - in `probabilities` dictionary each person is mapped to a "gene" distribution and a "trait" distribution.
    """
    for person in probabilities:

        # Find the average of gene values
        total_gene = sum(probabilities[person]["gene"].values())
        for i in range(3):
            probabilities[person]["gene"][i] /= total_gene

        # Find the average of trait values
        total_trait = sum(probabilities[person]["trait"].values())
        for i in range(2):
            probabilities[person]["trait"][i] /= total_trait


if __name__ == "__main__":
    main()
