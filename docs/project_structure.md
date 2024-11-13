qiftocsv/
├── .gitignore
├── README.md
├── requirements.txt
├── docs/
│   ├── project_overview.md
│   ├── project_checklist.md
│   └── project_structure.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── upload_screen.py
│   │   ├── conversion_screen.py
│   │   └── download_screen.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── qif_parser.py
│   │   └── csv_generator.py
│   └── utils/
│       ├── __init__.py
│       ├── error_handler.py
│       └── file_handler.py
└── tests/
    ├── __init__.py
    ├── test_qif_parser.py
    └── test_csv_generator.py 