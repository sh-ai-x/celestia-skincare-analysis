"""Celestia-specific hypothesis verification (descriptive analysis)."""
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA = Path('/Users/sanghee/dev/research_data_ananlysis/data/raw/CELESTIA_SKINCARE_DATASET_KAGGLE_READY.csv')
df = pd.read_csv(DATA)

results = []

# H1
retinol_df = df[df['Ingredients_with_Concentration'].str.contains('Retinol', case=False, na=False)]
h1 = (retinol_df['Concern'] == 'Wrinkles').all()
results.append(('H1: Retinol → Wrinkles 100%', h1, f"{len(retinol_df)}/{len(retinol_df)}"))

# H2
sa_df = df[df['Ingredients_with_Concentration'].str.contains('Salicylic Acid', case=False, na=False)]
acne_ratio = (sa_df['Concern'] == 'Acne').sum() / len(sa_df)
h2 = acne_ratio > 0.5
results.append(('H2: Salicylic Acid → Acne >50%', h2, f"{round(acne_ratio*100,1)}%"))

# H3
ni_df = df[df['Ingredients_with_Concentration'].str.contains('Niacinamide', case=False, na=False)]
h3 = ni_df['Concern'].nunique() == df['Concern'].nunique()
results.append(('H3: Niacinamide → 모든 컨선', h3, f"{ni_df['Concern'].nunique()}/{df['Concern'].nunique()}"))

# Bakuchiol 부재
n_bak = df['Ingredients_with_Concentration'].str.contains('Bakuchiol', case=False, na=False).sum()
results.append(('Bakuchiol 부재', n_bak == 0, f"{n_bak}/1120"))

# 데이터 무결성
n_rows = df.shape[0]
n_null = df.isnull().sum().sum()
results.append(('데이터 무결성', n_rows == 1120 and n_null == 0, f"shape={df.shape}, 결측치={n_null}"))

print("=" * 60)
print("Celestia 가설 검증 재실행")
print("=" * 60)
pass_count = 0
for name, passed, metric in results:
    status = "PASS ✅" if passed else "FAIL ❌"
    print(f"  {status}  {name}: {metric}")
    if passed:
        pass_count += 1

print("=" * 60)
print(f"총 {pass_count}/{len(results)} PASS")
print(f"기록값: 5/5")
print(f"검증: {'OK' if pass_count == 5 else 'MISMATCH'} (차이: {abs(5-pass_count)})")
