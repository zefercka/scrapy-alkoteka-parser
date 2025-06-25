from dataclasses import dataclass, asdict


@dataclass
class ProductItem:
    timestamp: int
    RPC: str
    url: str
    title: str
    marketing_tags: str
    brand: str
    section: list[str]
    price_data: dict[str, float | str]
    stock: dict[str, bool | int]
    assets: dict[str, str | list[str]]
    metadata: dict[str, str]
    variants: int
    
    def dict(self):
        return asdict(self)