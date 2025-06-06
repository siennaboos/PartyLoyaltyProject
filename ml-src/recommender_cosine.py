# import statements
import numpy as np
import pandas as pd

# creating DataFrame
def make_df(filepath):
    """
    Creating DataFrame from CSV
    
    Args:
        filepath (str): filepath for csv
    
    Returns:
        df (DataFrame): DataFrame of member info from CSV
    """
    
    df = pd.read_csv(filepath)
    return df

# getting vector for searching filters
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

# getting top 10 recommended candidates which match the inputter's criteria
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
        # cosine similarity score
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
    
    # this sorts the data by the cosine score
    sorted_df_mep = df_mep.sort_values(by='mep_cosine', ascending=False)
    
    # filtering df and returning top 10 MEPs
    filtered_df = sorted_df_mep[sorted_df_mep['current_party'] != party_name]
    recruits = filtered_df.head(10)

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

def main():
    """
    Main function
    
    Args:
        None
    
    Returns:
        None
    """
    
    df = make_df('members_cleaned.csv')
    df_encoded = make_df('metrics.csv')

    # testing functions
    filters = get_filters(.70, .60, 'European People’s Party', .70, 'Non-attached Members', 'France')
    recs = get_recommendations(df, df_encoded, filters, 'European People’s Party')

if __name__ == '__main__':
    main()