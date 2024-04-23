import cv2, pyautogui, mss, keyboard, threading
import numpy as np
from time import time, sleep
from IPython.display import clear_output
# https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html

match_found_dir = 'img/partida-encontrada.png'
accept_img_dir  = 'img/aceitar_recusar.png'
threshold      = .93                           # the threshold of 93% close to the model image
sct = mss.mss()

# Flag to control the loop
running = True

#TODO Check a way to read the window size (only working on 1920x1080)

def capture_and_display():
    with mss.mss() as sct:
        monitor = sct.monitors[1]               # Get information about the primary monitor
        scr = np.array(sct.grab(monitor))       # Capture a screenshot
        # cv2.imshow('Screen', scr)               # Display the screenshot
        cv2.waitKey(1)                          # Wait until a key is pressed
        sleep(3)                          
        # cv2.destroyAllWindows()                 # Close the window after a key is pressed
    return scr

def wait_n_destroy():       # This function is only invoked to close all opencv windows
    cv2.waitKey()
    cv2.destroyAllWindows()
    return

def convert_to_BW(image_name: str):     # Convert to Black and White image, so opencv can compare images
    bw_img = cv2.cvtColor(image_name, cv2.COLOR_BGR2GRAY)
    return bw_img

def print_image(window_name: str, image_name: str):  # Function only to print the image 
    cv2.imshow(window_name, image_name)
    return

def compare_images(image, template, mask):      # Compare the actual screen with the model (needs to be black and white)
    result = cv2.matchTemplate(image, template, mask)
    return result
    
def check_keyboard():           # Function to check for keyboard input asynchronously
    global running
    while True:
        if keyboard.is_pressed('q'):
            running = False
            break

# Create and start the keyboard checking thread
keyboard_thread = threading.Thread(target=check_keyboard)
keyboard_thread.start()

match_found_img         = cv2.imread(match_found_dir,   cv2.IMREAD_UNCHANGED)
accept_img              = cv2.imread(accept_img_dir,    cv2.IMREAD_UNCHANGED)
match_found_img_grey    = convert_to_BW(match_found_img)
accept_img_grey         = convert_to_BW(accept_img)

def convert_images(match_found_dir: str, accept_img_dir: str) -> str:
    match_found_img = cv2.imread(match_found_dir,   cv2.IMREAD_UNCHANGED)
    accept_img      = cv2.imread(accept_img_dir,    cv2.IMREAD_UNCHANGED)
    match_found_img_grey = convert_to_BW(match_found_img)
    accept_img_grey      = convert_to_BW(accept_img)
    return match_found_img_grey, accept_img_grey

def create_rectangle(match_found_img_grey,accept_img_grey,match_found_img,accept_img_dir):      # Create  and print the rectangle on the image. This function is only for visual purposes, and not in end product
    result = compare_images(match_found_img_grey, accept_img_grey, cv2.TM_CCOEFF_NORMED)
    # print_image('Result', result)
    # wait_n_destroy()

    yloc, xloc  = np.where(result >= threshold)
    xfound = len(xloc)
    print(f'\n {xfound} results found' )

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f' Min: {min_val}, Max {max_val}, Min Loc: {min_loc}, Max Loc: {max_loc}')
    w = accept_img.shape[1]
    h = accept_img.shape[0]

    # To highlight only 1 button
    cv2.rectangle(match_found_img, (max_loc), (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)
    # print_image('Match Found', match_found_img)
    # wait_n_destroy()
    return max_loc[0], max_loc[1]

def check_button(scr, accept_img_dir):          # Function to create the area in which the model may be found. If so we check how many were found, get the closest match and clink on center of the area 
    accept_img          = cv2.imread(accept_img_dir,    cv2.IMREAD_UNCHANGED)
    accept_img_grey     = convert_to_BW(accept_img)
    scr_grey            = convert_to_BW(scr)
    result = compare_images(scr_grey, accept_img_grey, cv2.TM_CCOEFF_NORMED)
    # print_image('Result', result)
    # wait_n_destroy()

    yloc, xloc  = np.where(result >= threshold)
    xfound = len(xloc)
    print(f'\n {xfound} results found' )

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f' Min: {min_val}, Max {max_val}, Min Loc: {min_loc}, Max Loc: {max_loc}')
    w = accept_img.shape[1]
    h = accept_img.shape[0]
    print(f"w: {w} h: {h}")

    # To highlight only 1 button
    cv2.rectangle(scr, (max_loc), (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)
    # print_image('Match Found', scr)
    # wait_n_destroy()
    w_half = w / 2
    h_half = h / 2
    print(f"w_half: {w_half} h_half: {h_half}")
    if xfound >= 1:
        return click(w_half, h_half ,max_loc[0], max_loc[1])
    return True # to maintain the 'not clicked' flag

def click(w, h , max_loc_x, max_loc_y):         # Function to execute the click
    # Calculate the middle point of the rectangle
    x_middle = max_loc_x + (w)
    y_middle = max_loc_y + (h)

    # Perform the click action at the middle point
    pyautogui.click(x_middle, y_middle)
    print(f"Button clicked at: {x_middle, y_middle}")
    keyboard.press_and_release('q')
    print("Keyboard 'q' pressed!")
    wait_click = False
    print(f"Wait click condition inside click function: {wait_click}")
    return wait_click

# Main function
def main():
    wait_click = True
    fps_time = time()
    x = 100  # X-coordinate of the pixel location
    y = 100  # Y-coordinate of the pixel location
    screen_width, screen_height = pyautogui.size()
    match_found_img_grey, accept_img_grey = convert_images(match_found_dir, accept_img_dir)
    max_loc_x, max_loc_y = create_rectangle(match_found_img_grey,accept_img_grey,match_found_img, accept_img_dir)
    while running:
        clear_output(wait=True)
        screen = capture_and_display()
        
        wait_click = check_button(screen, accept_img_dir)
        if wait_click == False:
            keyboard_thread.join()
            break
        print(f"Wait click condition inside the main while loop: {wait_click}")

        print('FPS: {}'.format(1 / (time() - fps_time)))
        fps_time = time()


    # Join the keyboard checking thread to ensure it terminates
    keyboard_thread.join()
    return


if __name__ == "__main__":
    main()
