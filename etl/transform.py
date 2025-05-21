import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor
from utils.salary_cleaner import clean_salary
from utils.classify import classify_category, classify_seniority
from utils.regions_mapping import map_region


def transform_jobicy():
    """
    Transforms the raw Jobicy job data by cleaning salary information, imputing missing values, 
    and encoding categorical features. The transformed data is saved to CSV files for further use.
    
    Reading the raw Jobicy jobs dataset.
    Dropping unnecessary columns.
    Converting salary columns to numeric format and imputing missing values.
    Creating salary_eaned as an average of salary min and max.
    Dropping duplicates and marking partial duplicates.
    Saving the cleaned job data and companies data to CSV files.
    Visualizing the salary distribution after imputation.

    Returns:
        pd.DataFrame: A cleaned DataFrame with transformed Jobicy job data.
    """
    df = pd.read_csv('data/raw/jobicy_jobs.csv')
    df = df.drop(columns=['companyLogo', 'jobSlug'])

    df['pubDate'] = pd.to_datetime(df['pubDate'], errors='coerce')
    df['annualSalaryMin'] = pd.to_numeric(df['annualSalaryMin'], errors='coerce')
    df['annualSalaryMax'] = pd.to_numeric(df['annualSalaryMax'], errors='coerce')
    df['annualSalaryMax'] = df['annualSalaryMax'].replace(0, np.nan)

    df_model = df[['annualSalaryMin', 'annualSalaryMax', 'region', 'jobTitle']].copy()
    df_encoded = pd.get_dummies(df_model, columns=['region', 'jobTitle'])

    imputer = IterativeImputer(estimator=RandomForestRegressor(n_estimators=10, random_state=0), max_iter=10, random_state=0)
    df_imputed_array = imputer.fit_transform(df_encoded)
    df_imputed = pd.DataFrame(df_imputed_array, columns=df_encoded.columns)

    df['annualSalaryMin'] = df_imputed['annualSalaryMin']
    df['annualSalaryMax'] = df_imputed['annualSalaryMax']
    df['salary_cleaned'] = (df['annualSalaryMin'] + df['annualSalaryMax']) / 2

    df = df[['jobTitle', 'companyName', 'annualSalaryMin', 'annualSalaryMax', 'salary_cleaned', 'pubDate', 'region']]
    df = df.drop_duplicates()
    df['is_partial_duplicate'] = df.duplicated(subset=['jobTitle', 'companyName', 'annualSalaryMin', 'annualSalaryMax', 'pubDate'], keep=False)

    os.makedirs('data/processed', exist_ok=True)
    df.drop(columns='is_partial_duplicate').to_csv('data/processed/jobs_data.csv', index=False)

    companies_df = df[['companyName']].drop_duplicates()
    companies_df.to_csv('data/processed/companies_data.csv', index=False)

    # Visualizations
    os.makedirs('visualizations/imputation_metrics/jobicy', exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes[0, 0].hist(df_imputed['annualSalaryMin'], bins=30, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('After Imputation: annualSalaryMin')
    axes[0, 1].hist(df_imputed['annualSalaryMax'], bins=30, color='salmon', edgecolor='black')
    axes[0, 1].set_title('After Imputation: annualSalaryMax')
    axes[1, 0].boxplot(df_imputed['annualSalaryMin'], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
    axes[1, 0].set_title('After Imputation: annualSalaryMin')
    axes[1, 1].boxplot(df_imputed['annualSalaryMax'], vert=False, patch_artist=True, boxprops=dict(facecolor='salmon'))
    axes[1, 1].set_title('After Imputation: annualSalaryMax')
    plt.tight_layout()
    plt.savefig('visualizations/imputation_metrics/jobicy/salary_metrics.png')
    plt.close()

    return df


def transform_remotive():
    """
    Transforms the raw Remotive job data by cleaning salary information, imputing missing values, 
    and encoding categorical features. Non-numeric salaries are logged for further inspection.

    Cleans salary data using a custom function and IterativeImputer.
    Saves non-numeric salary entries for later review.
    Encodes categorical variables using one-hot encoding.
    Imputes missing salary values.
    Removes duplicates and saves the cleaned data to a CSV file.

    Returns:
        pandas.DataFrame: The transformed Remotive job data with cleaned and imputed salary information.
    """
    df = pd.read_csv('data/raw/remotive_jobs.csv')
    df = df.drop(columns=['company_logo', 'tags', 'company_logo_url'], errors='ignore')

    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
    df['salary'] = df['salary'].astype(str)
    df['salary_cleaned'] = df['salary'].apply(lambda x: clean_salary(str(x)) if isinstance(x, str) else x)
    df['salary_cleaned'] = pd.to_numeric(df['salary_cleaned'], errors='coerce')

    non_numeric_salaries_df = df[df['salary_cleaned'].isna()][['salary', 'title', 'company_name']]
    non_numeric_salaries_df.to_csv('data/processed/non_numeric_salaries.csv', index=False)

    df_remotive_model = df[['salary_cleaned', 'title', 'company_name', 'category', 'job_type', 'candidate_required_location']].copy()
    df_remotive_model = df_remotive_model.dropna(axis=1, how='all')
    df_encoded = pd.get_dummies(df_remotive_model, drop_first=True)

    imputer = IterativeImputer(estimator=RandomForestRegressor(n_estimators=10, random_state=0), max_iter=10, random_state=0)
    df_imputed_array = imputer.fit_transform(df_encoded)
    df_imputed = pd.DataFrame(df_imputed_array, columns=df_encoded.columns)

    df['salary_cleaned'] = df_imputed['salary_cleaned']
    df = df.drop_duplicates()
    df.to_csv('data/processed/remotive_jobs_transformed.csv', index=False)

    return df

def combine_datasets():
    """
    Renames columns to create consistency between datasets.
    Applies region mapping to standardize location data.
    Classifies job categories and seniority levels based on job titles.
    Saves the combined dataset to a CSV file for further analysis.

    Returns:
        pandas.DataFrame: The combined and processed job data from both Jobicy and Remotive sources.
    """
    jobicy_df = pd.read_csv('data/processed/jobs_data.csv')
    remotive_df = pd.read_csv('data/processed/remotive_jobs_transformed.csv')

    remotive_df = remotive_df.rename(columns={
        'title': 'jobTitle',
        'company_name': 'companyName',
        'publication_date': 'pubDate',
        'candidate_required_location': 'region'
    })

    common_cols = ['jobTitle', 'companyName', 'salary_cleaned', 'pubDate', 'region']
    jobicy_df = jobicy_df[common_cols]
    remotive_df = remotive_df[common_cols]

    combined_df = pd.concat([jobicy_df, remotive_df], ignore_index=True)

    combined_df['region'] = combined_df['region'].apply(map_region)

    print(combined_df.columns)

    combined_df['category'] = combined_df['jobTitle'].apply(classify_category)

    combined_df['seniority'] = combined_df['jobTitle'].apply(classify_seniority)

    combined_df = combined_df.drop_duplicates()

    combined_df.to_csv('data/processed/all_jobs.csv', index=False)
    print(f"Archivo combinado guardado con {combined_df.shape[0]} filas.")



if __name__ == "__main__":
    print("Transformando datos de Jobicy...")
    df_jobicy = transform_jobicy()
    print(f"Jobicy procesado: {df_jobicy.shape}")

    print("\nTransformando datos de Remotive...")
    df_remotive = transform_remotive()
    print(f"Remotive procesado: {df_remotive.shape}")

    print("\n Concatenating datasets... ")
    combined_df = combine_datasets()
