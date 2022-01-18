from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# A knight is always honest (i.e. speaks the truth) whereas the knave is always dishonest (i.e. always lies!)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A can be either a Knight or a Knave; but not both
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),  # (AKnight ∨ AKnave) ∧ ¬(AKnight ∧ AKnave)

    # A claims to be knight and knave both; so with a perpective that A is a Knight!; speaking the truth
    Biconditional(AKnight, And(AKnight, AKnave))    # AKnight <=> (AKnight ∧ AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A can be either a Knight or a Knave; but not both
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),  # (AKnight ∨ AKnave) ∧ ¬(AKnight ∧ AKnave)
    # B can be either a Knight or a Knave; but not both
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),  # (BKnight ∨ BKnave) ∧ ¬(BKnight ∧ BKnave)

    # A says that "I'm a knave and so is B"; so with a perspective that A is a knight; speaking the truth
    Biconditional(AKnight, And(AKnave, BKnave))  # Anight <=> (AKnave ∧ BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A can be either a Knight or a Knave; but not both
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),  # (AKnight ∨ AKnave) ∧ ¬(AKnight ∧ AKnave)
    # B can be either a Knight or a Knave; but not both
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),  # (BKnight ∨ BKnave) ∧ ¬(BKnight ∧ BKnave)

    # A says "We are the same kind." So, with a perpective that A is a Knight; speaking the truth
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),  # AKnight <=> ((AKnight ∧ BKnight) ∨ (AKnave ∧ BKnave))
    # B says "We are of different kinds." So, with a perpective that B is a Knight; speaking the truth
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))  # BKnight <=> ((AKnight ∧ BKnave)) V (AKnave ∧ BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A can be either a Knight or a Knave; but not both
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),  # (AKnight ∨ AKnave) ∧ ¬(AKnight ∧ AKnave)
    # B can be either a Knight or a Knave; but not both
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),  # (BKnight ∨ BKnave) ∧ ¬(BKnight ∧ BKnave)
    # C can be either a Knight or a Knave; but not both
    Or(CKnight, CKnave), Not(And(CKnight, CKnave)),  # (CKnight ∨ CKnave) ∧ ¬(CKnight ∧ CKnave)

    # A says either "I am a knight." or "I am a knave."; so pretending a is a night(is saying the truth)
    Biconditional(AKnight, Or(AKnight, AKnave)),
    # B says "C is a knave."; so pretending b is a knight(is saying the truth)
    Biconditional(BKnight, CKnave),
    # C says "A is a knight." so pretending c is speaking the truth(i.e. is a knight)
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
