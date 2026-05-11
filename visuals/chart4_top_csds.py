import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_csv('data/master_clean.csv')

# CSD level only, immigrants only, sorted by renter STIR
csd = df[~df['geography'].str.contains('CMA|Canada', na=False)]
csd = csd[csd['city'] != 'Other']
imm = csd[csd['immigrant_status'] == 'Immigrant'].dropna(subset=['renter_stir'])
top = imm.nlargest(12, 'renter_stir').sort_values('renter_stir')

city_colors = {
    'Montreal': '#8e75c9',
    'Toronto': '#e8834a',
    'Edmonton': '#4dab7e',
    'Vancouver': '#5b9bd5'
}

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#0e0f13')
ax.set_facecolor('#16181f')

colors = [city_colors.get(c, '#888') for c in top['city']]

bars = ax.barh(top['csd_name'], top['renter_stir'], color=colors, alpha=0.85, height=0.6)

# 30% threshold line
ax.axvline(x=30, color='#e05555', linestyle='--', linewidth=1.2, alpha=0.8)
ax.text(30.2, 11.5, '30%\nthreshold', color='#e05555', fontsize=8, va='top')

# Value labels
for bar, val in zip(bars, top['renter_stir']):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=10, color='#e8e6e0')

# Income annotation on each bar
for i, (_, row) in enumerate(top.iterrows()):
    if pd.notna(row['total_income']):
        ax.text(1, i, f"  income: ${row['total_income']/1000:.0f}k",
                va='center', fontsize=8, color='#7a7870')

# Legend for cities
patches = [mpatches.Patch(color=v, label=k, alpha=0.85) for k,v in city_colors.items()]
ax.legend(handles=patches, framealpha=0, labelcolor='#e8e6e0',
          fontsize=9, loc='lower right')

# Styling
ax.set_xlabel('Immigrant Renter STIR (%)', color='#7a7870', fontsize=11)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.xaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)
ax.set_xlim(0, 40)

ax.set_title('Neighbourhoods Where Immigrant Renters Are Most Burdened',
             fontsize=14, color='#e8e6e0', pad=16, loc='left', fontweight='bold')
ax.text(0, -0.1,
        'Ranked by immigrant renter STIR. Colour = city. Income shown to highlight the paradox.',
        transform=ax.transAxes, fontsize=9, color='#7a7870')

plt.tight_layout()
plt.savefig('visuals/chart4_top_csds.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/chart4_top_csds.png")