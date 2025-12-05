import pandas as pd
import math
from datetime import datetime, date

def create_empty_timetable():
    """
    빈 시간표 생성 (9시~24시)
    """
    times = [f"{h}:00" for h in range(9, 25)]
    days = ["월", "화", "수", "목", "금", "토", "일"]
    df = pd.DataFrame(False, index=times, columns=days)
    return df

def get_free_time(timetable_df):
    """
    체크박스 데이터프레임에서 False인(빈) 시간만 추출합니다.
    """
    free_slots = []
    for day in timetable_df.columns:
        for time in timetable_df.index:
            if not timetable_df.loc[time, day]: 
                free_slots.append((day, time))
    return free_slots

def calculate_priority(task):
    """
    우선순위 계산기를 계산합니다. 점수가 높을수록 먼저 배치됩니다.
    (가중치) / (남은 일수 + 1) * 100
    """
    deadline = task['deadline']
    today = date.today()
    days_left = (deadline - today).days
    
    if days_left < 0:
        days_left = 0
        
    weight = 1.0
    category_name = task.get('category', '')
    sub_category_name = task.get('sub_category', '')
    
    if "전공" in category_name or "전공" in sub_category_name:
        weight = 1.5
    elif "코딩" in sub_category_name:
        weight = 1.3
        
    score = (weight / (days_left + 1)) * 100
    return score

def auto_schedule(tasks, original_timetable_df):
    """
    할 일 목록을 시간표에 추가합니다.
    """
    final_df = pd.DataFrame("", index=original_timetable_df.index, columns=original_timetable_df.columns)
    free_slots = get_free_time(original_timetable_df)
    
    for day in final_df.columns:
        for time in final_df.index:
            if original_timetable_df.loc[time, day]:
                final_df.loc[time, day] = "🚫 수업/일정"

    for task in tasks:
        task['priority_score'] = calculate_priority(task)
        
    sorted_tasks = sorted(tasks, key=lambda x: x['priority_score'], reverse=True)
    
    
    slot_idx = 0 
    for task in sorted_tasks:
        task_name = task['sub_category']
        display_name = f"{task_name}({int(task['priority_score'])}점)"
        
        for step in task['plan_list']:
            step_name = step['step']
            needed_time = step['time']
            needed_slots = math.ceil(needed_time)
            
            if slot_idx + needed_slots > len(free_slots):
                break 
                
            for _ in range(needed_slots):
                if slot_idx < len(free_slots):
                    day, time = free_slots[slot_idx]
                    final_df.loc[time, day] = f"[{display_name}]\n{step_name}"
                    slot_idx += 1
                
    return final_df