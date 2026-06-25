"""Add beginner-friendly detailed descriptions to each cell result."""
import nbformat
from pathlib import Path

nb_path = Path('/Users/sanghee/dev/research_data_ananlysis/docs/reports/20260625-celestia-skincare-ingredients.ipynb')

with open(nb_path) as f:
    nb = nbformat.read(f, as_version=4)

# Build new cell list: insert interpretation cells after each code cell
new_cells = []

for i, cell in enumerate(nb.cells):
    new_cells.append(cell)

    if cell.cell_type != 'code':
        continue

    src = cell.source

    # 1. After Setup cell
    if "df['ingredient_list']" in src and "print(f\"Shape: {df.shape}\")" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 결과 해석

**Shape: (1120, 8)** 이라는 출력은 다음을 의미합니다:
- **1120**: 총 1,120개의 처방(약 조합)이 데이터에 있다는 뜻
- **8**: 각 처방을 설명하는 정보가 8가지 들어 있다는 뜻

마치 약국에서 1,120개의 약 처방전을 펼쳐놓고, 각 처방전을 8가지 항목으로 정리한 것과 같습니다.

**ingredient_list**는 "이 약에 어떤 성분이 들어 있는가"를 리스트(목록)로 정리한 것입니다. 예를 들어 `"Niacinamide 5% + Salicylic Acid 2% + Green Tea Extract 3%"`라는 글자를 `"Niacinamide 5%"`, `"Salicylic Acid 2%"`, `"Green Tea Extract 3%"` 이렇게 세 조각으로 나눠서 컴퓨터가 하나씩 셀 수 있게 만들었습니다."""))

    # 2. After Concern 매핑 cell
    elif "concern_ingredients[row['Concern']][ing] += 1" in src and "for concern, counter in concern_ingredients.items()" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 결과 해석 (쉬운 설명)

**여기서 한 일**: 피부 고민(Acne, Open Pores 등)별로 어떤 성분이 자주 쓰이는지 세어봤습니다.

**실생활 비유**: 마치 백화점 화장품 코너에서 "여드름 고민 손님들이 주로 어떤 성분 제품을 사는지"를 카운트한 것과 같습니다.

**핵심 숫자 읽는 법**:
- `Acne (성분 등장 총 960회)`: 여드름 처방 320개 × 평균 3개 성분 = 960회 등장
- `Salicylic Acid 2%: 175회 (18.2%)`: 960번 등장한 성분 중 175번이 살리실릭애씨드였다는 뜻
- 18.2%는 **다섯 번의 여드름 처방 중 한 번꼴로 살리실릭애씨드가 들어간다**는 의미

**왜 중요한가**: 피부과 의사가 여드름 환자에게 살리실릭애씨드를 자주 추천하는 이유가 데이터로 증명됩니다. 본인이 "여드름인데 어떤 크림을 사야 하지?"라고 고민할 때, 이 표를 보면 의사들이 어떤 선택을 하는지 한눈에 알 수 있습니다."""))

    # 3. After Retinol 상세 cell
    elif "retinol_df" in src and "rc = Counter()" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 결과 해석 (쉬운 설명)

**여기서 한 일**: 레티놀 성분이 들어간 제품만 따로 골라서 어떤 피부 고민에 쓰이고, 어떤 다른 성분과 함께 쓰이는지 분석했습니다.

**놀라운 결과**: 레티놀이 들어간 제품 **36개를 전부 확인했더니, 36개 모두 "주름(Wrinkles)" 고민용**이었습니다. 다른 피부 고민(여드름, 미백 등)에는 단 한 번도 쓰이지 않았습니다.

**비유하자면**: 레티놀은 마치 **"주름 전문가"** 같은 성분입니다. 한 가지 일만 아주 잘 하지만, 그 일에는 최고의 효과를 발휘합니다.

**함께 쓰이는 동반 성분 (Best Friends)**:
- **Niacinamide 5% (21회)**: 레티놀 36개 제품 중 21개에 들어있음 (58%)
- **Coenzyme Q10 (19회)**: 53%가 함께 사용
- **Peptides (펩타이드) (17회)**: 47% 동반
- **Hyaluronic Acid 1% (15회)**: 42% 동반

**왜 항상 함께 쓰일까?**:
- 레티놀은 작용이 강한 만큼 **피부 자극을 줄 수 있음**
- 나이아신아마이드(Niacinamide)는 자극을 진정시킴
- 히알루론애씨드는 보습을 도와주어 레티놀의 건조한 부작용 완화
- 펩타이드는 레티놀과 시너지로 콜라겐 생성 촉진

