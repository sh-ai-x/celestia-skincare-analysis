"""Add TODO section to the notebook for future work tracking."""
import nbformat
from pathlib import Path

nb_path = Path('/Users/sanghee/dev/research_data_ananlysis/docs/reports/20260625-celestia-skincare-ingredients.ipynb')

with open(nb_path) as f:
    nb = nbformat.read(f, as_version=4)

todo_cells = []

todo_cells.append(nbformat.v4.new_markdown_cell("""---

# 📝 TODO — 후속 작업 목록

## 🔴 Priority 1: 데이터 보강 (필수)

### T1.1 Bakuchiol 데이터셋 확보
- **현황**: Celestia 데이터셋에 Bakuchiol 0건 → Retinol vs Bakuchiol 비교 불가
- **목표**: Bakuchiol을 포함한 화장품 성분 데이터셋 별도 다운로드
- **검색 키워드**: `bakuchiol skincare`, `retinol alternative cosmetic`, `natural retinol dataset`
- **기대 효과**: Retinol 대비 Bakuchiol의 효능·안전성 비교 분석 가능

### T1.2 임상 시험 결과 데이터 추가
- **현황**: 처방 매핑만 있고 실제 efficacy 수치(피부 수분도, 주름 깊이 변화)가 없음
- **목표**: PubMed/INCI에서 성분별 임상 시험 결과 수집
- **검색 키워드**: `clinical trial niacinamide efficacy`, `retinol wrinkle depth measurement`
- **기대 효과**: descriptive → 정량적 efficacy 분석 가능

### T1.3 Sephora 리뷰 데이터 보강
- **현황**: 처방만 있고 실제 사용자 만족도가 없음
- **목표**: `nadyinky/sephora-products-and-skincare-reviews` 다운로드 후 결합
- **기대 효과**: 처방 × 만족도 × 가격의 3차원 분석

## 🟡 Priority 2: 분석 고도화

### T2.1 결정 트리 추천 모델
- **현황**: Skin_Type×Concern 균등 분포 → 분류 모델 학습 불가
- **목표**: 새 데이터셋으로 Skin_Type → Concern → Ingredient 추천 트리 학습
- **전제**: T1.1 ~ T1.3 중 하나 이상 완료 후 진행

### T2.2 성분 농도별 효능 차이 분석
- **현황**: Niacinamide 5%, Vitamin C 10% 같이 일부만 농도 명시
- **목표**: 농도 수치를 추출하여 dose-response curve 그리기
- **전제**: 농도 정보가 완전한 데이터셋 확보 필요

### T2.3 성분 조합 시너지 분석
- **현황**: 어떤 성분+성분이 자주 함께 쓰이는지만 확인됨
- **목표**: Apriori 알고리즘으로 association rule 도출 (lift ≥ 2)
- **전제**: T1 완료 후

## 🟢 Priority 3: 시각화/리포트 개선

### T3.1 인터랙티브 대시보드
- **현황**: 정적 PNG만 있음
- **목표**: Plotly/Streamlit 기반 인터랙티브 HTML
- **산출물**: `dashboard.html` (셀렉터로 Skin_Type/Concern/Ingredient 필터)

### T3.2 다국어 리포트
- **현황**: 한국어/영어 혼용
- **목표**: 영문 버전 별도 작성 (`20260625-celestia-skincare-ingredients.en.md`)

### T3.3 인사이트 영상
- **현황**: 텍스트 리포트만
- **목표**: 1분 분량 핵심 발견 요약 영상 (선택)

## ✅ 완료된 작업 (2026-06-25)

- [x] Kaggle 데이터셋 검색 (Celestia Dermatology 선정)
- [x] 데이터 다운로드 및 무결성 검증 (1120 rows)
- [x] EDA Pass 1 (Wide distribution)
- [x] EDA Pass 2 (Concern × Ingredient mapping)
- [x] 가설 3개 도출 및 검증 (5/5 PASS)
- [x] Skin_Type 심층 EDA (6개 시각화)
- [x] 처방 가이드 매트릭스 작성
- [x] ipynb + HTML + md 리포트 생성
- [x] nbconvert 템플릿 복구 (lab, base 등)

## 📌 진행 원칙

1. **Priority 1부터 순서대로**
2. 각 TODO 완료 시 이 셀의 체크박스 `[x]`로 업데이트
3. 새 TODO 발견 시 본 셀에 추가
4. 데이터셋 추가 시 `scratch/local-setup.md` 업데이트
"""))

nb.cells = list(nb.cells) + todo_cells

with open(nb_path, 'w') as f:
    nbformat.write(nb, f)
print(f"Updated: {nb_path} (cells: {len(nb.cells)})")