import itertools
from .truths.truthtable import *
from.propositions import *
import sys
import random

class BeliefRevisionSystem:

    def __init__(self):
        pass

class FormalBeliefRevision(BeliefRevisionSystem):

    def __init__(self, belief_revision_system_args):
        self.closed_world_assumption = belief_revision_system_args[0]

    def set_closed_world_assumption(self, has_closed_world_assumption):
        self.closed_world_assumption = has_closed_world_assumption

    def revise_belief_base(self, new_sentences: list, belief_base: list):
        sentence_to_add = self.filter_sentences(new_sentences)
        revised_belief_base = []
        if len(belief_base) == 0:
            revised_belief_base.append(sentence_to_add)
            return revised_belief_base
        else:
            # Check if same sentence is already in belief base -> Question What if Already in Belief Base?
            if not self.sentence_is_in_belief_base(sentence_to_add, belief_base, revised_belief_base):
                negative_rank = self.calculate_rank(sentence_to_add, belief_base)
                for sentence in belief_base:
                    if sentence.evidence > negative_rank:
                        revised_belief_base.append(sentence)
                    # Merge sentence from belief_base with new sentence with "OR" and calculate new evidence
                    merged_sentence = Sentence(sentence.propositions + sentence_to_add.propositions, max(sentence.evidence + 1, sentence_to_add.evidence))
                    revised_belief_base.append(merged_sentence)
                revised_belief_base.append(sentence_to_add)
            return revised_belief_base

    # Choose sentence based on probability, or evidence
    def filter_sentences(self, new_sentences: list):
        total_weight = 0
        for sentence in new_sentences:
            total_weight = total_weight + sentence.evidence
        probability_list = []
        for sentence in new_sentences:
            probability_list.append(sentence.evidence / total_weight)
        choice = random.choices(population=new_sentences, weights=probability_list, k=1)
        return choice[0]

    # Check if sentence is already in belief base -> adjust evidence, return true and therefore the revision is done
    def sentence_is_in_belief_base(self, new_sentence, belief_base, revised_belief_base):
        propositions_in_new_sentence = ""
        for proposition in new_sentence.propositions[0][0]:
            propositions_in_new_sentence = propositions_in_new_sentence + proposition.variable
        propositions_in_new_sentence = propositions_in_new_sentence + new_sentence.propositions[0][1].value
        # If sentence is in belief base, adjust its evidence
        for stored_sentence in belief_base:
            propositions_in_belief_base= ""
            if len(stored_sentence.propositions) == 1:
                for proposition in stored_sentence.propositions[0][0]:
                    propositions_in_belief_base = propositions_in_belief_base + proposition.variable
                propositions_in_belief_base = propositions_in_belief_base + stored_sentence.propositions[0][1].value
                # Sentence already in belief base, now increase its evidence
                if propositions_in_new_sentence == propositions_in_belief_base:
                    stored_sentence.evidence = stored_sentence.evidence + new_sentence.evidence
                    # Add all sentences to revised belief base, as sentence is already in belief base
                    for stored_sentence in belief_base:
                        revised_belief_base.append(stored_sentence)
                    return True
        else:
            return False

    def calculate_rank(self, sentence: Sentence, belief_base: list):
        belief_base_truth_table = self.create_truth_table_for_belief_base(belief_base)
        sentence_truth_table = self.create_truth_table_for_new_sentence(sentence)
        if self.belief_base_infers_sentence(belief_base_truth_table, sentence_truth_table):
            #Calculate B^m
            return self.calculate_b_m_rank(sentence_truth_table, belief_base)
        else:
            return 0

    def create_truth_table_for_belief_base(self, belief_base: list):
        # All sentences, will be combined later with "AND"
        sentences = []
        # All sentences in a belief base
        for and_sentence in belief_base:
            # "OR" propositions, no logic yet for that part
            or_parts = []
            for sentence in and_sentence.propositions:
                # All variables found in the conjuction parts of the sentence, is need to be able to add non available variables, if closed world assumption is active
                available_variables = []
                for proposition in sentence[0]:
                    available_variables.append(proposition.variable)
                # If closed world assumption is set to true, for not available fact, it will be assumed that the negation holds
                # i.e if D is not in the setence, !D is assumed
                # Otherwise (D v !D) is assumed, but (D v !D) is always true and can be ignored
                if self.closed_world_assumption:
                    all_proposition_variable_names = get_variable_names_for_propositions()
                    for proposition in all_proposition_variable_names:
                        if not available_variables.__contains__(proposition) and not available_variables.__contains__("!" + proposition):
                            available_variables.append("!"+proposition )
                # Combine variables by conjunction
                conjuction_part =available_variables[0].replace("!", "") if "!" in available_variables[0] else "!"+ available_variables[0]
                i = 1
                while i < len(available_variables):
                    conjuction_part = "(" + conjuction_part  + "|" + available_variables[i].replace("!", "") + ")" if "!" in available_variables[i] else "(" + conjuction_part  + "|" + "!"+ available_variables[i] + ")"
                    i += 1
                or_parts.append("((" + conjuction_part + ")" + "|" + sentence[1].value + ")")
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
        # If closed world assumption is set to true, for not available fact, it will be assumed that the negation holds
        # i.e if D is not in the setence, !D is assumed
        # Otherwise (D v !D) is assumed, but (D v !D) is always true and can be ignored
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
        # Compared to the create_truth_table_for_belief_base method, here the negation is created -> not phi
        complete_sentence = ""
        if sentence.propositions[0][1].value == "!X":
            complete_sentence = "((" + conjuction_part + ")" + "&" + "(X))"
        else:
            complete_sentence = "((" + conjuction_part + ")" + "&" + "(!X))"

        return TruthTable(complete_sentence)

    # Does the Belief Base entails  the New Sentence?
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
        for row_for_truth_evaluation in indices_for_truth_evaluation:
            # Add leading zeros
            row_for_truth_evaluation = row_for_truth_evaluation.zfill(len(belief_base_truth_table.variables))
            output_str = ""
            for variable_index in variable_ordering:
                if variable_index == "*":
                    output_str = output_str + '*'
                else:
                    output_str = output_str + str(row_for_truth_evaluation[variable_index])
            # Check if sentence truth table evaluates the values to true, If * use 0 and 1 once -> need to be true for all
            # B entails phi means -> for ß -> phi, and this is true if for value ß = 1 also phi needs to be 1
            if sentence_truth_table.get_output(output_str.replace('*', '0')) == 0 or sentence_truth_table.get_output(output_str.replace('*', '1')) == 0:
                # For any vlaue where ß is true, phi is false, so B does not entail phi
                return False
        return True

    def calculate_b_m_rank(self, sentence_truth_table, belief_base):
        belief_base_sentences = sorted(belief_base, key=lambda x: x.evidence, reverse=True)

        next_index_to_check = len(belief_base_sentences)-1
        while next_index_to_check >= 0:
            evidence = belief_base_sentences[next_index_to_check].evidence
            belief_base_sentences_with_at_least_evidence = []
            for index, sentence in reversed(list(enumerate(belief_base_sentences))):
                if sentence.evidence >= evidence:
                    belief_base_sentences_with_at_least_evidence.append(sentence)
                    next_index_to_check = index - 1

            # Check B entails varphi
            belief_base_truth_table_with_at_least_evidence = self.create_truth_table_for_belief_base(belief_base_sentences_with_at_least_evidence)
            if self.belief_base_infers_sentence(belief_base_truth_table_with_at_least_evidence, sentence_truth_table):
                return belief_base_sentences[last_index_which_entails_new_sentence].evidence
        return belief_base_sentences[0].evidence

  
