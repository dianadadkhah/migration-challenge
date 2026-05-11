import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/master_clean.csv')

cma = df[df['geography'].str.contains('CMA', na=False)].copy()
cma = cma[cma['immigrant_status'].isin(['Immigrant', 'Non-immigrants'])]

cities = ['Montreal', 'Toronto', 'Edmonton', 'Vancouver']
statuses = ['Immigrant', 'Non-immigrants']

# Build matrix: rows = status, cols = cities, values = renter_owner_gap
matrix = []
annot_gap = []
annot_owner = []
annot_renter = []

for status in statuses:
    row_gap, row_own, row_ren = [], [], []
    for city in cities:
        r = cma[(cma['city']==city) & (cma['immigrant_status']==status)]
        row_gap.append(round(r['renter_owner_gap'].values[0], 1) if len(r) else None)
        row_own.append(round(r['owner_stir'].values[0], 1) if len(r) else None)
        row_ren.append(round(r['renter_stir'].values[0], 1) if len(r) else None)
    matrix.append(row_gap)
    annot_gap.append(row_gap)
    annot_owner.append(row_own)
    annot_renter.append(row_ren)

matrix = np.array(matrix, dtype=float)

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#0e0f13')
ax.set_facecolor('#16181f')

# Color scale: low gap = blue, high gap = orange
im = ax.imshow(matrix, cmap='RdYlBu_r', aspect='auto', vmin=0, vmax=12)

# Labels
ax.set_xticks(range(len(cities)))
ax.set_xticklabels(cities, fontsize=12, color='#e8e6e0')
ax.set_yticks(range(len(statuses)))
ax.set_yticklabels(statuses, fontsize=12, color='#e8e6e0')
ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
ax.tick_params(colors='#7a7870')

# Annotate each cell with 3 lines
for i in range(len(statuses)):
    for j in range(len(cities)):
        gap = annot_gap[i][j]
        own = annot_owner[i][j]
        ren = annot_renter[i][j]
        cell_text = f"Gap: +{gap}pp\nOwner: {own}%\nRenter: {ren}%"
        ax.text(j, i, cell_text, ha='center', va='center',
                fontsize=10, color='#0e0f13', fontweight='bold', linespacing=1.6)

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Renter–Owner Gap (pp)', color='#7a7870', fontsize=9)
cbar.ax.tick_params(colors='#7a7870')

ax.set_title('Renter vs Owner Housing Burden Gap by City & Immigration Status',
             fontsize=13, color='#e8e6e0', pad=30, loc='left', fontweight='bold')
ax.text(0, -0.18,
        'Gap = renter STIR minus owner STIR. Darker red = renters much more burdened than owners.',
        transform=ax.transAxes, fontsize=9, color='#7a7870')

ax.spines[['top','right','left','bottom']].set_visible(False)

plt.tight_layout()
plt.savefig('visuals/chart3_renter_owner_gap.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/chart3_renter_owner_gap.png")