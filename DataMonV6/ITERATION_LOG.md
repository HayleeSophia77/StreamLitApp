Haylee Paredes  
CTS-285-0001  
HW.3.1  
11/05/2025

### AI Prompts:

“Hi, can you build a Streamlit app that accepts datamon and answer inputs, please? I have my datamon files here.”  
	“Okay, I really like the web app, but there are some things that need to be improved on. For instance, every time I enter an answer, it says press enter to apply. For some reason, it won't move on, and I HAVE to click Submit to move on. I want to be able to do the same thing while also keeping Submit.”  
“‘Would you like me to show the full revised version of your answer\_checker\_ui.py (with the Enter key fix included and ready to paste in)?’ **‘**yeah’”  
“So if I update the file on GitHub, will it automatically update the web app on Streamlit?”   
“Would I also use it in the equation part of the code?”  
“‘Enter here — because they’ll normally move to the next box (Answer).’ ‘But it doesn't do that for me.”  
“It didn’t work.”  
“For the memory bank, I want to add a problem and use Enter to also add the problem. the same as add. I want both.”  
“Okay, it worked, but I see this: Enter a problem (e.g., 5+5, (2+3)4, 10-32, 2\*\*3). I don't want that. I want basic problems like; 5+6, 9-8, 9/2, 4\*2”  
“This is good, but when I start the practice round, I do my answer to the problem, then press enter on my keyboard, the 1st question takes me back to the answer checker, and when I click back to the memory bank, it moves on to the next problem. When I answer the problem, I press enter on my keyboard, and it won't submit the answer. I want to be able to press enter and click submit to move on to the next problem.”  
“Okay, I like it. I played all three, and this is what I noticed. Both the electro flash and the memory bank are perfect. Answer checker works great too, but when I check an answer and it's correct/wrong, it keeps the previous problem there and doesn't show it blank for the next problem to check. If possible, I want it to move on if the last problem was solved correctly, and if it was solved wrong, keep the previous problem so the user can try again.”  
“It didn't do anything.”, “It didn't work.”, “Okay, so that didn't work again. It just brings me back to the top of the page after it's correct.”  
“I get this error: ImportError: cannot import name 'render\_electro\_flash' from 'electro\_flash\_ui' (/mount/src/streamlitapp/DataMonV6/electro\_flash\_ui.py)”, “So it didn't work again. It just takes me to the section's options.”  
	“Did the same thing again, not working still.”, “It's still doing the same thing, but now going to the left cuz that's where the section options are.”  
“Okay, never mind, it's not working, I'm just going to leave it the way it is.”  
“Okay, can you at least fix it so that when I enter an answer for electro flash, it doesn't automatically highlight the answer checker section button?”

### What Worked:

	Basically, the entire code worked first try; we, ChatGPT and I, had to tweak some things that I wanted added in. Definitely, asking questions about questions helped ChatGPT to provide a working code that I really like, which helped a lot. I really liked the recommendation ChatGPT gave me for which framework was best to work with, and it helped me find a way to create the web app on a website and not directly on my personal computer. 

### What Didn’t Work:

	Weirdly enough, most of the code worked first try; it was after adding some more features that the code somewhat broke. For instance, when I was playing the answer checker, I would press Enter after typing an answer, and the app told me to “press Enter to apply,” but it didn’t actually move to the next question. I had to click the Submit button instead. I wanted the Enter key to work the same as clicking Submit so that either option would advance the app properly. I told ChatGPT that it was not working for me, and I was shown how to fix it. It still didn’t work, so I had to ask again.   
It ended up working after a fix, but I wanted to make it so that when you added a new problem to the memory bank, pressing Enter should also add the problem. Essentially, making the Enter key perform the same action as clicking the Add button. It worked, but it was showing examples that I didn’t like, and I wanted that to change as well. After it was fixed, I had a problem when I pressed Enter after answering the first question; it sent me back to the Answer Checker and skipped to the next problem. I wanted Enter and Submit to both move to the next problem correctly.  
An issue in Answer Checker was that the previous problem stays visible, and I wanted it to move on to a new problem if the answer is correct, and keep the same problem if it was wrong. ChatGPT was updating the answer\_checker\_ui.py so it would clear the interface and refocus on the Equation box after a correct answer. At first, it didn’t update properly, but after a quick fix, it finally worked. ChatGPT revised both the memory bank and the electro flash, to have in their code that as well. Although the update to electro flash didn’t work. I had to ask multiple times to see if I could get the code working. Unfortunately, I couldn’t fix that part of the code and decided to leave my code as it is because it is still really good, besides that part of the code. The code still works perfectly despite everything, and I am really grateful for that. 

### Where I Had To Fix AI Output Manually: 

1. Enter-to-submit everywhere: I asked for Enter to behave like Submit in all three parts. I had to make sure each st.text\_input used on\_change=\_submit\_\* and still kept the button as a second path. (Answer Checker, Memory Bank, Electro Flash).  
2. Stop sidebar from getting focus after Enter: The app kept jumping focus to the sidebar radio. I added a small HTML/JS snippet in app.py to blur focus inside the sidebar so Enter doesn’t “highlight” a different section.  
3. Answer Checker should clear correctly: Cleared; after a wrong answer, keep the equation, but clear just the answer. I adjusted the submit handler to do that.  
4. Memory Bank should only allow basic problems: I didn’t want advanced expressions. I added a simple regex validator (+ \- \* / only), clearer error text, and Enter-to-add in the “Add Problems” box.  
5. Electro Flash import/name issues: I hit an ImportError once. I checked that electro\_flash\_ui.py exposes render\_electro\_flash and that app.py imports it with the same name (it does now).  
6. Readme and requirements: I kept the README short and made sure the requirements include Streamlit. 

### Total Iteration Count:

	There were roughly around 14 iterations. 

### The Moment I Had Hit The “Vibe Coding Ceiling”:

The moment I hit the vibe coding ceiling was when I tried to control where the focus went after pressing Enter. Streamlit reacts to things on the server side, so it doesn’t really give you much control over what happens on the front end. Even simple stuff like stopping the sidebar buttons from taking focus needed some custom HTML and JavaScript fixes. Doing more, like making the next box automatically focus or using keyboard shortcuts, would probably be way easier in something like React or with a custom Streamlit setup. At that point, vibe coding in Streamlit just couldn’t do what I wanted anymore.