# 분광기 자동화
## Setup
* 분광기 프로그램 제한으로 인해 윈도우상에서 개발해야함!
* VScode + GUI를 혼합하여 활용! (SSH?)
* OpenSSH 서버 설치
	* https://eehoeskrap.tistory.com/763
	  * https://biomadscientist.tistory.com/110#:~:text=3.%20%EB%8B%A4%EC%9D%8C%20VS%20code%EB%A5%BC%20%ED%95%9C%EB%B2%88%20%EC%9E%AC%EC%8B%9C%EC%9E%91%ED%95%98%EA%B1%B0%EB%82%98%20%ED%84%B0%EB%AF%B8%EB%84%90,%EC%84%A4%EC%A0%95%EB%90%9C%20%ED%84%B0%EB%AF%B8%EB%84%90%EC%9D%B4%20%EC%97%B4%EB%A6%AC%EB%8A%94%20%EA%B2%83%EC%9D%84%20%ED%99%95%EC%9D%B8%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8B%A4.
	* ![Pasted image 20250707155152.png](https://github.com/coport-uni/UVAutomation/blob/main/Pasted%20image%2020250707155152.png)
* https://pyautogui.readthedocs.io/en/latest/quickstart.html#screenshot-functions
* https://wikidocs.net/85709

```powershell
# Proceed in admin mode!
# Install Conda/Vscode before
Get-Service sshd
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

```cmd
conda create -n uv_auto
conda activate uv_auto
pip install pyautogui waiting pillow

python main.py
```
## Code
```python title=main.py
import pyautogui as pag
from waiting import wait
import time
from PIL import Image
from sshmanager import SSHManager

class UVAutomation():
    def __init__(self):
        self.serverpath = "/workspace/input_image_from_system"

        self.sm = SSHManager()
        self.sm.create_ssh_client(hostname = "10.16.21.197", port = "17042", username = "root", password = "pealauto")

    def get_mouse_position(self):
        '''
        This function captures live mouse position.

        Input : None
        Output : dict
        '''
        mouse_current_position = pag.position()
        time.sleep(1)

        return mouse_current_position

    def move_mouse_position(self, position_x : int, position_y : int, is_click : bool):
        '''
        This function moves mouse pointer to desginated x,y coordinate. Also it can click if is_click is True.

        Input : int, int, bool
        Output : bool
        '''
        delay_second = 0.2

        if is_click is True:
            pag.click(x = position_x, y = position_y, clicks = 2, interval = 0.2, button='left')
        else:
            pag.moveTo(x = position_x, y = position_y, duration = delay_second)

        return True
    
    def run_keyboard_input(self, keyboard_input : str):
        '''
        This function simulates keyboard input with default delay 1s. 

        Input : str
        Output : bool
        '''
        pag.press(keyboard_input)

        return True

    def run_image_trim(self, filepath_output : str):
        '''
        This function trims image with designated size and location. 

        Input : str
        Output : None
        '''
        img = Image.open(filepath_output)
        img_output = img.crop((540,490,1030,650))
        img_output.save(filepath_output, "PNG")
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
        
        # Move to 45,227 and wait until initialization of spectrometer is complete
        time.sleep(2)
        self.move_mouse_position(45, 227, True)
        wait(lambda: self.get_scenario_status("Initialize.png"), timeout_seconds=60, waiting_for="Start of initialization")
        wait(lambda: self.get_scenario_status("Ready.png"), timeout_seconds=60 * 5, waiting_for="Finish of initialization")

        # Move to 1899,318 and wait until result is complete
        self.move_mouse_position(1899, 318, True)
        wait(lambda: self.get_scenario_status("Report.png"), timeout_seconds=60 * 2, waiting_for="Finish of measurement")

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
        self.sm.send_file_to(filepath_output, self.serverpath)

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
    This function is main code. it uses external sshmanager module to send image.

    Input : None
    Output : None
    '''
    # Ask user's confirmation
    ua = UVAutomation()
    wait(lambda: ua.get_user_confirmation(), timeout_seconds=60, waiting_for="Finish of comfirmation")

    for i in range(1):
        filepath = f"C:\\Users\\Peal_UV\\Desktop\\Workspace\\UVAutomation\\output\\data{i}.png"
        ua.run_scenario_1(filepath)

if __name__ == "__main__":
    main()   
```
##  Result
![data.png](https://github.com/coport-uni/UVAutomation/blob/main/output/data.png)
![KakaoTalk_20250707_213430876.mp4]()
