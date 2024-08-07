# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
from pathlib import Path
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapydemoPipeline:
    def process_item(self, item, spider):
        # 写入文件
        # print(item)
        # 字典数据写入
        df = pd.DataFrame(item, index=[0, 1, 2])
        file_path = "../outputs/teachers.cvs"
        path = Path(file_path)
        if not path.exists() or False:
            df.to_csv(file_path, mode='a', header=True, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)
        return item
