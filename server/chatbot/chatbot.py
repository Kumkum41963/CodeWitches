import json
from difflib import get_close_matches

# Load the base from a JSON file
def load_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, base: dict) -> str | None:
    for i in base["questions"]:
        if i["question"] == question:
            return i["answer"]
    return None

def chat_bot():
    base: dict = load_base("fitness_base.json")
    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [i["question"] for i in base["questions"]])
        if best_match:
            answer: str = get_answer_for_question(best_match, base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don’t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                # Append the new question-answer pair
                base["questions"].append({"question": user_input, "answer": new_answer})
                
                # Save the updated base back to the JSON file
                save_base('fitness_base.json', base)
                print('Bot: Thank you! I learned a new response!')

# Example fitness questions base
fitness_base = {
    "questions": [
        {
            "question": "Hello",
            "answer": "Hello there!."
        },
        {
            "question": "How often should I work out?",
            "answer": "It's recommended to do at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week."
        },
        {
            "question": "What are good exercises for beginners?",
            "answer": "Some good exercises for beginners include walking, jogging, bodyweight exercises like squats and push-ups, and yoga."
        },
        {
            "question": "How can I lose weight?",
            "answer": "To lose weight, focus on a healthy diet, regular exercise, staying hydrated, and getting enough sleep."
        },
         {
      "question": "What are the best exercises for abs?",
      "answer": "Planks, crunches, leg raises, and mountain climbers are great for targeting abs. Combine with a calorie deficit for visible results."
    },
    {
      "question": "How much protein should I eat daily?",
      "answer": "You should eat about 1.2-2.0 grams of protein per kilogram of body weight per day to support muscle building."
    },
    {
      "question": "What is the best time to work out?",
      "answer": "The best time to work out is whenever you can stay consistent, but mornings can help with discipline and energy throughout the day."
    },
    {
      "question": "How much water should I drink daily?",
      "answer": "Drink at least 2-3 liters of water daily, more if you exercise or sweat a lot."
    },
    {
      "question": "Can I lose fat without exercise?",
      "answer": "Yes, you can lose fat by maintaining a calorie deficit through diet, but combining it with exercise improves results and overall health."
    },
    {
      "question": "How can I improve flexibility?",
      "answer": "Incorporate daily stretching or yoga into your routine. Hold each stretch for 20-30 seconds and focus on proper breathing."
    },
    {
      "question": "What is a calorie deficit?",
      "answer": "A calorie deficit occurs when you consume fewer calories than you burn, leading to weight loss."
    },
    {
      "question": "How often should I work out?",
      "answer": "Aim for 3-5 workout sessions per week, including strength training, cardio, and flexibility exercises."
    }
    ]
}

# Save the example base to a file
save_base("fitness_base.json", fitness_base)

# Run the chatbot
