import os
import sqlite3
import logging

# 配置日志
logging.basicConfig(filename='file_delete.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='gbk',filemode='w')

# 数据库文件路径.
db_path = 'kill.sqlite'
# 数据库中的表名和查询字段.
table_name = 'file_paths'
field_name = 'Path'

# 获取用户的桌面路径
base_directory = os.path.join(os.path.expanduser("~"), 'Desktop')

try:
    # 连接数据库
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # 查询数据库获取所有文件路径
        cursor.execute(f"SELECT {field_name} FROM {table_name};")
        file_paths_to_delete = cursor.fetchall()

        # 遍历文件路径，尝试删除对应的文件
        for file_path_tuple in file_paths_to_delete:
            file_path = os.path.join(base_directory, file_path_tuple[0])  # 假设查询结果是元组

            # 确保路径是绝对的且存在，然后执行删除
            absolute_path = os.path.abspath(file_path)
            if os.path.exists(absolute_path) and os.path.isfile(absolute_path):
                try:
                    os.remove(absolute_path)
                    logging.info(f"【已删除】: {absolute_path}")
                except Exception as delete_error:
                    logging.error(f"删除文件时出错: {absolute_path}", exc_info=True)
                    print(f"删除文件时出错: {absolute_path}")
            else:
                logging.info(f"文件未找到或不是文件类型: {absolute_path}")

    logging.info("文件删除过程已完成。")

except Exception as e:
    logging.error("执行过程中发生错误:", exc_info=True)