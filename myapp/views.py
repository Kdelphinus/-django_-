from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

topics = [
    {"id": 1, "title": "routing", "body": "Routing is ..."},
    {"id": 2, "title": "view", "body": "View is ..."},
    {"id": 3, "title": "model", "body": "Model is ..."},
]


def html_template(article_tag: str, request_id: str = None) -> str:
    global topics
    context_ui = (
        ""
        if request_id is None
        else """<li>
                    <form action="/delete/" method="post">
                        <input type="hidden" name="id" value="{request_id}">
                        <input type="submit" value="delete">
                    </form>
                </li>"""
    )
    ol = ""
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f"""
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ul>
            {ol}
        </ul>
        {article_tag}
        <ul>
            <li><a href="/create/">create</a></li>
            {context_ui}
        </ul>
    </body>
    </html>
    """


def index(request):
    article = """
    <h2>Welcome</h2>
    Hello, Django
    """
    return HttpResponse(html_template(article))


def read(request, request_id: str):
    global topics
    for topic in topics:
        if topic["id"] == int(request_id):
            article_tag = f"""
            <h2>{topic["title"]}</h2>
            {topic["body"]}
            """
            return HttpResponse(html_template(article_tag, request_id))


@csrf_exempt
def create(request):
    if request.method == "GET":
        article = """
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        """
        return HttpResponse(html_template(article))
    elif request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        topics.append({"id": len(topics) + 1, "title": title, "body": body})
        url = "/read/" + str(len(topics))
        return redirect(url)


@csrf_exempt
def delete(request):
    global topics
    if request.method == "POST":
        print(request.POST)
        request_id = request.POST["id"]
        for i, topic in enumerate(topics):
            if topic["id"] == int(request_id):
                del topics[i]
                break
        return redirect("/")
