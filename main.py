import os
import google.generativeai as genai
from PIL import ImageGrab
from win10toast import ToastNotifier

# --- Configuration ---
# Replace "YOUR_GEMINI_API_KEY" with your actual Gemini API key.
GEMINI_API_KEY = "AIzaSyASdFVw43MezTSSp5ARi1W-lWTjSgnNAdI"

# The question you want to ask about the screenshot.
PROMPT = "What is the correct answer in this image?"
# --- End of Configuration ---

def take_screenshot(filename="screenshot.png"):
    """Takes a screenshot of the entire screen and saves it to a file."""
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
        return filename
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None

def analyze_image_with_gemini(image_path, prompt):
    """Sends an image and a prompt to the Gemini API and returns the response."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        return "Please set your Gemini API key in the script."

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro-vision')
        
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        image_parts = [
            {
                "mime_type": "image/png",
                "data": image_data
            },
        ]

        prompt_parts = [
            prompt,
            image_parts[0],
        ]

        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"An error occurred with the Gemini API: {e}"

def show_windows_notification(title, message):
    """Displays a Windows notification with a given title and message."""
    try:
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=10)
    except Exception as e:
        print(f"Error showing notification: {e}")

if __name__ == "__main__":
    # 1. Take a screenshot
    screenshot_file = take_screenshot()

    if screenshot_file:
        # 2. Analyze the screenshot with Gemini
        print("Analyzing the screenshot with Gemini...")
        answer = analyze_image_with_gemini(screenshot_file, PROMPT)
        print(f"Gemini's answer: {answer}")

        # 3. Show the answer as a Windows notification
        show_windows_notification("Gemini's Answer", answer)

        # 4. Clean up the screenshot file
        os.remove(screenshot_file)
        print(f"Deleted {screenshot_file}")