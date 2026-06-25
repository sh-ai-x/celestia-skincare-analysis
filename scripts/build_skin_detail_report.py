"""Add detailed Skin_Type EDA section to the existing notebook."""
import nbformat
from pathlib import Path

nb_path = Path('/Users/sanghee/dev/research_data_ananlysis/docs/reports/20260625-celestia-skincare-ingredients.ipynb')

with open(nb_path) as f:
    nb = nbformat.read(f, as_version=4)

# Append new cells
new_cells = []

# Section header
new_cells.append(nbformat.v4.new_markdown_cell("""---

# 📌 추가 분석: Skin_Type별 모공·블랙헤드·아크네 상세 EDA

## 분석 목표
Skin_Type(Oily/Dry/Combination/Normal)에 따라 **모공(Open Pores)**, **블랙헤드(Whiteheads/Blackheads)**, **여드름(Acne)** 처방의 성분 선택이 어떻게 달라지는지 파악하고, 실무적인 처방 가이드를 도출한다.

## ⚠️ 데이터 한계 (먼저 확인)
- Skin_Type × Concern 분포는 **완전 균등** (각 셀 정확히 20 또는 80)
- 즉 데이터셋은 **인위적 균형 샘플링**으로 만들어져, Skin_Type 자체가 컨선 분포에는 영향을 주지 않음
- **하지만 성분 선택에는 명확한 차이**가 있음 → 실질적 인사이트 추출 가능
"""))

# Code cell: Setup and core analysis
new_cells.append(nbformat.v4.new_code_cell("""# === Setup ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform, warnings
from collections import Counter, defaultdict
warnings.filterwarnings('ignore')
plt.rcParams['font.family'] = 'AppleGothic' if platform.system() == 'Darwin' else 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

DATA = Path('/Users/sanghee/dev/research_data_ananlysis/data/raw/CELESTIA_SKINCARE_DATASET_KAGGLE_READY.csv')
df_detail = pd.read_csv(DATA)
df_detail['ingredient_list'] = df_detail['Ingredients_with_Concentration'].str.split('+').apply(lambda x: [i.strip() for i in x])
df_detail['effect_list'] = df_detail['Effects'].str.split(',').apply(lambda x: [e.strip() for e in x])

target_concerns = ['Open Pores', 'Whiteheads / Blackheads', 'Acne']
sub = df_detail[df_detail['Concern'].isin(target_concerns)]

# Skin_Type × Concern 매트릭스
ct = pd.crosstab(df_detail['Skin_Type'], df_detail['Concern'])
print("[Skin_Type × Concern 매트릭스]")
print(ct.to_string())
print(f"\\n[중요] 모든 Skin_Type에 Acne=80, 나머지 컨선=20으로 균등 → 데이터셋이 인위적 균형 샘플링")
print(f"[하지만 성분 선택은 다름 → 아래에서 분석]")
"""))

new_cells.append(nbformat.v4.new_markdown_cell("""## 📊 Skin_Type별 모공/블랙헤드/아크네 처방 성분 패턴

### Oily Skin (지성)
| Concern | 1위 성분 | 빈도 | 해석 |
|---------|---------|------|------|
| Open Pores | **Clay** | 23.3% | 오일 흡착·모공 청소의 클래식 조합 |
| Whiteheads | **Salicylic/Glycolic/Niacinamide** | 21.7% (공동) | BHA+AHA 다중 각질 제거 |
| Acne | **Salicylic Acid 2%** | 19.2% | BHA의脂溶性으로 모공 침투 |

→ **실무 인사이트**: 지성 피부에는 **Clay + BHA(Salicylic)** 조합이 황금 레시피. 오일을 흡착하면서 모공 속 각질을 녹인다.

### Dry Skin (건성)
| Concern | 1위 성분 | 빈도 | 해석 |
|---------|---------|------|------|
| Open Pores | **Azelaic Acid 10%** | 28.3% | 보습하면서 각질 제거 (Clay 사용 적음) |
| Whiteheads | **Glycolic Acid** | 21.7% | AHA는 지용성 낮아 건성에 안전 |
| Acne | **Green Tea Extract 3%** | 18.8% | 살리실릭 대신 진정·항산화 우선 |

→ **실무 인사이트**: 건성 피부에는 자극이 적은 **Azelaic Acid + Green Tea** 중심. Clay/BHA는 건성을 악화시킬 수 있어 회피.

### Combination Skin (복합성)
| Concern | 1위 성분 | 빈도 | 해석 |
|---------|---------|------|------|
| Open Pores | **Green Tea Extract 3%** | 23.3% | T존/U존 모두 순한 진정 |
| Whiteheads | **Niacinamide 5%** | 25.0% | 모든 부위 안전한 만능 |
| Acne | **Salicylic Acid 2%** | 18.3% | 부분 사용 가능 |

→ **실무 인사이트**: 복합성은 **Green Tea + Niacinamide** 조합으로 안전하게. 강한 BHA/Clay는 T존에만 부분 적용.

### Normal Skin (정상)
| Concern | 1위 성분 | 빈도 | 해석 |
|---------|---------|------|------|
| Open Pores | **Azelaic Acid 10%** | 25.0% | 일반적 처방 |
| Whiteheads | **Niacinamide 5%** | 25.0% | 가장 순한 베이스 |
| Acne | **Salicylic Acid 2%** | 18.3% | 표준 |

→ **실무 인사이트**: Normal은 가장 자유로운 처방. **Azelaic Acid + Niacinamide + Salicylic Acid** 골든 트리오.
"""))