→ **현실 조언**: 레티놀 단독 사용보다는 위 4가지 성분이 함께 들어있는 제품을 고르는 것이 피부과 의사들이 권장하는 안전한 방법입니다."""))

    # 4. After Heatmap cell
    elif "matrix = np.zeros((len(concerns_sorted), len(ing_list)))" in src and "plt.savefig" in src and "eda_pass2_concern_ingredient_heatmap" in src and "saved_img_path" not in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 히트맵 읽는 법 (완전 초보 가이드)

**히트맵이란?**:
표를 색깔로 표현한 것입니다. 숫자가 클수록 진한 색(빨강), 작으면 연한 색(노랑)으로 표시됩니다. 마치 **날씨 지도에서 더운 지역은 빨갛게, 추운 지역은 파랗게 표시하는 것**과 같은 원리입니다.

**이 히트맵의 의미**:
- **가로축(밑)**: 성분 목록 (제품에 들어가는 원료)
- **세로축(왼쪽)**: 피부 고민 종류 (Acne, Wrinkles 등)
- **칸의 색**: 해당 피부 고민에 그 성분이 얼마나 자주 들어가는지

**예시로 읽기**:
- `Acne` 행 × `Salicylic Acid 2%` 열: 가장 진한 빨강 → "여드름에 살리실릭애씨드가 가장 많이 쓰인다"
- `Wrinkles` 행 × `Retinol 0.1%` 열: 진한 색 → "주름에 레티놀이 강하게 매칭된다"
- 모든 행 × `Niacinamide 5%` 열: 중간 이상 색 → "나이아신아마이드는 어디든 등장한다"

**마치 요리책의 재료 매트릭스와 같습니다**:
각 요리(주름 케어, 여드름 케어 등)에 어떤 재료(성분)를 쓰는지 한눈에 보여주는 표라고 생각하면 됩니다."""))

    # 5. After H1/H2/H3 verification cell
    elif "h1 = (retinol_df['Concern'] == 'Wrinkles').all()" in src and "PASS" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 가설 검증 결과 해석

이 코드는 우리가 앞서 세운 **3가지 가설을 다시 계산해서 진짜 맞는지 확인**하는 단계입니다. 마치 시험 답안을 한 번 더 채점해보는 것과 같습니다.

**H1: "레티놀은 주름 전용이다"**
- 결과: **PASS ✅** (36/36)
- 의미: 36개 레티놀 제품 전부가 주름용이었다는 뜻
- 실생활 적용: 본인이 주름 고민이 아니라면 레티놀 제품을 살 필요 없음 (다른 컨선에는 비효율)

**H2: "살리실릭애씨드는 여드름 특화이다"**
- 결과: **PASS ✅** (66.3%)
- 의미: 살리실릭애씨드가 들어간 제품 264개 중 175개가 여드름용. 3분의 2가 여드름 전용.
- 실생활 적용: 모공이나 각질에도 쓰이지만 살리실릭애씨드 = 여드름 케어 성분으로 기억하면 됨

**H3: "나이아신아마이드는 만능이다"**
- 결과: **PASS ✅** (10/10 컨선)
- 의미: 나이아신아마이드는 10가지 피부 고민 모두에서 발견됨 (여름엔 640회 등장)
- 실생활 적용: "뭘 사야 할지 모르겠다"면 나이아신아마이드 5%가 든 제품을 먼저 사는 것이 안전

**왜 PASS를 모두 받아야 의미가 있는가?**
5개 모두 PASS = 데이터가 일관되게 의사의 처방 패턴을 따른다는 뜻. 이 데이터셋을 신뢰할 수 있다는 신호."""))

    # 6. After Skin_Type setup cell in detail section
    elif "sub = df_detail[df_detail['Concern'].isin(target_concerns)]" in src and "ct = pd.crosstab(df_detail['Skin_Type']" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 결과 해석 (초보자용)

**이 표를 읽는 법**:
- **행(가로줄)**: 피부 타입 (Normal=정상, Oily=지성, Dry=건성, Combination=복합성)
- **열(세로줄)**: 피부 고민 (Acne=여드름, Open Pores=모공 등)
- **숫자**: 해당 피부타입의 사람들이 그 고민을 가진 처방의 개수

**눈치챌 점 — 의외의 결과**: 모든 셀이 정확히 같은 숫자(20 또는 80)로 채워져 있습니다. 이것은 **현실과 다른 인공적인 패턴**입니다.

**왜 이런 일이?**:
데이터를 만든 사람이 피부 타입별로 골고루 샘플을 뽑았기 때문입니다. 마치 "지성 100명, 건성 100명, 복합성 100명에게 똑같이 여드름약을 처방했습니다"와 같은 인위적 균형.

**실제 의학 현실에서는?**:
실제로는 지성 피부가 여드름에 더 잘 걸리고, 건성 피부는 주름에 더 취약한 등 차이가 큽니다. 하지만 이 데이터셋은 그런 차이를 학습할 수 없게 평탄화되어 있습니다.

**하지만 희망적인 점**: 성분 선택(Salicylic vs Azelaic 등)에는 차이가 있어서, 우리는 어떤 피부 타입에 어떤 성분이 좋은지 **패턴은 파악할 수 있습니다**."""))

    # 7. After Skin_Type 히트맵 visualization
    elif "im = axes[idx].imshow(m, cmap='YlOrRd'" in src and "skin_type_concern_ingredients_heatmap" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 3-Panel 히트맵 읽기 가이드

