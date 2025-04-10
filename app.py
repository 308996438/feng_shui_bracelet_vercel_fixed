"""
手串饰品预测软件 - 简化版Flask应用 (Vercel兼容版)
"""
from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import json
import requests
import datetime

# 创建Flask应用
app = Flask(__name__)

# 五行属性
FIVE_ELEMENTS = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
    "子": "水", "亥": "水",
    "寅": "木", "卯": "木",
    "巳": "火", "午": "火",
    "申": "金", "酉": "金",
    "丑": "土", "辰": "土", "未": "土", "戌": "土"
}

# 手串材质数据
BRACELET_MATERIALS = {
    "水晶": {
        "五行": "水",
        "颜色": ["透明", "白色", "紫色", "粉色", "黄色", "绿色", "蓝色"],
        "功效": ["净化能量", "增强直觉", "提升精神力"],
        "适合人群": ["需要净化负能量的人", "追求心灵平静的人"]
    },
    "琉璃": {
        "五行": "火",
        "颜色": ["蓝色", "绿色", "红色", "黄色", "紫色"],
        "功效": ["辟邪", "招财", "增强运势"],
        "适合人群": ["追求美好事物的人", "需要提升运势的人"]
    },
    "和田玉": {
        "五行": "土",
        "颜色": ["白色", "青白色", "青色", "黄色"],
        "功效": ["养生", "平衡情绪", "增强体质"],
        "适合人群": ["注重健康的人", "需要情绪稳定的人"]
    },
    "翡翠": {
        "五行": "木",
        "颜色": ["绿色", "紫色", "红色", "白色"],
        "功效": ["招财", "辟邪", "保平安"],
        "适合人群": ["追求财富的人", "需要保平安的人"]
    },
    "星月菩提": {
        "五行": "木",
        "颜色": ["棕色", "红棕色"],
        "功效": ["静心", "开智慧", "增强记忆力"],
        "适合人群": ["修行者", "学生", "需要静心的人"]
    },
    "金刚菩提": {
        "五行": "木",
        "颜色": ["棕色", "红棕色"],
        "功效": ["辟邪", "增强意志力", "提升自信"],
        "适合人群": ["需要增强意志力的人", "需要提升自信的人"]
    },
    "小叶紫檀": {
        "五行": "木",
        "颜色": ["紫红色", "深棕色"],
        "功效": ["安神", "辟邪", "增强气场"],
        "适合人群": ["睡眠质量差的人", "需要提升气场的人"]
    }
}

# 宗教信仰对应的吉祥物和符号
RELIGIOUS_SYMBOLS = {
    '佛教': ['佛珠', '莲花', '法轮', '卍字符', '佛像', '六字真言'],
    '道教': ['太极', '八卦', '五行', '道符', '如意', '灵芝'],
    '基督教': ['十字架', '鱼形符号', '圣经', '天使', '橄榄枝', '鸽子'],
    '无': ['如意', '福字', '寿字', '平安结', '铜钱', '龙凤']
}

