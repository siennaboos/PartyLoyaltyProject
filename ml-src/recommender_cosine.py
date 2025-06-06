# import statements
import numpy as np
import pandas as pd

def make_full_df(filepath):
    """
    Creating full DataFrame of MEP info from CSV
    
    Args:
        filepath (str): filepath for csv
    
    Returns:
        df (DataFrame): DataFrame of member info from CSV
    """
    
    df = pd.read_csv(filepath)
    return df

def get_metrics(df, party_name):
    """
    Returns DataFrame with just metrics for recommender, standardizing values from 0-1 scale
    
    Args:
        df (DataFrame): full DataFrame of member info
        party_name (str): inputter's party
    
    Returns:
        df_metrics (DataFrame): DataFrame of standardized metrics for recommender
    """

    # turning percent columns into decimals so all values are standardized - between 0 and 1
    columns_to_decimals = ['percent_agree_current', 'percent_show_up', 'European People’s Party percentage', 'Renew Europe percentage',
     'Progressive Alliance of Socialists and Democrats percentage',
     'European Conservatives and Reformists percentage',
     'Non-attached Members percentage',
     'Europe of Sovereign Nations percentage',
     'The Left in the European Parliament – GUE/NGL percentage',
     'Greens/European Free Alliance percentage',
     'Patriots for Europe percentage', 'Identity and Democracy percentage']
    
    df[columns_to_decimals] = df[columns_to_decimals] / 100

    # stats to compare the MEPs
    df_metrics = df[['party', 'percent_agree_current', 'percent_show_up', 'country', f'{party_name} percentage']]
    
    return df_metrics

def get_encoded_df(df):
   """
   Returns metrics DataFrame with
  
   Args:
       df (DataFrame): DataFrame with standardized metrics for filtering
  
   Returns:
       df_encoded (DataFrame): DataFrame with one-hot encoded categorical metrics
   """
  
   party_dummies = pd.get_dummies(df, columns=['party'], dtype='int', drop_first = True)
   df_encoded = pd.get_dummies(party_dummies, columns=['country'], dtype='int', drop_first = True)
   return df_encoded

def get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party, new_candidate_country):
    """
    Returns a vector of criteria for recommender model
    
    Args:
        percent_agree_current (float): alignment rate for potential recruit's current party 
        percent_attendance (float): attendance rate for votes  
        my_party (str): inputter's party  
        my_party_percentage (float): percent aligned with the inputter's party  
        new_candidate_party (str): party that new candidate is from  
        new_candidate_country (str): country that new candidate is from 
    
    Returns:
        vector (np array): vector of inputted criteria
    """
    
    # creating dictionary with inputted values
    nums = {'percent_agree_current': [percent_agree_current], 
           'percent_show_up': [percent_attendance], 
           f'{my_party} percentage': [my_party_percentage]}

    # creating starter party dictionary
    parties = {'party_European Conservatives and Reformists': [0], 
           'party_European People’s Party': [0],
           'party_Greens/European Free Alliance': [0],
           'party_Identity and Democracy': [0],
           'party_Non-attached Members': [0],
           'party_Patriots for Europe': [0], 
           'party_Progressive Alliance of Socialists and Democrats': [0],
           'party_Renew Europe': [0],
           'party_The Left in the European Parliament – GUE/NGL': [0]}

    # setting candidate party in dct
    for key in parties:
        if key[key.index('_')+1:] == new_candidate_party:
            parties[key] = [1]

    # creatng starter country dictionary
    countries = {'country_Belgium': [0], 
           'country_Bulgaria': [0], 
           'country_Croatia': [0], 
           'country_Cyprus': [0], 
           'country_Czechia': [0],
           'country_Denmark': [0], 
           'country_Estonia': [0], 
           'country_Finland': [0], 
           'country_France': [0],
           'country_Germany': [0], 
           'country_Greece': [0], 
           'country_Hungary': [0], 
           'country_Ireland': [0],
           'country_Italy': [0], 
           'country_Latvia': [0], 
           'country_Lithuania': [0], 
           'country_Luxembourg': [0],
           'country_Malta': [0], 
           'country_Netherlands': [0], 
           'country_Poland': [0], 
           'country_Portugal': [0],
           'country_Romania': [0], 
           'country_Slovakia': [0], 
           'country_Slovenia': [0], 
           'country_Spain': [0],
           'country_Sweden': [0]}

    # setting candidate country in dct
    for key in countries:
        if key[key.index('_')+1:] == new_candidate_country:
            countries[key] = [1]

    # turning combined dictionary into a numpy vector 
    vector = np.array(pd.DataFrame(nums | parties | countries))

    return vector

