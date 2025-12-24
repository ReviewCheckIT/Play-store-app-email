# পাইথন বেস ইমেজ
FROM python:3.9-slim

# প্রয়োজনীয় সিস্টেম প্যাকেজ এবং ক্রোম ইনস্টল করা
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable

# কাজের ডিরেক্টরি সেট করা
WORKDIR /app

# লাইব্রেরি ইনস্টল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# সব ফাইল কপি করা
COPY . .

# কোড রান করা
CMD ["python", "main.py"]
