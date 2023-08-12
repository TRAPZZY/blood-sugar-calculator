import matplotlib.pyplot as plt

class BloodSugarAnalyzer:
    def __init__(self):
        self.readings = []
        self.goals = {}

    def add_readings(self, values):
        self.readings.extend(values)

    def set_goal(self, goal_name, target_range):
        self.goals[goal_name] = target_range

    def calculate_average(self):
        if self.readings:
            total = sum(self.readings)
            return total / len(self.readings)
        else:
            return None

    def detect_trends(self):
        if len(self.readings) < 2:
            return "Insufficient data to detect trends"

        increasing = decreasing = stable = 0

        for i in range(1, len(self.readings)):
            if self.readings[i] > self.readings[i - 1]:
                increasing += 1
            elif self.readings[i] < self.readings[i - 1]:
                decreasing += 1
            else:
                stable += 1

        if increasing > decreasing and increasing > stable:
            return "Blood sugar is increasing over time"
        elif decreasing > increasing and decreasing > stable:
            return "Blood sugar is decreasing over time"
        else:
            return "Blood sugar is relatively stable"

    def generate_recommendation(self, average):
        if average is None:
            return "Insufficient data to provide recommendations"

        if average > 150:
            return "Your average blood sugar level is high. Consult a doctor for advice."
        elif average < 100:
            return "Your average blood sugar level is low. Consider adjusting your diet."

        return "Your blood sugar management is on track. Keep up the good work!"

    def suggest_meal(self, average):
        if average is None:
            return "Insufficient data to suggest a meal"

        if average > 150:
            return "Consider a balanced meal with whole grains, lean proteins, and plenty of vegetables."

        elif average < 100:
            return "Opt for a meal rich in complex carbohydrates, lean proteins, and healthy fats."

        return "Enjoy a well-balanced meal with a variety of nutrients to support your blood sugar levels."

    def plot_trends(self):
        if len(self.readings) < 2:
            print("Insufficient data to generate a plot")
            return

        plt.plot(self.readings, marker='o')
        plt.title("Blood Sugar Trends Over Time")
        plt.xlabel("Readings")
        plt.ylabel("Blood Sugar Level")

        # Plot goal ranges if set
        for goal_name, target_range in self.goals.items():
            if len(target_range) != 2:
                print(f"Invalid target range format for '{goal_name}'. Skipping.")
                continue

            plt.axhspan(target_range[0], target_range[1], alpha=0.3, color='green', label=goal_name)

        plt.legend()
        plt.show()

def main():
    print("Blood Sugar Trends Analyzer and Meal Planner with Progress Visualization and Goal Setting")
    print("=======================================================================================")

    user_name = input("Enter your name: ")
    analyzer = BloodSugarAnalyzer()

    num_weeks = int(input("Enter the number of weeks you want to track: "))
    for week in range(1, num_weeks + 1):
        print(f"\nWeek {week}")
        num_readings = int(input("Enter the number of blood sugar readings this week: "))
        readings = [float(input("Enter a blood sugar reading: ")) for _ in range(num_readings)]
        analyzer.add_readings(readings)

        average = analyzer.calculate_average()
        if average is not None:
            print("Average blood sugar:", average)

        trend = analyzer.detect_trends()
        print("Trend:", trend)

        recommendation = analyzer.generate_recommendation(average)
        print("Recommendation:", recommendation)

        meal_suggestion = analyzer.suggest_meal(average)
        print("Meal Suggestion:", meal_suggestion)

        goal_name = input("Enter a goal name (e.g., 'Normal Range'): ")
        target_range_input = input("Enter the target range (min max): ")
        target_range = tuple(map(float, target_range_input.split()))
        analyzer.set_goal(goal_name, target_range)

        analyzer.plot_trends()  # Display the blood sugar trends plot

        # Clear readings for the next week
        analyzer.readings.clear()

if __name__ == "__main__":
    main()
