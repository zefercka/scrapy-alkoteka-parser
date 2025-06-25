import re
from abc import ABC, abstractmethod
from datetime import datetime

from alkoteka.items import ProductItem


class Parser(ABC):
    @abstractmethod
    def parse(self, data: dict):
        pass


class ProductParser(Parser):
    @abstractmethod
    def parse(self, product: dict) -> ProductItem:
        pass


class AlkotekaProductParser(ProductParser):
    def parse(self, product: dict) -> ProductItem:
        product_catalog = product["product_catalog"]
        product = product["product"]["results"]
        return ProductItem(
            timestamp=int(datetime.now().timestamp()),
            RPC=product["uuid"],
            url=product_catalog["product_url"],
            title=self._get_title(product),
            marketing_tags=product.get("action_labels", []),
            brand=self._get_brand(product),
            section=self._get_category_path(product),
            price_data=product["price"],
            stock=self._get_stock(product),
            assets=self._get_assets(product),
            metadata=self._get_metadata(product),
            variants=1,
        )
        
    def _get_title(self, product: dict) -> str:
        add_title = [""]
        for filter_label in product.get("filter_labels", []):
            if filter_label.get("filter", None) in ["obem", "cvet"]:
                add_title.append(filter_label["title"])
            
        return f"{product['name']}{', '.join(add_title)}"
    
    def _get_brand(self, product: dict) -> str:
        blocks = product.get("description_blocks", [])
        for block in blocks:
            if block.get("code") == "brend":
                return block["values"][0]["name"]
        return ""
    
    def _get_category_path(self, product: dict) -> list[str]:
        category_obj = product.get("category", None)
        if category_obj is None:
            return []

        category_path = []
        while category_obj.get("parent", None):
            category_path.append(category_obj["name"])
            category_obj = category_obj["parent"]
        
        category_path.append(category_obj["name"])
        category_path.reverse()
        
        return category_path
    
    def _get_stock(self, product: dict) -> dict[str, bool | int]:
        in_stock = product.get("available", False)
        count = product.get("quantity_total", 0)
        
        return {
            "in_stock": in_stock,
            "stock": count
        }
    
    def _get_assets(self, product: dict) -> dict[str, str | list[str]]:
        return {
            "main_image": product["image_url"],
            "set_images": [],
            "view360": [],
            "video": []
        }
    
    def _get_metadata(self, product: dict):
        description = "\n".join(
            block["content"]
            for block in product.get("text_blocks", [])
            if block.get("title") == "Описание"
        ).strip()
        
        description = re.sub(r'\n', '', description)
        description = re.sub(r'<br\s*/?>', '. ', description)
        description = re.sub(r'<[^>]+>', '', description)
        description = re.sub(r'\s+', ' ', description)
        description = description.strip().strip(';').strip()
        
        attributes = {}
        for attribute in product.get("description_blocks", []):
            title = attribute["title"]
            unit = attribute.get("unit", "")
            if attribute["type"] == "select":
                attributes[title] = f"{attribute['values'][0]['name']}{unit}"
            elif attribute["type"] == "range":
                min_value, max_value = attribute["min"], attribute["max"] 
                attributes[title] = f"{min_value} - {max_value}" if min_value != max_value else str(min_value)
                attributes[title] += unit
        
        return {
            "__description": description,
            **attributes
        }