import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/master_clean.csv')

csd = df[~df['geography'].str.contains('CMA|Canada', na=False)]
csd = csd[csd['city'] != 'Other']

cities = ['Montreal', 'Toronto', 'Edmonton', 'Vancouver']
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.patch.set_facecolor('#0e0f13')
axes = axes.flatten()

for i, city in enumerate(cities):
    ax = axes[i]
    ax.set_facecolor('#16181f')

    imm = csd[(csd['city']==city) & (csd['immigrant_status']=='Immigrant')].dropna(subset=['total_income','renter_stir'])
    non = csd[(csd['city']==city) & (csd['immigrant_status']=='Non-immigrants')].dropna(subset=['total_income','renter_stir'])

    ax.scatter(non['total_income'], non['renter_stir'],
               color='#5b9bd5', alpha=0.4, s=35, label='Non-immigrant', zorder=2)
    ax.scatter(imm['total_income'], imm['renter_stir'],
               color='#e8834a', alpha=0.6, s=35, label='Immigrant', zorder=3)

    # Trendlines
    for data, color in [(imm, '#e8834a'), (non, '#5b9bd5')]:
        if len(data) > 2:
            m, b = np.polyfit(data['total_income'], data['renter_stir'], 1)
            x_line = np.linspace(data['total_income'].min(), data['total_income'].max(), 100)
            ax.plot(x_line, m*x_line + b, color=color, linewidth=2, alpha=0.9, zorder=4)

    # 30% line
    ax.axhline(y=30, color='#e05555', linestyle='--', linewidth=1, alpha=0.6)

    # City label
    ax.set_title(city, fontsize=13, color='#e8e6e0', fontweight='bold', loc='left', pad=8)

    # STIR gap annotation
    imm_mean = imm['renter_stir'].mean()
    non_mean = non['renter_stir'].mean()
    gap = imm_mean - non_mean
    sign = '+' if gap >= 0 else ''
    color = '#e8834a' if gap > 0 else '#4dab7e'
    ax.text(0.98, 0.95, f'Imm avg: {imm_mean:.1f}%\nNon-imm avg: {non_mean:.1f}%\nGap: {sign}{gap:.1f}pp',
            transform=ax.transAxes, fontsize=8.5, color=color,
            ha='right', va='top', linespacing=1.6)

    ax.set_xlabel('Household Income ($)', color='#7a7870', fontsize=9)
    ax.set_ylabel('Renter STIR (%)', color='#7a7870', fontsize=9)
    ax.tick_params(colors='#7a7870', labelsize=8)
    ax.spines[['top','right','left','bottom']].set_visible(False)
    ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
    ax.xaxis.grid(True, color='#ffffff', alpha=0.05)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))

    if i == 0:
        ax.legend(framealpha=0, labelcolor='#e8e6e0', fontsize=9)

fig.suptitle('Renter Housing Burden vs Income — By City',
             fontsize=15, color='#e8e6e0', fontweight='bold', y=1.01, x=0.02, ha='left')
fig.text(0.02, -0.01,
         'Each dot = one neighbourhood. Orange trendline above blue = immigrants pay more at every income level.',
         fontsize=9, color='#7a7870')

plt.tight_layout()
plt.savefig('visuals/chart5_income_stir_cities.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/chart5_income_stir_cities.png")