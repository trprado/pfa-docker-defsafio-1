import config
from database import Database
from http.server import BaseHTTPRequestHandler, HTTPServer
# import socketserver

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()

        message = str(get_course_topics())
        self.wfile.write(bytes(message, encoding='utf8'))


def get_course_topics():
    db = Database(config)
    sql = 'SELECT * FROM module'
    html = '<ul class="list-none md:list-disc">'
    modules = db.query(sql)
    for row in modules:
        # course.append({'module': row['name'], 'topics':[]})
        html += f'\n<li>{row["name"].encode("latin-1").decode("utf-8")}</li>'
        sql = f'''
            SELECT t.name
            FROM module AS m
            LEFT JOIN topics AS t
            ON t.module_id = m.id
            WHERE m.id = {row['id']}
        '''
        res = db.query(sql)
        html += '\n<ul class="list-decimal list-outside md:list-inside">'
        for item in res:
            # course[row['id']-1]['topics'].append(trow['name'])
            html += f'\n<li>{item["name"].encode("latin-1").decode("utf-8")}</li>'
        html += '\n</ul>'
    html += '\n</ul>'
    index = generate_index(html)
    print(index)
    return index

def generate_index(html):
    index = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/1.1.4/tailwind.min.css" 
            integrity="sha512-YQ6wKoZQdz0PlN9obSLOVkKeJnTPm2Kb+SiE6qwC0zODy9aStxyEp8fa1JeCMxb4qVHkHWr1pQvAcEWcnTiiEA==" 
            crossorigin="anonymous" />
        <title>FPA - DOCKER</title>
    </head>
    <body>
        <div class="container mx-auto">
            <h1 class="text-center text-5xl">FPA - Docker</h1>
            <div class="box-border md:box-content justify-center">
                {html}
            </div>
        </div>
    </body>
    </html>'''
    return index

PORT = 8000
with HTTPServer(('0.0.0.0', 8000), handler) as server:
    print("serving at port", PORT)
    server.serve_forever()
