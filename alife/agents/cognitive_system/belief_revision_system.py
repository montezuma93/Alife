import itertools
from .truths.truthtable import *
from.propositions import *

class BeliefRevisionSystem:

    def __init__(self):
        pass

class FormalBeliefRevision(BeliefRevisionSystem):

    def __init__(self):
        self.closed_world_assumption = False

    def set_closed_world_assumption(self, has_closed_world_assumption):
        self.closed_world_assumption = has_closed_world_assumption

    def revise_belief_base(self, new_sentence: Sentence, belief_base: list):
        revised_belief_base = []
        negative_rank = self.calculate_rank(new_sentence, belief_base)

        for sentence in belief_base:
            if sentence.evidence > negative_rank:
                revised_belief_base.append(sentence)
            # Merge sentence from belief_base with new sentence with "OR" and calculate new evidence
            merged_sentence = Sentence(sentence.propositions + new_sentence.propositions, max(sentence.evidence + 1, new_sentence.evidence))
            revised_belief_base.append(merged_sentence)
        revised_belief_base.append(new_sentence)
        return revised_belief_base


    def calculate_rank(self, sentence: Sentence, belief_base: list):
        belief_base_truth_table = self.create_truth_table_for_belief_base(belief_base)
        sentence_truth_table = self.create_truth_table_for_new_sentence(sentence)
        if self.belief_base_infers_sentence(belief_base_truth_table, sentence_truth_table):
            #Calculate B^m
            return self.calculate_b_m_rank(sentence_truth_table, belief_base)
        else:
            return 0

    def create_truth_table_for_belief_base(self, belief_base: list):
        #All sentences, will be combined later with "AND"
        sentences = []
        # all sentences in a belief base
        for dnf_sentence in belief_base:
            # "OR" propositions, no logic yet for that part
            or_parts = []
            for sentence in dnf_sentence.propositions:
                # Combine variables by conjunction
                conjuction_part = sentence[0][0].variable
                i = 1
                while i < len(sentence[0]):
                    conjuction_part = "(" + conjuction_part  + "&" + sentence[0][i].variable + ")"
                    i += 1

                or_parts.append("((!(" + conjuction_part + ")" + "^" + sentence[1].value + "))")

            # Adding up all or parts
            complete_sentence_or_sentence = or_parts[0]
            i = 1
            while i < len(or_parts):
                complete_sentence_or_sentence = "(" + complete_sentence_or_sentence  + "|" + or_parts[i] + ")"
                i += 1
            sentences.append(complete_sentence_or_sentence)
        # Adding up all parts
        complete_sentence = sentences[0]
        i = 1
        while i < len(sentences):
            complete_sentence = "(" + complete_sentence  + "&" + sentences[i] + ")"
            i += 1

        return TruthTable(complete_sentence)
        
    def create_truth_table_for_new_sentence(self, sentence):
        # All variables found in the conjuction parts of the sentence, is need to be able to add non available variables, if closed world assumption is active
        available_variables = []
        for proposition in sentence.propositions[0][0]:
            available_variables.append(proposition.variable)

        # If closed world assumption is true, all variables will be negated. It will be assumed that they are negative, because they are not available
        if self.closed_world_assumption:
            all_proposition_variable_names = get_variable_names_for_propositions()
            for proposition in all_proposition_variable_names:
                if not available_variables.__contains__(proposition) and not available_variables.__contains__("!" + proposition):
                    available_variables.append("!"+proposition )

        # Combine variables by conjunction
        conjuction_part = available_variables[0]
        i = 1
        while i < len(available_variables):
            conjuction_part = "(" + conjuction_part  + "&" + available_variables[i] + ")"
            i += 1
        
        # Compared to the create_truth_table_for_belief_base method, the missing ! (negation) comes from ! ! "XOR", is the same as "XOR"
        complete_sentence = "((" + conjuction_part + ")" + "^" + sentence.propositions[0][1].value + ")"

        return TruthTable(complete_sentence)



    def belief_base_infers_sentence(self, belief_base_truth_table, sentence_truth_table):
        # Get all indicies for which generated truth table of the belief base is true
        indices_for_truth_evaluation = [bin(i)[2:] for i, x in enumerate(belief_base_truth_table.outputs) if x == 1]
        # Get the variable ordering from sentence truth table by belief base truth table
        variable_ordering = []
        for variable in sentence_truth_table.variables:
            if variable in belief_base_truth_table.variables:
                variable_ordering.append(belief_base_truth_table.variables.index(variable))
            else:
                # New sentence has a variable which is not in belief base yet, we dont need to care about that value and add both 0 and 1
                variable_ordering.append("*")

        # Calculate output of sentence truth table to check if B -> phi
        does_infer_new_sentence = False
        for row_for_truth_evaluation in indices_for_truth_evaluation:
            # Add leading zeros
            row_for_truth_evaluation = row_for_truth_evaluation.zfill(len(belief_base_truth_table.variables))
            output_str = ""
            for variable_index in variable_ordering:
                if variable_index == "*":
                    output_str = output_str + '*'
                else:
                    output_str = output_str + str(row_for_truth_evaluation[variable_index])

            # Check if sentence truth table evaluates the values to true, If * use 0 and 1 once
            if sentence_truth_table.get_output(output_str.replace('*', '0')) == 1:
                does_infer_new_sentence = True
            if sentence_truth_table.get_output(output_str.replace('*', '1')) == 1:
                does_infer_new_sentence = True

        return does_infer_new_sentence

    def calculate_b_m_rank(self, sentence_truth_table, belief_base):
        belief_base_sentences = sorted(belief_base, key=lambda x: x.evidence, reverse=False)

        counter = 0
        while True:
            evidence = belief_base_sentences[counter].evidence
            belief_base_sentences_with_at_least_evidence = []
            for sentence in belief_base_sentences:
                if sentence.evidence >= evidence:
                    belief_base_sentences_with_at_least_evidence.append(sentence)

            # Get variables combinations, which are used to check if they infer the new sentence
            variables_combinations_to_check = []
            for sentence in belief_base_sentences_with_at_least_evidence:
                for propositions in sentence.propositions:
                    variable_combination_to_check = []
                    for proposition in propositions[0]:
                        variable_combination_to_check.append(proposition.variable)
                    variable_combination_to_check.append(propositions[1].value)
                    variables_combinations_to_check.append(variable_combination_to_check)
            
            if self.variables_combinations_infers_sentence(variables_combinations_to_check, sentence_truth_table):
                if counter == len(belief_base_sentences) - 1:
                    # If maximum subset m of B reached, return evidence
                    return belief_base_sentences[counter].evidence
                # Else check next smaller subset m of B
                counter = counter + 1
            else:
                # If does subset m of B does not infer new sentence return evidence
                return belief_base_sentences[counter - 1].evidence
    
    def variables_combinations_infers_sentence(self, variables_combinations_to_check, sentence_truth_table):
        for variable_combination in variables_combinations_to_check:
            output_str = ""
            for variable in sentence_truth_table.variables:
                if variable in variable_combination:
                    variable_index = variable_combination.index(variable)
                elif "!" + variable in variable_combination:
                    variable_index = variable_combination.index("!" + variable)
                else:
                    variable_index = "*"
                if variable_index == "*":
                    # New sentence has a variable which is not in belief base yet, we dont need to care about that value and add both 0 and 1
                    output_str = output_str + "*"
                else:   
                    if "!" in variable_combination[variable_index]:
                        output_str = output_str + "0"
                    else:
                        output_str = output_str + "1"

            if sentence_truth_table.get_output(output_str.replace("*", "0")) == 1:
                return True
            if sentence_truth_table.get_output(output_str.replace("*", "1")) == 1:
                return True
        return False


  
class ProbabilityBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self):
        pass

class ConditionalBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self):
        pass
 