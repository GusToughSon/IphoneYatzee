# **🎲 Yahtzee AI Automation Bot 🤖**  
### **@GusToughSon**  

## **🚀 The Ultimate AI-Powered Yahtzee Bot!**

Tired of rolling dice manually? Want an **AI-driven bot** that **plays Yahtzee for you, optimizes your scores, and never misclicks?** You're in the right place! This bot will:

✅ **Detect the game screen** automatically 🎮  
✅ **Click the "ROLL" button** when needed 🎲  
✅ **Read dice values using AI-powered OCR** 🔍  
✅ **Analyze the scoreboard and pick the best category** 📊  
✅ **Click the highest-scoring category for you** 🏆  
✅ **Repeat until the game is over!** 🔁  

---

## **📌 Features & How It Works**
### **🖥️ 1. Detects Yahtzee’s Game Screen**
- Uses **macOS AppleScript** to identify the **iPhone Mirroring window**.  
- Dynamically **captures a screenshot** of the game.  

### **🎲 2. Reads the Dice Values Like a Pro**
- Uses **Tesseract OCR (Optical Character Recognition)** to extract dice values.  
- Handles **missing dice or empty slots** intelligently.  
- Ensures **accurate number detection** for better decision-making.  

### **📊 3. Reads the Scoreboard**
- Detects **which categories are available**.  
- Ignores **already filled score slots**.  
- Ensures **no wasted scoring opportunities**.  

### **🧠 4. AI Chooses the Best Move**
- Dynamically analyzes all scoring categories.  
- Chooses **the highest-scoring available option**.  
- Prioritizes **rare opportunities** (Yahtzee, Full House, Straights).  
- **Handles all game logic automatically!**  

### **🖱️ 5. Clicks the Right Button Every Time**
- Uses **PyAutoGUI** to move the cursor.  
- **Clicks the best scoring category** (never misses a turn).  
- **Clicks "Roll" if dice rolling is available**.  
- No misclicks. No hesitation. Just **AI-driven perfection**.  

---

# **⚡ Installation & Setup (MacBook Air)**
### **🔹 Step 1: Clone the Repo**
```sh
git clone https://github.com/GusToughSon/YahtzeeAI.git
cd YahtzeeAI
```

### **🔹 Step 2: Install Dependencies**
```sh
pip install opencv-python numpy pytesseract pyautogui
```

### **🔹 Step 3: Install Tesseract OCR (Required for Dice Recognition)**
```sh
brew install tesseract
```

### **🔹 Step 4: Ensure Tesseract Works**
```sh
tesseract --version
```
If it prints a version number (e.g., `5.5.0`), you're good to go!  

---

# **🚀 Running the AI Bot**
### **🔹 Step 1: Open iPhone Mirroring**
Make sure your **Yahtzee game is running on iPhone Mirroring**.

### **🔹 Step 2: Run the AI Bot**
```sh
python3 main.py
```
💥 **Watch in amazement as the AI plays Yahtzee for you!** 💥  

---

# **💡 How It Works (Technical Overview)**
The AI is broken into **modular components** for maximum efficiency:  

### **📸 `window_capture.py` (Captures Game Screen)**
- Uses **AppleScript** to find the iPhone Mirroring window.  
- Extracts **X, Y, Width, and Height** for screenshot accuracy.  
- Saves the **game screen as an image** for processing.  

### **🎲 `dice_recognition.py` (Reads Dice Values)**
- Uses **OpenCV & Tesseract OCR** to **extract dice numbers**.  
- Handles **empty slots**, ensuring **reliable data** for decision-making.  

### **📊 `score_analysis.py` (Reads Scoreboard)**
- Extracts **which categories are still available**.  
- Filters out **bad OCR detections** using predefined categories.  

### **🧠 `ai_decision.py` (AI Chooses Best Move)**
- Evaluates all possible scores based on the **current dice roll**.  
- Prioritizes **highest value moves**.  
- **Remembers which categories are already filled.**  

### **🖱️ `main.py` (Controls the Game)**
- **Clicks "Roll" when needed**.  
- **Reads dice & scoreboard**.  
- **AI picks the best scoring category**.  
- **Clicks the chosen category** to **maximize points**.  
- **Repeats until the game ends!**  

---

# **🛠️ Future Features (Coming Soon)**
✅ **Train AI to predict future rolls & adjust strategy**  
✅ **Auto-detect game over & restart**  
✅ **Advanced strategy improvements (blocking opponents, etc.)**  
✅ **Multiplayer AI (play against others automatically)**  

---

# **🚀 Contributing**
Want to improve this AI?  
- **Fork the repo**  
- **Submit a pull request**  
- **Enhance the AI strategy!**  

---

# **📢 Shoutout to AI-Powered Gaming!**
This bot is **just the beginning** of AI-driven game automation. If you're **excited about AI gaming**, **follow this repo** for future updates!  

🛠️ Built by **@GusToughSon**  
🚀 **Join the AI gaming revolution!**  

💥 **Now go forth, automate, and let the AI dominate Yahtzee for you!** 🎲🤖🏆  

---  

