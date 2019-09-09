import itertools
from .truths.truthtable import *
from.propositions import *
import sys
import random
from sympy import *

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
                    stored_sentence.evidence = max(stored_sentence.evidence + 1, new_sentence.evidence)
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
        belief_base_sentences = sorted(belief_base, key=lambda x: x.evidence, reverse=False)

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
                return evidence
        return belief_base_sentences[0].evidence

  
class ProbabilityBeliefRevision(BeliefRevisionSystem):

    def __init__(self, belief_revision_system_args):
        # ALl observed data, will be added to this dict. Key will be the Propositions. 
        # For example: Rock and Green Plant <-> Toxic, will lead to key RGT.
        # The value for that entry will be the amount of observations for that key. 
        # If probability for that Propositions was 1/4, the value will be increased by 0.25
        self.observed_data = {}

        self.closed_world_assumption = belief_revision_system_args[0]
        self.uses_occams_razor_principle = belief_revision_system_args[1]
        if self.uses_occams_razor_principle == True:
            self.pseudo_sample_size = int(belief_revision_system_args[2])

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
        for sentence_to_add in new_sentences:
            new_observed_data_key = self.create_sentence_key(sentence_to_add)
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
            proposition_length_to_mean = {2:1/2, 3:1/4, 4:1/6, 5:1/12}
            mean = proposition_length_to_mean.get(len(sentence_key.replace('!','')))
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
    
    def __init__(self, belief_revision_system_args):
        self.closed_world_assumption = belief_revision_system_args[0]
        self.possible_worlds = self.create_possible_worlds()

    def create_possible_worlds(self):
        self.variables = get_variable_names_for_propositions()
        self.variables.append("!D")
        self.reward_variables = get_variable_names_for_reward_propositions()
        possible_worlds = {}
        for color in get_variable_names_for_color_propositions():
            possible_worlds[color] = {}
            all_combinations = [list(i) for i in itertools.product([0, 1], repeat=len(self.variables + self.reward_variables))]
            filtered_combiation = [combination for combination in all_combinations if combination[0]!= 1 or combination[3]!= 0]
            for combination in filtered_combiation:
                combination_str = [str(i) for i in combination]
                combination_key = "".join(combination_str)
                possible_worlds[color][combination_key] = 0
        return possible_worlds
    
    def revise_belief_base(self, new_sentences: Sentence, stored_stences = None):
        for sentence in new_sentences:
            kappa_values_and_color = self.calculate_kappa_values(sentence)
            kappa_values = kappa_values_and_color[0]
            color = kappa_values_and_color[1]
            y_values = self.solve_gamma_values(kappa_values[0][1], kappa_values[1][1])
            kappa_zero = self.calculate_kappa_zero(y_values[1], kappa_values[0][1], kappa_values[2][1])
            self.update_kappa_values(kappa_zero, y_values[0], y_values[1], kappa_values[0][0], kappa_values[1][0], kappa_values[2][0], color)
        sentences = self.map_possible_worlds_to_belief_base()

        return sentences


    def calculate_kappa_values(self, new_sentence):
        all_variables = get_variable_names_for_propositions()
        all_variables.append("!D")
        variables = []
        color = ""
        for proposition in new_sentence.propositions[0][0]:
            if issubclass(type(proposition), ColorProposition):
                color = proposition.variable
            else:
                variables.append(proposition.variable)
        
        # For closed world assumption
        # If closed world assumption is set to true, for not available fact, it will be assumed that the negation holds
        # i.e if D is not in the setence, !D is assumed
        # Otherwise (D v !D) is assumed, but (D v !D) is always true and can be ignored
        if self.closed_world_assumption:
            all_proposition_variable_names = get_variable_names_for_propositions()
            for proposition in all_proposition_variable_names:
                if not variables.__contains__(proposition) and not variables.__contains__("!" + proposition):
                    variables.append("!"+proposition )
        
        
        # Sorting
        remember_variables = variables
        variables = []
        for variable in remember_variables:
            variables.append(variable.replace("!", ""))
        variables.sort()
        for old_variable in remember_variables:
            index = variables.index(old_variable.replace("!", ""))
            variables[index] = old_variable
        # Add placeholder * where the literl doesn' matter
        replaced_variables = []
        if self.closed_world_assumption:
            for variable in all_variables:
                if variable not in variables:
                    replaced_variables.append("!")
                else:
                    replaced_variables.append(variable)
        else:
            for variable in all_variables:
                if variable not in variables:
                    replaced_variables.append("*")
                else:
                    replaced_variables.append(variable)

        variable_code = ""
        for variable in replaced_variables:
            if "!" in variable:
                variable_code = variable_code +"0"
            elif "*" in variable:
                variable_code = variable_code +"*"
            else:
                variable_code = variable_code +"1"

        if self.closed_world_assumption:
            if variable_code[:1] == '1' and variable_code[-1] == '0':
                variable_code = variable_code[:-1] + '1'

        
        conditional_variable_code = "1" if new_sentence.propositions[0][1].value == "X" else  "0"
        verifying_worlds = []
        falsifying_worlds = []
        not_applicable_worlds = []

        all_variable_codes = []

        indices = [i for i, x in enumerate(variable_code) if x == "*"]
        combinations = [list(i) for i in itertools.product([0, 1], repeat=len(indices))]
        for value in combinations:
            new_variable_code = list(variable_code)
            for i, index in enumerate(indices):
                new_variable_code[index] = str(value[i])
            all_variable_codes.append("".join(new_variable_code))

        filtered_combiation_all_variable_codes = [combination for combination in all_variable_codes if combination[:1] != '1' or combination[-1]!= '0']
        for variable_code in filtered_combiation_all_variable_codes:
            verifying_worlds.append((variable_code + conditional_variable_code, self.possible_worlds[color][variable_code + conditional_variable_code]))

        for variable_code in filtered_combiation_all_variable_codes:
            negated_conditional_variable_code = "0" if conditional_variable_code == "1" else "1"
            falsifying_worlds.append((variable_code + negated_conditional_variable_code, self.possible_worlds[color][variable_code + negated_conditional_variable_code]))

        for world, value in self.possible_worlds[color].items():
            is_not_applicable = True
            for falsifying_world in falsifying_worlds:
                if world == falsifying_world[0]:
                    is_not_applicable = False
            for verifying_world in verifying_worlds:
                if world == verifying_world[0]:
                    is_not_applicable = False
            if is_not_applicable:
                not_applicable_worlds.append((world, value))
        # Ad all not applicable worlds for other colors

        kappa_values = []
        min_value = None
        for world in verifying_worlds:
            if min_value is None or world[1] < min_value:
                min_value = world[1]

        kappa_values.append((verifying_worlds, min_value if min_value is not None else 0))    
        
        min_value = None
        for world in falsifying_worlds:
            if min_value is None or world[1] < min_value:
                min_value = world[1]
        kappa_values.append((falsifying_worlds, min_value if min_value is not None else 0))

        min_value = None
        for world in not_applicable_worlds:
            if min_value is None or world[1] < min_value:
                min_value = world[1]
        # Worlds with other colors are not applicable
        for color_world, possible_world in self.possible_worlds.items():
            if color_world != color:
                for propositions, ranking in possible_world.items():
                    if min_value is None or ranking < min_value:
                        min_value = ranking
        kappa_values.append((not_applicable_worlds, min_value if min_value is not None else 0))    

        return (kappa_values, color)


    def solve_gamma_values(self, kappa_verifying_worlds, kappa_falsifying_worlds):
        solution_not_found = True
        y_minus = 1
        y_plus = -1
        while solution_not_found:
            if y_minus - y_plus > kappa_verifying_worlds-kappa_falsifying_worlds:
                return (y_minus, y_plus)
            y_minus = y_minus + 1
            y_plus = y_plus -1

    def calculate_kappa_zero(self, y_plus, kappa_verifying_worlds, kappa_not_applicable_worlds):
        return min((y_plus + kappa_verifying_worlds), kappa_not_applicable_worlds)

    def update_kappa_values(self, kappa_zero, y_minus, y_plus, verifying_worlds, falsifying_worlds, not_applicable_worlds, color):
        for verifying_world in verifying_worlds:
            self.possible_worlds[color][verifying_world[0]] = self.possible_worlds[color][verifying_world[0]] - kappa_zero + y_plus
        for falsifying_world in falsifying_worlds:
            self.possible_worlds[color][falsifying_world[0]] = self.possible_worlds[color][falsifying_world[0]] - kappa_zero + y_minus
        for not_applicable_world in not_applicable_worlds:
            self.possible_worlds[color][not_applicable_world[0]] = self.possible_worlds[color][not_applicable_world[0]] - kappa_zero
        #Because all other colors are not applicable
        for color_world, possible_world in self.possible_worlds.items():
            if color_world != color:
                for propositions, ranking in possible_world.items():
                    self.possible_worlds[color_world][propositions] = self.possible_worlds[color_world][propositions] - kappa_zero


    def map_possible_worlds_to_belief_base(self):
        key_to_proposition_mapping = {
            "D": DayProposition(),
            "!D": NightProposition(),
            "R": NextToRock(),
            "T": NextToTreeTrunk(),
            "O": ColorOrange(),
            "G": ColorGreen(),
            "P": ColorPurple(),
            "B": ColorBlue()
        }
        variables = get_variable_names_for_propositions()
        variables.append("!D")
        reward_variables = get_variable_names_for_reward_propositions()
        max_amount_of_propositions = len(variables)
        sentences = []
        for color, possible_world in self.possible_worlds.items():
            for propositions, ranking in possible_world.items():
                sentence_propositions = [key_to_proposition_mapping.get(color)]
                for index, proposition in enumerate(propositions):
                    if index < max_amount_of_propositions:
                        if variables[index] == "D":
                            if proposition == "1":
                                sentence_propositions.append(key_to_proposition_mapping.get("D"))
                        elif variables[index] == "!D":
                            if proposition == "0":
                                sentence_propositions.append(key_to_proposition_mapping.get("!D"))
                        else:
                            if proposition == "1":
                                sentence_propositions.append(key_to_proposition_mapping.get(variables[index]))
                if propositions[max_amount_of_propositions] == "0":
                    sentences.append(Sentence([(sentence_propositions, Reward.nontoxic)], ranking))
                else:
                    sentences.append(Sentence([(sentence_propositions, Reward.toxic)], ranking))
        return sentences
            

# Belief Revision with Explanations
# See: Explanations, belief revision and defeasible reasoning
class KernelBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self):
        pass

# Try https://github.com/opennars/Narjure
class NARSBeliefRevision(BeliefRevisionSystem):
    
    def __init__(self):
        pass
 