# 宗教特色手串材质
RELIGIOUS_MATERIALS = {
    '佛教': ['菩提子', '檀香木', '金刚菩提', '凤眼菩提', '星月菩提'],
    '道教': ['黄杨木', '桃木', '檀木', '紫檀', '黑檀'],
    '基督教': ['橄榄木', '黑檀木', '紫檀木', '水晶', '玛瑙'],
    '无': ['黄花梨', '小叶紫檀', '沉香', '金丝楠', '鸡翅木']
}

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """预测接口"""
    try:
        # 获取表单数据
        data = request.form
        
        name = data.get('name', '')
        gender = data.get('gender', '')
        birth_year = int(data.get('birth_year', 2000))
        birth_month = int(data.get('birth_month', 1))
        birth_day = int(data.get('birth_day', 1))
        birth_hour = int(data.get('birth_hour', 12))
        purpose = data.get('purpose', '财运')
        religion = data.get('religion', '无')
        
        # 简化版预测逻辑
        # 计算生肖
        zodiac_animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        zodiac = zodiac_animals[(birth_year - 4) % 12]
        
        # 计算星座
        zodiac_signs = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', 
                        '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座']
        
        dates = [20, 19, 21, 20, 21, 22, 23, 23, 23, 24, 22, 21]
        month_index = birth_month - 1
        if birth_day < dates[month_index]:
            zodiac_sign = zodiac_signs[month_index]
        else:
            zodiac_sign = zodiac_signs[(month_index + 1) % 12]
        
        # 简化版八字计算
        heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        year_stem_index = (birth_year - 4) % 10
        year_branch_index = (birth_year - 4) % 12
        
        # 简化的五行计算
        five_elements = []
        year_element = FIVE_ELEMENTS.get(heavenly_stems[year_stem_index], "")
        if year_element and year_element not in five_elements:
            five_elements.append(year_element)
        
        month_element = FIVE_ELEMENTS.get(earthly_branches[(birth_month + 1) % 12], "")
        if month_element and month_element not in five_elements:
            five_elements.append(month_element)
        
        # 计算幸运数字
        lucky_number1 = (birth_day + birth_month) % 9 + 1
        lucky_number2 = (birth_year % 100) % 9 + 1
        if lucky_number1 == lucky_number2:
            lucky_number2 = (lucky_number2 % 9) + 1
        lucky_numbers = [lucky_number1, lucky_number2]
        
        # 获取幸运颜色
        color_map = {
            "木": ["绿色", "青色"],
            "火": ["红色", "紫色"],
            "土": ["黄色", "棕色"],
            "金": ["白色", "金色"],
            "水": ["黑色", "蓝色"]
        }
        
        lucky_colors = []
        for element in five_elements:
            if element in color_map:
                lucky_colors.extend(color_map[element])
        
        # 如果五行元素不足，添加默认元素
        if not five_elements:
            five_elements = ["木", "火"]
        
        if not lucky_colors:
            lucky_colors = ["绿色", "红色"]
        
        # 生成预测结果
        prediction = {
            'name': name,
            'gender': gender,
            'birth_date': f"{birth_year}年{birth_month}月{birth_day}日",
            'birth_time': f"{birth_hour}:00",
            'zodiac': zodiac,
            'zodiac_sign': zodiac_sign,
            'five_elements': five_elements,
            'lucky_numbers': lucky_numbers,
            'lucky_colors': lucky_colors,
            'purpose': purpose,
            'religion': religion
        }
        
        # 生成运势预测
        fortune_prediction = generate_fortune_prediction(prediction)
        
        # 推荐手串
        bracelet_recommendation = recommend_bracelet(prediction)
        
        # 合并结果
        result = {
            'prediction': prediction,
            'fortune_prediction': fortune_prediction,
            'bracelet_recommendation': bracelet_recommendation
        }
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

def generate_fortune_prediction(prediction):
    """生成运势预测"""
    zodiac = prediction.get('zodiac', '')
    zodiac_sign = prediction.get('zodiac_sign', '')
    purpose = prediction.get('purpose', '财运')
    
    # 基于生肖和星座的简单预测
    fortune_text = f"作为{zodiac}和{zodiac_sign}的您，"
    
    # 根据所求事项生成预测
    if purpose == '财运':
        fortune_text += "在财运方面，今年整体运势平稳，有望获得意外之财。建议保持积极的心态，把握机会，财运自然会有所提升。"
    elif purpose == '事业':
        fortune_text += "在事业方面，今年将有新的机遇和挑战。建议保持开放的心态，积极学习新技能，提升自己的竞争力。"
    elif purpose == '健康':
        fortune_text += "在健康方面，今年需要特别注意休息和饮食规律。建议加强锻炼，保持良好的作息习惯，健康状况会有所改善。"
    elif purpose == '婚姻':
        fortune_text += "在婚姻方面，今年感情运势较为稳定。已婚者需要更多关注伴侣的需求，单身者有望遇到心仪的对象。"
    elif purpose == '学业':
        fortune_text += "在学业方面，今年学习能力有所提升。建议制定合理的学习计划，保持专注和耐心，学业成绩会有所进步。"
    else:
        fortune_text += "今年整体运势平稳，建议保持积极乐观的心态，多关注自身的成长和发展。"
    
    return fortune_text

