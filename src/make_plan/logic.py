from data import task_template

def suggest_plan(category, sub_category, scope):
    """ (str, str, int) -> (str, int)
    카테고리, 서브 카테고리를 받고 범위가 얼마나 되는지 받아서 구체적인 계획과
    총 걸리는 예상 시간을 반환합니다.
    """
    try:
        template = task_template[category][sub_category]
    except KeyError:
        return [], 0
    time_info = template["time_per_unit"]
    total_time = time_info["default"] * scope

    decomposed_plan = []
    recipe = template["decomposition_template"]

    for name, ratio in recipe:
        task_time = round(total_time * ratio, 1)
        if task_time == 0.0:
            task_time = 0.1

        decomposed_plan.append({"step" : name, "time" : task_time, "ratio" : ratio})

    return decomposed_plan, total_time