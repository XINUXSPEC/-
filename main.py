import requests
url = input("下载链接:")

print("您需要下载的链接是:"+url)

#https://lf9-ug-sign.feishucdn.com/ee-appcenter/ba9359bd/Feishu-win32_x64-7.71.12-signed.exe?lk3s=fb957577\u0026x-expires=1783618326\u0026x-signature=aT1lXDrg7SumRnMrn9Hiqo60ugs%3D
response = requests.get(url)

filename = "software.exe"

with open(filename,"wb") as f:
    f.write(response.content)
