"""Skin_Type별 모공/블랙헤드/아크네 등 상세 EDA."""
import pandas as pd
import numpy as np
import platform
import warnings
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter, defaultdict

warnings.filterwarnings('ignore')
plt.rcParams['font.family'] = 'AppleGothic' if platform.system() == 'Darwin' else 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

DATA = Path('/Users/sanghee/dev/research_data_ananlysis/data/raw/CELESTIA_SKINCARE_DATASET_KAGGLE_READY.csv')
df = pd.read_csv(DATA)
df['ingredient_list'] = df['Ingredients_with_Concentration'].str.split('+').apply(lambda x: [i.strip() for i in x])
df['effect_list'] = df['Effects'].str.split(',').apply(lambda x: [e.strip() for e in x])

OUT = Path('/Users/sanghee/dev/research_data_ananlysis/scratch')

# === 1. 모공/블랙헤드 관련 Concern 정의 ===
target_concerns = ['Open Pores', 'Whiteheads / Blackheads', 'Acne']
print("=" * 70)
print("1. 모공/블랙헤드 관련 Concern 정의")
print("=" * 70)
print(f"  - Open Pores: 모공")
print(f"  - Whiteheads / Blackheads: 화이트헤드/블랙헤드")
print(f"  - Acne: 여드름 (모공·블랙헤드의 상위 컨선)")
print(f"\n  해당 Concern 데이터 수: {(df['Concern'].isin(target_concerns)).sum()}건")
print(f"  Concern별 × Skin_Type:")
print(df[df['Concern'].isin(target_concerns)].groupby(['Concern', 'Skin_Type']).size().unstack(fill_value=0).to_string())

# === 2. Skin_Type × Concern 전체 분포 ===
print("\n\n" + "=" * 70)
print("2. Skin_Type × Concern 매트릭스 (전체)")
print("=" * 70)
ct_all = pd.crosstab(df['Skin_Type'], df['Concern'])
print(ct_all.to_string())

# === 3. Skin_Type별 모공/블랙헤드 컨선의 상위 성분 ===
print("\n\n" + "=" * 70)
print("3. Skin_Type별 Open Pores / Whiteheads·Blackheads 처방 성분")
print("=" * 70)
sub = df[df['Concern'].isin(target_concerns)]
skin_concern_ing = defaultdict(lambda: defaultdict(Counter))
for _, row in sub.iterrows():
    for ing in row['ingredient_list']:
        skin_concern_ing[row['Skin_Type']][row['Concern']][ing] += 1

for skin_type in sorted(sub['Skin_Type'].unique()):
    print(f"\n[{skin_type}]")
    for concern in target_concerns:
        cnt = skin_concern_ing[skin_type][concern]
        if cnt:
            top5 = cnt.most_common(5)
            print(f"  {concern} (n={sum(cnt.values())}):")
            for ing, c in top5:
                print(f"    - {ing}: {c}회 ({round(c/sum(cnt.values())*100,1)}%)")

# === 4. Skin_Type별 Acne Internal_Type 분포 ===
print("\n\n" + "=" * 70)
print("4. Skin_Type별 Acne Internal_Type (여드름 세부 분류)")
print("=" * 70)
acne = df[df['Concern'] == 'Acne']
ct_acne = pd.crosstab(acne['Skin_Type'], acne['Internal_Type'])
print(ct_acne.to_string())
print(f"\n  인사이트:")
oily_acne = acne[acne['Skin_Type'] == 'Oily']
print(f"  - Oily 피부의 Acne은 {len(oily_acne)}건, 가장 흔한 Internal_Type:")
print(f"    {oily_acne['Internal_Type'].value_counts().head(3).to_string()}")
dry_acne = acne[acne['Skin_Type'] == 'Dry']
print(f"  - Dry 피부의 Acne은 {len(dry_acne)}건, 가장 흔한 Internal_Type:")
print(f"    {dry_acne['Internal_Type'].value_counts().head(3).to_string()}")

# === 5. Skin_Subtype별 Open Pores 처방 차이 ===
print("\n\n" + "=" * 70)
print("5. Skin_Subtype별 Open Pores 처방 차이")
print("=" * 70)
pores = df[df['Concern'] == 'Open Pores']
subtype_ing = defaultdict(Counter)
for _, row in pores.iterrows():
    for ing in row['ingredient_list']:
        subtype_ing[row['Skin_Subtype']][ing] += 1
for subtype in sorted(subtype_ing.keys()):
    cnt = subtype_ing[subtype]
    top3 = cnt.most_common(3)
    print(f"  {subtype:30s}: {', '.join([f'{ing}({c})' for ing, c in top3])}")

