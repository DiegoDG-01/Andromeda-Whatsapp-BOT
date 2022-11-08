FROM python:3.10-buster

WORKDIR /app

# ENvironment variables for language and Username
# Only available for:
# - English
# - Spanish
ENV Language English
ENV Username "Change to your chat name"

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt update
RUN apt install -y google-chrome-stable

# Install dependencies
RUN apt install wget libzbar0 -y

# Install Andromeda - WhatsApp Bot
COPY SRC/ .
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy files to configure the bot
COPY SRC/Data/Config/Lang/$Language/* Data/Config/
RUN  sed -i "s/Chat_Name/$Username/" Data/Config/Config.json


# Run Andromeda - WhatsApp Bot
CMD ["python3", "entrypoint.py"]