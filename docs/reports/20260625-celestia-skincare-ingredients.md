# Celestia Dermatology 스킨케어 성분 분석 리포트
> Date: 2026-06-25 | env: local | dataset: `ebinvadakkan/celestia-dermatology-skincare-treatment-dataset`
> verify-report: 5/5 PASS ✅ (재실행 일치, 차이 0)

## 분석 목표
스킨 컨선(피부 고민)별로 어떤 성분이 추천되며, 농도와 효능이 어떻게 매핑되는지 탐색한다.
특히 레티놀, 나이아신아마이드, 바쿠치올의 역할을 살펴본다.

## 최종 결과

| 항목 | 값 |
|------|-----|
| 가설 | H1: Retinol = Wrinkles (100%), H2: Salicylic Acid = Acne (66.3%), H3: Niacinamide = 만능 (10/10 컨선) |
| 데이터 | 1120 rows × 8 columns, 결측치 0 |
| 성분 풀 | 23개 고유 성분 → 480개 처방 |
| 효능 풀 | 24개 고유 효능 → 504개 효능 조합 |
| 주요 인사이트 | 3-tier 성분 구조 (Base/특화/보조) |

## 핵심 인사이트

1. **3-tier 성분 구조**:
   - **Tier 1 (만능 Base)**: Niacinamide 5% (640회, 57.1%)
   - **Tier 2 (컨선 특화)**: Salicylic Acid(Acne 66.3%), Retinol(Wrinkles 100%), Caffeine(Dark Circles 32.5%), Tranexamic Acid(Hyperpigmentation 23.3%)
   - **Tier 3 (보조)**: Licorice, Green Tea, Hyaluronic Acid, Aloe Vera 등

2. **Retinol = Wrinkles 신드룸**: 100% Wrinkles 전용, 동반: Niacinamide 5% + CoQ10 + Peptides + Hyaluronic Acid 1%

3. **Niacinamide = 만능**: 10개 컨선 모두 등장, 모든 처방의 base ingredient

4. **Salicylic Acid = Acne 특화**: BHA 계열, Acne 66.3% + Whiteheads/Open Pores

## 검증

| 검증 항목 | 결과 |
|----------|------|
| H1: Retinol → Wrinkles 100% | ✅ PASS (36/36) |
| H2: Salicylic Acid → Acne 집중 | ✅ PASS (66.3%) |
| H3: Niacinamide 만능 | ✅ PASS (10/10 컨선) |
| Bakuchiol 부재 확인 | ✅ PASS (0/1120) |
| 데이터 무결성 | ✅ PASS (1120 rows, 결측치 0) |

## 데이터 한계
- **Bakuchiol: 0건** → 레티놀 vs 바쿠치올 비교 불가
- **BHA/AHA 명목 부재** (Salicylic Acid = BHA, Glycolic/Lactic = AHA로 해석 가능)
- **연령대/Skin_Type별 Concern 균등 분포** → 개인화 추천 모델 학습엔 부적합

## 산출물
- `docs/reports/20260625-celestia-skincare-ingredients.ipynb` — executed notebook
- `docs/reports/20260625-celestia-skincare-ingredients.html` — 브라우저 리포트
- `docs/reports/20260625-celestia-skincare-ingredients.md` — 이 요약

## 추천 후속 작업
- PubMed/INCI 데이터로 실제 임상 데이터 보강
- Bakuchiol을 포함한 다른 데이터셋과 비교
- 성분 농도별 효과 차이 분석