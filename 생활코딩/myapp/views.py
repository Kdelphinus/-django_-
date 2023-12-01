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
        else f"""<li>
                    <form action="/delete/" method="post">
                        <input type="hidden" name="id" value="{request_id}">
                        <input type="submit" value="delete">
                    </form>
                </li>
                <li><a href="/update/{request_id}">update</a></li>"""
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
def update(request, request_id: str):
    global topics
    if request.method == "GET":
        selected_topic = {"title": "", "body": ""}
        for topic in topics:
            if topic["id"] == int(request_id):
                selected_topic["title"] = topic["title"]
                selected_topic["body"] = topic["body"]
                break
        article = f"""
            <form action="/update/{request_id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selected_topic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selected_topic["body"]}</textarea></p>
                <p><input type="submit"></p>
            </form>
        """
        return HttpResponse(html_template(article, request_id))
    elif request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        for topic in topics:
            if topic["id"] == int(request_id):
                topic["title"] = title
                topic["body"] = body
                break
        return redirect(f"/read/{request_id}")


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
