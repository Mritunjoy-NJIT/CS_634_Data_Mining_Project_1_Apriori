# -*- coding: utf-8 -*-
"""Project_1_Clean_Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aCFmqkYPTLv4A9QDl1xoIiHFBRGe7Shu
"""

#If you remove the quotations and run the below cell, you will have the needed functions to use the built-in libraries

# !pip install apyori
# !pip install fpgrowth
# !pip install mlxtend
import time
import pandas as pd
import numpy as np
from apyori import apriori
from mlxtend.frequent_patterns import fpgrowth, association_rules

#The below function will give the user flexibility to select the data

import pandas as pd

def get_dataset():
    datasets = {
        1: 'Best Buy.csv',
        2: 'Whole Foods.csv',
        3: 'Nike.csv',
        4: 'Walmart.csv',
        5: 'Barnes & Noble.csv'
    }

    print("Welcome to Apriori 2.0!")
    print("User please select your store:")
    print("1. Best Buy")
    print("2. Whole Foods")
    print("3. Nike")
    print("4. Walmart")
    print("5. Barnes & Nobles")

    user = 0

    #Keep asking until the user provides a valid selection
    while user < 1 or user > 5:
      user = int(input("Please enter a number between 1 and 5: "))

    #Return the selected dataset
    return datasets[user]

#This will count the frequency of occurrence for each item
def count_occurences(itemset, Transactions):
  count = 0
  for t in Transactions:
    if set(itemset).issubset(set(t)):
      count+=1
  return count

#This function will calculate the frequent item set
def get_frequent(itemsets, Transactions, min_support, prev_discarded):
  L=[]
  supp_count = []
  new_discarded = []
  k = len(prev_discarded.keys())
  for s in range(len(itemsets)):
    discarded_before = False
    if k>0:
      for item in prev_discarded[k]:
        if set(item).issubset(set(itemsets[s])):
          discarded_before = True
          break
    if not discarded_before:
      count = count_occurences(itemsets[s],Transactions)
      if count/len(Transactions) >= min_support:
        L.append(itemsets[s])
        supp_count.append(count)
      else:
        new_discarded.append(itemsets[s])

  return L,supp_count,new_discarded

#We will join two itemsets
def join_two_itemsets(it1,it2,order):
  it1.sort(key = lambda x:order.index(x))
  it2.sort(key = lambda x:order.index(x))
  for i in range(len(it1)-1):
    if it1[i]!=it2[i]:
      return []

  if order.index(it1[-1])<order.index(it2[-1]):
    return it1+[it2[-1]]
  else:
    return []

def join_itemsets(set_of_its, order):
  C = []
  for i in range(len(set_of_its)):
    for j in range(i+1, len(set_of_its)):
      it_out = join_two_itemsets(set_of_its[i],set_of_its[j],order)
      if len(it_out)>0:
        C.append(it_out)
  return C

#Befow function will calculate the combinations of different functions
from itertools import combinations, chain,permutations
def powerset(iterable):
    # Generate permutations of all possible lengths
    return list(chain.from_iterable(combinations(iterable, r) for r in range(1, len(iterable) + 1)))

#Format the output of brute force
def write_rules(counter,X, X_S,S,conf, supp, num_trans):
  out_rules = ""
  out_rules+="Rule {} ".format(counter)
  out_rules+="Freq.Itemset{}\n".format(X)
  out_rules+="Rule: {} -> {}\n".format(list(S),list(X_S))
  out_rules+="Support Count: {}\n".format(supp/num_trans)
  out_rules+="Confidence: {}\n".format(round(conf,2))
  out_rules+="-" * 30
  out_rules+="\n"
  return out_rules

#The below function will generate the final output
import time
def generate_association_rules(L, Transactions, min_confidence, min_support, num_trans):

    start_time = time.time()

    counter = 1
    assoc_rules_str = ""


    for i in range(1, len(L)):
        for j in range(len(L[i])):
            S = powerset(L[i][j])
            S.pop()


            for z in S:
                S = set(z)
                X = set(L[i][j])
                X_S = set(X - S)

                # Support and confidence calculations
                sup_x = count_occurences(X, Transactions)
                sup_x_s = count_occurences(X_S, Transactions)
                conf = sup_x / count_occurences(S, Transactions)

                # It will check the minimum thresholds
                if conf >= min_confidence and sup_x / num_trans >= min_support:
                    assoc_rules_str += write_rules(counter, X, X_S, S, conf, sup_x , num_trans)
                    counter += 1

    end_time = time.time()

    execution_time = end_time - start_time

    assoc_rules_str += f"\nExecution Time: {round(execution_time, 4)} seconds\n"

    return assoc_rules_str

#The below code will format the output for the fpgrwoth
def format_frequent_itemsets(frequent_itemsets):
    print("\nFrequent Itemsets:")
    for itemset in frequent_itemsets.iterrows():
        items = list(itemset['itemsets'])
        support = round(itemset['support'], 2)
        print(f"Itemset: {items}, Support: {support}")

