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

# 조 편성 버튼
if st.button('조 편성 시작!'):
    # 입력된 학생 수와 필요한 학생 수가 일치하는지 확인
    if num_students != total_required_students:
        st.error(f'입력한 전체 학생 수({num_students}명)가 조 구성을 위해 필요한 학생 수({total_required_students}명)와 다릅니다. 숫자를 맞춰주세요!')
    else:
        # 학생 리스트를 만들고 무작위로 섞기
        student_list = list(range(1, num_students + 1))
        random.shuffle(student_list)
        
        st.success('🎉 조 편성이 완료되었습니다!')
        
        current_index = 0
        
        # 조별 인원수와 개수에 따라 조 편성 및 출력
        for size, count in sorted(num_teams_by_size.items()):
            for i in range(count):
                team_members = student_list[current_index:current_index + size]
                
                # 조 제목 출력
                st.write(f'**{size}명인 조 ({i + 1}):**')
                
                # 학생 번호 리스트를 문자열로 변환하고 폰트 크기 키우기
                members_str = ' '.join(map(str, team_members))
                st.markdown(f"### {members_str}")

                current_index += size
