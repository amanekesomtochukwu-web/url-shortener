from flask import Flask, render_template, request, redirect
import random
import string

app = Flask(__name__)

# Temporary storage (later replace with database)
links = {}
clicks = {}


def generate_code(length=6):
    """Generate random short code like a8K29d"""
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']

    # create code
    code = generate_code()

    # avoid collisions (rare, but good practice)
    while code in links:
        code = generate_code()

    links[code] = long_url
    clicks[code] = 0

    short_link = request.host_url + code

    return render_template(
        'index.html',
        short_link=short_link
    )


@app.route('/<code>')
def redirect_short(code):

    if code in links:
        clicks[code] += 1
        return redirect(links[code])

    return "Link not found"


@app.route('/stats/<code>')
def stats(code):

    if code in clicks:
        return f"Clicks: {clicks[code]}"

    return "Code not found"


if __name__ == '__main__':
    app.run(debug=True)