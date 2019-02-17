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
    lst.pop(0)
    print("Result for {}".format(msg))
    try:
        for i in res[lst[0]]:
            if len(lst) > 2:
                if len(lst) == 3:
                    print(i[lst[1]][lst[2]])
                elif len(lst) == 4:
                    print(i[lst[1]][lst[2]][lst[3]])
                elif len(lst) == 5:
                    print(i[lst[1]][lst[2]][lst[3]][lst[4]])
                elif len(lst) == 6:
                    print(i[lst[1]][lst[2]][lst[3]][lst[4]][lst[5]])
            else:
                if len(lst) == 2:
                    print(i[lst[1]])
                else:
                    print(i)
    except TypeError:
        print(res[lst[0]])
    return None


def analyze_json(js):
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


# with open("user_friends.json") as f:
#     data = json.load(f)

analyze_json(get_json())