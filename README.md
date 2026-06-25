# Celestia Dermatology 스킨케어 성분 분석

> Dermatologist-validated skincare ingredient mapping analysis on the Celestia Dermatology dataset.

## 분석 목표
스킨 컨선(피부 고민)별로 어떤 성분이 추천되며, 농도와 효능이 어떻게 매핑되는지 탐색한다.
특히 레티놀(Retinol), 나이아신아마이드(Niacinamide), 바쿠치올(Bakuchiol)의 역할을 살펴본다.

## 데이터셋
- **출처**: [Celestia Dermatology Skincare Treatment Dataset](https://www.kaggle.com/datasets/ebinvadakkan/celestia-dermatology-skincare-treatment-dataset)
- **파일**: `CELESTIA_SKINCARE_DATASET_KAGGLE_READY.csv`
- **규모**: 1,120 rows × 8 columns
- **컬럼**: Age_Group, Skin_Type, Skin_Subtype, Sensitivity, Concern, Internal_Type, Ingredients_with_Concentration, Effects

## 핵심 발견

### 3-tier 성분 구조
- **Tier 1 (만능 Base)**: Niacinamide 5% (640회, 57.1%)
- **Tier 2 (컨선 특화)**: Salicylic Acid(Acne 66.3%), Retinol(Wrinkles 100%), Caffeine(Dark Circles), Tranexamic Acid(Hyperpigmentation)
- **Tier 3 (보조)**: Licorice, Green Tea, Hyaluronic Acid, Aloe Vera

### 검증된 가설 (5/5 PASS)
| 가설 | 신호강도 | 결과 |
|------|---------|------|
| H1: Retinol = Wrinkles 전용 | 36/36 = 100% | ✅ |
| H2: Salicylic Acid = Acne 특화 | 175/264 = 66.3% | ✅ |
| H3: Niacinamide = 만능 | 10/10 컨선 | ✅ |
| Bakuchiol 부재 확인 | 0/1120 | ✅ |
| 데이터 무결성 | 1120 rows, 결측치 0 | ✅ |

### 🔬 Verification Report

분석 완료 후 재실행 검증(verify-report) 결과:

```
============================================================
Celestia 가설 검증 재실행
============================================================
  PASS ✅  H1: Retinol → Wrinkles 100%: 36/36
  PASS ✅  H2: Salicylic Acid → Acne >50%: 66.3%
  PASS ✅  H3: Niacinamide → 모든 컨선: 10/10
  PASS ✅  Bakuchiol 부재: 0/1120
  PASS ✅  데이터 무결성: shape=(1120, 8), 결측치=0
============================================================
총 5/5 PASS
기록값: 5/5
검증: OK (차이: 0)
```

| 항목 | 값 |
|------|-----|
| 검증 방법 | `python3 scripts/verify_celestia.py` |
| 재실행 일치 | 5/5 (차이 0) |
| 최종 commit | `7696327 - Final verify-report: 5/5 PASS ✅` |
| slop 마커 | 0 (Celestia 전체 파일) |

### Skin_Type별 처방 가이드
| Skin Type | Open Pores 1위 | Acne 1위 | 처방 철학 |
|-----------|---------------|----------|----------|
| Oily | Clay | Salicylic 2% | 오일 흡착 + BHA |
| Dry | Azelaic Acid 10% | Green Tea | 보습 + 진정 |
| Combination | Green Tea | Salicylic 2% | 안전 균형 |
| Normal | Azelaic Acid 10% | Salicylic 2% | 표준 트리오 |

## 디렉토리 구조

```
├── README.md
├── docs/
│   ├── plans/
│   │   └── 20260625-celestia-dermatology-skincare.md  # 분석 계획
│   └── reports/
│       ├── 20260625-celestia-skincare-ingredients.ipynb  # executed notebook
│       ├── 20260625-celestia-skincare-ingredients.html   # 브라우저 리포트
│       └── 20260625-celestia-skincare-ingredients.md     # 요약
├── data/
│   └── raw/
│       └── CELESTIA_SKINCARE_DATASET_KAGGLE_READY.csv
├── scripts/
│   ├── check_data.py              # 데이터 검증
│   ├── eda_pass1.py               # EDA Pass 1 (Wide distribution)
│   ├── eda_pass2.py               # EDA Pass 2 (Concern × Ingredient)
│   ├── eda_skin_detail.py         # Skin_Type 심층 분석
│   ├── verify_celestia.py         # 가설 검증 (재실행용)
│   ├── build_report.py            # 노트북 빌드
│   ├── build_skin_detail_report.py # Skin_Type 섹션 추가
│   ├── add_descriptions.py        # 초보자용 해석 셀 추가
│   ├── add_todo.py                # TODO 섹션 추가
│   └── to_html.py                 # nbconvert 백업 변환기
└── scratch/                       # 중간 산출물 (PNG, JSON 등)
```

## 실행 방법

```bash
# 1. 환경 준비
pip install pandas scikit-learn matplotlib seaborn nbformat nbconvert jupyter

# 2. 데이터 다운로드
kaggle datasets download -d ebinvadakkan/celestia-dermatology-skincare-treatment-dataset \
  --unzip -p data/raw/

# 3. EDA 실행
python3 scripts/check_data.py
python3 scripts/eda_pass1.py
python3 scripts/eda_pass2.py
python3 scripts/eda_skin_detail.py

# 4. 검증
python3 scripts/verify_celestia.py

# 5. 노트북 빌드
python3 scripts/build_report.py
python3 scripts/build_skin_detail_report.py
python3 scripts/add_descriptions.py
python3 scripts/add_todo.py

# 6. 실행 + HTML 변환
jupyter nbconvert --to notebook --execute --inplace \
  docs/reports/20260625-celestia-skincare-ingredients.ipynb
jupyter nbconvert --to html \
  docs/reports/20260625-celestia-skincare-ingredients.ipynb \
  --output docs/reports/20260625-celestia-skincare-ingredients.html

# 7. 브라우저에서 열기
open docs/reports/20260625-celestia-skincare-ingredients.html
```

## 데이터 한계 (솔직한 평가)

- **Bakuchiol: 0건** → 레티놀 vs 바쿠치올 비교 불가 (다른 데이터셋 필요)
- **BHA/AHA 명목 부재** (단, Salicylic Acid = BHA, Glycolic/Lactic = AHA로 해석 가능)
- **연령대/Skin_Type별 Concern 균등 분포** → 개인화 추천 모델 학습에 부적합
- **민감성 차이 거의 없음** → Yes/No 처방 동일 (민감성 맞춤 학습 불가)

## 라이선스
Data: [CC0 (Public Domain)](https://www.kaggle.com/datasets/ebinvadakkan/celestia-dermatology-skincare-treatment-dataset)

## 후속 작업
노트북의 "📝 TODO" 섹션 참조. 우선순위는:
1. Bakuchiol 데이터셋 별도 확보
2. 임상 시험 결과 데이터 (PubMed/INCI)
3. Sephora 리뷰 데이터 보강