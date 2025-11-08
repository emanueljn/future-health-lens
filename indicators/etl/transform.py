import pandas as pd
import numpy as np

def clean_and_interpolate(df: pd.DataFrame, year_col='year', val_col='value'):
    # df: country, year, value
    df = df.drop_duplicates(subset=['country', 'year'])
    df = df.sort_values(['country', 'year'])
    # Pivot; fill missing years within range by interpolation
    def interp_group(g):
        g = g.set_index(year_col).reindex(range(g[year_col].min(), g[year_col].max()+1))
        g[val_col] = g[val_col].interpolate(limit_direction='both')
        g = g.reset_index().rename(columns={'index': year_col})
        return g
    out = df.groupby('country').apply(interp_group).reset_index(drop=True)
    return out