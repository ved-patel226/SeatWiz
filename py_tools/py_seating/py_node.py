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
    score_distance = 0
    score_postive = 0
    score_negative = 0
    score_neutral = 0
    
    def __init__(self, student_names, width, height, dbg=False, manual=False):
        self.students = {name: StudentNode(name) for name in student_names}
        self.width = width
        self.height = height
    
        
        self.scores = {
            "positive": -5,
            "negative": -10,
            "neutral": 5,
            
            "distance-factor": 0.1,
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
                right_neighbor = arrangement[idx + 1]
                score += self.evaluate_relationship(student, right_neighbor)
            if row < self.height - 1:
                bottom_neighbor = arrangement[idx + self.width]
                score += self.evaluate_relationship(student, bottom_neighbor)
            if row > 0:
                top_neighbor = arrangement[idx - self.width]
                score += self.evaluate_relationship(student, top_neighbor)

            for person in student.enemies + student.friends:
                person_idx = arrangement.index(person)
                person_row, person_col = index_to_coordinates(person_idx, self.width)
                distance = euclidean_distance((row, col), (person_row, person_col))
                if person in student.friends:
                    distance_score = distance * self.scores["distance-factor"] * -1 * self.scores["positive"]
                else:
                    distance_score = distance * self.scores["distance-factor"] * -1 *self.scores["negative"]
                
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

        for _ in range(100000):
            idx1, idx2 = random.sample(range(len(current_arrangement)), 2)
            current_arrangement[idx1], current_arrangement[idx2] = current_arrangement[idx2], current_arrangement[idx1]

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
        classroom = [['0' for _ in range(self.width)] for _ in range(self.height)]
        seating_index = 0

        for i in range(self.height):
            for j in range(self.width):
                if seating_index < len(best_arrangement):
                    classroom[i][j] = best_arrangement[seating_index]
                    seating_index += 1
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
    student_names = [chr(i) for i in range(ord('A'), ord('A') + 25)]
    print(student_names)
    classroom = Classroom(student_names, width=5, height=5, dbg=True)
    classroom.display_classroom()

if __name__ == '__main__':
    main()
