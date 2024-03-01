import tkinter as tk
from tkinter import ttk
import os
import subprocess

def load_aliases():
    aliases = {}
    zshrc_path = os.path.expanduser('~/.zshrc')  # .zshrcファイルのパスを動的に取得
    try:
        with open(zshrc_path, 'r') as file:
            for line in file:
                if line.startswith('alias'):
                    key, value = line.split('=')[0][6:], line.split('=')[1].strip().strip("'")
                    aliases[key] = value
    except FileNotFoundError:
        print(f"No such file: {zshrc_path}")
    return aliases

def search_aliases(tree, query, aliases):
    """
    検索クエリに基づいてaliasを検索し、結果をツリービューに表示します。
    """
    for i in tree.get_children():
        tree.delete(i)
    for alias, command in aliases.items():
        if query.lower() in alias.lower() or query.lower() in command.lower():
            tree.insert('', tk.END, values=(alias, command))

def reset_view(tree, aliases):
    """
    ツリービューをリセットし、全てのaliasを再表示します。
    """
    for i in tree.get_children():
        tree.delete(i)
    for alias, command in aliases.items():
        tree.insert('', tk.END, values=(alias, command))

def edit_zshrc():
    """
    デフォルトのターミナルを開き、viエディタで.zshrcファイルを編集します。
    """
    zshrc_path = os.path.expanduser('~/.zshrc')
    subprocess.run(['vi', zshrc_path], check=True)

def show_aliases():
    """
    aliasを表示するためのメインウィンドウを作成し、表示します。
    """
    aliases = load_aliases()
    root = tk.Tk()
    root.title("Alias Viewer")
    root.geometry("600x600")  # ウィンドウの横幅を広げる
    root.configure(bg='#333')

    style = ttk.Style()
    style.configure('Treeview', background="#333", foreground="white", fieldbackground="#333")
    style.map('Treeview', background=[('selected', '#005f5f')])

    search_frame = tk.Frame(root, bg='#333')
    search_frame.pack(fill=tk.X, padx=10, pady=10)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    search_button = tk.Button(search_frame, text="Search", command=lambda: search_aliases(tree, search_entry.get(), aliases))
    search_button.pack(side=tk.LEFT)
    reset_button = tk.Button(search_frame, text="Reset", command=lambda: reset_view(tree, aliases))  # リセットボタンを追加
    reset_button.pack(side=tk.LEFT, padx=10)
    edit_button = tk.Button(search_frame, text="Edit .zshrc", command=edit_zshrc)  # .zshrcを編集するボタンを追加
    edit_button.pack(side=tk.RIGHT)

    # スクロールバーをメインウィンドウに追加
    scrollbar = ttk.Scrollbar(root, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(root, columns=('Alias', 'Command'), show='headings', yscrollcommand=scrollbar.set)
    tree.heading('Alias', text='Alias')
    tree.heading('Command', text='Command')
    tree.column('Alias', width=200)  # Alias列の幅を広げる
    tree.column('Command', width=400)  # Command列の幅を広げる
    tree.pack(fill=tk.BOTH, expand=True)

    for alias, command in aliases.items():
        tree.insert('', tk.END, values=(alias, command))

    # インタラクティブな検索機能を追加
    search_entry.bind('<KeyRelease>', lambda event: search_aliases(tree, search_entry.get(), aliases))

    root.mainloop()

if __name__ == "__main__":
    show_aliases()

