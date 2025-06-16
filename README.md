# 🤖 Template Project Management: Simple AI Chatbot
## Python + Prompt Engineering + OpenAI/Gemini API

---

## 📋 Project Overview
**Project Name:** Simple AI Chatbot  
**Duration Estimate:** 3-5 hari  
**Difficulty:** Beginner-Intermediate  
**Goal:** Membuat chatbot sederhana dengan AI yang bisa diajak ngobrol

---

## 🎯 Phase 1: PROJECT SETUP
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 1.1 Environment Setup (30 menit)
- [ ] **Install Python 3.8+** *(5 menit)*
  - Cek versi: `python --version`
  - Update jika perlu

- [ ] **Setup Virtual Environment** *(10 menit)*
  - Buat venv: `python -m venv chatbot-env`
  - Activate: `source chatbot-env/bin/activate` (Mac/Linux) atau `chatbot-env\Scripts\activate` (Windows)
  - Test venv aktif (cek prompt)

- [ ] **Install Required Libraries** *(10 menit)*
  - `pip install openai` (untuk OpenAI API)
  - `pip install google-generativeai` (untuk Gemini)
  - `pip install python-dotenv` (untuk environment variables)
  - `pip install requests` (backup untuk HTTP calls)

- [ ] **Setup Code Editor** *(5 menit)*
  - Buka VS Code/PyCharm
  - Install Python extension
  - Setup Python interpreter ke venv

### 1.2 Project Structure (15 menit)
- [ ] **Create Main Folder** *(2 menit)*
  - Buat folder `simple-ai-chatbot`
  - Navigate ke folder tersebut

- [ ] **Create Project Files** *(8 menit)*
  - Buat `main.py` (file utama)
  - Buat `config.py` (konfigurasi API)
  - Buat `prompts.py` (template prompts)
  - Buat `.env` (API keys - jangan di-commit)
  - Buat `.gitignore` (exclude .env dan __pycache__)

- [ ] **Create Requirements File** *(3 menit)*
  - `pip freeze > requirements.txt`
  - Cek isi file requirements.txt

- [ ] **Initialize Git** *(2 menit)*
  - `git init`
  - `git add .` (pastikan .env tidak included)
  - `git commit -m "Initial project setup"`

---

## � Project Structure
Simple AI Chatbot/
├── .env                    # Environment variables
├── requirements.txt        # Dependencies
├── README.md              # Project documentation
├── src/                   # Source code
│   ├── __init__.py
│   ├── main.py            # Main application
│   └── chatbot/           # Chatbot module
│       ├── __init__.py
│       ├── core.py        # Core chatbot functionality
│       └── config.py      # Configuration settings
└── tests/                 # Test files
    └── __init__.py

---

## �🔑 Phase 2: API SETUP & AUTHENTICATION
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 2.1 Get API Keys (20 menit)
- [ ] **OpenAI API Setup** *(10 menit)*
  - Daftar di platform.openai.com
  - Create new API key
  - Copy API key ke notepad sementara
  - Cek quota/limit account

- [ ] **Google Gemini API Setup** *(10 menit)*
  - Daftar di ai.google.dev
  - Create API key untuk Gemini
  - Copy API key ke notepad
  - Test API access (optional)

### 2.2 Environment Configuration (15 menit)
- [ ] **Setup .env File** *(5 menit)*
  ```
  OPENAI_API_KEY=your_openai_key_here
  GEMINI_API_KEY=your_gemini_key_here
  ```
  - Paste API keys dari notepad
  - Double check no spaces

- [ ] **Test Environment Loading** *(5 menit)*
  ```python
  from dotenv import load_dotenv
  import os
  load_dotenv()
  print("OpenAI Key loaded:", bool(os.getenv("OPENAI_API_KEY")))
  ```
  - Buat test script sederhana
  - Run untuk memastikan keys terbaca

- [ ] **Setup config.py** *(5 menit)*
  ```python
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  ```

### 2.3 Basic API Connection Test (20 menit)
- [ ] **Test OpenAI Connection** *(10 menit)*
  ```python
  import openai
  from config import OPENAI_API_KEY
  
  openai.api_key = OPENAI_API_KEY
  # Simple test call
  response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": "Hello"}]
  )
  print(response.choices[0].message.content)
  ```

- [ ] **Test Gemini Connection** *(10 menit)*
  ```python
  import google.generativeai as genai
  from config import GEMINI_API_KEY
  
  genai.configure(api_key=GEMINI_API_KEY)
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content("Hello")
  print(response.text)
  ```

---

## 📝 Phase 3: PROMPT ENGINEERING BASICS
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 3.1 Create Prompt Templates (45 menit)
- [ ] **Setup prompts.py Structure** *(5 menit)*
  ```python
  # Basic prompt templates for different conversation types
  
  class PromptTemplates:
      pass
  ```