def get_recommendations(full_df, encoded_df, filters_vec, party_name):
    """
    Returns top 10 MEPs matching inputter's criteria
    
    Args:
        full_df (DataFrame): full df of MEP information 
        encoded_df (DataFrame): df of recommender criteria with encoded categorical variables  
        filters_vec (np array): vector for inputter's criteria 
        party_name (str): inputter's party name
    
    Returns:
        recruits (DataFrame): top 10 MEPs to join the inputter's party 
    """
    
    # initializing lists
    mep_dot_products = []
    mep_cosines = []
    
    # looping through encoded df of metrics
    for idx in range(len(encoded_df)):
        # turning row into a vector 
        row_vec = np.array(encoded_df.iloc[idx]).reshape(-1, 1)
        
        # dot product for filters and row vector
        temp_dot = np.dot(filters_vec, row_vec)
        # getting cosine similarity score
        temp_cos = temp_dot/(np.linalg.norm(filters_vec) * np.linalg.norm(row_vec))
    
        # appending data to the appropriate lists
        mep_dot_products.append(temp_dot[0])
        mep_cosines.append(temp_cos[0])
    
    # creating dictionary of MEP information
    dict_mep = {'mep_id': full_df.id,
            'first_name': full_df.first_name,
            'last_name': full_df.last_name,
            'country': full_df.country,
            'current_party': full_df.party,
            'current_party_alignment': full_df.percent_agree_current,
            f'{party_name} alignment': full_df[f'{party_name} percentage'],
            'attendance_rate': full_df.percent_show_up,
            'mep_dot_product': mep_dot_products,
            'mep_cosine': mep_cosines}
    
    # turning dictionary into DataFrame
    df_mep = pd.DataFrame(dict_mep)
    
    # sorting data by cosine score
    sorted_df_mep = df_mep.sort_values(by='mep_cosine', ascending=False)
    
    # filtering df and returning top 10 MEPs
    filtered_df = sorted_df_mep[sorted_df_mep['current_party'] != party_name]
    recruits = filtered_df.head(10)
    
    # renaming columns for UI organization
    recruits = recruits.rename(columns={'mep_id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name', 'country': 'Country',
                        'current_party': 'Current Party',
                            'current_party_alignment': 'Current Party Alignment Rate', 
                            'attendance_rate': 'Attendance Rate'})

    return recruits

def get_dissenters(df, party_name):
    """
    Returns top 10 dissenting MEPs in the inputter's party
    
    Args:
        df (DataFrame): full df of MEP information
        party_name (str): inputter's party name
    
    Returns:
        dissents (DataFrame): top 10 dissenting MEPs to the inputter's party
    """
    # filtering df to only members in the party who do not have 0% alignment rates
    df = df[df['party'] == party_name]
    df = df[df['percent_agree_current'] != 0]
    
    # filtering df to only features which will be returned
    df = df[['id', 'first_name', 'last_name', 'percent_dissent_current']]

    # getting highest dissenters, renaming columns
    df = df.sort_values(by = 'percent_dissent_current', ascending = False)
    df = df.rename(columns={'id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name', 'percent_dissent_current': 'Dissent Rate'})
    dissents = df.head(10)
    
    return dissents

def search_mep_metrics(df, mep_id):
    """
    Returns information for a single MEP
    
    Args:
        df (DataFrame): full df of MEP information
        mep_id (int): MEP the inputter wants info for
    
    Returns:
        mep_info (DataFrame): a single df row with information about the specified MEP
    """
    # filtering df to only necessary info
    df = df[['id', 'first_name', 'last_name', 'party', 'percent_agree_current', 'percent_dissent_current',
       'percent_show_up', 'country', 'European People’s Party percentage',
       'Renew Europe percentage',
       'Progressive Alliance of Socialists and Democrats percentage',
       'European Conservatives and Reformists percentage',
       'Non-attached Members percentage',
       'Europe of Sovereign Nations percentage',
       'The Left in the European Parliament – GUE/NGL percentage',
       'Greens/European Free Alliance percentage',
       'Patriots for Europe percentage',
       'Identity and Democracy percentage']]

    # renaming columns for organization on UI
    df = df.rename(columns={'id': 'MEP ID', 'first_name': 'First Name', 'last_name': 'Last Name', 
                            'percent_agree_current': 'Current Party Alignment Rate', 
                            'percent_dissent_current': 'Current Party Dissent Rate', 'percent_show_up': 'Attendance Rate',
                            'country': 'Country'})

    # getting and returning the MEP's info
    mep_info = df[df['MEP ID'] == mep_id]
    
    return mep_info

def main():
    """
    Main function
    
    Args:
        None
    
    Returns:
        None
    """
    
    # NOTE: party_name for get_metrics parameter, 
    # first party name in get_filters parameters, 
    # party_name for get_recommendations parameter,
    # and party_name for get_dissenters parameter
    # SHOULD ALL BE THE SAME!!

    # members_cleaned.csv is data in a SQL table
    df = make_full_df('/Users/Trayna/Desktop/PartyLoyaltyProject/ml-src/members_cleaned.csv')
    df_metrics = get_metrics(df, 'Renew Europe')
    df_encoded = get_encoded_df(df_metrics)

    # testing functions
    filters = get_filters(.70, .60, 'Renew Europe', .70, 'Non-attached Members', 'France')
    recs = get_recommendations(df, df_encoded, filters, 'Renew Europe')

    dissenters = get_dissenters(df, 'Renew Europe')

if __name__ == '__main__':
    main()