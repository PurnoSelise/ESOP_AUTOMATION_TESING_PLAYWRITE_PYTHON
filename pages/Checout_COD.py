from utils.config import CONFIG


class checkout_COD:
    def __init__(self,page):
        self.page=page
        self.shop_btn='//a[@href="/product-shop/"]'




    def checkout(self):

        self.page.click(self.shop_btn)
        self.page.wait_for_load_state('networkidle')