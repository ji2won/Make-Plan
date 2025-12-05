from logic import suggest_plan

def main():
    print("Make Plan!\n")
    print("[1] 시험공부 [2] 과제/프로젝트\n")
    input_category = input("카테고리를 선택해주세요 (숫자만 입력) : ")
    category = ""
    if input_category == "1" :
        category = "시험공부"
        print("\n[1] 전공/심화 [2] 교양/기초\n")
        input_sub = input("소분류를 선택하세요 (숫자만 입력) : ")
        while(True):
            if input_sub == "1":
                sub_category = "전공/심화"
                break
            elif input_sub == "2" :
                sub_category = "교양/기초"
                break
            else:
                print("1, 2 중에 다시 입력해주세요\n")
    elif input_category == "2":
        category = "과제/프로젝트"
        print("\n[1] 코딩/프로그래밍 [2] 레포트/글쓰기\n")
        input_sub = input("소분류를 선택하세요 (숫자만 입력) : ")
        while(True):
            if input_sub == "1":
                sub_category = "코딩/프로그래밍"
                break
            elif input_sub == "2" :
                sub_category = "레포트/글쓰기"
                break
            else:
                print("1, 2 중에 다시 입력해주세요\n")
    else:
        print("잘못된 입력입니다.")
        return
    
    input_scope = input("\n분량은 얼마나 되나요? (숫자만 입력) : ")
    scope = int(input_scope)

    plan_list, total_time = suggest_plan(category, sub_category, scope)

    print("\n[Make Plan의 제안]\n")
    print(f"선택하신 {sub_category}의 예상 소요 시간은 총 {total_time}시간 입니다.")
    print("\n[구체적인 실행 계획]")
    for step in plan_list:
        print(f"{step['step_name']} : {step['estimated_time']}시간")
if __name__ == "__main__":
    main()