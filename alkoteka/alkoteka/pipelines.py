from alkoteka.items import ProductItem
from alkoteka.data_parsers import AlkotekaProductParser


class ProductValidatePipeline:
    def open_spider(self, spider):
        self.product_parser = AlkotekaProductParser()

    def process_item(self, item, spider):
        product = self.product_parser.parse(item)
        return product


class JsonWriterPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ProductItem):
            return item.dict()
        return item