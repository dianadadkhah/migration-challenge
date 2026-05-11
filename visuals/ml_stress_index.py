import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv('data/master_clean.csv')

# === SETUP ===
csd = df[~df['geography'].str.contains('CMA|Canada', na=False)]
csd = csd[csd['city'] != 'Other']

imm = csd[csd['immigrant_status'] == 'Immigrant'].copy()
non = csd[csd['immigrant_status'] == 'Non-immigrants'].copy()

# Merge immigrant and non-immigrant on csd_name + city
merged = imm.merge(
    non[['csd_name', 'city', 'total_income', 'total_stir', 'renter_stir', 'owner_stir']],
    on=['csd_name', 'city'],
    suffixes=('_imm', '_non')
)
merged = merged.dropna(subset=[
    'total_stir_imm', 'renter_stir_imm',
    'total_income_imm', 'total_income_non'
])

print(f"Neighbourhoods with both immigrant and non-immigrant data: {len(merged)}")

# === COMPONENT 1: STIR above 30% threshold ===
# How far above (or below) the 30% affordability threshold
# Capped at 0 minimum (being below threshold doesn't help your score)
merged['c1_threshold'] = (merged['renter_stir_imm'] - 30).clip(lower=-5)

# === COMPONENT 2: Income gap ===
# How much less immigrants earn vs non-immigrants in same neighbourhood
merged['c2_income_gap'] = merged['total_income_non'] - merged['total_income_imm']

# === COMPONENT 3: Regression residual ===
# How much more immigrants pay than their income+city predicts
model_data = csd[csd['immigrant_status'].isin(['Immigrant','Non-immigrants'])].dropna(
    subset=['total_stir','total_income','city','immigrant_status']
)
X = model_data[['total_income','city','immigrant_status']]
y = model_data['total_stir']

preprocessor = ColumnTransformer(transformers=[
    ('num', 'passthrough', ['total_income']),
    ('cat', OneHotEncoder(drop='first', sparse_output=False), ['city','immigrant_status'])
])
pipe = Pipeline([('pre', preprocessor), ('reg', LinearRegression())])
pipe.fit(X, y)

imm_only = csd[csd['immigrant_status']=='Immigrant'].dropna(subset=['total_stir','total_income','city'])
imm_only = imm_only.copy()
imm_only['predicted'] = pipe.predict(imm_only[['total_income','city','immigrant_status']])
imm_only['residual'] = imm_only['total_stir'] - imm_only['predicted']

merged = merged.merge(
    imm_only[['csd_name','city','residual']],
    on=['csd_name','city'],
    how='left'
)
merged['c3_residual'] = merged['residual'].fillna(0)

# === BUILD IHSI ===
# Normalize each component to 0-100 using MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 100))
components = ['c1_threshold', 'c2_income_gap', 'c3_residual']
merged[components] = scaler.fit_transform(merged[components])

# Weighted average: threshold 40%, income gap 30%, residual 30%
merged['IHSI'] = (
    merged['c1_threshold'] * 0.40 +
    merged['c2_income_gap'] * 0.30 +
    merged['c3_residual'] * 0.30
).round(1)

merged = merged.sort_values('IHSI', ascending=False)

print()
print("=" * 60)
print("IMMIGRANT HOUSING STRESS INDEX (IHSI) — TOP 15")
print("Higher = more stressed. Scale: 0 to 100.")
print("=" * 60)
print(merged[['csd_name','city','IHSI','renter_stir_imm',
              'total_income_imm','c1_threshold','c2_income_gap','c3_residual']
     ].head(15).round(1).to_string())

print()
print("=" * 60)
print("IHSI — BOTTOM 10 (least stressed)")
print("=" * 60)
print(merged[['csd_name','city','IHSI','renter_stir_imm','total_income_imm']
     ].tail(10).round(1).to_string())

print()
print("=" * 60)
print("AVERAGE IHSI BY CITY")
print("=" * 60)
city_avg = merged.groupby('city')['IHSI'].agg(['mean','median','max']).round(1)
print(city_avg.to_string())

# === PLOT ===
fig, axes = plt.subplots(1, 2, figsize=(15, 7))
fig.patch.set_facecolor('#0e0f13')

# --- Plot 1: Top 20 and Bottom 10 neighbourhoods ---
ax = axes[0]
ax.set_facecolor('#16181f')

top20 = merged.head(20)
city_colors = {
    'Montreal': '#8e75c9',
    'Toronto': '#e8834a',
    'Edmonton': '#4dab7e',
    'Vancouver': '#5b9bd5'
}
colors = [city_colors.get(c, '#888') for c in top20['city']]

bars = ax.barh(range(len(top20)), top20['IHSI'],
               color=colors, alpha=0.85, height=0.7)
ax.set_yticks(range(len(top20)))
ax.set_yticklabels(
    [f"{row['csd_name']} ({row['city'][:3]})"
     for _, row in top20.iterrows()],
    fontsize=9, color='#e8e6e0'
)
ax.invert_yaxis()

for bar, val in zip(bars, top20['IHSI']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.0f}', va='center', fontsize=9, color='#e8e6e0')

ax.set_xlabel('IHSI Score (0–100)', color='#7a7870', fontsize=11)
ax.set_title('Top 20 Most Stressed Immigrant Neighbourhoods\nImmigrant Housing Stress Index (IHSI)',
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold')
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.xaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)

# City legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=v, alpha=0.85, label=k)
                   for k, v in city_colors.items()]
ax.legend(handles=legend_elements, framealpha=0,
          labelcolor='#e8e6e0', fontsize=9, loc='lower right')

# --- Plot 2: IHSI distribution by city ---
ax = axes[1]
ax.set_facecolor('#16181f')

cities = ['Montreal', 'Toronto', 'Edmonton', 'Vancouver']
positions = [1, 2, 3, 4]

for pos, city in zip(positions, cities):
    data = merged[merged['city'] == city]['IHSI']
    bp = ax.boxplot(data, positions=[pos], widths=0.5,
                    patch_artist=True,
                    boxprops=dict(facecolor=city_colors[city], alpha=0.7),
                    medianprops=dict(color='#e8e6e0', linewidth=2),
                    whiskerprops=dict(color='#7a7870'),
                    capprops=dict(color='#7a7870'),
                    flierprops=dict(marker='o', color=city_colors[city],
                                   alpha=0.5, markersize=5))
    mean_val = data.mean()
    ax.text(pos, mean_val + 1.5, f'avg\n{mean_val:.0f}',
            ha='center', fontsize=8, color='#e8e6e0')

ax.set_xticks(positions)
ax.set_xticklabels(cities, fontsize=11, color='#e8e6e0')
ax.set_ylabel('IHSI Score', color='#7a7870', fontsize=11)
ax.set_title('IHSI Distribution by City\n(median, spread, and outliers)',
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold')
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)

fig.text(0.02, -0.02,
         'IHSI combines three components: proximity to 30% STIR threshold (40%), '
         'income gap vs non-immigrants (30%), regression residual (30%).\n'
         'Higher score = greater immigrant housing stress. '
         'Developed for the Migration Data Challenge 2026.',
         fontsize=8, color='#7a7870')

plt.tight_layout()
plt.savefig('visuals/ml_stress_index.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print()
print("Saved: visuals/ml_stress_index.png")