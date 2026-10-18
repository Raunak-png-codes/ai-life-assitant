pip install mysql-connector-python

# ==========================================================
# PROJECT: AI LIFE ASSISTANT
# CLASS: XII - COMPUTER SCIENCE
# TECHNOLOGY: PYTHON AND MYSQL
# ==========================================================

import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- DATABASE CONNECTION ----------------

def connect_database():
    """Connect Python with the MySQL database."""
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ai_better_life"
        )

        if con.is_connected():
            print("\nDatabase connected successfully!")
            return con

    except Error as e:
        print("\nDatabase connection failed:", e)
        print("Check your MySQL server, username, password,")
        print("and whether the database has been created.")

    return None


# ---------------- RULE-BASED AI ENGINE ----------------

def get_suggestion(user_query):
    """
    Generate suggestions by matching keywords
    in the user's question.
    """

    query = user_query.lower()

    # Study Assistant
    if any(word in query for word in [
        "study", "exam", "revision", "concentrate",
        "focus", "homework", "learn"
    ]):
        category = "Study Assistant"
        suggestion = (
            "1. Set a small and achievable study goal.\n"
            "2. Keep your phone away while studying.\n"
            "3. Take short breaks between study sessions.\n"
            "4. Revise important topics regularly."
        )

    # Healthy Habits Assistant
    elif any(word in query for word in [
        "health", "sleep", "water", "hydration",
        "exercise", "healthy", "routine"
    ]):
        category = "Healthy Habits"
        suggestion = (
            "1. Maintain a regular sleep schedule.\n"
            "2. Drink water regularly throughout the day.\n"
            "3. Eat balanced meals.\n"
            "4. Include suitable physical activity in your routine."
        )

    # Stress Management Assistant
    elif any(word in query for word in [
        "stress", "anxiety", "worried", "tension",
        "relax", "pressure", "nervous"
    ]):
        category = "Stress Management"
        suggestion = (
            "1. Pause and take a few slow, comfortable breaths.\n"
            "2. Break a difficult task into smaller steps.\n"
            "3. Take a short break or talk to someone you trust.\n"
            "4. Seek help from a trusted adult if stress continues."
        )

    # Productivity Assistant
    elif any(word in query for word in [
        "time", "productive", "distraction", "schedule",
        "lazy", "organize", "organise", "manage"
    ]):
        category = "Productivity"
        suggestion = (
            "1. Write down your three most important tasks.\n"
            "2. Complete one task before starting another.\n"
            "3. Reduce unnecessary distractions.\n"
            "4. Review your progress at the end of the day."
        )

    # Eco-Friendly Living Assistant
    elif any(word in query for word in [
        "environment", "water saving", "electricity",
        "pollution", "plastic", "waste", "eco",
        "nature", "energy", "recycle"
    ]):
        category = "Eco-Friendly Living"
        suggestion = (
            "1. Switch off unused lights and appliances.\n"
            "2. Avoid single-use plastic where possible.\n"
            "3. Reuse and recycle suitable materials.\n"
            "4. Avoid wasting water and other resources."
        )

    # General Assistant
    else:
        category = "General Assistant"
        suggestion = (
            "Here are some general ways to improve daily life:\n"
            "1. Set realistic daily goals.\n"
            "2. Maintain a balanced routine.\n"
            "3. Learn something useful every day.\n"
            "4. Make time for rest and recreation.\n"
            "Try asking about studies, health, stress, "
            "productivity, or the environment for more "
            "specific suggestions."
        )

    return category, suggestion


# ---------------- SAVE INTERACTION ----------------

def save_interaction(con, user_name, category,
                     user_query, suggestion):

    cursor = None

    try:
        cursor = con.cursor()

        sql = """
        INSERT INTO interactions
        (user_name, category, user_query, suggestion)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            user_name,
            category,
            user_query,
            suggestion
        )

        cursor.execute(sql, values)
        con.commit()

        print("\nInteraction saved successfully in MySQL!")

    except Error as e:
        print("\nCould not save the interaction:", e)

        try:
            con.rollback()
        except Error:
            pass

    finally:
        if cursor is not None:
            cursor.close()


# ---------------- VIEW INTERACTION HISTORY ----------------

def view_history(con, user_name):
    cursor = None

    try:
        cursor = con.cursor()

        sql = """
        SELECT id, category, user_query, suggestion, created_at
        FROM interactions
        WHERE user_name = %s
        ORDER BY created_at DESC, id DESC
        """

        cursor.execute(sql, (user_name,))
        records = cursor.fetchall()

        print("\n" + "=" * 55)
        print("          PREVIOUS INTERACTIONS")
        print("=" * 55)

        if not records:
            print("No previous interactions found.")
            return

        for record in records:
            print("\nRecord ID:", record[0])
            print("Category:", record[1])
            print("Your Question:", record[2])
            print("AI Suggestion:")
            print(record[3])
            print("Date and Time:", record[4])
            print("-" * 55)

    except Error as e:
        print("\nCould not retrieve history:", e)

    finally:
        if cursor is not None:
            cursor.close()


# ---------------- VIEW ALL CATEGORIES ----------------

def show_categories():
    print("\n========== AVAILABLE CATEGORIES ==========")
    print("1. Study Assistant")
    print("2. Healthy Habits")
    print("3. Stress Management")
    print("4. Productivity")
    print("5. Eco-Friendly Living")
    print("6. General Assistant")
    print("==========================================")
    print("Enter a question related to any category.")


# ---------------- MAIN PROGRAM ----------------

def main():
    print("=" * 55)
    print("             AI LIFE ASSISTANT")
    print("       Artificial Intelligence for a Better Life")
    print("=" * 55)

    user_name = input("\nEnter your name: ").strip()

    if not user_name:
        user_name = "Guest"

    user_name = user_name[:50]

    # Connect to MySQL
    con = connect_database()

    if con is None:
        print("\nProgram stopped because the database")
        print("connection could not be established.")
        return

    try:
        while True:
            print("\n========== MAIN MENU ==========")
            print("1. Ask the AI Life Assistant")
            print("2. View Previous Interactions")
            print("3. View Available Categories")
            print("4. Exit")
            print("===============================")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                user_query = input(
                    "\nEnter your question: "
                ).strip()

                if not user_query:
                    print("Question cannot be empty.")
                    continue

                if len(user_query) > 255:
                    print("Please keep your question")
                    print("within 255 characters.")
                    continue

                # Generate the AI-style response
                category, suggestion = get_suggestion(
                    user_query
                )

                print("\n" + "=" * 55)
                print("AI LIFE ASSISTANT RESPONSE")
                print("=" * 55)
                print("Category:", category)
                print("\nYour Question:", user_query)
                print("\nSuggested Solutions:")
                print(suggestion)
                print("=" * 55)

                # Save the interaction
                save_interaction(
                    con,
                    user_name,
                    category,
                    user_query,
                    suggestion
                )

            elif choice == "2":
                view_history(con, user_name)

            elif choice == "3":
                show_categories()

            elif choice == "4":
                print("\nThank you for using AI Life Assistant!")
                print("Make every day a little better.")
                break

            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram interrupted. Goodbye!")

    finally:
        if con.is_connected():
            con.close()
            print("MySQL connection closed.")


# Execute the main program
if __name__ == "__main__":
    main()
