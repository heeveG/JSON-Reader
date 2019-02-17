import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import copy

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_json():
    """
    None -> dict
    Returns json dict, got using Twitter API, containing entered user friends' info
    """
    acct = input('Enter Twitter Account:')
    if len(acct) < 1:
        return None
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    return js


def print_res(res, lst, msg):
    """
    (dict, list, str) -> None
    Prints out info from dict based on input
    """
    lst.pop(0)
    print("Result for {}".format(msg))
    try:
        for i in res[lst[0]]:
            out = ''
            for j in range(len(lst)):
                if j == 0:
                    out += 'i'
                else:
                    out += '[lst[{}]]'.format(j)
            print(eval(out))
    except TypeError:
        print(res[lst[0]])
    return None


def analyze_json(js):
    """
    dict -> None
    Gets input from user and calls print_res with it
    """
    res = copy.deepcopy(js)
    lst = [" "]
    msg = "/"
    while True:
        print("You are currently at " + msg)
        a = list(js.keys())
        print("Keys: \n----")
        for i in range(len(a)):
            print(a[i], end=' / ')
            if i % 7 == 0 and i != 0:
                print('\n')
        k = input("\n----\nChoose a key: \n")
        while k not in a:
            k = input("Enter a right key please: \n")
        lst.append(k)
        msg += '{}/'.format(lst[-1])
        ask = input("Do you want to see {} info for whole dict(y) or go deeper(n) ?".format(k))
        if ask == 'y':
            print_res(res, lst, msg)
            break
        elif ask == 'n':
            try:
                js[k][0].keys()
                js = js[k][0]
            except:
                try:
                    js[k].keys()
                    js = js[k]
                except:
                    print('\nYou cannot go any deeper \n')
                    print_res(res, lst, msg)
                    break
    return None


if __name__ == "__main__":
    ask = input("Welcome to JSON Reader!\n If you want to explore Twitter JSON file enter '1'\n If you want to \
explore provided JSON file enter '2'\n If you want to explore you own JSON file copy \
it inside module folder and enter '3'\n")
    while ask not in ['1', '2', '3']:
        ask = input("Your answer is invalid. Please reenter\n")
    if ask == '1':
        analyze_json(get_json())
    elif ask == '2':
        with open("user_friends.json") as f:
            data = json.load(f)
        analyze_json(data)
    elif ask == '3':
        name = input("Please enter your file name without '.json'\n")
        try:
            with open("{}.json".format(name)) as f:
                data = json.load(f)
            analyze_json(data)
        except FileNotFoundError:
            print('You entered invalid file name. Try again.')
