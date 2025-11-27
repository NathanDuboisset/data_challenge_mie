"""
Script de conversion automatique Pandas → Polars pour le notebook
Usage: Copiez-collez ces conversions dans votre notebook
"""

print("=" * 80)
print("CONVERSIONS POLARS - Copiez-collez dans votre notebook")
print("=" * 80)

# ============================================================================
# Cellule 10: KPIs principaux
# ============================================================================
print("\n### Cellule 10: KPIs principaux ###")
print("""
# KPIs principaux - Syntaxe Polars
print("\\nKPIS PRINCIPAUX")
print("=" * 80)

# Panier moyen
avg_basket = df_purchases['sales'].mean()
print(f"Panier moyen: {avg_basket:.2f} $")

# Total par client (convertir temporairement pour calcul pandas-style)
total_per_customer = df_purchases.group_by('customer_id').agg(pl.col('sales').sum())
avg_basket_per_buyer = total_per_customer['sales'].mean()
print(f"Panier moyen par acheteur (total dépenses): {avg_basket_per_buyer:.2f} $")

# Transactions par client
transactions_per_customer = df_purchases.group_by('customer_id').agg(pl.len())
avg_transactions = transactions_per_customer['len'].mean()
print(f"Nombre moyen de transactions par client: {avg_transactions:.2f}")

# Prix moyen par unité
avg_unit_price = df_purchases['sales'].sum() / df_purchases['quantity'].sum()
print(f"Prix moyen par unité: {avg_unit_price:.2f} $")

# Quantité moyenne
avg_quantity = df_purchases['quantity'].mean()
print(f"Quantité moyenne par transaction: {avg_quantity:.2f} unités")
""")

# ============================================================================
# Cellule 12: Distribution des ventes
# ============================================================================
print("\n### Cellule 12: Distribution des ventes ###")
print("""
# Graphique: Distribution du panier moyen
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Histogramme - Conversion en numpy pour matplotlib
sales_data = df_purchases['sales'].to_numpy()
axes[0].hist(sales_data, bins=50, edgecolor='black', alpha=0.7)
axes[0].axvline(avg_basket, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {avg_basket:.2f}$')
axes[0].set_xlabel('Montant de la transaction ($)')
axes[0].set_ylabel('Fréquence')
axes[0].set_title('Distribution des Montants de Transaction')
axes[0].legend()
axes[0].set_xlim(0, df_purchases['sales'].quantile(0.99))

# Boxplot par marque (top 10) - Conversion en Pandas pour boxplot
top_brands = (df_purchases
              .filter(pl.col('brand').is_not_null())
              .group_by('brand')
              .agg(pl.len().alias('count'))
              .sort('count', descending=True)
              .head(10)['brand']
              .to_list())
df_top_brands = df_purchases.filter(pl.col('brand').is_in(top_brands)).to_pandas()
df_top_brands.boxplot(column='sales', by='brand', ax=axes[1], rot=45)
axes[1].set_xlabel('Marque')
axes[1].set_ylabel('Montant ($)')
axes[1].set_title('Distribution des Ventes par Marque (Top 10)')
plt.suptitle('')

plt.tight_layout()
plt.show()

print("✓ Graphiques générés")
""")

# ============================================================================
# Cellule 14: Évolution temporelle
# ============================================================================
print("\n### Cellule 14: Évolution temporelle ###")
print("""
# Evolution des ventes dans le temps - Polars
df_purchases_with_date = df_purchases.with_columns(
    pl.col('timestamp_utc').cast(pl.Date).alias('date')
)

daily_sales = (
    df_purchases_with_date
    .group_by('date')
    .agg([
        pl.col('sales').sum().alias('revenue'),
        pl.len().alias('transactions')
    ])
    .sort('date')
)

# Conversion pour visualisation
daily_sales_pd = daily_sales.to_pandas()

fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Chiffre d'affaires quotidien
axes[0].plot(daily_sales_pd['date'], daily_sales_pd['revenue'], linewidth=2)
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Chiffre d\\'affaires ($)')
axes[0].set_title('Évolution du Chiffre d\\'Affaires Quotidien')
axes[0].grid(True, alpha=0.3)

# Nombre de transactions quotidiennes
axes[1].plot(daily_sales_pd['date'], daily_sales_pd['transactions'], linewidth=2, color='orange')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Nombre de transactions')
axes[1].set_title('Nombre de Transactions Quotidiennes')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Analyse temporelle effectuée")
""")

