# from dataclasses import dataclass
# from flask_sqlalchemy import sqlalchemy
# from sqlalchemy import func, Tuple

# '''
# Code to create custom SQLAlchemy type to store a lat_long type in the database

#     References:

#     - https://gist.github.com/kwatch/02b1a5a8899b67df2623
#     - https://docs.sqlalchemy.org/en/14/core/custom_types.html#sqlalchemy.types.UserDefinedType  # noqa
#     - https://stackoverflow.com/questions/37233116/point-type-in-sqlalchemy 
# '''


# @dataclass(eq=True, frozen=True, slots=True)
# class Coordinate:

# # container to hold a geolocation
#     lat: float
#     lng: float


# class LatLngType(sqlalchemy.types.UserDefinedType):
#     """
#     Custom SQLAlchemy type to handle POINT columns.
#     """

#     # Can do because we made the Coordinate dataclass hashable.
#     cache_ok = True

#     def get_col_spec(self):
#         return "POINT"

#     def bind_expression(self, bindvalue):
#         return func.POINT(bindvalue, type_=self)

#     def bind_processor(self, dialect):
#         """
#         Return function to serialize a Coordinate into a database string literal.
#         """

#         def process(value: Coordinate | Tuple[float, float] | None) -> str | None:
#             if value is None:
#                 return None

#             if isinstance(value, tuple):
#                 value = Coordinate(*value)

#             return f"({value.lat},{value.lng})"

#         return process

#     def result_processor(self, dialect, coltype):
#         """
#         Return function to parse a database string result into Python data type.
#         """

#         def process(value: str) -> Coordinate | None:
#             if value is None:
#                 return None

#             lat, lng = value.strip("()").split(",")

#             return Coordinate(float(lat), float(lng))

#         return process