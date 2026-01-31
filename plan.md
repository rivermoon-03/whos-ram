# Whos-Ram 프로젝트 계획 (UI 고도화)

## 1. 프로젝트 개요

**목표**: 삼성전자 DDR5 RAM 가격을 주식 그래프(Highcharts Stock) 형태로 시각화하며, Nord Dark 테마를 적용하여 전문적인 대시보드를 구축합니다.

## 2. UI/UX 디자인 가이드 (Nord Dark)

- **테마**: Dark Nord (#2e3440 배경, #88c0d0 액센트)
- **컴포넌트 스타일**:
  - 버튼 및 카드의 곡률(Border Radius)을 최소화 (Sharp/Semi-sharp).
  - 차트를 중앙에 배치하여 시인성 확보.
- **필터**: 3일(3D), 1주(1W), 1달(1M), 3달(3M) 기간 필터 제공.

## 3. 차트 구현 상세 (Highcharts Stock)

- **차트 타입**: Candlestick 또는 고급 Area/Line Stock Chart.
- **데이터 처리**: 수집된 가격 데이터를 일별 시고저종(OHLC)으로 가공하거나, Stock용 시계열 데이터로 렌더링.
- **기능**: 내비게이터(Navigator), 범위 선택기(Range Selector) 포함.

## 4. 보안 및 배포

- `X-API-KEY` 인증 유지.
- Vercel 배포 시 영속성 DB(External DB) 및 환경 변수 설정.
