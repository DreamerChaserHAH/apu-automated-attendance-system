import subprocess
import time
import cv2
import pyautogui
import pytesseract

# Specify the path to the application you want to launch
app_path = "/Applications/APSpace.app"

# Launch the application as a subprocess
process = None
screen_width, screen_height = pyautogui.size()

def click_area(target_text):
    screenshot_path = "/Users/victormak/Projects/Personal/Experiments/apu-automated-attendance-system/src/" + target_text + ".png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    image = cv2.imread(screenshot_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray_image, lang='eng', config='--psm 6', output_type=pytesseract.Output.DICT)
    # Loop through the detected text and find the bounding box for the target text
    n_boxes = len(data['text'])
    print(n_boxes)
    for i in range(n_boxes):
        #print(data['text'][i])
        if target_text.lower() in data['text'][i].lower():
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            # Draw a rectangle around the detected text
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("Found the target text at index", i)
            # Click at the center of the bounding box
            center_x = x + w // 2
            center_y = y + h // 2
            print(center_x, center_y)
            image_height, image_width, channels = image.shape
            actual_x = center_x * screen_width // image_width
            actual_y = center_y * screen_height // image_height
            pyautogui.moveTo(actual_x + 20, actual_y)
            time.sleep(0.25)
            pyautogui.click(clicks=1)
            time.sleep(0.25)

    #cv2.imshow("Screenshot", image)
    #cv2.waitKey(0)
    #v2.destroyAllWindows()

def attendance(attendance_code):
    # Save the screenshot as an image file
    global process
    process = subprocess.Popen(["open", "-a", app_path])
    process.wait()

    time.sleep(1.25)
    pyautogui.moveTo(screen_width/2, screen_height/2)
    pyautogui.click(clicks=1)
    time.sleep(0.5)
    
    click_area("Attendance")
    time.sleep(0.5)
    click_area("Sign")
    time.sleep(0.3)
    pyautogui.typewrite(attendance_code)
    print("attendance code:", attendance_code)
    time.sleep(0.3)
    pyautogui.press("enter")
    process = None

if __name__ == "__main__":
    attendance("123")
