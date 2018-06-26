import urllib
import requests
import re
import semail_pub
import time

URL = "https://www.reg.uci.edu/perl/WebSoc"
BASE_DATA = {'Submit':'Display Web Results', 'YearTerm':'2018-14'}

# Example 
CLASS = {'Mgmt7':{38016},'Mgmt30A':{38026},'Mgmt105':{38061,38063},'Math3A':{44340,44378},'ICS32':{36570}}


def search_by_id(code):
    try:
        data = BASE_DATA
        data['CourseCodes'] = int(code)
        response = requests.post(URL, data=data)
        #To find RE with the raw html
        with open("exp.html","w") as f:
            f.write(response.text)
        return response.text
    except Exception as e:
        print(e)

def find_name(text):
    name = re.findall('(<tr bgcolor="#fff0ff" valign="top"><td class="CourseTitle" colspan="16" nowrap="nowrap">)(.+<f)',text)
    name = name[0][1]
    name = name[:-2]
    name = name.replace("&nbsp; ","")
    name = name.replace("&amp;","&")
    return name

def find_restriction(text):
    res = re.findall(">(([A-Z])(\ and\ [A-Z])?)<",text)
    res = res[1][0]
    return res

def find_num(text):
    nums = re.findall(">(\d\d\d)<|>(\d\d)<|>(\d)<",text) 
    return nums

#Possible improvent on performance if only get the num once
def find_nonempty(nums):
    for num in nums:
        if num: return num

    return result

def find_detail(text,detail):
    nums = find_num(text)
    if len(nums) == 6:
        if detail == "Units":
            result = find_nonempty(nums[0])
        elif detail == "Max":
            result = find_nonempty(nums[1])
        elif detail == "Enr": 
            result = find_nonempty(nums[2])
        elif detail == "WL":
            result = find_nonempty(nums[3])
        elif detail == "Req":
            result = find_nonempty(nums[4])
        elif detail == "Nor":
            result = find_nonempty(nums[5])

    elif len(nums) == 5:
        if detail == "Units":
            result = find_nonempty(nums[0])
        elif detail == "Max":
            result = find_nonempty(nums[1])
        elif detail == "Enr": 
            result = find_nonempty(nums[2])
        elif detail == "WL":
            result = -1 #Means n/a
        elif detail == "Req":
            result = find_nonempty(nums[3])
        elif detail == "Nor":
            result = find_nonempty(nums[4])
    else: 
        print("Something Wrong!! Check the nums!")
    
    return result

if __name__ == '__main__':
    while True:
        for c in CLASS.values():
            for Code in c:

                text = search_by_id(Code)
                name = find_name(text)
                Rstr = find_restriction(text)
                num = find_num(text)
                Units = find_detail(text,"Units")
                Max = find_detail(text,"Max")
                Enr = find_detail(text,"Enr")
                WL = find_detail(text,"WL")
                Req = find_detail(text,"Req")
                Nor = find_detail(text,"Nor") 
                print(name,Rstr,Units,Max,Enr,WL,Req,Nor)

                if ('L' in Rstr) or ('N' in Rstr):
                    print("The course {}({}) is major restricted now".format(name,Code))

                elif Max == "0":
                    print("The course {}({}) is not open now".format(name,Code))
                else:
                    print("No major restriction on {}({}) now".format(name,Code))
                    semail_pub.send_email("CLASS IS OPEN!","The class {}({}) has lifted its major restriction!".format(name,Code))
                    print("Mail sent")
                time.sleep(10)
            

"""
#Or Using urllib.request
import urllib.request
import urllib.parse

URL_SOC = "https://www.reg.uci.edu/perl/WebSoc"

def main():
    post_params = {"Submit":"Display Web Results","YearTerm":"2018-03","CourseCodes":34340}
    data = urllib.parse.urlencode(post_params)
    data = data.encode('ascii')
    response = urllib.request.urlopen(URL_SOC,data)
    print(response.read().decode('utf-8'))

if __name__ == "__main__":
    main()
"""


