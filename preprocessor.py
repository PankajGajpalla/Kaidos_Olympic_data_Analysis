import pandas as pd


def preprocess(df, region_df):
    # global df, region_df

    #filtering for summer
    df = df[df['Season'] == 'Summer']

    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')

    # drop duplicates
    df.drop_duplicates(inplace=True)

    # create three columns gold silver and bronze
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)

    return df