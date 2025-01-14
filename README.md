
# fastapi-odt-template

```json

{
    "convert_to_pdf": true,
    "pdf_filter_options": {
        "Watermark": "draft（下書き）",
        "SelectPdfVersion": "3"
    },
    "document_content": {
        "image": "writer.png",
        "document": {
            "datetime": "2025/01/23 12:34",
            "md_sample": "マークアップテキストです。"
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"]
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {"country": "Japan", "capital": "奈良県\u845B\uDB40\uDD02城市", "cities": ["hiroshima", "nagazaki"]},
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"]
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {"country": "Mexico", "capital": "MExico City", "cities": ["puebla", "cancun"]}
        ]
    }
}

```

```json

{
    "template_id": "simple_template.odt",
    "convert_to": "pdf",
    "filtername": "writer_pdf_Export",
    "context": {
        "document": {
            "datetime": "2025/01/23 12:34",
            "md_sample": "マークアップテキストです。"
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"]
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {"country": "Japan", "capital": "Tokio", "cities": ["hiroshima", "nagazaki"]},
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"]
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {"country": "Mexico", "capital": "MExico City", "cities": ["puebla", "cancun"]}
        ]
    }
}

```


```json

{
    "template_id": "simple_template.odt",
    "convert_to": "pdf",
    "filtername": "writer_pdf_Export",
    "filter_options": {
        "Watermark": "draft（下書き）",
        "SelectPdfVersion": "2"
    },
    "context": {
        "image": "writer.png",
        "document": {
            "datetime": "2025/01/23 12:34",
            "md_sample": "マークアップテキストです。"
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"]
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {"country": "Japan", "capital": "Tokio", "cities": ["hiroshima", "nagazaki"]},
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"]
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {"country": "Mexico", "capital": "MExico City", "cities": ["puebla", "cancun"]}
        ]
    }
}

```
