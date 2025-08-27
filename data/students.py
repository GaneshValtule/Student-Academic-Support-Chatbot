import pandas as pd
import random
import faker

# Initialize Faker
fake = faker.Faker()

# Parameters
num_students = 50
subjects = ['DBMS', 'OS', 'DSA', 'ML']
total_assignments_per_subject = {'DBMS': 10, 'OS': 12, 'DSA': 15, 'ML': 8}

# Generate student info
students = []
for i in range(1, num_students + 1):
    students.append({
        'Student_ID': f"S{i:03d}",
        'Student Name': fake.name()
    })

# Generate academic data
data = []
for student in students:
    for subject in subjects:
        total_assignments = total_assignments_per_subject[subject]
        assignments_completed = random.randint(0, total_assignments)
        marks = random.randint(40, 100)
        attendance = round(random.uniform(60, 100), 2)
        remarks = 'Pass' if marks >= 50 and attendance >= 75 else 'Fail'
        
        data.append({
            'Student_ID': student['Student_ID'],
            'Student Name': student['Student Name'],
            'Subject': subject,
            'Marks': marks,
            'Assignments Completed': assignments_completed,
            'Total Assignments': total_assignments,
            'Attendance %': attendance,
            'Remarks': remarks
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('students.csv', index=False)

print("CSV file 'students.csv' created successfully!")
