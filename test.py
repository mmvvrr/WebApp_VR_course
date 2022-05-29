import pandas as pd
import db_controller

users = db_controller.Students()
data = pd.read_excel('users.xlsx')

for i in range(data.shape[0]):
    las = data['last_name'][i]
    fir = data['first_name'][i]
    sur = data['surname'][i]
    group = str(data['group_id'][i])
    teacher = str(data['teacher_id'][i])
    users.add_user(group, teacher, fir, sur, las)