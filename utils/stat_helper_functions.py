# import packages
import numpy as np
import pandas as pd
import math
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_ind, ttest_rel, ranksums, wilcoxon

print('packages imported')


# perform shapiro-wilk test
# def normality_test(df, param, output=False):
#     shapiro_result = shapiro(df[param])
#     pval = shapiro_result[1]
#     if pval > 0.05:
#         print(f'normality test for {param} succeeded! p = {shapiro_result[1]:.2} > 0.05')
#     else:
#         print(f'normality test for {param} failed! p = {shapiro_result[1]:.4} < 0.05')
#     if output:
#         return pval


# perfrom a basic t-test between groups
# def ttest_between_groups(df, param, output=False):
#     healthy, injured = extract_val_for_groups(df, param)
#     test_result = ttest_ind(healthy, injured)
#     pval = test_result.pvalue
#     if pval < 0.05:
#         print(f'{param} between groups are different! p = {pval:.4} < 0.05')
#     else:
#         print(f'{param} between groups are NOT different! p = {pval:.2} > 0.05')
#     if output:
#         return pval, [healthy, injured]