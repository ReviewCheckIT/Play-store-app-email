import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ================= কনফিগারেশন =================
TELEGRAM_TOKEN = "আপনার_বট_টোকেন_এখানে_দিন"
TELEGRAM_CHAT_ID = "আপনার_চ্যাট_আইডি_এখানে_দিন"
SEARCH_KEYWORD = "health tracker"  # কিওয়ার্ড পরিবর্তন করুন
# =============================================

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # ক্লাউড সার্ভারের জন্য জরুরি
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_playstore():
    driver = setup_driver()
    send_telegram_msg(f"🚀 স্ক্র্যাপিং শুরু হয়েছে: {SEARCH_KEYWORD}")
    
    try:
        search_url = f"https://play.google.com/store/search?q={SEARCH_KEYWORD}&c=apps"
        driver.get(search_url)
        time.sleep(5)

        # অ্যাপের লিংকগুলো সংগ্রহ
        links = set()
        elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/store/apps/details?id=')]")
        for elem in elements:
            links.add(elem.get_attribute('href'))
        
        links = list(links)[:30] # প্রথম ৩০টি অ্যাপ চেক করবে

        for link in links:
            driver.get(link)
            time.sleep(3)
            
            # রিভিউ চেক করার লজিক
            try:
                # যদি রিভিউ কাউন্ট খুঁজে না পাওয়া যায় (অর্থাৎ নতুন অ্যাপ)
                review_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'reviews')]")
                if not review_elements:
                    # ইমেইল বের করার চেষ্টা
                    contact_btn = driver.find_element(By.XPATH, "//div[contains(text(), 'Developer contact')]")
                    driver.execute_script("arguments[0].click();", contact_btn)
                    time.sleep(1)
                    
                    email_elem = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
                    email = email_elem.get_attribute('href').replace('mailto:', '')
                    
                    # টেলিগ্রামে পাঠানো
                    msg = f"✅ নতুন অ্যাপ পাওয়া গেছে!\nনাম: {driver.title}\nইমেইল: {email}\nলিংক: {link}"
                    send_telegram_msg(msg)
                    print(f"Found: {email}")
            except:
                continue

    finally:
        driver.quit()
        send_telegram_msg("🏁 স্ক্র্যাপিং শেষ হয়েছে।")

if __name__ == "__main__":
    scrape_playstore()
