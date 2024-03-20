import json
from flask import Flask, render_template

app = Flask(__name__)

def parse_chart_data(data_str):
    data_list = data_str.split('/')
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return [{'height': int(height) if height.isdigit() else 0, 'day': day} for height, day in zip(data_list, days)]

def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            parts = line.strip().split('/')
            if len(parts) >= 5:
                name, number, image_number, *chart_data, total_time = parts
                # number가 숫자인지 확인하고, 아니면 0을 사용
                number = int(number) if number.isdigit() else 0
                chart_data_str = '/'.join(chart_data)
                data.append({
                    'name': name,
                    'number': number,
                    'image_number': image_number,
                    'chart_data': parse_chart_data(chart_data_str),
                    'total_time': total_time
                })
        return data

#이름/번호/이미지번호/월요일데이터/화요일데이터/수요일데이터/목요일데이터/금요일데이터/토요일데이터/총시간

@app.route('/')
def index():
    target_name = "Jae woo"
    black_box_items = load_data_from_file('/Users/sfumato/0W/data.txt')
    target_item = None
    for item in black_box_items:
        if item['name'] == target_name:
            target_item = item
            break
    if target_item:
        name = target_item['name']
        time = target_item['total_time']
        chart_data = target_item['chart_data']
        image_number = target_item['image_number']
        chart_box2_data = [{'height': data['height'], 'day': data['day']} for data in chart_data]
    else:
        name = target_name
        time = "00:00:00"
        chart_data = []
        image_number = "default.png"
        chart_box2_data = []

    chart_data_json = json.dumps(chart_data)
    chart_box2_data_json = json.dumps(chart_box2_data)
    return render_template('index.html', name=name, time=time, black_box_items=black_box_items, chart_data_json=chart_data_json, image_number=image_number, chart_box2_data_json=chart_box2_data_json)

if __name__ == '__main__':
    app.run(debug=True)