import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error

df = pd.read_csv('data/master_clean.csv')

# === SETUP ===
# CSD level only, immigrants and non-immigrants only
csd = df[~df['geography'].str.contains('CMA|Canada', na=False)]
csd = csd[csd['city'] != 'Other']
csd = csd[csd['immigrant_status'].isin(['Immigrant', 'Non-immigrants'])]
csd = csd.dropna(subset=['total_stir', 'total_income', 'city', 'immigrant_status'])

# === FEATURES ===
# We predict STIR using: income + city + immigrant_status
# If immigrant_status coefficient is positive after controlling for income+city
# that IS the invisible tax — quantified
X = csd[['total_income', 'city', 'immigrant_status']]
y = csd['total_stir']

# === MODEL ===
# One-hot encode city and immigrant_status
preprocessor = ColumnTransformer(transformers=[
    ('num', 'passthrough', ['total_income']),
    ('cat', OneHotEncoder(drop='first', sparse_output=False), ['city', 'immigrant_status'])
])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

model.fit(X, y)
y_pred = model.predict(X)
residuals = y - y_pred

# === RESULTS ===
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

print("=" * 50)
print("REGRESSION RESULTS")
print("=" * 50)
print(f"R² score:  {r2:.3f}  (how much variance the model explains)")
print(f"RMSE:      {rmse:.3f} percentage points")
print()

# Get feature names and coefficients
cat_features = model.named_steps['preprocessor']\
    .named_transformers_['cat'].get_feature_names_out(['city', 'immigrant_status'])
feature_names = ['total_income'] + list(cat_features)
coefficients = model.named_steps['regressor'].coef_
intercept = model.named_steps['regressor'].intercept_

print("COEFFICIENTS:")
print(f"  Intercept: {intercept:.3f}")
for name, coef in zip(feature_names, coefficients):
    print(f"  {name}: {coef:.4f}")

print()
print("=" * 50)
print("KEY FINDING — THE INVISIBLE TAX")
print("=" * 50)
imm_coef = coefficients[list(feature_names).index('immigrant_status_Non-immigrants')]
print(f"Being immigrant (vs non-immigrant) adds: {-imm_coef:.2f} percentage points to STIR")
print("This is AFTER controlling for income and city.")
print("This is your Invisible Tax, quantified.")

# === RESIDUALS ===
csd = csd.copy()
csd['predicted'] = y_pred
csd['residual'] = residuals

print()
print("=" * 50)
print("MOST UNDER-PREDICTED (paying MORE than model expects)")
print("=" * 50)
over = csd.nlargest(10, 'residual')[['csd_name','city','immigrant_status','total_income','total_stir','predicted','residual']]
print(over.round(2).to_string())

# === PLOT ===
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#0e0f13')

# Plot 1: Actual vs Predicted
ax = axes[0]
ax.set_facecolor('#16181f')
colors = csd['immigrant_status'].map({'Immigrant': '#e8834a', 'Non-immigrants': '#5b9bd5'})
ax.scatter(y_pred, y, c=colors, alpha=0.5, s=35)
ax.plot([y.min(), y.max()], [y.min(), y.max()],
        color='#7a7870', linewidth=1.2, linestyle='--')
