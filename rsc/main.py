import os.path
import re
from time import sleep

import requests

import reflection

reflectionTable = str.maketrans(reflection.utf16dic)
basicUrl = "https://www.youduzw.com/book/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
re_obj = re.compile(
    r"t[0-9]+_1:'/book/(?P<nextID>.*?)',t[0-9]+_index.*?"
    r'<h1>正文 (?P<title>.*?)</h1>.*?'
    r'</script></div><p>(?P<text>.*?)</p><div class="bar">',
    re.S
)


def down_load_start(book_id, name="unnamed"):
    file_path = os.path.join("./books/" + name + ".txt")
    with open(file_path, mode="wb") as txt:
        book = book_id
        cycling = True
        while cycling:
            resp = requests.get(
                url=basicUrl + book + ".html#google_vignette",
                headers=headers
            )
            result = re_obj.finditer(resp.text)
            resp.close()

            for it in result:
                if len(it.group("nextID")) < len(book_id):
                    cycling = False

                book = it.group("nextID").split(".")[0]
                text = (
                        it.group("title") + "\n" * 2 +
                        it.group("text")
                        .translate(reflectionTable)
                        .replace("<p>", "")
                        .replace("</p>", "")
                )
                print(it.group("title"), "has been finished")

            if cycling:
                text += "\n" * 3
            txt.write(text.encode("utf-8"))
            sleep(0.2333)


if __name__ == "__main__":
    bookID = input("book ID:")
    bookName = input("book name:")
    down_load_start(bookID, bookName)