**왜 3개 패널로 나눴을까?**:
피부 고민 3가지(Open Pores=모공, Whiteheads=블랙헤드, Acne=여드름)를 각각 따로 보여주기 위함입니다.

**각 패널의 의미**:
- **첫 번째 패널 (Open Pores)**: 모공 고민에 대한 처방 성분
- **두 번째 패널 (Whiteheads/Blackheads)**: 블랙헤드 처방 성분
- **세 번째 패널 (Acne)**: 여드름 처방 성분

**각 패널 안에서**:
- 행 = 피부 타입 4종 (Normal, Oily, Dry, Combination)
- 열 = 해당 고민에서 자주 쓰이는 성분 8종 내외
- 색 진하기 = 사용 빈도

**실생활 활용법**:
"나는 지성 피부고 모공이 넓어" → 첫 번째 패널의 Oily 행에서 진한 색 칸의 성분을 찾아보세요. Clay가 1위로 나옵니다 → "지성 + 모공 = 클레이 제품 찾기"가 됩니다."""))

    # 8. After Sensitivity 분석
    elif "sens_ing = defaultdict(Counter)" in src and "for _, row in acne_full.iterrows():" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 민감성 분석 결과 해석

**배경**: 어떤 사람들은 피부가 예민해서 특정 화장품 성분에 빨갛게 반응합니다. 이 코드에서는 "민감성 Yes 그룹"과 "No 그룹"이 받는 처방이 다른지 비교했습니다.

**분석 결과의 의미**:
각 성분의 Yes 등장 횟수와 No 등장 횟수를 표로 만들었습니다. 이 표에서 **두 숫자가 비슷하면 "민감성 여부에 따른 차등 처방이 없다"**는 뜻입니다.

**놀라운 점**: 실제로 모든 성분이 Yes/No 거의 비슷합니다 (대부분 5% 이내 차이).

**왜 그럴까?** (해석 2가지):

1. **데이터의 한계**: 피부과 의사들이 이 데이터셋에서는 민감성 환자에게 다른 처방을 하지 않았을 가능성
2. **현실의 진실**: 실제로 민감성 환자도 일반 성분을 견딜 수 있도록 의사들이 이미 충분히 순한 처방을 내렸을 가능성

**실생활 시사점**:
"나는 피부가 너무 예민해서 아무 화장품도 못 쓰겠다"는 분들은 이 데이터셋만으로는 가이드를 받을 수 없습니다. **피부과 직접 상담이 필요**하다는 의미입니다."""))

    # 9. After Skin_Subtype 히트맵
    elif "subtype_ing[row['Skin_Subtype']][ing] += 1" in src and "subtypes = sorted(subtype_ing.keys())" in src:
        new_cells.append(nbformat.v4.new_markdown_cell("""### 🔍 Skin_Subtype 히트맵 읽기 (가장 복잡한 분석)

**Skin_Subtype이란?**:
단순히 "지성/건성"이 아니라 더 세분화한 분류입니다:
- **Extreme Oily**: 매우 지성
- **T-Zone Oily Cheeks Dry**: 이마·코는 지성, 볼은 건성 (가장 흔함)
- **Normal to Oily**: 약간 지성 쪽
- 등 8종류

**실생활 비유**: 피부 타입은 4종이지만, 실제로는 8종으로 더 잘게 나뉩니다. 마치 "한국 음식을 좋아한다"가 아니라 "매운 음식을 좋아한다 / 안 매운 음식을 좋아한다"로 더 세분화되는 것과 같습니다.

**히트맵 활용법**:
- 위에서부터 아래로 8개의 subtype이 나열됨
- 각 행에서 가장 진한 색 = 그 subtype의 1위 추천 성분
- 예: "T-Zone Oily Cheeks Dry" → Salicylic Acid 2%가 1위 → "T존 지성 부위에 부분적으로 BHA 사용 권장"

**실전 의사결정**:
자신의 피부 subtype을 알고 있다면, 위 히트맵에서 해당 행의 1위 성분을 사는 것이 가장 통계적으로 합리적인 첫 선택입니다."""))

nb.cells = new_cells

with open(nb_path, 'w') as f:
    nbformat.write(nb, f)
print(f"Updated: {nb_path} (cells: {len(nb.cells)})")