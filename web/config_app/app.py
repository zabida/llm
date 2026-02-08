from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
from cachetools import TTLCache
import uuid
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于 session

# 缓存：key=cache_id, value=data_dict
cache = TTLCache(maxsize=100, ttl=600)  # 10分钟过期

EXPORT_PASSWORD = "secret123"  # 导出口令


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    git_addr = request.form.get('git_address')
    token = request.form.get('token')

    group_names = []
    groups_data = {}

    # 收集所有组
    idx = 1
    while True:
        group_name = request.form.get(f'group_name_{idx}')
        if not group_name:
            break
        group_names.append(group_name)
        groups_data[group_name] = {
            'appid': request.form.get(f'appid_{idx}', ''),
            'static_token': request.form.get(f'static_token_{idx}', ''),
            'region': request.form.get(f'region_{idx}', ''),
            'environ': request.form.get(f'environ_{idx}', ''),
            'onekey': request.form.get(f'onekey_{idx}', ''),
            'twokey': request.form.get(f'twokey_{idx}', ''),
        }
        idx += 1

    if not groups_data:
        flash("请至少添加一组配置！", "error")
        return redirect(url_for('index'))

    # 构造数据结构
    data = {
        'git_address': git_addr,
        'token': token,
        'groups': groups_data
    }

    cache_id = str(uuid.uuid4())
    cache[cache_id] = data
    session['cache_id'] = cache_id

    return redirect(url_for('config_list'))


@app.route('/list')
def config_list():
    cache_id = session.get('cache_id')
    if not cache_id or cache_id not in cache:
        flash("数据已过期或不存在，请重新提交。", "error")
        return redirect(url_for('index'))

    data = cache[cache_id]
    groups = data['groups']
    group_names = list(groups.keys())

    # 表格行定义
    rows = [
        {'key': 'Git Address', 'values': [data['git_address']] * len(group_names), 'notes': [''] * len(group_names)},
        {'key': 'Token', 'values': [data['token']] * len(group_names), 'notes': [''] * len(group_names)},
        {'key': 'AppID', 'values': [groups[name]['appid'] for name in group_names], 'notes': [''] * len(group_names)},
        {'key': 'Static Token', 'values': [groups[name]['static_token'] for name in group_names],
         'notes': [''] * len(group_names)},
        {'key': 'Region', 'values': [groups[name]['region'] for name in group_names], 'notes': [''] * len(group_names)},
        {'key': 'Environ', 'values': [groups[name]['environ'] for name in group_names],
         'notes': [''] * len(group_names)},
        {'key': 'OneKey', 'values': [groups[name]['onekey'] for name in group_names], 'notes': [''] * len(group_names)},
        {'key': 'TwoKey', 'values': [groups[name]['twokey'] for name in group_names], 'notes': [''] * len(group_names)},
    ]

    return render_template('list.html', group_names=group_names, rows=rows, cache_id=cache_id)


@app.route('/export', methods=['POST'], endpoint='export')
def export_excel():
    password = request.json.get('password')
    cache_id = request.json.get('cache_id')

    if password != EXPORT_PASSWORD:
        return jsonify({'success': False, 'msg': '口令错误！'})

    if not cache_id or cache_id not in cache:
        return jsonify({'success': False, 'msg': '数据已过期！'})

    data = cache[cache_id]
    groups = data['groups']
    group_names = list(groups.keys())

    # 构建 DataFrame
    df_data = {
        'Key': ['Git Address', 'Token', 'AppID', 'Static Token', 'Region', 'Environ', 'OneKey', 'TwoKey']
    }
    for i, name in enumerate(group_names):
        df_data[f'{name}-值'] = [
            data['git_address'],
            data['token'],
            groups[name]['appid'],
            groups[name]['static_token'],
            groups[name]['region'],
            groups[name]['environ'],
            groups[name]['onekey'],
            groups[name]['twokey']
        ]
        df_data[f'{name}-备注'] = [''] * 8

    df = pd.DataFrame(df_data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Config')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='config_export.xlsx'
    )


if __name__ == '__main__':
    app.run(debug=True)