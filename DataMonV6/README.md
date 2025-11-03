# Datamon — Web Edition

Datamon is a math problem helper that helps students, teachers, and parents make math fun!  
This web version uses **Streamlit** to provide an interactive interface for three math games:
- **Answer Checker**
- **Memory Bank**
- **Electro Flash**

------------------------------------

## How to Install Dependencies:

1. Make sure you have **Python 3.9+** installed.
2. Install Streamlit using:
   ```bash
   pip install -r requirements.txt

------------------------------------

How to Run the Application:

If running locally (on your computer):

	1. Open a terminal (or command prompt).
	2. Navigate to the folder containing app.py.
	3. Run:
		  streamlit run app.py
	4. Your default browser will open automatically to the app.

If running online on Streamlit Cloud:

	1. The app runs automatically when deployed.
	2. The Main file path is app.py.

------------------------------------

What it Does:

Answer Checker:
	Lets users input a math equation and an answer (e.g., 4+4 and 8) and checks correctness.

Memory Bank:
	Users can create a custom set of math problems to practice with up to 3 tries per problem. Feedback messages are given based on performance.

Electro Flash:
	A fast-paced math quiz that lets users practice math tables using addition, subtraction, multiplication, or division.

------------------------------------

Known Limitations:

The app does not yet save user progress or scores between sessions. All problems reset if the app is refreshed. Some features from the original console version (e.g., text-based menus) are simplified for the web. The app assumes valid numeric inputs — invalid text entries might cause minor errors.

------------------------------------

Developed by:
Haylee, Kaheel, Teresa, Aryan, and James

------------------------------------

(Written with the assistance of ChatGPT, prompted and edited by Haylee.)