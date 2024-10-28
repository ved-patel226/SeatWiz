import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import random
from enum import Enum
import math

try:
    from .py_distance import euclidean_distance, index_to_coordinates
except ImportError:
    from py_distance import euclidean_distance, index_to_coordinates

from py_tools.essentials import MongoDBHandler


class StudentNode:
    def __init__(self, name):
        self.name = name
        self.friends = []
        self.enemies = []

    def add_relationships(self, friends, enemies):
        self.friends = friends
        self.enemies = enemies

    def __str__(self):
        return self.name


class Style(Enum):
    NEUTRAL = {
        "positive": -5,
        "negative": -10,
        "neutral": 5,
        "distance-factor": 0.1,
    }

    PROMOTE_FRIENDS = {
        "positive": 5,
        "negative": -10,
        "neutral": 0,
        "distance-factor": 0.1,
    }

    PROMOTE_DISTANCE = {
        "positive": 5,
        "negative": -10,
        "neutral": 0,
        "distance-factor": 1,
    }

    def __init__(self, values):
        self.values = values

    def get_values(self):
        return self.values


class Classroom:
    score_distance = 0
    score_postive = 0
    score_negative = 0
    score_neutral = 0

    def __init__(
        self,
        width,
        height,
        student_names=None,
        dbg=False,
        manual=False,
        style: Style = Style.NEUTRAL,
    ):

        if student_names is None:
            mongo = MongoDBHandler()
            students = mongo.find_many("students", {})
            student_names = [student["name"] for student in students]
            mongo.close()

        self.students = {name: StudentNode(name) for name in student_names}

        self.width = width
        self.height = height

        self.scores = style.get_values()

        self.debug = dbg
        if not manual:
            self.setup_relationships()
        else:
            self.manual_setup_relationships()

    def setup_relationships(self):
        all_students = list(self.students.keys())
        relationships_dict = {}
        for student in self.students.values():
            friends = random.sample(all_students, k=random.randint(1, 3))
            enemies = random.sample(all_students, k=random.randint(1, 3))
            friends = [f for f in friends if f != student.name]
            enemies = [e for e in enemies if e != student.name and e not in friends]
            student.add_relationships(friends, enemies)
            relationships_dict[student.name] = {"friends": friends, "enemies": enemies}
            if self.debug:
                print(f"{student.name}")
                print(f" - Friends: {friends}")
                print(f" - Enemies: {enemies}")
        return relationships_dict

    def db_make_relationships(self):
        mongo = MongoDBHandler()

        students = self.setup_relationships()

        id = 3019532
        for name, relations in students.items():
            document = {
                "_id": id,
                "name": name,
                "friends": relations["friends"],
                "enemies": relations["enemies"],
            }
            id += 1
            mongo.insert_one("students", document)

        print("Data inserted successfully")
        mongo.close()

    def load_relationships(self):
        mongo = MongoDBHandler()
        students = mongo.find_many("students", {})
        for student in students:
            student_name = student["name"]
            friends = student["friends"]
            enemies = student["enemies"]
            self.students[student_name].add_relationships(friends, enemies)
        mongo.close()

    def manual_setup_relationships(self):
        relationships = [
            ("A", ["B"], ["E"]),
            ("B", [], []),
            ("C", [], []),
            ("D", [], []),
            ("E", [], []),
            ("F", [], []),
            ("G", [], []),
            ("H", [], []),
            ("I", [], []),
        ]

        for student_name, friends, enemies in relationships:
            student = self.students[student_name]
            student.add_relationships(friends, enemies)
            if self.debug:
                print(f"{student.name}")
                print(f" - Friends: {friends}")
                print(f" - Enemies: {enemies}")

    def calculate_happiness_score(self, arrangement):
        score = 0
        student_map = {student.name: student for student in self.students.values()}
        Classroom.score_distance = 0
        Classroom.score_postive = 0
        Classroom.score_negative = 0
        Classroom.score_neutral = 0

        for idx, student_name in enumerate(arrangement):
            student = student_map[student_name]
            row = idx // self.width
            col = idx % self.width

            if col > 0:
                left_neighbor = arrangement[idx - 1]
                score += self.evaluate_relationship(student, left_neighbor)
            if col < self.width - 1:
                try:
                    right_neighbor = arrangement[idx + 1]
                    score += self.evaluate_relationship(student, right_neighbor)
                except:
                    pass

            if row < self.height - 1:
                try:
                    bottom_neighbor = arrangement[idx + self.width]
                    score += self.evaluate_relationship(student, bottom_neighbor)
                except:
                    pass
            if row > 0:
                top_neighbor = arrangement[idx - self.width]
                score += self.evaluate_relationship(student, top_neighbor)

            for person in student.enemies + student.friends:
                person_idx = arrangement.index(person)
                person_row, person_col = index_to_coordinates(person_idx, self.width)
                distance = euclidean_distance((row, col), (person_row, person_col))
                if person in student.friends:
                    distance_score = (
                        distance
                        * self.scores["distance-factor"]
                        * -1
                        * self.scores["positive"]
                    )
                else:
                    distance_score = (
                        distance
                        * self.scores["distance-factor"]
                        * -1
                        * self.scores["negative"]
                    )

                Classroom.score_distance += distance_score
                score += distance_score

        return score

    def evaluate_relationship(self, student, neighbor):
        if neighbor in student.friends:
            Classroom.score_postive += self.scores["positive"]
            return self.scores["positive"]
        elif neighbor in student.enemies:
            Classroom.score_negative += self.scores["negative"]
            return self.scores["negative"]
        else:
            Classroom.score_neutral += self.scores["neutral"]
            return self.scores["neutral"]

    def find_best_arrangement(self):
        current_arrangement = list(self.students.keys())
        random.shuffle(current_arrangement)
        best_arrangement = current_arrangement
        best_score = self.calculate_happiness_score(current_arrangement)

        for _ in range(10000):
            idx1, idx2 = random.sample(range(len(current_arrangement)), 2)
            current_arrangement[idx1], current_arrangement[idx2] = (
                current_arrangement[idx2],
                current_arrangement[idx1],
            )

            current_score = self.calculate_happiness_score(current_arrangement)

            if current_score > best_score:

                Classroom.best_negative = Classroom.score_negative
                Classroom.best_positive = Classroom.score_postive
                Classroom.best_neutral = Classroom.score_neutral
                Classroom.best_distance = Classroom.score_distance

                best_score = current_score
                best_arrangement = current_arrangement.copy()

        return best_arrangement, best_score

    def display_classroom(self):
        best_arrangement, best_score = self.find_best_arrangement()
        classroom = [["0" for _ in range(self.width)] for _ in range(self.height)]
        seating_index = 0

        for i in range(self.height):
            for j in range(self.width):
                if seating_index < len(best_arrangement):
                    classroom[i][j] = best_arrangement[seating_index]
                    seating_index += 1

        for row in classroom:
            while "0" in row:
                row.remove("0")

        if self.debug:
            print(f"Best Happiness Score: {best_score}")
            print("Score Breakdown:")
            print(f" - Positive: {Classroom.best_positive}")
            print(f" - Negative: {Classroom.best_negative}")
            print(f" - Neutral: {Classroom.best_neutral}")
            print(f" - Distance: {Classroom.best_distance}")

            print("Classroom Layout:")
            for row in classroom:
                print(row)
        return classroom


def main() -> None:
    student_names = [chr(i) for i in range(ord("A"), ord("A") + 23)]

    classroom = Classroom(student_names, width=5, height=5, dbg=True)
    classroom.load_relationships()
    classroom.display_classroom()


if __name__ == "__main__":
    main()
