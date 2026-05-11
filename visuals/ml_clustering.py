import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/master_clean.csv')

# CSD level, immigrants only, drop nulls
csd = df[~df['geography'].str.contains('CMA|Canada', na=False)]
csd = csd[csd['city'] != 'Other']
imm = csd[csd['immigrant_status'] == 'Immigrant'].dropna(
    subset=['total_income', 'total_stir', 'renter_stir', 'owner_stir', 'renter_owner_gap']
).copy()

# === FEATURES FOR CLUSTERING ===
# We use income, total STIR, renter STIR, owner STIR, and the gap
# This groups neighbourhoods by their full housing burden profile
features = ['total_income', 'total_stir', 'renter_stir', 'owner_stir', 'renter_owner_gap']
X = imm[features].copy()

# Standardize so no single feature dominates
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === FIND OPTIMAL K ===
# Run KMeans for k=2 to 8, record inertia (elbow method)
inertias = []
ks = range(2, 9)
for k in ks:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

# === FIT WITH K=4 ===
# 4 clusters maps cleanly to 4 meaningful neighbourhood types
km = KMeans(n_clusters=4, random_state=42, n_init=10)
imm['cluster'] = km.fit_predict(X_scaled)

# === LABEL CLUSTERS by their profile ===
# Look at mean values per cluster to assign meaningful names
summary = imm.groupby('cluster')[features + ['city']].agg(
    {f: 'mean' for f in features} | {'city': 'count'}
).rename(columns={'city': 'count'})
summary = summary.round(1)
print("=" * 60)
print("CLUSTER PROFILES (immigrant neighbourhoods)")
print("=" * 60)
print(summary.to_string())
print()

# Assign names based on income and STIR pattern
# We'll auto-label after seeing the output
cluster_means = imm.groupby('cluster')['total_stir'].mean().sort_values()
print("Clusters sorted by mean STIR:")
print(cluster_means.round(2))
print()

# City distribution per cluster
city_dist = imm.groupby(['cluster','city']).size().unstack(fill_value=0)
print("City distribution per cluster:")
print(city_dist.to_string())
print()

# Top CSDs per cluster
print("=" * 60)
print("SAMPLE NEIGHBOURHOODS PER CLUSTER")
print("=" * 60)
for c in sorted(imm['cluster'].unique()):
    subset = imm[imm['cluster']==c].nlargest(4, 'renter_stir')
    print(f"\nCluster {c} (mean STIR: {imm[imm['cluster']==c]['total_stir'].mean():.1f}%)")
    print(subset[['csd_name','city','total_income','total_stir','renter_stir']].to_string())

# === PLOT ===
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#0e0f13')

cluster_colors = ['#5b9bd5', '#e8834a', '#4dab7e', '#8e75c9']
cluster_labels = {0: '', 1: '', 2: '', 3: ''}

# Plot 1: Income vs Renter STIR, colored by cluster
ax = axes[0]
ax.set_facecolor('#16181f')
for c in sorted(imm['cluster'].unique()):
    subset = imm[imm['cluster'] == c]
    ax.scatter(subset['total_income'], subset['renter_stir'],
               color=cluster_colors[c], alpha=0.7, s=45,
               label=f'Cluster {c+1}')

ax.axhline(y=30, color='#e05555', linestyle='--', linewidth=1, alpha=0.7)
ax.text(290000, 30.4, '30% threshold', color='#e05555', fontsize=8)
ax.set_xlabel('Household Income ($)', color='#7a7870', fontsize=11)
ax.set_ylabel('Immigrant Renter STIR (%)', color='#7a7870', fontsize=11)
ax.set_title('Neighbourhood Clusters — Income vs Renter STIR\n(immigrant households)',
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x/1000:.0f}k'))
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.xaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)
ax.legend(framealpha=0, labelcolor='#e8e6e0', fontsize=9)

# Plot 2: Cluster profiles — radar-style bar chart
ax = axes[1]
ax.set_facecolor('#16181f')
cluster_summary = imm.groupby('cluster')[['total_income','total_stir','renter_stir','renter_owner_gap']].mean()

x = np.arange(4)
width = 0.2
metrics = ['total_income', 'total_stir', 'renter_stir', 'renter_owner_gap']
labels = ['Avg Income\n($10k)', 'Total STIR\n(%)', 'Renter STIR\n(%)', 'Renter-Owner\nGap (pp)']
scales = [10000, 1, 1, 1]

for i, (metric, label, scale) in enumerate(zip(metrics, labels, scales)):
    vals = [cluster_summary.loc[c, metric] / scale for c in sorted(imm['cluster'].unique())]
    offset = (i - 1.5) * width
    bars = ax.bar(x + offset, vals, width, color=[cluster_colors[c] for c in range(4)], alpha=0.8)

ax.set_xticks(x)
ax.set_xticklabels([f'Cluster {c+1}' for c in range(4)], color='#e8e6e0', fontsize=10)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)

# Manual legend for metrics
metric_patches = [mpatches.Patch(color='#888', alpha=a, label=l)
                  for l, a in zip(labels, [0.9, 0.75, 0.6, 0.45])]
ax.set_title('Cluster Profiles — Key Metrics\n(immigrant neighbourhoods)',
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold')
ax.text(0, -0.14,
        'Each cluster = a distinct type of immigrant neighbourhood by housing burden profile.',
        transform=ax.transAxes, fontsize=9, color='#7a7870')

plt.tight_layout()
plt.savefig('visuals/ml_clustering.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print("Saved: visuals/ml_clustering.png")