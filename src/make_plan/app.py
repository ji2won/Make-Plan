import streamlit as st
import sys
import os
import pandas as pd
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from make_plan.data import task_template
from make_plan.logic import suggest_plan
from make_plan.scheduler import create_empty_timetable, get_free_time, auto_schedule

TIMETABLE_FILE = "timetable.csv"
def set_space_theme():
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
        color: #ffffff;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
        background-size: 550px 550px, 350px 350px, 250px 250px;
        background-position: 0 0, 40px 60px, 130px 270px;
        z-index: 0;
        opacity: 0.6;
        pointer-events: none;
    }

    .main .block-container {
        z-index: 1;
        position: relative;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        border-bottom: 1px solid #2b303b;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        flex-grow: 1; /* 화면 꽉 채우기 */
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 8px 8px 0px 0px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #a0a0a0;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #00d2ff !important;
        height: 3px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(to top, rgba(0, 210, 255, 0.1), transparent) !important;
        color: #00d2ff !important;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }

    h1, h2, h3, h4, p, span, label, div {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(13, 17, 23, 0.8);
        border-right: 1px solid #30363d;
        z-index: 2;
    }

    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="base-input"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: white !important;
        border-radius: 6px;
    }
    input { color: white !important; }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2e1065 0%, #00d2ff 100%);
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.6);
    }

    [data-testid="stDataFrame"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    
    .stCheckbox span { color: #e0e0e0 !important; }
    .stProgress > div > div > div > div { background-color: #00d2ff; }
    
    .stSuccess, .stInfo {
        background-color: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid #30363d;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
def load_timetable():
    """
    파일이 있으면 불러오고 없으면 빈 시간표를 만듭니다.
    """
    if os.path.exists(TIMETABLE_FILE):
        return pd.read_csv(TIMETABLE_FILE, index_col=0)
    else:
        return create_empty_timetable()


def main():
    st.set_page_config(page_title="Make Plan", page_icon="🚀", layout="wide")
    set_space_theme()
    st.title("Make Plan 🌌")
    st.markdown("### ✨ 계획을 비서처럼 짜드려요!")
    st.markdown("막막한 계획을 Make Plan이 구체적인 실행 계획으로 바꿔드립니다.")
    st.divider()

    if 'timetable' not in st.session_state:
        st.session_state.timetable = load_timetable()

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
        
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = None
    
    tab1, tab2, tab3 = st.tabs(["1. 내 시간표 설정", "2. 할 일 추가", "3. 결과 확인"])
    
    with tab1 :
        st.header("주간 시간표를 입력해주세요")
        st.info("수업이 있거나 바쁜 시간을 체크해주세요. (자동으로 저장됩니다 💾)")

        edited_df = st.data_editor(
            st.session_state.timetable,
            column_config = {
                col: st.column_config.CheckboxColumn(col, default=False)
                for col in ["월", "화", "수", "목", "금", "토", "일"]
            },
            height = 600,
            width="stretch",
            key="timetable_editor" 
        )

        edited_df.to_csv(TIMETABLE_FILE)
        
        st.session_state.timetable = edited_df
        
        free_times = get_free_time(edited_df)
        st.write(f"현재 확보된 남는 시간 : **{len(free_times)}시간**")
        
    with tab2:
        st.header("📒 해야할 일 분석")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("1. 할 일 설정")
            category = st.selectbox("어떤 종류의 할 일인가요?", list(task_template.keys()))
            sub_categories = list(task_template[category].keys())
            sub_category = st.selectbox("구체적으로 어떤 작업인가요?", sub_categories)
            
            current_template = task_template[category][sub_category]
            unit_name = current_template["unit"]
            deadline = st.date_input("마감일은 언제인가요?", min_value=date.today())
            scope = st.number_input(f"분량은 얼마나 되나요? ({unit_name} 수)", min_value=1, value=1, step=1)
            
            if st.button("💫 계획 생성하기", type="primary"):
                plan_list, total_time = suggest_plan(category, sub_category, scope)
                st.session_state.current_plan = {
                    "category": category,
                    "sub_category": sub_category,
                    "scope": scope,
                    "total_time": total_time,
                    "plan_list": plan_list,
                    "template": current_template,
                    "deadline": deadline
                }

        with col2:
            st.subheader("2. 분석 결과")
            
            if st.session_state.current_plan:
                plan_data = st.session_state.current_plan
                days_left = (plan_data['deadline'] - date.today()).days
                d_day_str = "오늘 마감! 🔥" if days_left == 0 else f"D-{days_left}"
                st.success(f"[{d_day_str}] 계획을 실행하기 위해 총 **{plan_data['total_time']}시간**이 필요할 것으로 예상됩니다.")

                with st.container():
                    st.subheader("⏰ 시간 범위 제안")
                    min_t = plan_data['template']["time_per_unit"]['min'] * plan_data['scope']
                    max_t = plan_data['template']["time_per_unit"]["max"] * plan_data['scope']

                    st.info(f"""이런 종류의 할 일({plan_data['sub_category']} {plan_data['scope']} {unit_name})은 보통
                            최소 **{min_t}시간 ~ 최대 {max_t}시간**이 소요됩니다.
                            Make Plan은 합리적인 **{plan_data['total_time']}시간**을 기본값으로 제안합니다.""")
                
                st.divider()
                st.caption("🗒️ 구체적인 실행 단계")
                
                for idx, item in enumerate(plan_data['plan_list']):
                    label = f"Step {idx + 1}. {item['step']} ({item['time']}시간)"
                    st.checkbox(label, value=True, key=f"check_{idx}")
                    st.progress(item['ratio'])
                
                st.divider()
                
                if st.button("📌 이 계획을 할 일 목록에 추가하기"):
                    st.session_state.tasks.append(plan_data)
                    st.session_state.current_plan = None
                    st.toast("할 일이 성공적으로 추가되었습니다!", icon="✅")
                    st.rerun()

    with tab3:
        st.header("📓 최종 할 일 목록")
        
        if not st.session_state.tasks:
            st.warning("아직 추가된 할 일이 없습니다. 계획을 생성하고 추가해주세요.")
        else:
            st.write(f"총 **{len(st.session_state.tasks)}개**의 할 일이 등록되었습니다.")
            
            for i, task in enumerate(st.session_state.tasks):
                with st.expander(f"{i + 1}. {task['sub_category']} (총 {task['total_time']}시간)"):
                    st.write(f"분량: {task['scope']} 단위")
                    st.write("세부 계획:")
                    for step in task['plan_list']:
                        st.text(f"- {step['step']}: {step['time']}시간")
                    
                    if st.button("삭제", key=f"del_{i}"):
                        del st.session_state.tasks[i]
                        st.rerun()
            
            st.divider()
            
            st.subheader("🚀 빈 시간 자동 스케줄링")
            if st.button("빈 시간에 채워넣기", type="primary"):
                final_schedule = auto_schedule(st.session_state.tasks, edited_df)
                st.session_state.final_schedule = final_schedule
                st.success("배치가 완료되었습니다! 아래 시간표를 확인하세요.")

        if 'final_schedule' in st.session_state:
            st.markdown("### 🗓️ 완성된 주간 계획표")
            st.dataframe(
                st.session_state.final_schedule, 
                use_container_width=True, 
                height=600
            )

if __name__ == "__main__":
    main()