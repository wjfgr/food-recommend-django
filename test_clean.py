import re

def clean_name(raw):
    name = raw.strip()
    name = re.sub(r'【[^】]*】', '', name)
    name = re.sub(r'^[\d\.\s\+\-\~]+', '', name)
    name = re.sub(r'^[\d\.\s]+(克|g|kg|斤|两|勺|个|根|片|瓣|颗|把|条|块|杯|ml|毫升|只|朵|粒|份|包|瓶|罐|节|大|小|半)', '', name)
    name = re.sub(r'[\d\.\s]+(克|g|kg|斤|两|勺|个|根|片|瓣|颗|把|条|块|杯|ml|毫升|只|朵|粒|份|包|瓶|罐|节)$', '', name)
    name = re.sub(r'^(一小勺|一勺|两勺|少许|适量|一点|一些|大|小|半|整|颗|根|片|个|一)', '', name)
    name = re.sub(r'（[^）]*）', '', name)
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'[#\*\+\-\~\/\\]', '', name)
    return name.strip()

# 测试几个例子
test_cases = [
    '适量盐',
    '6克盐',
    '3根香菜',
    '5片姜',
    '3瓣蒜',
    '1勺耗油',
    '2勺生抽',
    '1嘬香葱',
]

print("测试清理函数:")
for t in test_cases:
    result = clean_name(t)
    print(f"  '{t}' → '{result}'")
