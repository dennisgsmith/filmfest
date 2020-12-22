import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter
from pathlib import Path


HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

# read in csv to pd.DataFrame
raw = pd.read_csv(DATA_FOLDER / "filmfreeway-submissions.csv")
subs_df = raw.copy() # shallow copy

### CLEAN ###

# Drop withdrawn entries
subs_df = subs_df[subs_df['Submission Status'] != 'Withdrawn']

# There are no duplicate entries
# duplicate_entries = subs_df[subs_df['Project Title'].duplicated()==True]

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

### EDA ###

# Convert Duration column to timedelta datatype
subs_df['Duration'] = pd.to_timedelta(subs_df['Duration'])

# Get Duration metrics per category
duration_per_cat = subs_df.groupby(by='Submission Categories')['Duration'].apply(
        lambda x: x.astype('timedelta64[m]').describe().round(decimals=2)
)

subs_per_cat = dict(Counter(subs_df['Submission Categories']))
sorted_sub_cat = sorted(subs_per_cat.items(), key=lambda x: x[1])
total_subs = len(subs_df['Project Title'])

### PLOT ###

labels = [k for k, v in sorted_sub_cat]
ratios = [(v / total_subs) for k, v in sorted_sub_cat]
n_subs = [v for k, v in sorted_sub_cat]
y_pos = np.arange(len(labels)) # Label locations


def make_bar():
        plt.rcdefaults()
        fig, ax = plt.subplots()
        _ = ax.barh(y_pos, n_subs, align='center')
        _ = ax.set_yticks(y_pos)
        _ = ax.set_yticklabels(labels)
        _ = ax.invert_yaxis()
        _ = ax.set_xlabel('Number of Submissions')
        _ = ax.set_title('Entries per Submission Category')
        _ = plt.tight_layout()
        plt.savefig(DATA_FOLDER / 'EntriesPerCat_BAR.png')


def make_pie():
        fig1, ax = plt.subplots()
        _ = ax.pie(ratios, labels=labels, autopct='%1.1f%%', shadow=False, normalize=True)
        _ = ax.set_title('Entries per Submission Category')
        _ = ax.axis('equal') # make sure pie is circle
        plt.savefig(DATA_FOLDER / 'EntriesPerCat_PIE.png', bbox_inches='tight')


def main():
        make_bar()
        make_pie()


if __name__ == "__main__":
        main()