# ============================================================================
# Cellule 19: Analyse socio-démographique
# ============================================================================
print("\n### Cellule 19: Analyse socio-démographique ###")
print("""
# Merge avec les données socio-démographiques - Polars
df_purchases_socio = df_purchases.join(df_socio, on='customer_id', how='left')

print("ANALYSE SOCIO-DÉMOGRAPHIQUE")
print("=" * 80)

# Distribution par âge
print("\\nDistribution par âge:")
age_dist = df_socio.group_by('age').agg(pl.len()).sort('age')
print(age_dist)

# Distribution par revenu
print("\\nDistribution par revenu:")
income_dist = df_socio.group_by('income').agg(pl.len()).sort('len', descending=True)
print(income_dist)

# Distribution par breed
print("\\nDistribution par breed:")
breed_dist = df_socio.group_by('breed').agg(pl.len()).sort('len', descending=True)
print(breed_dist)
""")

# ============================================================================
# Cellule 20: Graphiques socio-démographiques
# ============================================================================
print("\n### Cellule 20: Graphiques socio-démographiques ###")
print("""
# Performance par segment socio-démographique - Polars
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Ventes par âge
age_sales = (
    df_purchases_socio
    .filter(pl.col('age').is_not_null())
    .group_by('age')
    .agg([
        pl.col('sales').sum().alias('sum'),
        pl.col('sales').mean().alias('mean'),
        pl.len().alias('count')
    ])
    .sort('age')
    .to_pandas()
)

axes[0, 0].bar(range(len(age_sales)), age_sales['sum'])
axes[0, 0].set_xticks(range(len(age_sales)))
axes[0, 0].set_xticklabels(age_sales['age'], rotation=45)
axes[0, 0].set_xlabel('Tranche d\\'âge')
axes[0, 0].set_ylabel('Chiffre d\\'affaires total ($)')
axes[0, 0].set_title('Chiffre d\\'Affaires par Tranche d\\'Âge')

# Panier moyen par âge
axes[0, 1].bar(range(len(age_sales)), age_sales['mean'], color='orange')
axes[0, 1].set_xticks(range(len(age_sales)))
axes[0, 1].set_xticklabels(age_sales['age'], rotation=45)
axes[0, 1].set_xlabel('Tranche d\\'âge')
axes[0, 1].set_ylabel('Panier moyen ($)')
axes[0, 1].set_title('Panier Moyen par Tranche d\\'Âge')

# Ventes par revenu
income_sales = (
    df_purchases_socio
    .filter(pl.col('income').is_not_null())
    .group_by('income')
    .agg([
        pl.col('sales').sum().alias('sum'),
        pl.col('sales').mean().alias('mean'),
        pl.len().alias('count')
    ])
    .to_pandas()
)

axes[1, 0].bar(range(len(income_sales)), income_sales['sum'], color='green')
axes[1, 0].set_xticks(range(len(income_sales)))
axes[1, 0].set_xticklabels(income_sales['income'], rotation=45)
axes[1, 0].set_xlabel('Tranche de revenu')
axes[1, 0].set_ylabel('Chiffre d\\'affaires total ($)')
axes[1, 0].set_title('Chiffre d\\'Affaires par Tranche de Revenu')

# Ventes par breed
breed_sales = (
    df_purchases_socio
    .filter(pl.col('breed').is_not_null())
    .group_by('breed')
    .agg([
        pl.col('sales').sum().alias('sum'),
        pl.col('sales').mean().alias('mean'),
        pl.len().alias('count')
    ])
    .to_pandas()
)

axes[1, 1].bar(range(len(breed_sales)), breed_sales['sum'], color='purple')
axes[1, 1].set_xticks(range(len(breed_sales)))
axes[1, 1].set_xticklabels(breed_sales['breed'], rotation=45)
axes[1, 1].set_xlabel('Breed')
axes[1, 1].set_ylabel('Chiffre d\\'affaires total ($)')
axes[1, 1].set_title('Chiffre d\\'Affaires par Breed')

plt.tight_layout()
plt.show()

print("\\n✓ Analyse socio-démographique complétée")
""")

