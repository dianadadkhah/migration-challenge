import pandas as pd
import re

# === LOAD DATA ===
mtl = pd.read_csv('data/Cleaned_Mtl_Data.csv', encoding='latin1')

raw = pd.read_csv('data/Mtl_Tor_Edm_Van_CSDs_Natasha.csv', encoding='latin1', header=None, skiprows=5)
raw.columns = [
    'geography', 'immigrant_status',
    'total_pop', 'total_income', 'total_stir',
    'owner_pop', 'owner_income', 'owner_stir',
    'renter_pop', 'renter_income', 'renter_stir'
]

# Fix leading spaces in status column
raw['immigrant_status'] = raw['immigrant_status'].str.strip()

# Keep only the 3 valid statuses
valid = ['Total Immigrant Status', 'Non-immigrants', 'Immigrant']
df = raw[raw['immigrant_status'].isin(valid)].copy()

# Convert all number columns
num_cols = ['total_pop','total_income','total_stir',
            'owner_pop','owner_income','owner_stir',
            'renter_pop','renter_income','renter_stir']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Calculate renter-owner gap
df['renter_owner_gap'] = df['renter_stir'] - df['owner_stir']

# Tag each row with its city
def tag_city(g):
    g = str(g)
    if 'Montréal (CMA)' in g: return 'Montreal'
    if 'Toronto (CMA)' in g: return 'Toronto'
    if 'Edmonton (CMA)' in g: return 'Edmonton'
    if 'Vancouver (CMA)' in g: return 'Vancouver'
    for code in [str(i) for i in range(2452,2477)]:
        if '('+code in g: return 'Montreal'
    for code in [str(i) for i in range(3518,3544)]:
        if '('+code in g: return 'Toronto'
    for code in [str(i) for i in range(4810,4814)]:
        if '('+code in g: return 'Edmonton'
    for code in [str(i) for i in range(5915,5922)]:
        if '('+code in g: return 'Vancouver'
    return 'Other'

df['city'] = df['geography'].apply(tag_city)

# Extract clean CSD name
def extract_name(g):
    m = re.match(r'^(.+?)\s*\(', str(g))
    return m.group(1).strip() if m else str(g)[:30]

df['csd_name'] = df['geography'].apply(extract_name)

print("Shape:", df.shape)
print("Cities:", df['city'].value_counts().to_dict())
print("Statuses:", df['immigrant_status'].value_counts().to_dict())
print("Done.")



# === SAVE CLEAN DATA ===
df.to_csv('data/master_clean.csv', index=False)
print("Saved to data/master_clean.csv")