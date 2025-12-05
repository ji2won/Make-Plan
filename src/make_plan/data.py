task_template = {
    "시험공부" : {
        "전공/심화" : {
            "unit" : "챕터",
            "time_per_unit" : {"min" : 2.0, "max" : 4.0, "default" : 2.5},
            "decomposition_template" : [("개념 정독 및 요약", 0.5), ("연습문제 풀이 및 오답노트", 0.4), ("최종 암기", 0.1)]
        },
        "교양/기초" : {
        "unit" : "챕터",
        "time_per_unit" : {"min" : 1.0, "max": 2.5, "default" : 1.5},
        "decomposition_template" : [("개념 정독 및 요약", 0.3), ("핵심 내용 요약", 0.2), ("암기", 0.3)]
        }
    },
    "과제/프로젝트" : {
        "코딩/프로그래밍" : {
            "unit" : "주요 기능",
            "time_per_unit" : {"min" : 1.0, "max" : 5.0, "default" : 3.0},
            "decomposition_template" : [("기본 설계 및 자료조사", 0.2), ("핵심 기능 개발", 0.6), ("테스트 및 디버깅", 0.2)] 
        },
        "레포트/글쓰기" : {
        "unit" : "페이지",
        "time_per_unit" : {"min" : 0.3, "max" : 2.0, "default" : 1.0},
        "decomposition_template" : [("자료 조사", 0.3), ("개요 작성", 0.1), ("본문 작성", 0.5), ("검토 및 수정", 0.1)]
        }
    }
}