# ============================================================================
# Cellule 22: Investissements publicitaires
# ============================================================================
print("\n### Cellule 22: Coûts publicitaires ###")
print("""
# Conversion des coûts (milli cents -> dollars) - Polars
df_tv = df_tv.with_columns(
    (pl.col('cost_milli_cent') / 100000).alias('cost_dollar')
)
df_prog = df_prog.with_columns(
    (pl.col('cost_milli_cent') / 100000).alias('cost_dollar')
)

print("INVESTISSEMENTS PUBLICITAIRES")
print("=" * 80)

# TV
tv_investment = df_tv['cost_dollar'].sum()
tv_impressions = len(df_tv)
tv_cpm = (tv_investment / tv_impressions) * 1000

print(f"\\nPublicité TV:")
print(f"  - Investissement total: {tv_investment:,.2f} $")
print(f"  - Nombre d'impressions: {tv_impressions:,}")
print(f"  - CPM (Coût pour 1000 impressions): {tv_cpm:.2f} $")

# Programmatique
prog_investment = df_prog['cost_dollar'].sum()
prog_impressions = len(df_prog)
prog_cpm = (prog_investment / prog_impressions) * 1000

print(f"\\nPublicité Programmatique:")
print(f"  - Investissement total: {prog_investment:,.2f} $")
print(f"  - Nombre d'impressions: {prog_impressions:,}")
print(f"  - CPM (Coût pour 1000 impressions): {prog_cpm:.2f} $")

print(f"\\nTotal investissement publicitaire: {tv_investment + prog_investment:,.2f} $")
""")

# ============================================================================
# Cellule 25: Analyse temporelle publicité
# ============================================================================
print("\n### Cellule 25: Analyse temporelle publicité ###")
print("""
# Agrégation quotidienne des dépenses publicitaires - Polars
df_tv_with_date = df_tv.with_columns(pl.col('timestamp_utc').cast(pl.Date).alias('date'))
df_prog_with_date = df_prog.with_columns(pl.col('timestamp_utc').cast(pl.Date).alias('date'))

tv_daily = (
    df_tv_with_date
    .group_by('date')
    .agg(pl.col('cost_dollar').sum().alias('tv_cost'))
    .sort('date')
)

prog_daily = (
    df_prog_with_date
    .group_by('date')
    .agg(pl.col('cost_dollar').sum().alias('prog_cost'))
    .sort('date')
)

# Merge avec les ventes - Polars
ad_sales_daily = (
    daily_sales
    .join(tv_daily, on='date', how='outer_coalesce')
    .join(prog_daily, on='date', how='outer_coalesce')
    .with_columns([
        pl.col('tv_cost').fill_null(0),
        pl.col('prog_cost').fill_null(0),
        pl.col('revenue').fill_null(0)
    ])
    .with_columns(
        (pl.col('tv_cost') + pl.col('prog_cost')).alias('total_ad_cost')
    )
    .sort('date')
)

# Conversion pour visualisation
ad_sales_daily_pd = ad_sales_daily.to_pandas()

# Visualisation
fig, ax1 = plt.subplots(figsize=(15, 6))

ax1.set_xlabel('Date')
ax1.set_ylabel('Chiffre d\\'affaires ($)', color='blue')
ax1.plot(ad_sales_daily_pd['date'], ad_sales_daily_pd['revenue'], color='blue', linewidth=2, label='Ventes')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Dépenses publicitaires ($)', color='red')
ax2.plot(ad_sales_daily_pd['date'], ad_sales_daily_pd['total_ad_cost'], color='red', linewidth=2, alpha=0.7, label='Pub totale')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Évolution des Ventes et des Dépenses Publicitaires')
fig.tight_layout()
plt.show()

print("✓ Corrélation temporelle visualisée")
""")

print("\n" + "=" * 80)
print("CONVERSIONS TERMINÉES!")
print("Copiez-collez ces blocs dans les cellules correspondantes de votre notebook")
print("=" * 80)