def recommend_bracelet(prediction):
    """推荐手串"""
    five_elements = prediction.get('five_elements', [])
    lucky_colors = prediction.get('lucky_colors', [])
    purpose = prediction.get('purpose', '财运')
    religion = prediction.get('religion', '无')
    
    # 根据五行属性选择材质
    missing_elements = []
    all_elements = ['木', '火', '土', '金', '水']
    for element in all_elements:
        if element not in five_elements:
            missing_elements.append(element)
    
    # 如果没有缺失的五行，选择与所求事项相关的五行
    if not missing_elements:
        if purpose == '财运':
            missing_elements = ['金', '木']
        elif purpose == '事业':
            missing_elements = ['火', '木']
        elif purpose == '健康':
            missing_elements = ['土', '金']
        elif purpose == '婚姻':
            missing_elements = ['火', '土']
        elif purpose == '学业':
            missing_elements = ['水', '木']
        else:
            missing_elements = ['土']
    
    # 选择材质
    recommended_materials = []
    for material, info in BRACELET_MATERIALS.items():
        if info['五行'] in missing_elements:
            # 检查是否有幸运颜色
            has_lucky_color = False
            for color in info['颜色']:
                if color in lucky_colors:
                    has_lucky_color = True
                    break
            
            recommended_materials.append({
                'name': material,
                'element': info['五行'],
                'colors': info['颜色'],
                'effects': info['功效'],
                'suitable_for': info['适合人群'],
                'has_lucky_color': has_lucky_color
            })
    
    # 根据宗教信仰选择特色材质
    religious_materials = RELIGIOUS_MATERIALS.get(religion, [])
    
    # 选择宗教符号
    religious_symbols = RELIGIOUS_SYMBOLS.get(religion, [])
    
    # 生成推荐文本
    recommendation_text = f"根据您的五行属性和{purpose}需求，推荐以下手串材质组合：\n\n"
    
    # 添加材质描述
    for i, material in enumerate(recommended_materials[:3]):
        recommendation_text += f"{i+1}. {material['name']}（{material['element']}属性）\n"
        recommendation_text += f"   颜色：{', '.join(material['colors'])}\n"
        recommendation_text += f"   功效：{', '.join(material['effects'])}\n"
        recommendation_text += f"   适合：{', '.join(material['suitable_for'])}\n\n"
    
    # 添加宗教符号建议
    if religious_symbols:
        recommendation_text += f"根据您的{religion}信仰，建议在手串上添加以下吉祥物或符号：\n"
        recommendation_text += f"{', '.join(religious_symbols[:3])}\n\n"
    
    # 添加佩戴建议
    recommendation_text += "佩戴建议：\n"
    recommendation_text += "1. 手串通常佩戴在左手，因为左手靠近心脏，能更好地吸收能量。\n"
    recommendation_text += "2. 新购买的手串最好先净化，可以用清水冲洗或放在阳光下晒一晒。\n"
    recommendation_text += "3. 佩戴时保持心态平和，有助于增强手串的效果。\n"
    recommendation_text += "4. 定期清洁手串，保持其能量纯净。\n"
    
    return {
        'materials': recommended_materials[:3],
        'religious_symbols': religious_symbols[:3],
        'religious_materials': religious_materials[:3],
        'recommendation': recommendation_text
    }

@app.route('/health')
def health():
    """健康检查接口"""
    return jsonify({"status": "ok"})

# Vercel需要这个变量
app = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
