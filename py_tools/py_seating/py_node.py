import itertools
import random

try:
    from .py_distance import euclidean_distance, index_to_coordinates
except ImportError:
    from py_distance import euclidean_distance, index_to_coordinates

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

class Classroom:
    def __init__(self, student_names, width, height, dbg=False, manual=False):
        self.students = {name: StudentNode(name) for name in student_names}
        self.width = width
        self.height = height
        self.scores = {
            "positive": -5,
            "negative": -10,
            "neutral": 5,
        }
        self.debug = dbg
        if not manual:
            self.setup_relationships()
        else:
            self.manual_setup_relationships()
        
    def setup_relationships(self):
        all_students = list(self.students.keys())
        for student in self.students.values():
            friends = random.sample(all_students, k=random.randint(1, 3))
            enemies = random.sample(all_students, k=random.randint(1, 3))
            friends = [f for f in friends if f != student.name]
            enemies = [e for e in enemies if e != student.name and e not in friends]
            student.add_relationships(friends, enemies)
            if self.debug:
                print(f"{student.name}")
                print(f" - Friends: {friends}")
                print(f" - Enemies: {enemies}")

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
        
        for idx, student_name in enumerate(arrangement):
            student = student_map[student_name]
            row = idx // self.width
            col = idx % self.width

            print(f"Student: {student} ({row}, {col})")
            
            if col > 0:
                left_neighbor = arrangement[idx - 1]
                score += self.evaluate_relationship(student, left_neighbor)
            if col < self.width - 1:
                right_neighbor = arrangement[idx + 1]
                score += self.evaluate_relationship(student, right_neighbor)
            if row < self.height - 1:
                bottom_neighbor = arrangement[idx + self.width]
                score += self.evaluate_relationship(student, bottom_neighbor)
            if row > 0:
                top_neighbor = arrangement[idx - self.width]
                score += self.evaluate_relationship(student, top_neighbor)
        
        return score

    def evaluate_relationship(self, student, neighbor):
        if neighbor in student.friends:
            return self.scores["positive"]
        elif neighbor in student.enemies:
            return self.scores["negative"]
        else:
            return self.scores["neutral"]

    def find_best_arrangement(self):
        current_arrangement = list(self.students.keys())
        random.shuffle(current_arrangement)
        best_arrangement = current_arrangement
        best_score = self.calculate_happiness_score(current_arrangement)

        for _ in range(100000):
            idx1, idx2 = random.sample(range(len(current_arrangement)), 2)
            current_arrangement[idx1], current_arrangement[idx2] = current_arrangement[idx2], current_arrangement[idx1]

            current_score = self.calculate_happiness_score(current_arrangement)

            if current_score > best_score:
                best_score = current_score
                best_arrangement = current_arrangement.copy()

        return best_arrangement, best_score

    def display_classroom(self):
        best_arrangement, best_score = self.find_best_arrangement()
        classroom = [['0' for _ in range(self.width)] for _ in range(self.height)]
        seating_index = 0

        for i in range(self.height):
            for j in range(self.width):
                if seating_index < len(best_arrangement):
                    classroom[i][j] = best_arrangement[seating_index]
                    seating_index += 1

        print(f"Best Happiness Score: {best_score}")
        print("Classroom Layout:")
        for row in classroom:
            print(row)

student_names = [chr(i) for i in range(ord('A'), ord('A') + 9)]
print(student_names)
classroom = Classroom(student_names, width=3, height=3, dbg=True, manual=True)
classroom.display_classroom()
