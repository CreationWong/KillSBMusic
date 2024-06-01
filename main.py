import logging
import os
import re
import sqlite3

# 设置日志配置
logging.basicConfig(filename='./run.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='gbk', filemode='w')


def create_table_if_not_exists(conn):
    """如果表不存在，则创建表"""
    try:
        conn.execute('''drop table if exists file_paths;''')
        conn.execute('''CREATE TABLE IF NOT EXISTS file_paths
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      Path TEXT NOT NULL);''')
        logging.info("表 'file_paths' 创建成功或已存在。")
    except sqlite3.Error as e:
        logging.error(f"创建表时发生错误: {e}")


def insert_paths_to_db(conn, paths):
    """将文件路径插入数据库"""
    try:
        cursor = conn.cursor()
        for path in paths:
            cursor.execute("INSERT INTO file_paths (Path) VALUES (?)", (path,))
        conn.commit()
        logging.info("文件路径已成功插入数据库。")
    except sqlite3.Error as e:
        logging.error(f"插入路径到数据库时发生错误: {e}")


def main():
    # 连接SQLite数据库
    db_path = "kill.sqlite"  # 数据库文件路径
    conn = sqlite3.connect(db_path)

    # 创建表
    create_table_if_not_exists(conn)

    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # 指定文件后缀
    file_formats = [".mp3", ".mp4", ".wav", ".ogg", ".flac", ".mkv"]

    # 使用列表来收集含有非ASCII字符的文件完整路径
    paths_with_NotASCII = []
    pattern = re.compile(r'.*[^\x00-\xff]+.*')  # 匹配含有非ASCII字符的正则表达式

    for root, _, files in os.walk(desktop_path):
        for file_name in files:
            for file_format in file_formats:
                if file_name.endswith(file_format):
                    # 构建完整路径并检查文件名
                    full_path = os.path.join(root, file_name)
                    if pattern.match(file_name):
                        paths_with_NotASCII.append(full_path)
                        logging.info(f"找到的文件路径: {full_path}")

    # 如果找到了含有非ASCII字符的文件路径，则直接插入数据库
    if paths_with_NotASCII:
        insert_paths_to_db(conn, paths_with_NotASCII)
    else:
        logging.warning("未找到任何含有非ASCII字符的文件路径。")
        return

    conn.close()
    logging.info("数据库连接已关闭。")


if __name__ == "__main__":
    main()