- [ ] **General Chat Prompt** *(10 menit)*
  ```python
  GENERAL_CHAT = """
  You are a helpful and friendly AI assistant. 
  Respond in a conversational, warm tone.
  Keep responses concise but informative.
  If you don't know something, just say so.
  
  User: {user_message}
  Assistant:"""
  ```
  - Test prompt dengan beberapa input
  - Adjust tone sesuai keinginan

- [ ] **Professional Assistant Prompt** *(10 menit)*
  ```python
  PROFESSIONAL = """
  You are a professional AI assistant.
  Provide clear, accurate, and well-structured responses.
  Use formal language and be direct.
  
  User: {user_message}
  Assistant:"""
  ```

- [ ] **Creative Helper Prompt** *(10 menit)*
  ```python
  CREATIVE = """
  You are a creative AI assistant.
  Be imaginative, inspiring, and think outside the box.
  Help with brainstorming and creative problem-solving.
  
  User: {user_message}
  Assistant:"""
  ```

- [ ] **Learning Tutor Prompt** *(10 menit)*
  ```python
  TUTOR = """
  You are a patient AI tutor.
  Explain concepts clearly with examples.
  Ask follow-up questions to check understanding.
  Break down complex topics into simple parts.
  
  User: {user_message}
  Assistant:"""
  ```

### 3.2 Dynamic Prompt Building (30 menit)
- [ ] **Create Prompt Builder Function** *(15 menit)*
  ```python
  def build_prompt(template_name, user_message, context=""):
      templates = {
          "general": GENERAL_CHAT,
          "professional": PROFESSIONAL,
          "creative": CREATIVE,
          "tutor": TUTOR
      }
      
      prompt = templates.get(template_name, GENERAL_CHAT)
      return prompt.format(user_message=user_message)
  ```

- [ ] **Test Prompt Builder** *(10 menit)*
  - Test dengan berbagai template
  - Print hasil untuk validation
  - Adjust format jika perlu

- [ ] **Add Context Support** *(5 menit)*
  - Modify function untuk support conversation history
  - Test dengan sample context

### 3.3 Conversation Memory (25 menit)
- [ ] **Design Conversation Storage** *(10 menit)*
  ```python
  class ConversationMemory:
      def __init__(self):
          self.history = []
      
      def add_message(self, role, content):
          self.history.append({"role": role, "content": content})
      
      def get_history(self, limit=5):
          return self.history[-limit:]
  ```

- [ ] **Test Memory System** *(10 menit)*
  - Create sample conversation
  - Test add dan get functions
  - Verify history format

- [ ] **Integrate with Prompts** *(5 menit)*
  - Modify prompt builder untuk include history
  - Test conversation continuity

---

## 🤖 Phase 4: CHATBOT CORE FUNCTIONALITY  
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 4.1 API Wrapper Functions (40 menit)
- [ ] **OpenAI Wrapper Function** *(20 menit)*
  ```python
  def get_openai_response(messages, model="gpt-3.5-turbo"):
      try:
          response = openai.chat.completions.create(
              model=model,
              messages=messages,
              max_tokens=150,
              temperature=0.7
          )
          return response.choices[0].message.content
      except Exception as e:
          return f"Error: {str(e)}"
  ```
  - Test dengan sample messages
  - Handle berbagai error cases

- [ ] **Gemini Wrapper Function** *(20 menit)*
  ```python
  def get_gemini_response(prompt):
      try:
          model = genai.GenerativeModel('gemini-pro')
          response = model.generate_content(prompt)
          return response.text
      except Exception as e:
          return f"Error: {str(e)}"
  ```
  - Test dengan sample prompts
  - Handle API errors

### 4.2 Response Formatting (30 menit)
- [ ] **Create Response Formatter** *(15 menit)*
  ```python
  def format_response(response, max_length=200):
      # Clean up response
      response = response.strip()
      
      # Truncate if too long
      if len(response) > max_length:
          response = response[:max_length] + "..."
      
      return response
  ```

- [ ] **Add Response Styling** *(10 menit)*
  ```python
  def style_response(response, style="casual"):
      if style == "casual":
          return f"😊 {response}"
      elif style == "professional":
          return f"📋 {response}"
      elif style == "creative":
          return f"💡 {response}"
      return response
  ```

- [ ] **Test Formatting Functions** *(5 menit)*
  - Test dengan berbagai panjang response
  - Test berbagai style options

