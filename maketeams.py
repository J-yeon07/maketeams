import streamlit as st
import random

st.title('학생 조 편성 프로그램 🧑‍🤝‍🧑')
st.write('전체 학생 수와 조장을 선택해서 조를 편성해 보세요!')

# 1. 전체 학생 수 입력
# min_value를 2 이상으로 설정해 조장이 있어도 나머지 학생이 1명 이상 있도록 합니다.
num_students = st.number_input('전체 학생 수를 입력하세요:', min_value=2, value=10, step=1)

# 2. 조장 선택
student_list = list(range(1, num_students + 1))
if num_students > 0:
    team_leader = st.selectbox('조장을 선택하세요:', options=student_list)
else:
    st.info('학생 수를 먼저 입력해 주세요.')
    team_leader = None

# 조 편성 버튼
if st.button('조 편성 시작!'):
    if team_leader is not None:
        # 조장을 제외한 나머지 학생들 리스트 생성
        remaining_students = [s for s in student_list if s != team_leader]
        
        # 나머지 학생들을 무작위로 섞기
        random.shuffle(remaining_students)
        
        st.subheader(f'🌟 **{team_leader}번 학생이 조장인 조**')
        st.write('**조원:**', remaining_students)
        st.balloons()
    else:
        st.warning('조장과 학생 수를 선택해주세요!')
