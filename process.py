import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter
from pathlib import Path


HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

# read in csv to pd.DataFrame
subs_df = pd.read_csv(DATA_FOLDER / "filmfreeway-submissions.csv")
desc_df = pd.read_csv(DATA_FOLDER / "descriptions.csv")
### CLEAN ###

# Drop withdrawn entries
subs_df = subs_df[subs_df['Submission Status'] != 'Withdrawn']

# Replace column to shorten: Feel Good Shorts
subs_df['Submission Categories'] = subs_df['Submission Categories'].apply(
        lambda x: x.replace('Short films that make you feel good.', 'Feel Good Shorts')
)

# 'Youth Short Films, Short Documentary' force to 'Short Documentary'
subs_df['Submission Categories'] = subs_df['Submission Categories'].apply(
        lambda x: x.replace('Youth Short Films, Short Documentary', 'Short Documentary')
)

# drop rating, genres cols due to all missing data
subs_df.drop(columns=['Rating', 'Genres'], inplace=True)

# fill na with empty str to allow apply method
subs_df['State'].fillna('', inplace=True)

# replace to unify state names
subs_df['State'] = subs_df['State'].apply(
    lambda x: x.replace('maryland', 'MD')
               .replace('Maryland', 'MD')
               .replace('Virginia', 'VA')
               .replace('Georgia', 'GA')
               .replace('Pennsylvania', 'PA')
               .replace('Florida', 'FL')
               .replace('New York', 'NY')
               .replace('ny', 'NY')
)

# SUBSET SELECTED FILMS
selected_df = subs_df[subs_df['Judging Status']=='Selected']

pd.to_timedelta(selected_df['Duration'])

# new dataframe without necceary columns for export
selected_excel_export = selected_df.drop(columns=['Submission Status', 'Submission ID', 'Birthdate', 'Gender', 'Judging Status', 'Submission Date'])

# Output new spreasheet for Excel
selected_excel_export.sort_values(by='Submission Categories').to_excel(DATA_FOLDER / 'OCFF-2021_selected-films_01-12-21.xlsx')
desc_df.to_excel(DATA_FOLDER / 'descriptions.xlsx')

# DEFINE PLOTTING FUNCTIONS

subs_per_cat = dict(Counter(selected_df['Submission Categories']))
sorted_cat = sorted(subs_per_cat.items(), key=lambda x: x[1])
total_selected = len(selected_df['Project Title'])
labels = [k for k, v in sorted_cat]
number_of_entries = [v for k, v in sorted_cat]
ratios = [(v / total_selected) for k, v in sorted_cat]

# Plot number of submissions
# bar
plt.rcdefaults()
fig, ax = plt.subplots()
_ = ax.barh(np.arange(len(labels)), number_of_entries, align='center')
_ = ax.set_yticks(np.arange(len(labels)))
_ = ax.set_yticklabels(labels)
_ = ax.invert_yaxis()
_ = ax.set_xlabel('Number of Sumbissions')
_ = ax.set_title('Submissions Per Category')
_ = plt.tight_layout()
plt.savefig(DATA_FOLDER / 'entries-per-cat-bar.png')

# pie
fig1, ax = plt.subplots()
_ = ax.pie(ratios, labels=labels, autopct='%1.1f%%', shadow=False, normalize=True)
_ = ax.set_title('Submissions Per Category')
_ = ax.axis('equal') # make sure pie is circle
plt.savefig(DATA_FOLDER / 'entries-per-cat-pie.png', bbox_inches='tight')
