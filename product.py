class Product:
    def __init__(self, article_nr, name, price, image_url, url):
        self.article_nr = article_nr
        self.name = name
        self.price = price
        self.image_url = image_url
        self.url = url

    def __str__(self):
        return "[article-number: {}, name: {}]".format(
            self.article_nr, self.name)