# === 6. Age × Skin_Type × Concern 상호작용 ===
print("\n\n" + "=" * 70)
print("6. Age_Group × Skin_Type × 모공·블랙헤드 분포")
print("=" * 70)
sub2 = df[df['Concern'].isin(['Open Pores', 'Whiteheads / Blackheads'])]
ct_3way = sub2.groupby(['Age_Group', 'Skin_Type']).size().unstack(fill_value=0)
print(ct_3way.to_string())

# === 7. Sensitivity 영향 분석 ===
print("\n\n" + "=" * 70)
print("7. Sensitivity 별 처방 차이 (민감성 피부 회피 성분)")
print("=" * 70)
acne_full = df[df['Concern'].isin(target_concerns)]
sens_ing = defaultdict(Counter)
for _, row in acne_full.iterrows():
    for ing in row['ingredient_list']:
        sens_ing[row['Sensitivity']][ing] += 1
all_ings = set()
for c in sens_ing.values():
    all_ings.update(c.keys())
ing_list = sorted(all_ings)
matrix = np.zeros((2, len(ing_list)))
for i, sens in enumerate(['Yes', 'No']):
    for j, ing in enumerate(ing_list):
        matrix[i, j] = sens_ing[sens].get(ing, 0)
sens_df = pd.DataFrame(matrix, index=['Sensitive (Yes)', 'Non-sensitive (No)'], columns=ing_list)
print(sens_df.to_string())
print("\n  → 민감성 피부에서 회피되는 성분 (Yes < No):")
for ing in ing_list:
    y = sens_ing['Yes'].get(ing, 0)
    n = sens_ing['No'].get(ing, 0)
    if y < n * 0.7 and n > 0:
        print(f"    - {ing}: Yes={y}, No={n} (차이 {round((n-y)/n*100,1)}%)")
print("\n  → 민감성 피부에서 더 많이 쓰이는 성분 (Yes > No):")
for ing in ing_list:
    y = sens_ing['Yes'].get(ing, 0)
    n = sens_ing['No'].get(ing, 0)
    if y > n * 1.3 and y > 0:
        print(f"    - {ing}: Yes={y}, No={n} ({round(y/n,2)}배)")

# === 시각화 ===
print("\n\n[시각화 생성 중...]")

