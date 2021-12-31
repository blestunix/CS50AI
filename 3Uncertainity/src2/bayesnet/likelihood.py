from model import model

# Calculate probability for a given observation
#                        no rain, no track maintainance, train is on time, attended the meeting
probability = model.probability([["none", "no", "on time", "attend"]])

print(probability)
