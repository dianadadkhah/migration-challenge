import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/master_clean.csv')

# CSD-level only, no CMA rows
csd = df[~df['geography'].str.contains('CMA|Canada', na=False)]
csd = csd[csd['city'] != 'Other']

imm = csd[csd['immigrant_status'] == 'Immigrant'].dropna(subset=['total_income','total_stir'])
non = csd[csd['immigrant_status'] == 'Non-immigrants'].dropna(subset=['total_income','total_stir'])

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#0e0f13')
ax.set_facecolor('#16181f')

# Plot non-immigrants first (background)
ax.scatter(non['total_income'], non['total_stir'],
           color='#5b9bd5', alpha=0.35, s=40, label='Non-immigrant', zorder=2)

# Plot immigrants on top
ax.scatter(imm['total_income'], imm['total_stir'],
           color='#e8834a', alpha=0.55, s=40, label='Immigrant', zorder=3)

# Trendlines
for data, color in [(imm, '#e8834a'), (non, '#5b9bd5')]:
    m, b = np.polyfit(data['total_income'], data['total_stir'], 1)
    x_line = np.linspace(data['total_income'].min(), data['total_income'].max(), 100)
    ax.plot(x_line, m*x_line + b, color=color, linewidth=1.8, alpha=0.9, zorder=4)

# 30% threshold line
ax.axhline(y=30, color='#e05555', linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(310000, 30.4, '30% affordability threshold', color='#e05555', fontsize=9, ha='right')

# Annotate key paradox CSDs
paradox = [
    ('Richmond Hill', 153400, 27.1),
    ('West Vancouver', 245000, 30.7),
    ('Aurora', 154000, 27.5),
    ('King', 190600, 26.8),
]
for name, income, stir in paradox:
    ax.annotate(name,
                xy=(income, stir),
                xytext=(income + 8000, stir + 0.8),
                fontsize=8, color='#e8e6e0',
                arrowprops=dict(arrowstyle='->', color='#7a7870', lw=0.8))

# Styling
ax.set_xlabel('Average Household Income ($)', color='#7a7870', fontsize=11)
ax.set_ylabel('Total STIR (%)', color='#7a7870', fontsize=11)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.xaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)

# Format x-axis as $
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))

ax.set_title('The Invisible Tax: Income Does Not Explain the Housing Gap',
             fontsize=14, color='#e8e6e0', pad=16, loc='left', fontweight='bold')
ax.text(0, -0.12,
        'Each dot = one neighbourhood. Higher income should mean lower STIR — for immigrants, the trendline sits persistently higher.',
        transform=ax.transAxes, fontsize=9, color='#7a7870')

ax.legend(framealpha=0, labelcolor='#e8e6e0', fontsize=10, loc='upper right')

plt.tight_layout()
plt.savefig('visuals/chart2_invisible_tax.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/chart2_invisible_tax.png")