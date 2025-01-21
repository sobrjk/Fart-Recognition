1. Install python 3.11 https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
2. Download and unpack archive from github
3. install all requirements: pip install -r requirements.txt
4. Use shortcut file to launch chrome. Close all chrome instances before launch.
You can manual create shortcut with next additional data
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
![изображение](https://github.com/user-attachments/assets/362bf8d8-54b3-4b0e-a6cb-95baac1fe619)
5. Make sure that the page opens correctly: http://localhost:9222/json
6. .env file contains info about token to create
7. Run script: python main.py
8. After loading the script, wait for the message: Recording...
9. FART