class ProbabilityBeliefRevision(BeliefRevisionSystem):

    def __init__(self, belief_revision_system_args):
        # ALl observed data, will be added to this dict. Key will be the Propositions. 
        # For example: Rock and Green Plant <-> Toxic, will lead to key RGT.
        # The value for that entry will be the amount of observations for that key. 
        # If probability for that Propositions was 1/4, the value will be increased by 0.25
        self.observed_data = {}
        self.pseudo_sample_size = 10
        self.closed_world_assumption = belief_revision_system_args[0]
        self.uses_occams_razor_principle = belief_revision_system_args[1]

    def set_closed_world_assumption(self, has_closed_world_assumption):
        self.closed_world_assumption = has_closed_world_assumption
    
    def set_occams_razor_principle(self, uses_occams_razor_principle):
        self.uses_occams_razor_principle = uses_occams_razor_principle

    def revise_belief_base(self, new_sentences: list, belief_base: list):
        revised_belief_base = []
        for sentence_to_add in new_sentences:
            new_observed_data_key = self.add_to_observed_data(sentence_to_add)
            
            for sentence in belief_base:
                sentence_key = self.create_sentence_key(sentence)
                posterior = self.calculate_posterior(sentence_key)
                sentence.evidence = posterior
                revised_belief_base.append(sentence)
            
            if len(revised_belief_base) < len(self.observed_data.keys()):
                posterior_of_new_sentence = self.calculate_posterior(new_observed_data_key)
                sentence_to_add.evidence = posterior_of_new_sentence
                revised_belief_base.append(sentence_to_add)
        return revised_belief_base

    def add_to_observed_data(self, new_sentence):
        created_key = self.create_sentence_key(new_sentence)
        if created_key in self.observed_data:
            self.observed_data[created_key] = self.observed_data[created_key] + new_sentence.evidence
        else:
            self.observed_data[created_key] = new_sentence.evidence
        return created_key
    
    def create_sentence_key(self, sentence):
        created_key = ""
        for proposition in sentence.propositions[0][0]:
            created_key = created_key + proposition.variable
        created_key = created_key + sentence.propositions[0][1].value
        if self.closed_world_assumption:
            all_proposition_variable_names = get_variable_names_for_propositions()
            for proposition in all_proposition_variable_names:
                if not created_key.__contains__(proposition) and not created_key.__contains__("!" + proposition):
                    created_key + ("!"+proposition )
        return created_key

    def calculate_posterior(self, sentence_key):
        alpha_beta = self.calculate_alpha_and_beta(sentence_key)
        alpha = alpha_beta[0]
        beta = alpha_beta[1]
        amount_of_sentence_key = self.observed_data[sentence_key]
        total_amount_of_observed_data = sum(self.observed_data.values())
        return (amount_of_sentence_key + alpha) / (total_amount_of_observed_data + alpha + beta)
    
    def calculate_alpha_and_beta(self, sentence_key):
        if not self.closed_world_assumption and self.uses_occams_razor_principle:
            # Total different combinations = 96
            # () = 2*4 = 8 * length of 2 -> 8/96 = 8,33 %
            # (T, R, D, !D) = 4*2*4 = 32 * length of 3 -> 32/96 = 33,33 %
            # (TR, TD, RD, T!D, R!D) = 5*2*4 = 40 * length of 4 -> 40/96 = 41,66 %
            # (TRD, TR!D) = 2*2*4 = 16 * length of 5 -> 16/96 = 16,66 %
            total_different_combinations = 96
            proposition_length_to_mean = {2:8, 3:32, 4:40, 5:16}
            mean = proposition_length_to_mean.get(len(sentence_key.replace('!','')))/total_different_combinations
            alpha = mean* self.pseudo_sample_size
            beta = (1-mean) *self.pseudo_sample_size
            
            return (alpha, beta)
        else:
            # If closed_world_assumption all have the same length
            return (1, 1)


