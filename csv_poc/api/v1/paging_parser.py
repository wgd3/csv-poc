"""RequestParser used for pagination purposes in the Files namespace"""
from flask_restx import reqparse

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    "per_page",
    type=int,
    help="Number of items to return per page",
    required=False,
    default=10,
    location="args",
)
pagination_parser.add_argument(
    "page",
    type=int,
    help="Which page of items to return",
    required=False,
    default=1,
    location="args",
)
pagination_parser.add_argument(
    "sort_by",
    choices=["id", "name"],
    help="Sort result list by this column",
    location="args",
)
pagination_parser.add_argument(
    "sort_order",
    choices=[
        "asc",
        "desc",
    ],
    help="Sort direction",
    location="args",
)
