from app import db
from app.models import Faculty, Department, Course, User, Application


faculties_data = {
    "Faculty of Arts and Humanities": {
        "Departments": {
            "Arts": [
                {"name": "Art & Visual Culture", "code": "ARTS101"},
                {"name": "Music", "code": "ARTS102"}
            ],
            "History": [
                {"name": "Africana", "code": "HIS101"},
                {"name": "American Studies", "code": "HIS102"},
                {"name": "European Studies", "code": "HIS103"},
                {"name": "French & Francophone Studies", "code": "HIS104"},
                {"name": "Religious Studies", "code": "HIS105"}
            ]
        }
    },

    "Faculty of Science": {
        "Departments": {
            "Biology": [
                {"name": "Bio Chemistry", "code": "BIO101"},
                {"name": "Genetics", "code": "BIO102"},
                {"name": "Microbiology", "code": "BIO103"}
            ],
            "Physics": [
                {"name": "Chemistry", "code": "PHY101"},
                {"name": "Earth & Climate Sciences", "code": "PHY102"},
                {"name": "Quantum Mechanics", "code": "PHY103"},
                {"name": "Thermodynamics", "code": "PHY104"}
            ]
        }
    },

    "Faculty of Communication and Social Sciences": {
        "Departments": {
            "Communication": [
                {"name": "Mass Communication", "code": "COM101"},
                {"name": "Journalism", "code": "COM102"}
            ],
            "Social Sciences": [
                {"name": "Anthropology", "code": "SOS101"},
                {"name": "English", "code": "SOS102"},
                {"name": "Economics", "code": "SOS103"},
                {"name": "Educational Studies", "code": "SOS104"},
                {"name": "Political Science", "code": "SOS105"},
                {"name": "Psychology", "code": "SOS106"},
                {"name": "Sociology", "code": "SOS107"}
            ]
        }
    },
    "Faculty of Law": {
        "Departments": {
            "Ethics": [
                {"name": "Ethics", "code": "ETH101"},
                {"name": "Morals", "code": "ETH102"}
            ],
            "Law": [
                {"name": "Law", "code": "LAW101"}
            ]
        }
    },
    "Faculty of Engineering": {
        "Departments": {
            "Engineering": [
                {"name": "Computer Science", "code": "ENG101"},
                {"name": "Digital & Computational Studies", "code": "ENG102"},
                {"name": "Engineering", "code": "ENG103"}
            ]
        }
    }
}

def seed_faculty_data():
    for faculty_name, faculty_info in faculties_data.items():
        faculty = Faculty(name=faculty_name)
        db.session.add(faculty)
        db.session.flush()  # Allows access to faculty.id without commit

        for dept_name, courses in faculty_info["Departments"].items():
            department = Department(name=dept_name, facultyID=faculty.id)
            db.session.add(department)
            db.session.flush()

            for course in courses:
                course_entry = Course(name=course["name"],code=course["code"],departmentID=department.id)
                db.session.add(course_entry)

    db.session.commit()
    print("Faculty, departments, and courses added successfully.")
