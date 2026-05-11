import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv('data/master_clean.csv')
cma = df[df['geography'].str.contains('CMA', na=False)]

cities = ['Montreal', 'Toronto', 'Edmonton', 'Vancouver']

imm = cma[cma['immigrant_status']=='Immigrant'].set_index('city')
non = cma[cma['immigrant_status']=='Non-immigrants'].set_index('city')

# Data for 3 panels
income_gap    = [non.loc[c,'total_income'] - imm.loc[c,'total_income'] for c in cities]
stir_gap      = [imm.loc[c,'total_stir']   - non.loc[c,'total_stir']   for c in cities]
renter_stir   = [imm.loc[c,'renter_stir']  for c in cities]

fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.patch.set_facecolor('#0e0f13')

colors_city = ['#8e75c9','#e8834a','#4dab7e','#5b9bd5']

# --- Panel 1: Income gap ---
ax = axes[0]
ax.set_facecolor('#16181f')
bars = ax.bar(cities, income_gap, color=colors_city, alpha=0.85, width=0.5)
for bar, val in zip(bars, income_gap):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+300,
            f'${val/1000:.0f}k', ha='center', fontsize=10, color='#e8e6e0', fontweight='bold')
ax.set_title('Income Gap\n(Non-imm minus Immigrant)', fontsize=11, color='#e8e6e0', pad=10)
ax.set_ylabel('$ per year', color='#7a7870', fontsize=9)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x/1000:.0f}k'))

# --- Panel 2: STIR gap ---
ax = axes[1]
ax.set_facecolor('#16181f')
bar_colors = ['#e8834a' if v > 0 else '#4dab7e' for v in stir_gap]
bars = ax.bar(cities, stir_gap, color=bar_colors, alpha=0.85, width=0.5)
ax.axhline(y=0, color='#7a7870', linewidth=0.8)
for bar, val in zip(bars, stir_gap):
    ypos = val + 0.05 if val >= 0 else val - 0.25
    ax.text(bar.get_x()+bar.get_width()/2, ypos,
            f'{val:+.1f}pp', ha='center', fontsize=10, color='#e8e6e0', fontweight='bold')
ax.set_title('STIR Gap\n(Immigrant minus Non-immigrant)', fontsize=11, color='#e8e6e0', pad=10)
ax.set_ylabel('Percentage points', color='#7a7870', fontsize=9)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)
ax.text(0.5, -0.15, 'Orange = immigrants pay more  |  Green = immigrants pay less',
        transform=ax.transAxes, ha='center', fontsize=8, color='#7a7870')

# --- Panel 3: Immigrant renter STIR vs 30% line ---
ax = axes[2]
ax.set_facecolor('#16181f')
bar_colors2 = ['#e05555' if v >= 30 else '#e8834a' for v in renter_stir]
bars = ax.bar(cities, renter_stir, color=bar_colors2, alpha=0.85, width=0.5)
ax.axhline(y=30, color='#e05555', linestyle='--', linewidth=1.2, alpha=0.8)
ax.text(3.4, 30.2, '30%', color='#e05555', fontsize=9)
for bar, val in zip(bars, renter_stir):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
            f'{val:.1f}%', ha='center', fontsize=10, color='#e8e6e0', fontweight='bold')
ax.set_title('Immigrant Renter STIR\n(vs 30% affordability threshold)', fontsize=11, color='#e8e6e0', pad=10)
ax.set_ylabel('STIR (%)', color='#7a7870', fontsize=9)
ax.set_ylim(0, 33)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)

fig.suptitle('Three Dimensions of the Immigrant Housing Penalty',
             fontsize=15, color='#e8e6e0', fontweight='bold', y=1.03, x=0.02, ha='left')
fig.text(0.02, -0.04,
         'Left: income gap driving vulnerability. Centre: STIR gap showing burden is not income-explained. Right: how close immigrant renters are to the affordability crisis threshold.',
         fontsize=9, color='#7a7870', wrap=True)

plt.tight_layout()
plt.savefig('visuals/chart6_policy_summary.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/chart6_policy_summary.png")