# 8.1 Skin_Type × 모공/블랙헤드/아크네 빈도
fig, ax = plt.subplots(figsize=(10, 6))
ct_target = df[df['Concern'].isin(target_concerns)].groupby(['Skin_Type', 'Concern']).size().unstack(fill_value=0)
ct_target = ct_target.reindex(['Normal', 'Oily', 'Dry', 'Combination'])
ct_target.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c', '#2ecc71'])
ax.set_title('Skin_Type별 모공/블랙헤드/아크네 분포', fontsize=14, fontweight='bold')
ax.set_xlabel('Skin Type', fontsize=12)
ax.set_ylabel('처방 수', fontsize=12)
ax.legend(title='Concern', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.setp(ax.get_xticklabels(), rotation=0)
for container in ax.containers:
    ax.bar_label(container, fontsize=9)
plt.tight_layout()
plt.savefig(OUT / 'skin_type_target_concerns.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  ✓ skin_type_target_concerns.png")

# 8.2 Skin_Type별 Acne Internal_Type 스택 바
fig, ax = plt.subplots(figsize=(10, 6))
ct_acne.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
ax.set_title('Skin_Type별 Acne Internal_Type 분포 (여드름 세부 분류)', fontsize=14, fontweight='bold')
ax.set_xlabel('Skin Type', fontsize=12)
ax.set_ylabel('Acne 처방 수', fontsize=12)
ax.legend(title='Internal Type', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
plt.setp(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(OUT / 'acne_internal_by_skintype.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  ✓ acne_internal_by_skintype.png")

# 8.3 Skin_Type별 모공 처방 성분 히트맵
fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for idx, concern in enumerate(target_concerns):
    concern_data = defaultdict(Counter)
    for _, row in df[df['Concern'] == concern].iterrows():
        for ing in row['ingredient_list']:
            concern_data[row['Skin_Type']][ing] += 1

    skin_types = ['Normal', 'Oily', 'Dry', 'Combination']
    all_ings_for_concern = set()
    for st in skin_types:
        all_ings_for_concern.update([ing for ing, _ in concern_data[st].most_common(8)])
    ing_list_c = sorted(all_ings_for_concern)

    m = np.zeros((len(skin_types), len(ing_list_c)))
    for i, st in enumerate(skin_types):
        for j, ing in enumerate(ing_list_c):
            m[i, j] = concern_data[st].get(ing, 0)

    im = axes[idx].imshow(m, cmap='YlOrRd', aspect='auto')
    axes[idx].set_xticks(range(len(ing_list_c)))
    axes[idx].set_xticklabels(ing_list_c, rotation=45, ha='right', fontsize=8)
    axes[idx].set_yticks(range(len(skin_types)))
    axes[idx].set_yticklabels(skin_types)
    axes[idx].set_title(f'{concern}\nSkin_Type × 성분 빈도', fontsize=11, fontweight='bold')
    for i in range(len(skin_types)):
        for j in range(len(ing_list_c)):
            if m[i, j] > 0:
                axes[idx].text(j, i, int(m[i, j]), ha='center', va='center', fontsize=8)
    plt.colorbar(im, ax=axes[idx], fraction=0.046, pad=0.04, label='count')

plt.suptitle('Skin_Type별 모공/블랙헤드/아크네 처방 성분 패턴', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT / 'skin_type_concern_ingredients_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  ✓ skin_type_concern_ingredients_heatmap.png")

# 8.4 Skin_Type별 평균 성분 수 + 평균 효능 수 (practical insight)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
agg = df.groupby('Skin_Type').agg(
    avg_ingredients=('ingredient_list', lambda x: np.mean([len(i) for i in x])),
    avg_effects=('effect_list', lambda x: np.mean([len(e) for e in x])),
    total=('Concern', 'size')
).round(2).reindex(['Normal', 'Oily', 'Dry', 'Combination'])
agg['avg_ingredients'].plot(kind='bar', ax=axes[0], color='coral')
axes[0].set_title('Skin_Type별 평균 성분 수')
axes[0].set_ylabel('평균 성분 개수')
axes[0].set_ylim(2.5, 3.5)
for i, v in enumerate(agg['avg_ingredients']):
    axes[0].text(i, v + 0.02, str(v), ha='center', fontsize=10)
plt.setp(axes[0].get_xticklabels(), rotation=0)

agg['total'].plot(kind='bar', ax=axes[1], color='steelblue')
axes[1].set_title('Skin_Type별 전체 처방 수')
axes[1].set_ylabel('처방 수')
for i, v in enumerate(agg['total']):
    axes[1].text(i, v + 5, str(int(v)), ha='center', fontsize=10)
plt.setp(axes[1].get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(OUT / 'skin_type_practical.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  ✓ skin_type_practical.png")

# 8.5 Sensitivity 별 처방 차이 시각화
fig, ax = plt.subplots(figsize=(14, 7))
sens_df.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'])
ax.set_title('민감성 여부에 따른 처방 성분 차이 (모공·블랙헤드·아크네)', fontsize=13, fontweight='bold')
ax.set_xlabel('민감성', fontsize=12)
ax.set_ylabel('등장 횟수', fontsize=12)
ax.legend(title='Sensitivity', labels=['Sensitive (Yes)', 'Non-sensitive (No)'])
plt.setp(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(OUT / 'sensitivity_ingredient_diff.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  ✓ sensitivity_ingredient_diff.png")

# 8.6 Skin_Type × Internal_Type 매트릭스 (실무 추천 가이드)
fig, ax = plt.subplots(figsize=(12, 6))
ct_acne_norm = ct_acne.div(ct_acne.sum(axis=1), axis=0) * 100  # 비율로
ct_acne_norm.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
ax.set_title('Skin_Type별 Acne Internal_Type 비율 (%)\n— 처방 설계 가이드', fontsize=13, fontweight='bold')
ax.set_xlabel('Skin Type', fontsize=12)
ax.set_ylabel('비율 (%)', fontsize=12)
ax.legend(title='Internal Type', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
ax.set_ylim(0, 105)
plt.setp(ax.get_xticklabels(), rotation=0)
for container in ax.containers:
    labels = [f'{v:.0f}%' if v > 3 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, fontsize=7, label_type='center')
plt.tight_layout()
plt.savefig(OUT / 'skin_type_acne_guide.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"  ✓ skin_type_acne_guide.png")

print("\n\n모든 시각화 완료. scratch/ 에서 확인:")
print(f"  - skin_type_target_concerns.png")
print(f"  - acne_internal_by_skintype.png")
print(f"  - skin_type_concern_ingredients_heatmap.png")
print(f"  - skin_type_practical.png")
print(f"  - sensitivity_ingredient_diff.png")
print(f"  - skin_type_acne_guide.png")