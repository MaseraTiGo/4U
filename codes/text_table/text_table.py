import re

src_string = "name=asshole&& age=33||age=22&&(sex_gender=F||female=F)||info$$fuck&&msg^^you"
new_string = re.sub('([a-zA-Z]+|[a-zA-Z]+_[a-zA-Z]+)=([0-9a-zA-Z\u4E00-\u9FA5]+)',
                    lambda m: '"{' + m.group(1) + '}"=' + '"' + m.group(2) + '"', src_string)
print(new_string)
new_string = re.sub('([a-zA-Z]+|[a-zA-Z]+_[a-zA-Z]+)[\$\^]+([0-9a-zA-Z\u4E00-\u9FA5]+)',
                    lambda m: '"' + m.group(2) + '" in ' + '"{' + m.group(1) + '}"', new_string)
print(new_string)

final_str = new_string.replace('=', ' == ').replace('&&', ' and ').replace('||', ' or ')
print(final_str)
args = {
    'name': "dante",
    "age": '44',
    'sex_gender': 'Ff',
    'female': "female",
    'info': "shit",
    'msg': "motherfucker",
}
logic_str = final_str.format(**args)
print(logic_str)
if_str = 'if ' + logic_str + ':\r\n    print("fuck you")'
print(if_str)
print(exec(if_str))
# if "dante" == "asshole" and "22" == "33" or "22" == "22" and (
#         "F" == "F" or "female" == "F") or "fuck" in "fuck shit" and "you" in "motherfucker":
#     print("fuck you=========")
# src = src_string.replace('=', ' == ').replace('&&', ' and ').replace('||', ' or ')
# print(src)

# symbols = re.findall('[=|\&|\||\^|\$|\(|\)]+', src_string)
# print(symbols)
# new_str = re.sub('[=|\&|\||\^|\$|\(|\)]+', '@', src_string)
# print(new_str)
# args = [item.strip() for item in new_str.split('@')]
# print(args)
# logic_fragment = ''
# logic_str = ''
# if symbols[0] != '(':
#     logic_str = f'{}'
