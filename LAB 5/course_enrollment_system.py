
"""Course enrollment management with safer coding practices."""

import hashlib
import json
import os
import secrets

COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

ENROLLMENT_STATE = {"total_tuition": 0.0}


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Enroll a student if the requested course is open."""
    if audit_trail is None:
        audit_trail = []

    if course_id not in COURSES or COURSES[course_id]["is_closed"]:
        return False

    COURSES[course_id]["seats"] -= 1
    if COURSES[course_id]["seats"] <= 0:
        COURSES[course_id]["is_closed"] = True

    ENROLLMENT_STATE["total_tuition"] += COURSES[course_id]["fee"]
    audit_trail.append(
        f"Enrolled {student_name} in {course_id} "
        f"with {credits_registered} credits."
    )
    return True


def drop_course(course_id):
    """Reopen a course and restore a seat if it exists."""
    if course_id not in COURSES:
        return False

    COURSES[course_id]["seats"] += 1
    COURSES[course_id]["is_closed"] = False
    return True


def check_course_status(course_id):
    """Return whether a course exists and is open."""
    course = COURSES.get(course_id)
    return course is not None and not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Calculate tuition after a validated discount between 0 and 1."""
    if course_id not in COURSES:
        raise ValueError(f"Unknown course: {course_id}")

    if not isinstance(discount_rate, (int, float)):
        raise ValueError("Discount rate must be numeric.")

    if isinstance(discount_rate, bool) or not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_fee = COURSES[course_id]["fee"]
    return base_fee * (1 - discount_rate)


def generate_student_hash(roll_no):
    """Return a SHA-256 digest of a student identifier."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a four-digit OTP using a secure random generator."""
    return secrets.randbelow(9000) + 1000


def export_course_roster(filename="course_roster.txt"):
    """Export the course catalog as UTF-8 JSON."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        json.dump(COURSES, roster_file, indent=4)

    print(f"Course roster exported to: {filename}")


def get_open_courses_summary(catalog):
    """Count courses that are currently open."""
    return sum(
        not details["is_closed"] for details in catalog.values()
    )


def main():
    """Run a demonstration of the enrollment system."""
    registrar_token = os.environ.get("REGISTRAR_AUTH_TOKEN")

    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")

    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", 0.25),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())

    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    print("Registrar token configured:", bool(registrar_token))


if __name__ == "__main__":
    main()