ax.set_xlabel('Predicted STIR (%)', color='#7a7870', fontsize=11)
ax.set_ylabel('Actual STIR (%)', color='#7a7870', fontsize=11)
ax.set_title(f'Actual vs Predicted STIR\nR² = {r2:.3f}', 
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold')
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.xaxis.grid(True, color='#ffffff', alpha=0.05)

# Plot 2: Residuals by immigrant status
ax = axes[1]
ax.set_facecolor('#16181f')
for status, color, label in [
    ('Immigrant', '#e8834a', 'Immigrant'),
    ('Non-immigrants', '#5b9bd5', 'Non-immigrant')
]:
    subset = csd[csd['immigrant_status'] == status]['residual']
    ax.hist(subset, bins=25, color=color, alpha=0.6, label=label, edgecolor='none')

ax.axvline(x=0, color='#7a7870', linewidth=1, linestyle='--')
imm_mean = csd[csd['immigrant_status']=='Immigrant']['residual'].mean()
non_mean = csd[csd['immigrant_status']=='Non-immigrants']['residual'].mean()
ax.axvline(x=imm_mean, color='#e8834a', linewidth=1.5)
ax.axvline(x=non_mean, color='#5b9bd5', linewidth=1.5)
ax.text(imm_mean + 0.1, ax.get_ylim()[1]*0.85,
        f'Imm\nmean\n{imm_mean:+.2f}', color='#e8834a', fontsize=8)
ax.text(non_mean + 0.1, ax.get_ylim()[1]*0.65,
        f'Non\nmean\n{non_mean:+.2f}', color='#5b9bd5', fontsize=8)

ax.set_xlabel('Residual (Actual − Predicted STIR)', color='#7a7870', fontsize=11)
ax.set_ylabel('Number of neighbourhoods', color='#7a7870', fontsize=11)
ax.set_title('Residuals by Immigration Status\n(positive = paying more than predicted)',
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold')
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.legend(framealpha=0, labelcolor='#e8e6e0', fontsize=10)

plt.tight_layout()
plt.savefig('visuals/ml_regression.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print()
print("Saved: visuals/ml_regression.png")

# ============================================================
# INTERACTION MODEL — immigrant penalty by city
# ============================================================
from sklearn.preprocessing import PolynomialFeatures

# Create interaction manually: immigrant_status × city
# Easier to do this with pandas + statsmodels for clean output
import statsmodels.formula.api as smf

# Prepare data with clean column names
model_df = csd[['total_stir', 'total_income', 'city', 'immigrant_status']].copy()
model_df['is_immigrant'] = (model_df['immigrant_status'] == 'Immigrant').astype(int)
model_df['income_k'] = model_df['total_income'] / 1000

# Interaction model: STIR ~ income + city + immigrant + city*immigrant
formula = 'total_stir ~ income_k + C(city) + is_immigrant + C(city):is_immigrant'
interaction_model = smf.ols(formula, data=model_df).fit()

print()
print("=" * 60)
print("INTERACTION MODEL — Immigrant Penalty by City")
print("=" * 60)
print(interaction_model.summary())

# Extract the penalty per city cleanly
print()
print("=" * 60)
print("IMMIGRANT HOUSING PENALTY BY CITY (percentage points)")
print("(after controlling for income)")
print("=" * 60)

base_penalty = interaction_model.params['is_immigrant']
cities_list = ['Montreal', 'Toronto', 'Edmonton', 'Vancouver']

penalties = {}
for city in cities_list:
    if city == 'Montreal':
        # Montreal is the reference city
        penalties[city] = base_penalty
    else:
        interaction_term = f'C(city)[T.{city}]:is_immigrant'
        if interaction_term in interaction_model.params:
            penalties[city] = base_penalty + interaction_model.params[interaction_term]
        else:
            penalties[city] = base_penalty

for city, penalty in penalties.items():
    pval_key = f'C(city)[T.{city}]:is_immigrant'
    sig = ''
    if city != 'Montreal' and pval_key in interaction_model.pvalues:
        p = interaction_model.pvalues[pval_key]
        sig = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else ''
    direction = 'immigrants pay MORE' if penalty > 0 else 'immigrants pay LESS'
    print(f"  {city}: {penalty:+.2f}pp  {sig}  ({direction})")

print()
print("*** p<0.01  ** p<0.05  * p<0.1")
print("Base city (reference): Montreal")

# === PLOT interaction results ===
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('#0e0f13')
ax.set_facecolor('#16181f')

city_colors = ['#8e75c9', '#e8834a', '#4dab7e', '#5b9bd5']
cities_plot = list(penalties.keys())
values = list(penalties.values())
bar_colors = ['#e05555' if v > 0 else '#4dab7e' for v in values]

bars = ax.bar(cities_plot, values, color=bar_colors, alpha=0.85, width=0.5)
ax.axhline(y=0, color='#7a7870', linewidth=0.8)

for bar, val in zip(bars, values):
    ypos = val + 0.05 if val >= 0 else val - 0.25
    ax.text(bar.get_x() + bar.get_width()/2, ypos,
            f'{val:+.2f}pp', ha='center', fontsize=12,
            color='#e8e6e0', fontweight='bold')

ax.set_ylabel('Immigrant housing penalty (pp)', color='#7a7870', fontsize=11)
ax.set_title('The Immigrant Housing Penalty is Not Equal Across Cities\n'
             'Percentage points added to STIR by being immigrant, after controlling for income',
             fontsize=12, color='#e8e6e0', loc='left', fontweight='bold', pad=12)
ax.tick_params(colors='#7a7870')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff', alpha=0.05)
ax.set_axisbelow(True)
ax.text(0, -0.15,
        'Red = immigrants pay more than non-immigrants at same income level. '
        'Green = immigrants pay less.',
        transform=ax.transAxes, fontsize=9, color='#7a7870')

plt.tight_layout()
plt.savefig('visuals/ml_interaction.png', dpi=150, bbox_inches='tight',
            facecolor='#0e0f13')
print()
print("Saved: visuals/ml_interaction.png")