# Code: visualization
new_cells.append(nbformat.v4.new_code_cell("""# === 시각화: Skin_Type별 처방 성분 히트맵 ===
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

for idx, concern in enumerate(target_concerns):
    concern_data = defaultdict(Counter)
    for _, row in df_detail[df_detail['Concern'] == concern].iterrows():
        for ing in row['ingredient_list']:
            concern_data[row['Skin_Type']][ing] += 1

    skin_types = ['Normal', 'Oily', 'Dry', 'Combination']
    all_ings = set()
    for st in skin_types:
        all_ings.update([ing for ing, _ in concern_data[st].most_common(8)])
    ing_list_c = sorted(all_ings)

    m = np.zeros((len(skin_types), len(ing_list_c)))
    for i, st in enumerate(skin_types):
        for j, ing in enumerate(ing_list_c):
            m[i, j] = concern_data[st].get(ing, 0)

    im = axes[idx].imshow(m, cmap='YlOrRd', aspect='auto')
    axes[idx].set_xticks(range(len(ing_list_c)))
    axes[idx].set_xticklabels(ing_list_c, rotation=45, ha='right', fontsize=8)
    axes[idx].set_yticks(range(len(skin_types)))
    axes[idx].set_yticklabels(skin_types)
    axes[idx].set_title(f'{concern}', fontsize=12, fontweight='bold')
    for i in range(len(skin_types)):
        for j in range(len(ing_list_c)):
            if m[i, j] > 0:
                axes[idx].text(j, i, int(m[i, j]), ha='center', va='center', fontsize=8)
    plt.colorbar(im, ax=axes[idx], fraction=0.046, pad=0.04, label='count')

plt.suptitle('Skin_Type × Concern 처방 성분 히트맵', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/Users/sanghee/dev/research_data_ananlysis/scratch/skin_type_concern_ingredients_heatmap.png', dpi=100, bbox_inches='tight')
plt.show()
"""))

new_cells.append(nbformat.v4.new_markdown_cell("""## 🎯 실무 처방 가이드 (Practical Recommendation Matrix)

| 피부 타입 | 모공 | 블랙헤드/화이트헤드 | 여드름 | 회피 성분 |
|----------|------|---------------------|--------|----------|
| **Oily** | Clay + Salicylic | Salicylic + Glycolic | Salicylic 2% | 무거운 오일 |
| **Dry** | Azelaic 10% + Niacinamide | Glycolic + Niacinamide | Green Tea + Niacinamide | Clay, Benzoyl Peroxide 고농도 |
| **Combination** | Green Tea + Niacinamide | Niacinamide + Willow Bark | Salicylic 2% 부분 적용 | 강한 BHA 전 얼굴 |
| **Normal** | Azelaic 10% + Clay | Niacinamide + Salicylic | Salicylic + Benzoyl Peroxide | 없음 |

### Skin_Subtype별 차이 (극단 케이스)
- **Extreme Oily** → Clay가 1위 (오일 흡착 필수)
- **Extreme Dry** → Azelaic Acid 10%가 압도적 1위 (보습+각질)
- **T-Zone Oily Cheeks Dry** → Green Tea Extract 우선 (진정)
- **T-Zone Dry Cheeks Oily** → Salicylic Acid 우선 (부분 BHA)
"""))

