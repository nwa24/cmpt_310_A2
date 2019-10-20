#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>


"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        #start_time = time.time()
        solve_dpll(instance, verbosity)
        #print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')

# finds a unit clause
# returns: variable and the value
# def findUnit(clauses):
#     for clause in clauses:
#         # a unit clause is one that only contains one literal
#         if (len(clause) == 1):
#             return [abs(clause[0]), clause[0]] # returns [symbol, literal]
#     return False

# def removeSymbol(clauses, symbol):
#     # print(clauses)
#     # print(symbol)
#     oppositeSymbol = symbol * -1
    
#     for x in range(len(clauses)):
#         for y in range(len(clauses[x])):
#             # print(clauses[x][y])
#             current = clauses[x][y]
#             # print(current)
#             if (current == symbol or current == oppositeSymbol):
#                 print(x,y)
#                 clauses[x].pop(y)
#         if (len(clauses[x]) == 0):
#             clauses.pop(x)
#         print(clauses)

def simplify(clauses, unit):
    simplifiedList = []

    for clause in clauses:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]

            if not new_clause:
                return -1
        
            simplifiedList.append(new_clause)
        else:
            simplifiedList.append(clause)
    return simplifiedList


        




# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses
    variables = instance.VARS
    printSolution = []

    solution = DPLL(clauses, variables, [])

    if solution:
        print("SAT")

        if (verbosity):
            for literal in solution:
                if (literal > 0):
                    printSolution.append(literal)
            printSolution.sort()
            print(printSolution)
    else:
        print("UNSAT")


    ###########################################

def DPLL(clauses, symbols, model):
    # print(clauses)
    # print(symbols)
    # print(model)

    if clauses == -1:
        return []
    
    # if there are no more clauses
    if not clauses:
        return model 
    
    # to find the variable that occurs the most in the formula
    lits = [abs(x) for clause in clauses for x in clause]
    symbol = max(lits, key=lambda ele: lits.count(abs(ele)))
    
    solution = DPLL(simplify(clauses, symbol), symbols, model + [symbol])

    if not solution:
        solution = DPLL(simplify(clauses, -symbol), symbols, model + [-symbol])
    
    return solution

    
    # pick a symbol that has not been assigned a value yet

    
    # if there is a unit clause
    # if (findUnit(clauses) != False):
    #     unitClause = findUnit(clauses)
    #     # print(unitClause)
    #     # remove the unit clause from the clauses
    #     removeSymbol(clauses, unitClause[0])
    #     # remove the unit symbol from the list of symbols
    #     symbols.remove(unitClause[0])
    #     # add it to the model
    #     model[unitClause[0]] = unitClause[1]
    #     # recursively call DPLL
    #     # return DPLL(clauses, symbols, model)

if __name__ == "__main__":
    main(sys.argv[1:])
