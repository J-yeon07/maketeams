import streamlit as st
import random

st.title('학생 조 편성 프로그램 🧑‍🤝‍🧑')
st.write('조별 인원수를 설정해서 조를 편성해 보세요!')

# 1. 전체 학생 수 입력
num_students = st.number_input('전체 학생 수를 입력하세요:', min_value=1, value=10, step=1)

# 2. 각 조별 인원수 설정
st.subheader('각 조에 몇 명씩 배정할까요?')
num_teams_by_size = {}
num_teams_by_size[2] = st.number_input('2명인 조의 개수:', min_value=0, value=2, step=1)
num_teams_by_size[3] = st.number_input('3명인 조의 개수:', min_value=0, value=1, step=1)

# 계산된 총 학생 수 확인
total_required_students = sum(size * count for size, count in num_teams_by_size.items())
st.info(f'선택된 조 구성으로 필요한 총 학생 수: {total_required_students}명')

# 3. 조장 선택
student_list = list(range(1, num_students + 1))
if num_students > 0:
    team_leader = st.selectbox('조장을 선택하세요:', options=student_list)
else:
    st.info('학생 수를 먼저 입력해 주세요.')
    team_leader = None

# 조 편성 버튼
if st.button('조 편성 시작!'):
    # 입력된 학생 수와 필요한 학생 수가 일치하는지 확인
    if num_students != total_required_students:
        st.error(f'입력한 전체 학생 수({num_students}명)가 조 구성을 위해 필요한 학생 수({total_required_students}명)와 다릅니다. 숫자를 맞춰주세요!')
    elif team_leader is None:
        st.warning('조장을 선택해주세요!')
    else:
        # 조장 제외 학생 리스트
        remaining_students = [s for s in student_list if s != team_leader]
        random.shuffle(remaining_students)
        
        st.success('🎉 조 편성이 완료되었습니다!')
        
        # 조장 조 편성
        st.subheader(f'🌟 **1번 조 (조장: {team_leader}번 학생)**')
        # 조장이 1명이므로, 2명인 조는 1명, 3명인 조는 2명이 필요
        required_members_for_leader_team = 2 if num_teams_by_size.get(2) > 0 else 3
        st.write('**조원:**', remaining_students[:required_members_for_leader_team - 1])
        
        # 나머지 학생들로 다른 조 편성
        other_students = remaining_students[required_members_for_leader_team - 1:]
        
        st.subheader('---')
        st.subheader('📚 **나머지 조 편성**')
        
        current_index = 0
        
        for size, count in sorted(num_teams_by_size.items()):
            for i in range(count):
                # 조장 조는 이미 편성했으므로 2명인 조가 1개 이상이면 조장 조로 사용
                if size == 2 and i == 0 and num_teams_by_size.get(2) > 0:
                    continue
                
                team_members = other_students[current_index:current_index + size]
                st.write(f'**{size}명인 조:**', team_members)
                current_index += size
