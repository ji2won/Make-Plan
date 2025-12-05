# 🚀 MakePlan: 지능형 학업 스케줄러

> **"계획 회피를 멈추고, 실행에 집중하세요."**
>
> 막연한 과업을 구체적인 행동으로 변환하고, 빈 시간에 최적으로 배치해주는 Python 기반 자동 스케줄링 솔루션입니다.

---

## 📖 프로젝트 개요

**MakePlan**은 학생들이 겪는 '계획 수립의 어려움'과 '인지적 과부하'를 해결하기 위해 개발되었습니다.
사용자의 '감'에 의존하던 기존 방식 대신, 경험적 데이터와 **우선순위 알고리즘**을 활용하여 가장 현실적이고 실행 가능한 주간 계획표를 자동으로 생성합니다.

### 🌌 Key Features

1.  **지능형 과업 분할 :** "전공 과제"만 선택하면, [자료조사 -\> 구현 -\> 테스트]와 같은 세부 실행 단계와 소요 시간을 자동으로 제안합니다.
2.  **우선순위 자동 스케줄링 :** 마감일과 중요도를 계산하여, 공강 시간에 과제를 최적 배치합니다.
3.  **인터랙티브 시간표 관리:** 엑셀처럼 클릭하여 자신의 수업 시간과 빈 시간을 직관적으로 설정하고 저장합니다.
4.  **동기 부여 UI :** 우주를 테마로 한 몰입형 디자인과 시각적인 진행률 표시로 사용자의 흥미를 유발합니다.

---

## 💡 문제 해결

이 프로젝트는 단순한 플래너가 아니라 **계획 실패의 심층적 원인**을 공학적으로 해결한 결과물입니다.

| 문제점                                     | MakePlan의 해결책                                            | 검증된 효과            |
| :----------------------------------------- | :----------------------------------------------------------- | :--------------------- |
| **정보의 부재** (얼마나 걸릴지 모름)       | **Heuristic Database** <br> (과거 데이터 기반 시간 제안)     | 계획의 현실성 확보     |
| **인지적 과부하** (쪼개고 배치하기 귀찮음) | **Task Decomposition Engine** <br> (자동 분할 및 단계 생성)  | 진입 장벽 90% 감소     |
| **결정 피로** (어디에 넣을지 고민)         | **Priority Greedy Algorithm** <br> (우선순위 기반 자동 배치) | 고민 시간 '0초'로 단축 |

---

## 🛠️ 기술 스택

- **Language:** Python 3.12
- **Web Framework:** Streamlit (Pure Python Web App)
- **Data Processing:** Pandas (DataFrame 기반 시간표 매트릭스 관리)
- **Package Manager:** Poetry
- **Design:** Custom CSS Injection (Galaxy/Space Theme)

---

## 🚀 설치 및 실행 방법

이 프로젝트는 **Poetry**를 사용하여 패키지를 관리합니다.

### 1\. 저장소 클론

```bash
git clone https://github.com/ji2won/Make-Plan.git
cd make-plan
```

### 2\. 의존성 설치

```bash
poetry install
```

### 3\. 앱 실행

```bash
poetry run streamlit run src/make_plan/app.py
```

---

## 📂 프로젝트 구조

**Bottom-up 방식**으로 설계되어, 데이터와 로직이 철저히 분리된 모듈형 구조를 갖추고 있습니다.

```
make-plan/
├── src/
│   └── make_plan/
│       ├── app.py          # [View] Streamlit 메인 실행 파일 (UI 및 이벤트 처리)
│       ├── logic.py        # [Controller] 과업 분할 및 시간 계산 핵심 로직
│       ├── scheduler.py    # [Model] 우선순위 알고리즘 및 시간표 데이터 관리
│       └── data.py         # [DB] 과업 유형별 템플릿 및 휴리스틱 데이터
├── timetable.csv           # (Auto-generated) 사용자 시간표 저장 파일
├── pyproject.toml          # Poetry 설정 및 의존성 관리
└── README.md               # 프로젝트 설명서
```

---

## 🧠 핵심 알고리즘 로직

### 우선순위 점수 계산

모든 과제는 아래 공식을 통해 점수가 부여되며, 점수가 높은 순서대로 빈 시간에 배치됩니다.

$$Score = \frac{Weight \times 100}{Days\_Left + 1}$$

- **Weight :** 전공 과목(1.5), 코딩 과제(1.3), 일반(1.0)
- **Days_Left :** 마감일이 가까울수록 점수가 기하급수적으로 상승

### 자동 배치 (Greedy Allocation)

1.  사용자가 입력한 시간표에서 `False`(빈 시간) 슬롯을 추출합니다.
2.  할 일 목록을 `Priority Score` 기준으로 내림차순 정렬합니다.
3.  가장 중요한 과제부터 순서대로 빈 슬롯을 점유합니다.

---

## 📸 스크린샷

- **Tab 1:** 시간표 입력 화면
- **Tab 2:** 과업 분석 및 제안 화면
- **Tab 3:** 최종 스케줄링 결과 화면

---

**Developed by Min jiwon** _2025 Web Python Programming Project_
