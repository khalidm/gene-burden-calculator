#!/usr/bin/env python

'''
A tool to calculate two proportion Z-test and binomial test
to compare frequency of deleterious variants between cases and
expected population for example ExAC.
The two input files contain gene variants counts for their
corresponding populations.

<input format>
gene variants_in_cases total_cases variants_in_population_sample total_population

Author: Khalid Mahmood
Contact: khalid.mahmood@unimelb.edu.au
'''

import math
import scipy.stats
import statsmodels.stats.proportion

def calculate_burden_statistics(case_burden, total_cases, population_burden, total_population):
    '''
    >>> calculate_burden_statistics(1,20,1000,20000)
    (1.0, 1.0)
    >>> calculate_burden_statistics(1,20,1000,100000)
    (0.072339541170780119, 0.18209306240276923)
    >>> calculate_burden_statistics(3,692,65,53105)
    (0.022099924798115057, 0.054308032446737049)
    >>> calculate_burden_statistics(2,692,56,53105)
    (0.14375451576421008, 0.16615019140170481)
    '''
    case_proportion = 1.0 * case_burden / total_cases
    population_proportion = 1.0 * population_burden / total_population
    #print("case_burden {} total_cases {} pop_burden {} total_pop {}".format(case_burden, total_cases, population_burden, total_population))

    # z proportion test
    psp = ((case_proportion * total_cases) + (population_proportion * total_population)) / (total_cases + total_population)
    #print("psp {} total cases {} total pop {}".format(psp, total_cases, total_population))
    standard_error = math.sqrt(psp * (1.0 - psp) * (1.0 / total_cases + 1.0 / total_population))
    z_score = (case_proportion - population_proportion) / standard_error

    # p-value from z-proportion test
    z_test_p_value = 2 * scipy.stats.norm.sf(abs(z_score))

    # binomial test
    obs = [[case_burden, (total_cases - case_burden)], [population_burden, (total_population - population_burden)]]
    binomial_z_score, binomial_pval, binomial_dof, binomial_expected = scipy.stats.chi2_contingency(obs, correction=True)

    # p-value from binomial test
    binomial_p_value = statsmodels.stats.proportion.binom_test(case_burden, total_cases, prop=population_proportion, alternative="two-sided")

    return (z_test_p_value, binomial_p_value)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
