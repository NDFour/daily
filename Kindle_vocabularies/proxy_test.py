import requests

def test(p ):
	proxies = {
		'http': p,
		'https': p
	}

	print(proxies)

	url = 'http://ip.chinaz.com/'
	# url = 'https://www.ip138.com'
	# url = 'http://www.baidu.com'

	r = requests.get(url, proxies = proxies, timeout = 15)

	with open('a.html', 'w') as f:
		f.write(r.text)

if __name__ == '__main__':
	p = input('proxy:').strip()
	test( p )

