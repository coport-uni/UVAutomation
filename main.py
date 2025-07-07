import pyautogui as pag
from waiting import wait
import time
from PIL import Image
from sshmanager import SSHManager

class UVAutomation():

    def get_mouse_position(self):
        '''
        This function captures live mouse position.

        Input : None
        Output : dict
        '''
        mouse_current_position = pag.position()
        time.sleep(1)

        return mouse_current_position

    def move_mouse_position(self, x_position : int, y_position : int, is_click : bool):
        '''
        This function moves mouse pointer to desginated x,y coordinate. Also it can click if is_click is True.

        Input : int, int, bool
        Output : bool
        '''
        delay_second = 0.2

        if is_click is True:
            pag.click(x = x_position, y = y_position, clicks = 2, interval = 0.2, button='left')
        else:
            pag.moveTo(x = x_position, y = y_position, duration = delay_second)

        return True
    
    def run_keyboard_input(self, keyboard_input : str):
        '''
        This function simulates keyboard input with default delay 1s. 

        Input : str
        Output : bool
        '''
        pag.press(keyboard_input)

        return True

    def run_image_trim(self, filepath):
        '''
        This function trims image with designated size and location. 

        Input : str
        Output : None
        '''
        img = Image.open(filepath)
        img_output = img.crop((540,490,1030,650))
        img_output.save(filepath, "PNG")
        # img_output.show(title = "Result")

    def get_user_confirmation(self):
        '''
        This function asks user confirmation for automation. 

        Input : None
        Output : bool
        '''
        user_output = pag.confirm(text='분광기 자동화 실행?', title='분광기 자동화 프로그램 V0.1', buttons=['OK', 'Cancel'])

        if user_output == "OK":

            return True

        else:

            return False

    def run_scenario_1(self,filepath_output : str):
        '''
        This function runs whole automation jobs. Since it is vertically long code. I add additionally comment for each section.

        Input : str
        Output : None
        '''
        # Clear workspace
        pag.hotkey("win", "d")

        # Ask user's confirmation
        wait(lambda: self.get_user_confirmation(), timeout_seconds=60, waiting_for="Finish of comfirmation")
        
        # Move to 45,227 and wait until initialization of spectrometer is complete
        self.move_mouse_position(45, 227, True)
        wait(lambda: self.get_status("Initialize.png"), timeout_seconds=60, waiting_for="Start of initialization")
        wait(lambda: self.get_status("Ready.png"), timeout_seconds=60 * 5, waiting_for="Finish of initialization")

        # Move to 1899,318 and wait until result is complete
        self.move_mouse_position(1899, 318, True)
        wait(lambda: self.get_status("Report.png"), timeout_seconds=60 * 2, waiting_for="Finish of measurement")

        # Check result of measurement and save as image
        self.move_mouse_position(1885, 210, True)
        # Run Shortcut of nextpage
        self.run_keyboard_input("n")
        # Run Shortcut of zoom
        self.run_keyboard_input("i")
        time.sleep(3)
        pag.screenshot(filepath_output)

        # Trim image and send to server
        self.run_image_trim(filepath_output)

        # Shutdown spectrometer program
        time.sleep(2)
        pag.hotkey("alt", "f4")
        time.sleep(1)
        pag.hotkey("alt", "f4")
        
    def get_scenario_status(self, filename : str):
        '''
        This function runs pixel-match vision method to control scenario's automated flow.

        Input : str
        Output : bool
        '''
        filepath = "C:\\Users\\Peal_UV\\Desktop\\Workspace\\UVAutomation\\screenshot\\" + filename

        try:
            is_initalize = pag.locateOnScreen(filepath)
            print(is_initalize)

            if is_initalize is not None:
                print("Status is success") 

                return True

            else:

                return False

        except:
                print("Wait until next status is complete")

def main():
    '''
    This function is main code.  

    Input : None
    Output : None
    '''
    ua = UVAutomation()
    sm = SSHManager()

    ua.run_scenario_1("C:\\Users\\Peal_UV\\Desktop\\Workspace\\UVAutomation\\output\\data.png")
    # while True:
    #     print(ua.get_mouse_position())

if __name__ == "__main__":
    main()
        