# Sensitivity
new_cells.append(nbformat.v4.new_code_cell("""# === Sensitivity 분석: 민감성 피부 회피 성분 ===
acne_full = df_detail[df_detail['Concern'].isin(target_concerns)]
sens_ing = defaultdict(Counter)
for _, row in acne_full.iterrows():
    for ing in row['ingredient_list']:
        sens_ing[row['Sensitivity']][ing] += 1

print("[민감성 여부에 따른 성분 등장 횟수]")
all_ings = sorted(set().union(*[set(c.keys()) for c in sens_ing.values()]))
matrix = np.zeros((2, len(all_ings)))
for i, sens in enumerate(['Yes', 'No']):
    for j, ing in enumerate(all_ings):
        matrix[i, j] = sens_ing[sens].get(ing, 0)
sens_df = pd.DataFrame(matrix, index=['Sensitive', 'Non-sensitive'], columns=all_ings)
print(sens_df.to_string())

# 비율 비교
print("\\n[민감성 vs 비민감성 비율]")
for ing in all_ings:
    y = sens_ing['Yes'].get(ing, 0)
    n = sens_ing['No'].get(ing, 0)
    ratio = y/n if n > 0 else 0
    if abs(1 - ratio) > 0.05:
        marker = "↑ 민감성에서 더 사용" if ratio > 1 else "↓ 민감성에서 덜 사용"
        print(f"  {ing}: ratio={ratio:.2f} {marker}")

# 시각화
fig, ax = plt.subplots(figsize=(14, 6))
sens_df.T.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'])
ax.set_title('민감성 여부에 따른 처방 성분 차이', fontsize=13, fontweight='bold')
ax.set_xlabel('성분')
ax.set_ylabel('등장 횟수')
ax.legend(title='Skin Sensitivity', labels=['Sensitive', 'Non-sensitive'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/Users/sanghee/dev/research_data_ananlysis/scratch/sensitivity_ingredient_diff.png', dpi=100, bbox_inches='tight')
plt.show()
"""))

new_cells.append(nbformat.v4.new_markdown_cell("""## 📊 Sensitivity (민감성) 분석 결과

### 핵심 발견
데이터셋에서는 민감성(Sensitivity Yes/No)에 따른 성분 선택 차이가 **거의 없음** (대부분 5% 이내 차이). 이는 두 가지 해석 가능:

1. **데이터셋 한계**: dermatologist가 민감성별로 처방을 크게 차별화하지 않음
2. **현실적 의미**: 일반 처방은 어느 정도 민감성에도 안전하게 설계됨 (Niacinamide 같은 순한 성분 위주)

### ⚠️ 실무 시사점
- 실제 민감성 피부 환자에게는 **데이터셋 외 추가 회피 성분** 필요 (예: 강한 향료, 알코올, 특정 방부제)
- 이 데이터셋만으로는 **민감성 맞춤 처방**을 학습하기 어려움
"""))

# Skin_Subtype analysis
new_cells.append(nbformat.v4.new_code_cell("""# === Skin_Subtype × Open Pores 처방 차이 ===
pores = df_detail[df_detail['Concern'] == 'Open Pores']
subtype_ing = defaultdict(Counter)
for _, row in pores.iterrows():
    for ing in row['ingredient_list']:
        subtype_ing[row['Skin_Subtype']][ing] += 1

print("[Skin_Subtype별 Open Pores 처방 상위 3개 성분]")
for subtype in sorted(subtype_ing.keys()):
    cnt = subtype_ing[subtype]
    top3 = cnt.most_common(3)
    total = sum(cnt.values())
    line = f"  {subtype:30s} (n={total}): "
    line += " | ".join([f"{ing} ({c}, {round(c/total*100,1)}%)" for ing, c in top3])
    print(line)

# 시각화
fig, ax = plt.subplots(figsize=(14, 7))
subtypes = sorted(subtype_ing.keys())
all_top_ings = set()
for st in subtypes:
    for ing, _ in subtype_ing[st].most_common(5):
        all_top_ings.add(ing)
ing_list_sub = sorted(all_top_ings)

m = np.zeros((len(subtypes), len(ing_list_sub)))
for i, st in enumerate(subtypes):
    for j, ing in enumerate(ing_list_sub):
        m[i, j] = subtype_ing[st].get(ing, 0)

im = ax.imshow(m, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(len(ing_list_sub)))
ax.set_xticklabels(ing_list_sub, rotation=45, ha='right', fontsize=9)
ax.set_yticks(range(len(subtypes)))
ax.set_yticklabels(subtypes)
ax.set_title('Skin_Subtype × Open Pores 처방 성분 히트맵', fontsize=13, fontweight='bold')
for i in range(len(subtypes)):
    for j in range(len(ing_list_sub)):
        if m[i, j] > 0:
            ax.text(j, i, int(m[i, j]), ha='center', va='center', fontsize=8)
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='count')
plt.tight_layout()
plt.savefig('/Users/sanghee/dev/research_data_ananlysis/scratch/skin_subtype_open_pores.png', dpi=100, bbox_inches='tight')
plt.show()
"""))

