import pandas as pd
from scipy.stats import pearsonr

def compute_correlations(df_wide):
    # df_wide: index=year, columns=indicator codes (per country)
    corr = df_wide.corr(method='pearson')
    pvals = pd.DataFrame(index=corr.index, columns=corr.columns, data=None)
    for a in corr.columns:
        for b in corr.columns:
            s1 = df_wide[a].dropna()
            s2 = df_wide[b].dropna()
            common = pd.concat([s1, s2], axis=1).dropna()
            if len(common) >= 3:
                p = pearsonr(common[a], common[b])
                pvals.loc[a,b] = p.pvalue
            else:
                pvals.loc[a,b] = None
    return corr, pvals