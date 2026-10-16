import json, re

print("读取JSON文件...")
with open('data/tran_dataset_single_0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 找几个例子看看
print("\n=== 看看前5道菜的食材列表 ===")
for i, item in enumerate(data[:5]):
    conv = item['conversation'][0]
    input_text = conv['input']
    output_text = conv['output']
    
    name = input_text.replace('的做法', '').strip()
    
    m = re.search(r"您需要准备以下食材:\n\[(.*?)\]\n按以下方法制作:", output_text, re.DOTALL)
    if m:
        ingredient_str = m.group(1)
        print(f"\n菜名: {name}")
        print(f"食材列表: {ingredient_str[:200]}...")