### 4.3 Main Chatbot Logic (45 menit)
- [ ] **Create Chatbot Class** *(25 menit)*
  ```python
  class SimpleChatbot:
      def __init__(self, ai_provider="openai"):
          self.provider = ai_provider
          self.memory = ConversationMemory()
          self.current_template = "general"
      
      def chat(self, user_message):
          # Add user message to memory
          self.memory.add_message("user", user_message)
          
          # Build prompt
          prompt = build_prompt(self.current_template, user_message)
          
          # Get AI response
          if self.provider == "openai":
              response = get_openai_response([{"role": "user", "content": prompt}])
          else:
              response = get_gemini_response(prompt)
          
          # Format response
          formatted_response = format_response(response)
          
          # Add to memory
          self.memory.add_message("assistant", formatted_response)
          
          return formatted_response
  ```

- [ ] **Add Template Switching** *(10 menit)*
  ```python
  def switch_mode(self, template_name):
      valid_templates = ["general", "professional", "creative", "tutor"]
      if template_name in valid_templates:
          self.current_template = template_name
          return f"Switched to {template_name} mode!"
      return "Invalid mode. Available: " + ", ".join(valid_templates)
  ```

- [ ] **Test Chatbot Class** *(10 menit)*
  - Create chatbot instance
  - Test basic chat functionality
  - Test mode switching

---

## 🖥️ Phase 5: USER INTERFACE
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 5.1 Console Interface (35 menit)
- [ ] **Create Welcome Screen** *(10 menit)*
  ```python
  def show_welcome():
      print("="*50)
      print("🤖 SIMPLE AI CHATBOT")
      print("="*50)
      print("Commands:")
      print("  /help    - Show commands")
      print("  /mode    - Switch AI mode")
      print("  /clear   - Clear conversation")
      print("  /quit    - Exit chatbot")
      print("="*50)
  ```

- [ ] **Create Help System** *(10 menit)*
  ```python
  def show_help():
      print("\n📖 HELP:")
      print("  /mode general     - Casual conversation")
      print("  /mode professional - Professional assistant")
      print("  /mode creative    - Creative helper")
      print("  /mode tutor       - Learning tutor")
      print("  /clear            - Start fresh conversation")
      print("  /quit             - Exit the chatbot")
  ```

- [ ] **Create Main Interface Loop** *(15 menit)*
  ```python
  def main_interface():
      chatbot = SimpleChatbot()
      show_welcome()
      
      while True:
          user_input = input("\n💬 You: ").strip()
          
          if user_input.lower() in ['/quit', 'exit', 'bye']:
              print("👋 Goodbye!")
              break
          elif user_input.lower() == '/help':
              show_help()
          elif user_input.startswith('/mode'):
              mode = user_input.split()[1] if len(user_input.split()) > 1 else ""
              print(chatbot.switch_mode(mode))
          elif user_input.lower() == '/clear':
              chatbot.memory.history = []
              print("🧹 Conversation cleared!")
          else:
              response = chatbot.chat(user_input)
              print(f"🤖 Bot: {response}")
  ```

### 5.2 Input Validation (20 menit)
- [ ] **Add Input Sanitization** *(10 menit)*
  ```python
  def sanitize_input(user_input):
      # Remove excessive whitespace
      user_input = user_input.strip()
      
      # Limit length
      if len(user_input) > 500:
          return user_input[:500] + "..."
      
      # Check for empty input
      if not user_input:
          return None
      
      return user_input
  ```

- [ ] **Add Command Validation** *(10 menit)*
  ```python
  def is_valid_command(command):
      valid_commands = ['/help', '/mode', '/clear', '/quit', '/exit']
      return command.lower() in valid_commands or command.startswith('/mode')
  ```

### 5.3 Error Handling (25 menit)
- [ ] **Add Connection Error Handling** *(10 menit)*
  ```python
  def handle_api_error(error):
      if "quota" in str(error).lower():
          return "❌ API quota exceeded. Please try again later."
      elif "network" in str(error).lower():
          return "❌ Network error. Check your connection."
      else:
          return "❌ Something went wrong. Please try again."
  ```

- [ ] **Add Graceful Degradation** *(10 menit)*
  - Fallback response jika API error
  - Retry mechanism (optional)
  - User-friendly error messages

- [ ] **Test Error Scenarios** *(5 menit)*
  - Test dengan API key invalid
  - Test dengan network error
  - Test dengan empty response

---

## 🧪 Phase 6: TESTING & DEBUGGING
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 6.1 Unit Testing (30 menit)
- [ ] **Test Prompt Templates** *(10 menit)*
  - Test semua template formatting
  - Verify variable substitution
  - Check prompt length limits

- [ ] **Test API Wrappers** *(10 menit)*
  - Test OpenAI function dengan mock data
  - Test Gemini function dengan sample prompts
  - Verify error handling

- [ ] **Test Memory System** *(10 menit)*
  - Test conversation history storage
  - Test history retrieval
  - Test memory limits

### 6.2 Integration Testing (25 menit)
- [ ] **Test Complete Chat Flow** *(15 menit)*
  - Start chatbot → send message → get response
  - Test mode switching mid-conversation
  - Test command execution