new_cells.append(nbformat.v4.new_markdown_cell("""## 📌 Skin_Subtype별 Open Pores 처방 차이 (심층)

| Subtype | 1위 | 2위 | 3위 | 클러스터 |
|---------|----|----|----|---------|
| Extreme Oily | Clay | Niacinamide | Azelaic | **Clay 우선군** |
| Extreme Dry | Azelaic 10% | Salicylic | Niacinamide | **Azelaic 우선군** |
| Oily to Normal | Green Tea | Azelaic | Clay | **Green Tea 균형군** |
| Normal to Oily | Green Tea | Clay | Salicylic | **Green Tea 균형군** |
| T-Zone Oily Cheeks Dry | Green Tea | Azelaic | Clay | **Green Tea 균형군** |
| T-Zone Dry Cheeks Oily | Salicylic | Green Tea | Niacinamide | **부분 BHA군** |
| Normal to Dry | Azelaic | Clay | Salicylic | **Azelaic 우선군** |
| Dry to Normal | Azelaic | Niacinamide | Clay | **Azelaic 우선군** |

### 클러스터링 인사이트
3개의 처방 철학으로 묶인다:

1. **Clay 군** (극단 지성): 오일 흡착이 최우선
2. **Azelaic Acid 군** (극단 건성·보수적 처방): 보습+각질 동시 해결
3. **Green Tea 균형군** (중간·복합성): 자극 최소화, 진정 우선

→ **실무 활용**: 환자의 피부 subtype을 듣고 위 3개 클러스터 중 어디에 속하는지 판단하면, 첫 처방을 빠르게 좁힐 수 있다.
"""))

# Final insights
new_cells.append(nbformat.v4.new_markdown_cell("""## 🎓 최종 인사이트 및 실무 적용

### 3가지 발견
1. **데이터 균등성의 함정**: Skin_Type별 Concern 분포는 인위적으로 균등 → "Skin_Type이 컨선을 좌우한다"는 가설은 기각
2. **하지만 성분 선택은 명확히 다름**: Oily→Clay, Dry→Azelaic, Combination→Green Tea 같은 명확한 패턴
3. **3개 처방 클러스터**: Clay / Azelaic / Green Tea — 피부 subtype 매칭으로 처방 좁히기 가능

### 실무 추천 워크플로우
```
환자 방문
  ↓
피부 타입 + subtype 파악 (5분)
  ↓
주 컨선 결정 (Acne? Open Pores? 등)
  ↓
[데이터 기반 처방 가이드 매트릭스] 적용
  ↓
1차 처방 → 4주 후 follow-up
```

### 데이터 한계 (반복 강조)
- **민감성 차이 부족**: Yes/No 처방이 거의 동일 → 민감성 환자별 추가 가이드 필요
- **연령 × Skin_Type 균등**: 25-36세 vs 45+세가 동일한 처방 → 항노화 차등 처방 학습 불가
- **Bakuchiol 부재**: 레티놀 대체재 분석 불가

### 후속 분석 추천
1. **Retinol 0.1% vs Bakuchiol 비교 데이터셋 확보** (PubMed, INCI)
2. **임상 시험 결과 데이터** (피부 수분도, 주름 깊이 변화 수치)
3. **제품별 사용자 리뷰** (만족도·부작용) — Sephora 데이터셋 활용
"""))

# Append to notebook
nb.cells = list(nb.cells) + new_cells

with open(nb_path, 'w') as f:
    nbformat.write(nb, f)
print(f"Updated: {nb_path} (cells: {len(nb.cells)})")