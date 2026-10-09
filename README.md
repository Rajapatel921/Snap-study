Snap & Study 📚

Snap & Study is an AI-powered study assistant built with Streamlit and powered by Google's Gemini 3.5 Flash model. It allows students to photograph or upload images of complex math problems, scientific diagrams, or handwritten notes, generating simple, plain-language explanations. Students can also save and export explanations directly via Telegram Bot or Email.

🌟 Key Features

Visual Problem Solving: Upload images (PNG, JPG, WEBP) of homework, diagrams, or handwritten notes.

AI-Powered Explanations: Formats complex topics into a 3-part layout:

📌 Core Concept Summary

🔍 Step-by-Step Breakdown

💡 Key Takeaway

Instant Telegram Export: Send explanations straight to a Telegram chat using a Telegram Bot (python-telegram-bot).

Email Sharing Support: Send notes via email using Mailgun API integration (with fallback to default client mailto links).

📁 Repository Structure

snap-and-study/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example  # Template for API keys
├── app.py                   # Main Streamlit application
├── requirements.txt         # Project dependencies
├── .gitignore               # Excludes secrets, venv, and cache files
└── README.md                # Project documentation


🛠️ Local Installation & Setup

Follow these steps to run the application locally:

1. Clone the Repository

git clone https://github.com/your-username/snap-and-study.git
cd snap-and-study


2. Set Up a Virtual Environment

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate


3. Install Dependencies

pip install -r requirements.txt


4. Configure Environment Secrets

Create a .streamlit/secrets.toml file inside your project directory (refer to .streamlit/secrets.toml.example).

Add your API credentials:

GEMINI_API_KEY = "your_gemini_api_key_here"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"

# Optional (for Mailgun email delivery)
MAILGUN_API_KEY = "your_mailgun_api_key"
MAILGUN_DOMAIN = "your_mailgun_domain.mailgun.org"
SENDER_EMAIL = "Snap & Study <noreply@yourdomain.com>"


5. Launch the Streamlit App

streamlit run app.py


🔑 How to Obtain API Keys

Google Gemini API Key:

Visit Google AI Studio.

Click Get API key and create a key for your project.

Telegram Bot Token:

Search for @BotFather on Telegram.

Send /newbot and follow the setup prompts.

Copy the HTTP API token provided by BotFather.

Note: To receive messages, users must search for @userinfobot on Telegram to retrieve their Chat ID and send at least one message to your new bot.

Mailgun API Key (Optional):

Sign up at Mailgun and retrieve your sandbox domain and API key under Sending > Domains.

🚀 Deployment (Streamlit Community Cloud)

Push your project code to a public GitHub repository.

Sign in to Streamlit Community Cloud.

Click New App, select your repository, branch, and set app.py as the main entry point.

Expand Advanced Settings > Secrets and paste your TOML configuration:

GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