- [ ] **Test Different Scenarios** *(10 menit)*
  - Long conversations
  - Quick mode switches
  - Mixed commands and chat

### 6.3 User Acceptance Testing (20 menit)
- [ ] **Test User Experience** *(10 menit)*
  - Ask friend/colleague to test
  - Note confusing parts
  - Gather feedback on responses

- [ ] **Test Edge Cases** *(10 menit)*
  - Very long messages
  - Special characters
  - Rapid-fire messages

---

## 🚀 Phase 7: ENHANCEMENTS & POLISH
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 7.1 Advanced Features (45 menit)
- [ ] **Add Conversation Export** *(15 menit)*
  ```python
  def export_conversation(self, filename="chat_history.txt"):
      with open(filename, 'w') as f:
          for msg in self.memory.history:
              f.write(f"{msg['role']}: {msg['content']}\n")
  ```

- [ ] **Add Response Time Display** *(10 menit)*
  ```python
  import time
  start_time = time.time()
  # ... get AI response ...
  response_time = time.time() - start_time
  print(f"⏱️ Response time: {response_time:.2f}s")
  ```

- [ ] **Add Token Usage Tracking** *(20 menit)*
  - Track API usage
  - Display cost estimation
  - Usage limits warning

### 7.2 Code Quality (30 menit)
- [ ] **Add Documentation** *(15 menit)*
  - Docstrings untuk semua functions
  - Code comments untuk complex logic
  - Usage examples

- [ ] **Code Cleanup** *(15 menit)*
  - Remove debug prints
  - Consistent variable naming
  - Remove unused imports

### 7.3 Configuration Options (25 menit)
- [ ] **Add Settings File** *(15 menit)*
  ```python
  # settings.py
  DEFAULT_MODEL = "gpt-3.5-turbo"
  MAX_RESPONSE_LENGTH = 200
  CONVERSATION_HISTORY_LIMIT = 10
  DEFAULT_TEMPERATURE = 0.7
  ```

- [ ] **Make Settings Configurable** *(10 menit)*
  - User can modify via commands
  - Save/load user preferences

---

## 📝 Phase 8: DOCUMENTATION & DEPLOYMENT
**Status:** ⏳ To Do | 🔄 In Progress | ✅ Done

### 8.1 Create Documentation (40 menit)
- [ ] **Write README.md** *(20 menit)*
  - Project description
  - Installation instructions
  - Usage examples
  - API setup guide
  - Screenshots/examples

- [ ] **Create User Manual** *(20 menit)*
  - Command reference
  - Mode explanations
  - Troubleshooting guide
  - FAQ section

### 8.2 Packaging (30 menit)
- [ ] **Finalize requirements.txt** *(5 menit)*
  - `pip freeze > requirements.txt`
  - Remove unnecessary packages

- [ ] **Create setup script** *(15 menit)*
  ```bash
  #!/bin/bash
  # setup.sh
  python -m venv chatbot-env
  source chatbot-env/bin/activate
  pip install -r requirements.txt
  echo "Setup complete! Run python main.py"
  ```

- [ ] **Test Installation Process** *(10 menit)*
  - Test pada fresh environment
  - Verify semua dependencies terinstall

### 8.3 Version Control & Sharing (20 menit)
- [ ] **Final Git Commit** *(5 menit)*
  - Add all changes
  - Commit dengan descriptive message
  - Create tag v1.0

- [ ] **Upload to GitHub** *(10 menit)*
  - Create repository
  - Push all code
  - Write good repository description

- [ ] **Share Project** *(5 menit)*
  - Add to portfolio
  - Share with friends/community
  - Get feedback for improvements

---

## 📊 PROJECT SUMMARY

**Total Estimated Time:** 15-20 jam  
**Timeline:** 3-5 hari (3-4 jam per hari)  
**Skill Level:** Beginner-Intermediate  
**Technologies:** Python, OpenAI API, Google Gemini API, Prompt Engineering

### Key Learning Outcomes:
- ✅ API integration (OpenAI/Gemini)
- ✅ Prompt engineering basics
- ✅ Conversation memory management  
- ✅ Error handling & user experience
- ✅ Template-based AI responses
- ✅ Command-line interface design

### Potential Extensions:
1. **Web Interface** - Add Flask/Streamlit GUI
2. **Voice Integration** - Add speech-to-text/text-to-speech
3. **Multi-language** - Support bahasa Indonesia
4. **Personality Customization** - User-defined bot personalities
5. **File Processing** - Chat about uploaded documents

### Next Project Suggestions:
1. **Text Summarizer** - File upload → AI summary
2. **Writing Assistant** - Grammar/style improvement
3. **Question Generator** - Educational content creator

---

**Happy Coding! 🚀🤖**