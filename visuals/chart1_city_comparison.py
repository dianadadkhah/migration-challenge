import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv('data/master_clean.csv')

# Get CMA-level rows only (the 4 city summaries)
cma = df[df['geography'].str.contains('CMA', na=False)].copy()
imm = cma[cma['immigrant_status'] == 'Immigrant'].set_index('city')
non = cma[cma['immigrant_status'] == 'Non-immigrants'].set_index('city')

cities = ['Montreal', 'Toronto', 'Edmonton', 'Vancouver']
x = np.arange(len(cities))
width = 0.2

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#0e0f13')
ax.set_facecolor('#16181f')

# Plot 4 bar groups: imm owner, non owner, imm renter, non renter
bars1 = ax.bar(x - width*1.5, [imm.loc[c,'owner_stir'] for c in cities], width, label='Immigrant — Owner',  color='#e8834a', alpha=0.9)
bars2 = ax.bar(x - width*0.5, [non.loc[c,'owner_stir'] for c in cities], width, label='Non-immigrant — Owner', color='#5b9bd5', alpha=0.9)
bars3 = ax.bar(x + width*0.5, [imm.loc[c,'renter_stir'] for c in cities], width, label='Immigrant — Renter', color='#e8834a', alpha=0.55)
bars4 = ax.bar(x + width*1.5, [non.loc[c,'renter_stir'] for c in cities], width, label='Non-immigrant — Renter', color='#5b9bd5', alpha=0.55)

# 30% affordability threshold line
ax.axhline(y=30, color='#e05555', linestyle='--', linewidth=1.2, alpha=0.8)
ax.text(3.85, 30.4, '30% threshold', color='#e05555', fontsize=9, ha='right')

# Value labels on bars
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                f'{h:.1f}', ha='center', va='bottom',
                fontsize=8, color='#e8e6e0')

# Styling
ax.set_xticks(x)
ax.set_xticklabels(cities, fontsize=12, color='#e8e6e0')
ax.set_ylabel('STIR (%)', color='#7a7870', fontsize=11)
ax.set_ylim(0, 35)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)

# Title
ax.set_title('Housing Cost Burden by City, Tenure & Immigration Status',
             fontsize=14, color='#e8e6e0', pad=16, loc='left', fontweight='bold')
ax.text(0, -0.12, 'STIR = Shelter-to-Income Ratio. Darker bars = owners. Lighter bars = renters.',
        transform=ax.transAxes, fontsize=9, color='#7a7870')

# Legend
ax.legend(loc='upper left', framealpha=0, labelcolor='#e8e6e0', fontsize=9)

plt.tight_layout()
plt.savefig('visuals/chart1_city_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/chart1_city_comparison.png")