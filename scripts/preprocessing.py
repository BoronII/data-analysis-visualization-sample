import pandas as pd
import numpy  as np

from pathlib      import Path
from Preprocessor import Preprocessor

# The data sets are loaded in and processed in sequence

if __name__ == '__main__':
    
    path = Path('../data')
    
    # Work on Social Services Dataset-----------------------------------------
    
    #load in social services dataset
    ss_data = pd.read_excel(path/'social_services_data/SocialServicesData.xls')
    
    ss_preproc = Preprocessor(ss_data)
    
    # Drop rows where the depdant variable is missing
    ss_preproc.dropna(['Support_Services'])
    
    # dict for remapping 'Income_Group' column entries
    income_group = {1.0: 'Under $5,000', 2.0: '$5,000-$9,999',
                    3.0: '$10,000-$12,499', 4.0: '$12,500-$14,999',
                    5.0: '$15,000-$17,499', 6.0: '$17,500-$19,999',
                    7.0: '$20,000-$22,499', 8.0: '$22,500-$24,999',
                    9.0: '$25,000-$27,499', 10.0: '$27,500-$29,999',
                    11.0: '$30,000-$34,999', 12.0: '$35,000-$39,999',
                    13.0: '$40,000-$44,999', 14.0: '$45,000-$49,999',
                    15.0: '$50,000-$54,999', 16.0: '$55,000-$59,999',
                    17.0: '$60,000-$64,999', 18.0: '$65,000-$69,999',
                    19.0: '$70,000-$74,999', 20.0: '$75,000-$79,999',
                    21.0: '$80,000-$89,999', 22.0: '$90,000-$99,999',
                    23.0: '$100,000-$109,999', 24.0: '$110,000-$124,999',
                    25.0: '$125,000-$149,999', 26.0: '$150,000-$174,999',
                    27.0: '$175,000-$249,999', 28.0: '$250,000 or more'}
    
    # dict for remapping 'Retired_Status' column
    retirement_status = {'1. Retired': 'Retired', 
                      '0. Not Retired': 'Not Retired'}
    
    # dict for remapping 'Employment_Status' column
    employment_status = {'0. Unemployed': 'Unemployed', 
                         '1. Employed': 'Employed'}
    
    # dict for remapping 'Ideology' column
    ideology = {'1. Extremely Liberal': 'Extremely Liberal',
                '2. Liberal': 'Liberal',
                '3. Slightly Liberal': 'Slightly Liberal',
                '4. Moderate': 'Moderate',
                '5. Slightly Conservative': 'Slightly Conservative',
                '6. Conservative': 'Conservative',
                '7. Extremely Conservative': 'Extremely Conservative'}
    
    # dict for remapping 'Trust_In_Gov' column
    trust_in_gov = {'1. Always': 'Always',
                    '2. Most of the time': 'Most of the time',
                    '3. About half the time': 'About half the time',
                    '4. Some of the time': 'Some of the time',
                    '5. Never': 'Never'}
    
    
    columns = ['Income_Group', 'Retirement_Status', 'Employment_Status', 
               'Ideology', 'Trust_In_Gov']
    
    mappers = {'Income_Group': income_group, 
               'Retirement_Status': retirement_status, 
               'Employment_Status': employment_status,
               'Ideology': ideology,
               'Trust_In_Gov': trust_in_gov}
    
    assert len(columns)==len(mappers)
   
    ss_preproc.map(columns, mappers)
    
    ss_preproc.save('social_services_data_processed.csv')
    
    # Work on Turkey Political Opinions Dataset-------------------------------
    
    political_opinions = pd.read_csv(path/'turkey_political_opinion/yonelimfinal.csv', 
                                     low_memory=False)
    
    po_preproc = Preprocessor(political_opinions)
    
    # dict for translating columns into english
    columns_eng = {'Timestamp': 'Timestamp',
                   'Cinsiyet': 'Sex',
                   'Yas': 'Age',
                   'Bolge':'City',
                   'Egitim': 'Education level',
                   'soru1': 'Q1',
                   'soru2': 'Q2',
                   'soru3': 'Q3',
                   'soru4': 'Q4',
                   'soru5': 'Q5',
                   'soru6': 'Q6',
                   'soru7': 'Q7',
                   'soru8': 'Q8',
                   'soru9': 'Q9',
                   'soru10': 'Q10',
                   'parti': 'Political View'}
    
    po_preproc.map_cols(columns_eng)
    
    # dict for mapping 'Sex' column
    sex = {'Erkek': 'Male',
           'Kadın': 'Female'}
    
    #dict for mapping 'Education level' columun
    education_level = {'Lisans': 'University',
                       'İlkokul': 'Primary School',
                       'Ortaokul': 'Junior High School',
                       'Lise': 'High School',
                       'Lisans Üstü': 'MA',
                       'Ön Lisans': 'Associate Degree'}
    columns = ['Sex', 'Education level']
    
    mappers = {'Sex': sex ,'Education level': education_level}
    
    assert len(columns)==len(mappers)
    
    po_preproc.map(columns, mappers)
    
    # The columns that need need the yes/no response translated to english
    response_cols = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10']
    
    # dict for translating response columns
    response = {'Hayır': 'No',
                'Evet': 'Yes'}
    
    assert len(response_cols)!=len(response)
    
    po_preproc.map(response_cols, response)
    
    po_preproc.save('turkey_political_opinions_processed.csv')
    
    # Work on US presidential approval Datasets-------------------------------
    obama = pd.read_csv(path/'presidential_approval_huffpost/obama.csv', 
                        low_memory=False)
    
    trump = pd.read_csv(path/'presidential_approval_huffpost/trump.csv', 
                        low_memory=False)
    
    obama_preproc = Preprocessor(obama)
    trump_preproc = Preprocessor(trump)
    
    # Columns to drop
    to_drop = ['survey_question']
    
    obama_preproc.drop(to_drop)
    trump_preproc.drop(to_drop)
    
    assert np.all(obama_preproc.columns==trump_preproc.columns)
    
    # dict for renaming columns
    columns_new = {'survey_organization': 'survey_organization',
               'party_affiliation': 'party_affiliation',
               'start_date': 'start_date',
               'end_date': 'end_date',
               'survey_method': 'method',
               'survey_population': 'population',
               'survey_sample': 'sample_size',
               'approve_percent': 'pct_approval',
               'disapprove_percent': 'pct_disapproval',
               'undecided_percent': 'pct_undecided',
               'margin_of_error': 'margin_of_error'}
    
    obama_preproc.map_cols(columns_new)
    trump_preproc.map_cols(columns_new)
    
    assert np.all(obama_preproc.columns==trump_preproc.columns)
    
    trump_preproc.save('trump_processed.csv')
    obama_preproc.save('obama_processed.csv')
    
    # Work on basic income support Datasets-----------------------------------
    
    basic_income_support = pd.read_csv(path/'basic_income_survey_europe_2016/basic_income_dataset_dalia.csv', 
                                       low_memory=True)
    
    bi_preproc = Preprocessor(basic_income_support)
    
    # columns to drop
    to_drop = ['weight', 'uuid']
    
    bi_preproc.drop(to_drop)
    
    # dicts for renaming columns
    columns_new = {'country_code': 'country_code', 
                   'age': 'age',
                   'gender': 'gender', 
                   'rural': 'rural', 
                   'dem_education_level': 'education_level',
                   'dem_full_time_job': 'full_time_job', 
                   'dem_has_children': 'has_children',
                   'question_bbi_2016wave4_basicincome_awareness': 'awareness',
                   'question_bbi_2016wave4_basicincome_vote': 'vote',
                   'question_bbi_2016wave4_basicincome_effect': 'effect',
                   'question_bbi_2016wave4_basicincome_argumentsfor': 'arguments_for',
                   'question_bbi_2016wave4_basicincome_argumentsagainst': 'arguments_against',
                   'age_group': 'age_group'}
    
    bi_preproc.map_cols(columns_new)
        
    # dict for remapping age column 
    age_group = {'40_65': '40-65', '26_39': '26-39', '14_25': '14-25'}
    
    # dict for remapping effect column
    effect = {'None of the above': 'None of the above',
              'A basic income would not affect my work choices': 'A basic income would not affect my work choices',
              '‰Û_ gain additional skills': 'gain additional skills',
              '‰Û_ work less': 'work less',
              '‰Û_ work as a freelancer': 'work as a freelancer',
              '‰Û_ do more volunteering work': 'do more volunteering work',
              '‰Û_ stop working': 'stop working',
              '‰Û_ spend more time with my family': 'spend more time with my family',
              '‰Û_ look for a different job': 'look for a different job'}
    
    # columns to be remapped
    columns = ['age_group', 'effect']
    
    mappers = {'age_group': age_group, 'effect': effect}
    
    assert len(columns)==len(mappers)
    
    bi_preproc.map(columns, mappers)
    
    bi_preproc.save('basic_income_support_processed.csv')

    print('Success')
    
    