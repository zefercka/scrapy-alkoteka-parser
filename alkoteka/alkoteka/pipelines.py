# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from alkoteka.data import Product
from alkoteka.data_parsers import AlkotekaProductParser
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ProductValidatePipeline:
    def open_spider(self, spider):
        self.product_parser = AlkotekaProductParser()
    
    def process_item(self, item, spider) -> Product:
        product = self.product_parser.parse(item)
        
        return product


class JsonWriterPipeline:
    def process_item(self, item: Product, spider):
        if not isinstance(item, dict):
            item = item.dict()

        return item