#The below function will format the rules for the fpgrowth tree
def format_rules(rules):
    for rule_no, rule in enumerate(rules.iterrows(), start=1):
        base_items = list(rule[1]['antecedents'])
        add_items = list(rule[1]['consequents'])
        support = round(rule[1]['support'], 2)
        confidence = round(rule[1]['confidence'], 2)

        print(f"Rule {rule_no}: {base_items} -> {add_items}")
        print(f"Support Count: {support}")
        print(f"Confidence: {confidence}")
        print("-" * 30)

def run_apriori(transactions, min_support, min_confidence):
    import time
    start_time = time.time()

    rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence)

    rules = list(rules)

    apriori_time = time.time() - start_time

    print("\nGenerated Association Rules (Apriori):")

    rule_no = 1
    for rule in rules:
        for ordered_stat in rule.ordered_statistics:
            LHS = list(ordered_stat.items_base)
            RHS = list(ordered_stat.items_add)
            support = rule.support
            confidence = ordered_stat.confidence

            if len(LHS) > 0:
                print(f"Rule {rule_no}: {LHS} -> {RHS}")
                print(f"Support Count: {round(support, 2)}")
                print(f"Confidence: {round(confidence, 2)}")
                print("-" * 30)
                rule_no += 1

    return apriori_time

def run_fp_growth(transactions, min_support, min_confidence):
    import time
    from mlxtend.frequent_patterns import fpgrowth, association_rules
    import pandas as pd

    # Ensure each transaction is treated as a set to remove duplicates
    transactions = [list(set(transaction)) for transaction in transactions]

    # Convert transactions to one-hot encoded format
    onehot = pd.get_dummies(pd.DataFrame(transactions).stack()).groupby(level=0).sum()

    # Validate the empty set as it was generating error
    if onehot.empty:
        return

    start_time = time.time()

    # Run FP-Growth algorithm
    frequent_itemsets = fpgrowth(onehot, min_support=min_support, use_colnames=True)

    if frequent_itemsets.empty:
        return

    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    # Validate the empty set as it was generating error
    if rules.empty:
        return

    fp_growth_time = time.time() - start_time

    print("\nGenerated Association Rules (FP-Growth):")
    format_rules(rules)

    return fp_growth_time

def main():
    import time
    selected_dataset = get_dataset()
    print(f"You have selected dataset located in {selected_dataset}")

    data = pd.read_csv(selected_dataset)

    #Convert the data set into sets
    Transactions = []
    for i in data['Items']:
        Transaction = i.split(", ")
        Transactions.append(Transaction)

    # Define minimum support and confidence
    # Restriction has been imposed for user input
    min_support = 0

    while min_support < 1 or min_support > 100:

       min_support = float(input("Please give the minimum support in % (Value from 1 to 100): "))

    min_support = min_support / 100


    min_confidence = 0

    while min_confidence < 1 or min_confidence > 100:

      min_confidence = float(input("Please give the Minimum confidence in % (Value from 1 to 100): "))

    min_confidence = min_confidence / 100



    #find the unique items in the set

    unique_items = set(item for sublist in Transactions for item in sublist)
    order = list(unique_items)


    #We will define two empty dictionaries for Candidate and frequent itemsets
    #We will take each unique item from the list and convert them into their own list
    C = {}
    L = {}
    supp_count_L = {}
    item_size = 1
    C.update({item_size:[[f] for f in order]})

    discarded = {item_size:[]}
    f,sup,new_discarded = get_frequent(C[item_size],Transactions,min_support, discarded)

    discarded.update({item_size:new_discarded})
    L.update({item_size:f})
    supp_count_L.update({item_size:sup})
    k = item_size+1

    convergence = False
    while not convergence:
      C.update({k:join_itemsets(L[k-1],order)})

      f,sup, new_discarded = get_frequent(C[k],Transactions,min_support,discarded)
      discarded.update({k:new_discarded})
      L.update({k:f})
      supp_count_L.update({k:sup})
      if len(L[k])==0:
        convergence = True

      k+=1
    num_trans =len(Transactions)

    #We will calculate the frequent item set out of total itemset
    print("For brute force Apriori output\n")

    print(generate_association_rules(L, Transactions, min_confidence, min_support, num_trans))


    print("\nRunning Apriori Algorithm...")
    apriori_time = run_apriori(Transactions, min_support, min_confidence)
    print(f"\nApriori Algorithm Runtime: {apriori_time:.4f} seconds")


    print("\nRunning FP-Growth Algorithm...")
    fp_growth_time = run_fp_growth(Transactions, min_support, min_confidence)

    if fp_growth_time is not None:
        print(f"\nFP-Growth Algorithm Runtime: {fp_growth_time:.4f} seconds")
    else:
        print("\nFP-Growth did not produce any results.")


if __name__ == "__main__":
    main()