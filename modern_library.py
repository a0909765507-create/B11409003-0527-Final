import json
import os
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class Library:
    def __init__(self, file_name="books.json"):
        self.file_name = file_name
        self.books = []
        self.load_books()

    def load_books(self):
        """從 JSON 檔案載入圖書資料"""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except json.JSONDecodeError:
                print("檔案格式錯誤，無法載入圖書資料。")
            except Exception as e:
                print(f"載入圖書資料時發生錯誤: {e}")

    def save_books(self):
        """將圖書資料儲存到 JSON 檔案"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存圖書資料時發生錯誤: {e}")

    def add_book(self, title, isbn, status):
        """新增一本書到圖書館"""
        if status not in [s.value for s in BookStatus]:
            print("無效的狀態值，請使用 'available' 或 'borrowed'")
            return
        if self.is_isbn_exist(isbn):
            print("ISBN 已存在，無法新增。")
            return
        self.books.append({"title": title, "isbn": isbn, "status": status})
        print("成功新增圖書。")

    def is_isbn_exist(self, isbn):
        """檢查 ISBN 是否已存在"""
        return any(book["isbn"] == isbn for book in self.books)

    def show_books(self):
        """顯示所有圖書"""
        if not self.books:
            print("目前沒有任何圖書資料。")
            return
        for book in self.books:
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")

    def borrow_book(self, isbn):
        """借閱圖書"""
        for book in self.books:
            if book["isbn"] == isbn:
                if book["status"] == BookStatus.AVAILABLE.value:
                    book["status"] = BookStatus.BORROWED.value
                    print("成功借閱圖書。")
                else:
                    print("該圖書已被借出。")
                return
        print("找不到指定的 ISBN。")

    def return_book(self, isbn):
        """歸還圖書"""
        for book in self.books:
            if book["isbn"] == isbn:
                if book["status"] == BookStatus.BORROWED.value:
                    book["status"] = BookStatus.AVAILABLE.value
                    print("成功歸還圖書。")
                else:
                    print("該圖書未被借出。")
                return
        print("找不到指定的 ISBN。")


def main():
    library = Library()

    print("=== 圖書管理系統 v1.0 ===")
    while True:
        command = input("> ").strip()
        if command == "exit":
            library.save_books()
            print("系統關閉，資料已儲存。")
            break
        elif command.startswith("add "):
            try:
                _, data = command.split(" ", 1)
                parts = data.split("/")
                if len(parts) != 3:
                    raise ValueError("輸入格式錯誤")
                title, isbn, status = parts
                library.add_book(title.strip(), isbn.strip(), status.strip())
            except ValueError:
                print("格式錯誤！正確格式為：add 書名/ISBN/狀態")
        elif command == "show":
            library.show_books()
        elif command.startswith("borrow "):
            isbn = command[7:].strip()
            if not isbn:
                print("請輸入有效的 ISBN！")
            else:
                library.borrow_book(isbn)
        elif command.startswith("return "):
            isbn = command[7:].strip()
            if not isbn:
                print("請輸入有效的 ISBN！")
            else:
                library.return_book(isbn)
        else:
            print("未知指令，請重新輸入。")


if __name__ == "__main__":
    main()