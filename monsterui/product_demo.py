from fasthtml.common import *
from monsterui.all import *

# Get frankenui and tailwind headers via CDN using Theme.blue.headers()
hdrs = Theme.blue.headers()

# fast_app is shadowed by MonsterUI to make it default to no Pico, and add body classes
# needed for frankenui theme styling
app, rt = fast_app(hdrs=hdrs)

# Example Product Data to render in the gallery and detail pages
products = [
    {"name": "Laptop", "price": "$999", "img": "https://picsum.photos/400/100?random=1"},
    {"name": "Smartphone", "price": "$599", "img": "https://picsum.photos/400/100?random=2"},
    {"name": "Headphones", "price": "$199", "img": "https://picsum.photos/400/100?random=3"},
    {"name": "Smartwatch", "price": "$299", "img": "https://picsum.photos/400/100?random=4"},
    {"name": "Tablet", "price": "$449", "img": "https://picsum.photos/400/100?random=5"},
    {"name": "Camera", "price": "$799", "img": "https://picsum.photos/400/100?random=6"},
]

def ProductCard(p):
    # Card does lots of boilerplate classes so you can just pass in the content
    return Card(
        # width:100% makes the image take the full width
        Img(src=p["img"], alt=p["name"], style="width:100%"),
        # All components can take a cls argument to add additional styling
        H4(p["name"], cls="mt-2"),
        # bold_sm is helpful for things that you want to look like regular text, but stand out
        P(p["price"], cls=TextPresets.bold_sm),
        # ButtonT.primary for primary actions
        Button("View Details", cls=(ButtonT.primary, "mt-2"),
               hx_get=product_detail.to(product_name=p['name']),
               hx_push_url='true',
               hx_target='body')
    )

@rt
def index():
    # Titled using a H1 title, sets the page title, and wraps contents in Main(Container(...))
    return Titled("MonsterUI Store Front!",
        Grid(*[ProductCard(p) for p in products], cols_lg=3))

example_product_description = """
This is a sample detailed description of the {product_name}. You can see when clicking on the card
from the gallery you can:

+ Have a detailed description of the product on the page
+ Have an order form to fill out and submit
+ Anything else you want!
"""

@rt
def product_detail(product_name: str):
    return Titled("Product Detail",
        Grid(
            Div(
                H1(product_name),
                # render_md is a helper that renders markdown into HTML using frankenui styles
                render_md(example_product_description.format(product_name=product_name))
            ),
            Div(
                H3("Order Form"),
                # Form automatically has a class of 'space-y-3' for a margin between each child
                Form(
                    # LabelInput is a convenience wrapper for a label and input that links them
                    LabelInput("Name", id='name'),
                    LabelInput("Email", id='email'),
                    LabelInput("Quantity", id='quantity'),
                    # ButtonT.primary because this is the primary action of the page
                    Button("Submit", cls=ButtonT.primary)
                )
            ),
            # Grid has defaults and args for cols at different breakpoints
            cols_lg=2
        )
    )

if __name__ == '__main__':
    serve()
