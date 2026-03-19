import json


def build_faq_schema_json(faqs):
    if not faqs:
        return None

    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["answer"],
                    },
                }
                for item in faqs
            ],
        },
        ensure_ascii=False,
    )


def build_item_list_schema_json(name, items):
    if not items:
        return None

    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": name,
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "url": item["url"],
                        "name": item["name"],
                    }
                    for index, item in enumerate(items, start=1)
                ],
            },
        },
        ensure_ascii=False,
    )
