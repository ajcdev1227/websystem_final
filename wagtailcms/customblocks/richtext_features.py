RICHTEXT_BLOCKYPES = ["h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol"]
RICHTEXT_INLINESTYLES = [
    "bold",
    "italic",
    "strikethrough",
    "superscript",
    "subscript",
    "blockquote",
]
RICHTEXT_ENTITIES = ["image", "embed", "link", "document-link"]
RICHTEXT_MISC = ["hr", "code"]
CUSTOM_FEATURES = ["primary-color", "secondary-color", "tertiary-color"]

ALL_RICHTEXT_FEATURES = (
    RICHTEXT_BLOCKYPES
    + RICHTEXT_INLINESTYLES
    + RICHTEXT_ENTITIES
    + RICHTEXT_MISC
    + CUSTOM_FEATURES
)
