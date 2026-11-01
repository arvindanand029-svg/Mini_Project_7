import json


class StudentRecordError(Exception):
    pass

def validate_student(record, seen_ids):

    if not isinstance(record, dict):
        raise StudentRecordError("Record must be a dictionary.")

    required = ["student_id", "name", "department", "marks"]

    for field in required:
        if field not in record:
            raise StudentRecordError(
                f"Missing required field '{field}'."
            )

    student_id = record["student_id"]


    if not isinstance(student_id, str) or not student_id.strip():
        raise TypeError("Student ID must be a non-empty string.")

    if not isinstance(record["name"], str) or not record["name"].strip():
        raise TypeError("Name must be a non-empty string.")

    if not isinstance(record["department"], str) or not record["department"].strip():
        raise TypeError("Department must be a non-empty string.")


    if student_id in seen_ids:
        raise StudentRecordError(
            f"Duplicate student ID: {student_id}"
        )

    seen_ids.add(student_id)

    marks = record["marks"]

    if not isinstance(marks, list):
        raise TypeError("Marks must be a list.")

    if len(marks) != 3:
        raise StudentRecordError(
            "Marks must contain exactly 3 values."
        )

    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise TypeError("Marks must be numeric values.")

        if not 0 <= mark <= 100:
            raise StudentRecordError(
                "Marks must be between 0 and 100."
            )

    return record



def main():

    path = input(
        "Enter input file path (press Enter for default): "
    ).strip()

    if not path:
        path = "students_input.json"

    print(f"\nImport started: {path}")

    try:
        with open(path, "r", encoding="utf-8") as file:
            students = json.load(file)

    except FileNotFoundError:
        print("Error: Input file not found.")
        return

    except PermissionError:
        print("Error: Permission denied.")
        return

    except json.JSONDecodeError as error:
        print("Error: Invalid JSON format:", error)
        return

    except OSError as error:
        print("File error:", error)
        return

    else:
        print("JSON file loaded successfully.")

    finally:
        print("Input reading attempt finished.")


    if not isinstance(students, list):
        print("Error: JSON must contain a list of student records.")
        return

    valid_students = []
    errors = []
    seen_ids = set()

    for index, student in enumerate(students, start=1):

        try:
            valid = validate_student(student, seen_ids)
            valid_students.append(valid)

            print(
                f"Accepted: {valid['student_id']} - {valid['name']}"
            )

        except (StudentRecordError, TypeError, ValueError, KeyError) as error:

            message = f"Rejected record {index}: {error}"
            errors.append(message)
            print(message)

    try:
        with open(
            "students_valid.json", "w", encoding="utf-8"
        ) as file:
            json.dump(valid_students, file, indent=4)

        # Write rejected records
        with open(
            "import_errors.txt", "w", encoding="utf-8"
        ) as file:
            for error in errors:
                file.write(error + "\n")

    except OSError as error:
        print("Output file error:", error)
        return

    print("\nImport completed.")
    print("Accepted records:", len(valid_students))
    print("Rejected records:", len(errors))
    print("Valid output: students_valid.json")
    print("Error log: import_errors.txt")


if __name__ == "__main__":
    main()


