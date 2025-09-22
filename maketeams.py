import streamlit as st
import random
import math

st.title('학생 조 편성 프로그램 🧑‍🤝‍🧑')
st.write('전체 학생 수와 한 조당 인원수를 입력해서 조를 편성해 보세요!')

# 1. 전체 학생 수 입력
num_students = st.number_input('전체 학생 수를 입력하세요:', min_value=1, value=10, step=1)

# 2. 한 조당 인원수 입력
# 최소 1명으로 설정하여 조를 만들 수 있도록 합니다.
num_per_team = st.number_input('한 조에 몇 명씩 배정할까요?', min_value=1, value=3, step=1)

# 3. 조장 선택 (이 부분은 이전과 동일)
student_list = list(range(1, num_students + 1))
if num_students > 0:
    team_leader = st.selectbox('조장을 선택하세요:', options=student_list)
else:
    st.info('학생 수를 먼저 입력해 주세요.')
    team_leader = None

# 조 편성 버튼
if st.button('조 편성 시작!'):
    if num_students > 0 and num_per_team > 0 and team_leader is not None:
        
        # 4. 조 편성 로직
        remaining_students = [s for s in student_list if s != team_leader]
        random.shuffle(remaining_students)
        
        # 조장 조 편성 (조장 + 남는 학생으로 구성)
        st.subheader(f'🌟 **1번 조 (조장: {team_leader}번 학생)**')
        st.write('**조원:**', remaining_students[:num_per_team-1]) # 조장을 제외한 나머지 인원으로 구성
        
        # 나머지 학생들로 다른 조 편성
        other_students = remaining_students[num_per_team-1:]
        
        if len(other_students) > 0:
            st.subheader('---')
            st.subheader('📚 **나머지 조 편성**')
            
            # math.ceil() 함수를 사용해 남은 학생들을 나눌 조의 개수를 계산
            num_other_teams = math.ceil(len(other_students) / num_per_team)
            
            for i in range(num_other_teams):
                start_index = i * num_per_team
                end_index = start_index + num_per_team
                team_members = other_students[start_index:end_index]
                
                st.write(f'**{i + 2}번 조:**', team_members)
    else:
        st.warning('학생 수, 조당 인원, 조장을 모두 선택해주세요!')