# See: A Constraint Logic Programming Approach for Computing Ordinal Conditional Functions
# See Postulates for conditional belief revision
# See Towards a General framework of Kinds of Forgetting in Common-Sense Belief Management
class ConditionalBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self, closed_world_assumption, belief_revision_system_args):
        self.closed_world_assumption = closed_world_assumption

    def revise_belief_base(self, new_sentence: Sentence, belief_base: list):
        self.calculate_kappa_values(belief_base)

    def calculate_kappa_values(self, belief_base):       
        self.variables = get_variable_names_for_all_propositions()
        self.create_possible_worlds()
        # indicies = length of belief_base or length of conditionals and is given
        conditionals = self.create_conditionals(belief_base)
        kappa_vector = [None] * len(conditionals)
        # Ki entries: [([for each verified world: [k_j which falsify i],[],..], for each falsified world: [k_j which falsify i],[],..] ), ()]
        constraints = self.create_constraints(conditionals, kappa_vector)

    def create_constraints(self, conditionals, kappa_vector):
        constraints = []
        for index, conditional in enumerate(conditionals):
            k_i_constraint = self.calculating_k_i_constraint(index, conditional, conditionals, kappa_vector)
            constraints.append(k_i_constraint)
        return constraints
    
    def create_possible_worlds(self):
        possible_worlds = []
        all_possible_worlds = [list(i) for i in itertools.product([0, 1], repeat=len(self.variables))]
        # Remove all worlds, which aren't possible because of a plant can't be orange and blue at the same time but at least one color need to be set
        for possible_world in all_possible_worlds:
            amount_of_ones_in_color_propositions = possible_world[0] + possible_world[1] + possible_world[2] + possible_world[3]
            if amount_of_ones_in_color_propositions == 1:
                possible_worlds.append(possible_world)
        self.possible_worlds = possible_worlds

    def calculate_verifying_worlds(self, conditional):
        verifying_worlds = []
        for possible_world in self.possible_worlds:
            for proposition in conditional.antecedent:
                index_of_propostion = self.variables.index(proposition.replace("!", ""))
                if (proposition.__contains__("!") and possible_world[index_of_propostion] == 1) or (not proposition.__contains__("!") and possible_world[index_of_propostion] == 0):
                    break
            else:
                index_of_propostion = self.variables.index(conditional.consequence.replace("!", ""))
                if (conditional.consequence.__contains__("!") and possible_world[index_of_propostion] == 1) or (not conditional.consequence.__contains__("!") and possible_world[index_of_propostion] == 0):
                    continue
                verifying_worlds.append(possible_world)
        return verifying_worlds      

    def calculate_falsifying_worlds(self, conditional):
        falsifying_worlds = []
        for possible_world in self.possible_worlds:
            for proposition in conditional.antecedent:
                index_of_propostion = self.variables.index(proposition.replace("!", ""))
                if (proposition.__contains__("!") and possible_world[index_of_propostion] == 1) or (not proposition.__contains__("!") and possible_world[index_of_propostion] == 0):
                    break
            else:
                index_of_propostion = self.variables.index(conditional.consequence.replace("!", ""))
                if (conditional.consequence.__contains__("!") and possible_world[index_of_propostion] == 0) or (not conditional.consequence.__contains__("!") and possible_world[index_of_propostion] == 1):
                    continue
                falsifying_worlds.append(possible_world)
        return falsifying_worlds      

    def calculating_k_i_constraint(self, index, conditional, conditionals, kappa_vector):
        # All worlds verifying i-th conditional
        verifying_worlds = self.calculate_verifying_worlds(conditional)
        # All worlds falsifying i-th conditional
        falsifying_worlds = self.calculate_falsifying_worlds(conditional)

        verification_sums = self.calculate_list_of_sums(index, conditionals, verifying_worlds)
        falsifying_sums = self.calculate_list_of_sums(index, conditionals, falsifying_worlds)
        # Calculating mimimum

        return (verification_sums, falsifying_sums)

    def calculate_list_of_sums(self, i_index, conditionals, worlds):
        list_of_sums = []
        for world in worlds:
            sum_of_kappa_j = []
            for index, conditional in enumerate(conditionals):
                if index != i_index:
                    for proposition in conditional.antecedent:
                        index_of_propostion = self.variables.index(proposition.replace("!", ""))
                        if (proposition.__contains__("!") and world[index_of_propostion] == 1) or (not proposition.__contains__("!") and world[index_of_propostion] == 0):
                            break
                    else:
                        index_of_propostion = self.variables.index(conditional.consequence.replace("!", ""))
                        if (conditional.consequence.__contains__("!") and world[index_of_propostion] == 0) or (not conditional.consequence.__contains__("!") and world[index_of_propostion] == 1):
                            continue
                        sum_of_kappa_j.append(index)
            list_of_sums.append(sum_of_kappa_j)
        return list_of_sums


    # Sentence([([proposition, proposition, ...], reward), ([proposition, proposition, ...], reward), ...], evidence)
    # Belief Base list of Sentences
    def create_conditionals(self, belief_base):
        conditionals = []
        for sentence in belief_base:
            antecedent = []
            for proposition in sentence.propositions[0][0]:
                antecedent.append(proposition.variable)
            conditional = Conditional(antecedent, sentence.propositions[0][1].value)
            conditionals.append(conditional)
        return conditionals

# Just needed for ConditionalBeliefRevision
# Conditional([antecedent,...], consequence)
class Conditional:
    def __init__(self, antecedent, consequence):
        self.antecedent = antecedent
        self.consequence = consequence

# Belief Revision with Explanations
# See: Explanations, belief revision and defeasible reasoning
class KernelBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self):
        pass

# Try https://github.com/opennars/Narjure
class NARSBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self):
        pass
 