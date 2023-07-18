import json
import os
import time

TEST_CLASS = "SCL-90"

def loaddata() -> dict:
    global TEST_CLASS
    data = None
    with open(os.path.join("data",TEST_CLASS+".json"),"r",encoding="utf-8") as f:
        data = json.load(f)
    return data

def log(text:str,output:bool=False) -> None:
    if output:
        print(text)
    with open(
        os.path.join("log",f'{time.strftime("%Y%m%d", time.localtime())}.log'),
        "a+",
        encoding="utf-8"
    ) as f:
        f.write(str(text)+"\n")

def test():
    data = loaddata()
    answer = {}
    positive = 0
    print(data['name'])
    print("version:"data['version'])
    print(data['introduce'])
    input("开始答题请回车")
    all_qu = len(data['questions'])
    now_qu = 1
    for id,body in data['questions'].items():
        print("\n["+str(now_qu)+"/"+str(all_qu)+"] "+body['question'])
        while True:
            for key,key_body in body['options'].items():
                print(str(key)+":"+str(key_body["text"]))
            inp = input("输入选择>>>")
            if inp in body["options"].keys():
                ans_socre = body["options"][inp]["score"]
                answer[id] = ans_socre
                if ans_socre > 1:
                    positive += 1
                break
            else:
                print("输入错误，请重新输入")
        now_qu += 1

    print("测试结束,计算中")
    chart = "图表：\n"
    text = "解析：\n"
    for key in data["direction"]:
        socre = 0
        if [0] == key["bind"]:
            socre = sum(answer.values())
        else:
            for qus in key["bind"]:
                socre += answer[str(qus)]
        if key["type"] == "avg":
            # chart
            socre = socre/len(key["bind"])
            if [0] == key["bind"]:
                socre = socre/all_qu
        if key["chart"]:
            chart += key["name"].rjust(6," ").replace(" ","  ")+str(round(socre,2)).ljust(5)
            chart += str("|"*int(round(socre*8,0))).ljust(40,"-")+"|\n"
        # text

        text += "\n\n"+key["name"]+"\n"
        for key_text,value in key["diagnosis"].items():
            key_data = key_text[1:-1].split(",")
            if key_text[0] == "[":
                if socre >= float(key_data[0]):
                    if key_text[-1] == ")":
                        if socre < float(key_data[1]):
                            text += value+"\n"
                            break
                    elif key_text[-1] == "]":
                        if socre <= float(key_data[1]):
                            text += value+"\n"
                            break
            elif key_text[0] == "(":
                if socre > float(key_data[0]):
                    if key_text[-1] == ")":
                        if socre < float(key_data[1]):
                            text += value+"\n"
                            break
                    elif key_text[-1] == "]":
                        if socre <= float(key_data[1]):
                            text += value+"\n"
                            break
    
    print("测试结束,以下是您的报告")
    log("="*80)
    log(data['name'].center(80,"="))
    log(time.strftime("%H:%M:%S", time.localtime()).center(80,"="))
    log("="*80)
    log(chart,True)
    log(text,True)
    log(json.dumps(answer,ensure_ascii=False))
test()
input("按回车退出")
