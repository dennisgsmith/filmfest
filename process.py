import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter
from pathlib import Path

### ETL ###
HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

# read in csv to pd.DataFrame
raw = pd.read_csv(DATA_FOLDER / "filmfreeway-submissions.csv")
subs_df = raw.copy() # dont step on the raw data, assumes data is local

# Drop withdrawn entries
subs_df = subs_df[subs_df['Submission Status'] != 'Withdrawn']
duplicate_entries = subs_df[subs_df['Project Title'].duplicated()==True]

# Replace column to shorten: Feel Good Shorts
subs_df['Submission Categories'] = subs_df['Submission Categories'].apply( \
        lambda x: x.replace('Short films that make you feel good.', 'Feel Good Shorts'))

# Correct 'Youth Short Films, Short Documentary' column
print(subs_df.info())
# Force to 'Short Documentary' for now
subs_df['Submission Categories'] = subs_df['Submission Categories'].apply( \
        lambda x: x.replace('Youth Short Films, Short Documentary', 'Short Documentary'))

subs_per_cat = dict(Counter(subs_df['Submission Categories']))
sorted_sub_cat = sorted(subs_per_cat.items(), key=lambda x: x[1])
total_subs = len(subs_df['Project Title'])


# PLOTTING
labels = [k for k, v in sorted_sub_cat]
ratios = [(v / total_subs) for k, v in sorted_sub_cat]
n_subs = [v for k, v in sorted_sub_cat]
y_pos = np.arange(len(labels)) # Label locations

# BAR CHART
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

# PIE CHART
fig1, ax1 = plt.subplots()
_ = ax1.pie(ratios, labels=labels, autopct='%1.1f%%', shadow=True, normalize=True)
_ = ax.set_title('Entries per Submission Category')
_ = ax1.axis('equal') # make sure pie is circle
plt.savefig(DATA_FOLDER / 'EntriesPerCat_PIE.png', bbox_inches='tight')