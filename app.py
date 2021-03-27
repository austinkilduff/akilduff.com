from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

debug = False

blogJsonFilename = 'blog.json' if debug else '/var/www/akilduff/blog.json'

@app.route('/')
def index():
    return page(1)

@app.route('/page/<num>')
def page(num):
    blog = []

    with open(blogJsonFilename) as jsonFile:
        jsonStr = jsonFile.read()
        blog = sorted(json.loads(jsonStr), key = lambda post: post['id'])

    pageCount = (len(blog) / 10) if (len(blog) % 10) == 0 else (int(len(blog) / 10) + 1)
    num = int(num)
    if num < 1 or num > pageCount:
        return notfound(None)

    startIndex = 0 if (len(blog) < (num * 10)) else (len(blog) - (num * 10))
    endIndex = len(blog) - ((num - 1) * 10)
    posts = blog[startIndex:endIndex][::-1]

    showPrev = num > 1
    showNext = len(blog) > (num * 10)

    return render_template('blog.html', posts = posts, showPrev = showPrev, showNext = showNext, num = num)

@app.route('/post/<num>')
def post(num):
    blog = []

    with open(blogJsonFilename) as jsonFile:
        jsonStr = jsonFile.read()
        blog = json.loads(jsonStr)

    for post in blog:
        if str(post['id']) == num:
            return render_template('post.html', post = post)

    return notfound(None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404

if debug:
    app.run()
