from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# 连接数据库
engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
session = Session()

# 首页和查询表单
@app.route('/')
def index():
    return render_template('index.html')

# 处理查询请求
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        major = request.form.get('major', '')
        school = request.form.get('school', '')
        rank_min = request.form.get('rank_min', '0')
        rank_max = request.form.get('rank_max', '99999')
        year = request.form.get('year', '')
        return redirect(url_for('search', major=major, school=school, rank_min=rank_min, rank_max=rank_max, year=year, page=1))
    else:
        major = request.args.get('major', '')
        school = request.args.get('school', '')
        rank_min = request.args.get('rank_min', '0')
        rank_max = request.args.get('rank_max', '99999')
        year = request.args.get('year', '')
        page = request.args.get('page', 1, type=int)
        sort_by = request.args.get('sort_by', '位次')  # 默认按位次排序
    
    per_page = 20

    major = f'%{major}%' if major else '%'
    school = f'%{school}%' if school else '%'
    year = f'%{year}%' if year else '%'

    try:
        rank_min = int(rank_min) if rank_min else 0
    except ValueError:
        rank_min = 0

    try:
        rank_max = int(rank_max) if rank_max else 99999
    except ValueError:
        rank_max = 999999
    
    query = text("""
            SELECT * FROM schools
            WHERE 专业 LIKE :major
            AND 学校 LIKE :school
            AND 位次 BETWEEN :rank_min AND :rank_max
            AND 年份 LIKE :year
            ORDER BY """ + sort_by + """
            LIMIT :limit OFFSET :offset
        """)
    
    results = session.execute(query, {
        'major': major,
        'school': school,
        'rank_min': rank_min,
        'rank_max': rank_max,
        'year': year,
        'limit': per_page,
        'offset': (page - 1) * per_page
    }).fetchall()
    
    total_query = text("""
        SELECT COUNT(*) FROM schools
        WHERE 专业 LIKE :major
        AND 学校 LIKE :school
        AND 位次 BETWEEN :rank_min AND :rank_max
        AND 年份 LIKE :year
    """)
    
    total_results = session.execute(total_query, {
        'major': major,
        'school': school,
        'rank_min': rank_min,
        'rank_max': rank_max,
        'year': year
    }).scalar()
    
    total_pages = (total_results + per_page - 1) // per_page
    
    return render_template('results.html', results=results, page=page, total_pages=total_pages, 
                               major=request.args.get('major'), school=request.args.get('school'), 
                               rank_min=request.args.get('rank_min'), rank_max=request.args.get('rank_max'), 
                               year=request.args.get('year'), sort_by=sort_by)
if __name__ == '__main__':
    app.run(debug=True)
