"""
Exercise 8: NewType, TypeAlias, Annotated, and cast
====================================================

This exercise covers tools for creating clearer, safer type definitions:

1. NewType: Create distinct types from existing ones
   - UserId and ProductId are both int, but shouldn't be mixed
   - Catches bugs at type-check time, zero runtime cost
   - The new type is a "brand" on the underlying type

2. TypeAlias: Explicitly declare type aliases
   - Makes complex types readable and reusable
   - Clearer than implicit aliases (just assignment)
   - Required for some recursive type definitions

3. Annotated: Attach metadata to types
   - Add validation hints, documentation, or constraints
   - Used by FastAPI, Pydantic, and other frameworks
   - Metadata is available at runtime via get_type_hints()

4. cast(): Tell the type checker "trust me"
   - Override type inference when you know better
   - No runtime effect - purely for the type checker
   - Use sparingly - it bypasses type safety!

Run tests with: pytest tests/test_ex08.py -v
Run type checker with: mypy exercises/ex08_newtypes_aliases_annotated.py
"""

from typing import NewType, TypeAlias, Annotated, cast, Any, get_type_hints


# =============================================================================
# PART 1: NewType - Distinct Types from Existing Ones
# =============================================================================

# NewType creates a distinct type that the type checker treats as different
# from the underlying type. At runtime, it's just the underlying type.

# TODO: Create these NewTypes:
# UserId = NewType('UserId', int)
# ProductId = NewType('ProductId', int)
# Email = NewType('Email', str)


def get_user_by_id(user_id):
    """
    Fetch a user by their ID.

    TODO: Add type hint using UserId (not int!)

    This should ONLY accept UserId, not plain int or ProductId.
    """
    return {"id": user_id, "name": f"User_{user_id}"}


def get_product_by_id(product_id):
    """
    Fetch a product by its ID.

    TODO: Add type hint using ProductId (not int!)
    """
    return {"id": product_id, "name": f"Product_{product_id}"}


def send_email(to_address, subject, body):
    """
    Send an email.

    TODO: Add type hints. to_address should be Email, not str.
    """
    return f"Sending '{subject}' to {to_address}"


def create_user_id(raw_id):
    """
    Create a UserId from a raw integer.

    This is how you "brand" a plain int as a UserId.

    TODO: Add type hints. Takes int, returns UserId.
    """
    # In real code, you might validate here
    if raw_id <= 0:
        raise ValueError("User ID must be positive")
    return raw_id  # TODO: Return UserId(raw_id)


def create_email(raw_email):
    """
    Create an Email from a raw string after validation.

    TODO: Add type hints. Takes str, returns Email.
    """
    if "@" not in raw_email:
        raise ValueError("Invalid email format")
    return raw_email  # TODO: Return Email(raw_email)


# =============================================================================
# PART 2: TypeAlias - Named Type Aliases
# =============================================================================

# TypeAlias makes it explicit that you're defining a type alias,
# not just a regular variable assignment.

# TODO: Define these type aliases:
# JsonValue: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
# Headers: TypeAlias = dict[str, str]
# Callback: TypeAlias = Callable[[str], None]

from typing import Callable


def parse_json(data):
    """
    Parse a JSON string into a JsonValue.

    TODO: Add type hints using the JsonValue alias.
    """
    import json
    return json.loads(data)


def make_request(url, headers=None):
    """
    Make an HTTP request with optional headers.

    TODO: Add type hints. headers should use the Headers alias.
    """
    if headers is None:
        headers = {}
    return {"url": url, "headers": headers, "status": 200}


def register_callback(name, callback):
    """
    Register a callback function.

    TODO: Add type hints using the Callback alias.
    """
    print(f"Registered callback '{name}'")
    return True


# Complex nested type aliases
# TODO: Define these:
# Point: TypeAlias = tuple[float, float]
# Polygon: TypeAlias = list[Point]
# LayeredPolygons: TypeAlias = dict[str, list[Polygon]]


def calculate_area(polygon):
    """
    Calculate the area of a polygon using the shoelace formula.

    TODO: Add type hint using the Polygon alias.
    """
    n = len(polygon)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i][0] * polygon[j][1]
        area -= polygon[j][0] * polygon[i][1]
    return abs(area) / 2.0


def get_layer_polygons(layers, layer_name):
    """
    Get all polygons for a specific layer.

    TODO: Add type hints using the type aliases.
    """
    return layers.get(layer_name, [])


# =============================================================================
# PART 3: Annotated - Types with Metadata
# =============================================================================

# Annotated lets you attach arbitrary metadata to types.
# The metadata can be used by frameworks (FastAPI, Pydantic, etc.)
# or your own validation code.

# TODO: Define these annotated types:
# PositiveInt = Annotated[int, "Must be > 0"]
# NonEmptyStr = Annotated[str, "Must not be empty"]
# Percentage = Annotated[float, "Must be between 0 and 100"]


def set_age(age):
    """
    Set a user's age.

    TODO: Use PositiveInt for the age parameter.
    """
    if age <= 0:
        raise ValueError("Age must be positive")
    return age


def set_username(username):
    """
    Set a user's username.

    TODO: Use NonEmptyStr for the username parameter.
    """
    if not username:
        raise ValueError("Username cannot be empty")
    return username


def set_discount(discount):
    """
    Set a discount percentage.

    TODO: Use Percentage for the discount parameter.
    """
    if not (0 <= discount <= 100):
        raise ValueError("Discount must be between 0 and 100")
    return discount


# More sophisticated Annotated usage with custom metadata classes

class MinLen:
    """Metadata indicating minimum length."""
    def __init__(self, length: int):
        self.length = length


class MaxLen:
    """Metadata indicating maximum length."""
    def __init__(self, length: int):
        self.length = length


class Pattern:
    """Metadata indicating a regex pattern."""
    def __init__(self, pattern: str):
        self.pattern = pattern


# TODO: Define these using the metadata classes above:
# Username = Annotated[str, MinLen(3), MaxLen(20)]
# PhoneNumber = Annotated[str, Pattern(r'^\+?[0-9]{10,14}$')]


def validate_field(value, field_type):
    """
    Validate a value against its Annotated metadata.

    This demonstrates how frameworks use Annotated metadata.

    TODO: Add type hints.

    Example:
        validate_field("ab", Username)  # Returns (False, "Too short")
        validate_field("validuser", Username)  # Returns (True, None)
    """
    # Get the metadata from the Annotated type
    hints = get_type_hints(lambda x: x, globalns=None, localns={"x": field_type}, include_extras=True)

    # This is a simplified validator - real frameworks do much more
    if hasattr(field_type, '__metadata__'):
        for meta in field_type.__metadata__:
            if isinstance(meta, MinLen) and len(value) < meta.length:
                return (False, f"Too short (min {meta.length})")
            if isinstance(meta, MaxLen) and len(value) > meta.length:
                return (False, f"Too long (max {meta.length})")
    return (True, None)


# =============================================================================
# PART 4: cast() - Type Assertions
# =============================================================================

# cast(Type, value) tells the type checker to treat value as Type.
# It has NO runtime effect - it's purely for type checking.
# Use it when you know more than the type checker.


def get_config_value(config, key):
    """
    Get a config value, knowing it will be a string.

    The config dict has Any values, but we know certain keys are strings.

    TODO: Add type hints and use cast() to tell mypy the return is str.

    Example:
        config = {"name": "app", "version": "1.0", "debug": True}
        name = get_config_value(config, "name")  # We know this is str
    """
    value = config[key]
    # TODO: Use cast(str, value) to tell mypy this is a string
    return value


def parse_int_safely(data, key):
    """
    Get a value from a dict and parse it as int.

    The value might be stored as string or int, but we return int.

    TODO: Add type hints and use cast() appropriately.
    """
    value = data.get(key)
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    # For any other type, try to convert
    return int(value)  # TODO: cast if needed


def find_first_string(items):
    """
    Find the first string in a list of mixed items.

    After filtering with isinstance, we know the result is str,
    but mypy might not narrow the type perfectly in all cases.

    TODO: Add type hints. Use cast() if needed to help mypy.
    """
    for item in items:
        if isinstance(item, str):
            return item
    return None


# More complex cast usage

def deserialize_user(data):
    """
    Deserialize user data from a JSON-like dict.

    We know the structure of valid user data, so we can use cast()
    to tell mypy about the types.

    TODO:
    1. Add type hints
    2. Use cast() to assert the types of extracted values

    Note: In real code, you'd use TypedDict or Pydantic for this.
    This example shows when cast() might be used.
    """
    # We "know" these fields exist and have the right types
    # (In real code, validate first!)
    user_id = data["id"]  # TODO: cast to int
    name = data["name"]  # TODO: cast to str
    email = data["email"]  # TODO: cast to str

    return {
        "id": user_id,
        "name": name,
        "email": email,
    }


# =============================================================================
# PART 5: Combining Concepts
# =============================================================================

# TODO: Create a NewType for OrderId
# OrderId = NewType('OrderId', int)

# TODO: Create type aliases for order-related types
# OrderStatus: TypeAlias = Literal["pending", "shipped", "delivered", "cancelled"]
# OrderItem: TypeAlias = dict[str, Any]  # Simplified for this exercise

from typing import Literal


class Order:
    """
    An order in an e-commerce system.

    Demonstrates combining NewType, TypeAlias, Annotated, and cast.

    TODO:
    1. Add proper type hints throughout
    2. Use the NewType and TypeAlias definitions
    3. Use Annotated for validated fields
    4. Use cast() where the type checker needs help
    """

    def __init__(self, order_id, customer_id, items):
        self.order_id = order_id  # TODO: OrderId
        self.customer_id = customer_id  # TODO: UserId
        self.items = items  # TODO: list[OrderItem]
        self.status = "pending"  # TODO: OrderStatus
        self.total = 0.0  # TODO: Annotated[float, "Total in dollars"]

    def calculate_total(self):
        """Calculate the order total from items."""
        # TODO: Add return type
        self.total = sum(
            item.get("price", 0) * item.get("quantity", 1)
            for item in self.items
        )
        return self.total

    def ship(self):
        """Mark the order as shipped."""
        # TODO: Add return type (Self or Order)
        if self.status != "pending":
            raise ValueError(f"Cannot ship order in {self.status} status")
        self.status = "shipped"
        return self

    def deliver(self):
        """Mark the order as delivered."""
        # TODO: Add return type
        if self.status != "shipped":
            raise ValueError(f"Cannot deliver order in {self.status} status")
        self.status = "delivered"
        return self

    @staticmethod
    def from_dict(data):
        """
        Create an Order from a dictionary.

        TODO:
        1. Add type hints (data: dict[str, Any]) -> Order
        2. Use cast() to extract typed values from the dict
        3. Use NewType constructors (OrderId, UserId) to brand the IDs
        """
        order_id = data["order_id"]  # TODO: cast and wrap in OrderId
        customer_id = data["customer_id"]  # TODO: cast and wrap in UserId
        items = data.get("items", [])  # TODO: cast to list[OrderItem]

        return Order(order_id, customer_id, items)


# =============================================================================
# PART 6: Challenge - Type-Safe ID System
# =============================================================================


def create_id_system():
    """
    Create a type-safe ID system using NewType.

    This challenge asks you to design NewTypes and functions
    that prevent mixing different kinds of IDs.

    TODO: Implement the following:

    1. Define NewTypes:
       - CustomerId = NewType('CustomerId', int)
       - InvoiceId = NewType('InvoiceId', int)
       - PaymentId = NewType('PaymentId', int)

    2. Implement create_customer_id(raw: int) -> CustomerId
    3. Implement create_invoice_id(raw: int) -> InvoiceId
    4. Implement create_payment_id(raw: int) -> PaymentId

    5. Implement link_payment_to_invoice(payment_id: PaymentId, invoice_id: InvoiceId) -> bool
       - This should ONLY accept PaymentId and InvoiceId, not plain ints

    6. Implement get_customer_invoices(customer_id: CustomerId) -> list[InvoiceId]
       - Returns a list of invoice IDs for a customer

    The goal: if someone tries to call link_payment_to_invoice(customer_id, invoice_id),
    mypy should report an error because CustomerId is not PaymentId.
    """
    pass  # This function is just for documentation


# TODO: Define the NewTypes here
# CustomerId = NewType('CustomerId', int)
# InvoiceId = NewType('InvoiceId', int)
# PaymentId = NewType('PaymentId', int)


def create_customer_id(raw):
    """Create a CustomerId from a raw int."""
    # TODO: Add type hints, return CustomerId(raw)
    return raw


def create_invoice_id(raw):
    """Create an InvoiceId from a raw int."""
    # TODO: Add type hints, return InvoiceId(raw)
    return raw


def create_payment_id(raw):
    """Create a PaymentId from a raw int."""
    # TODO: Add type hints, return PaymentId(raw)
    return raw


def link_payment_to_invoice(payment_id, invoice_id):
    """
    Link a payment to an invoice.

    TODO: Add type hints using the NewTypes.
    Should only accept PaymentId and InvoiceId, not plain ints.
    """
    # In real code, this would update a database
    return True


def get_customer_invoices(customer_id):
    """
    Get all invoices for a customer.

    TODO: Add type hints. Returns list[InvoiceId].
    """
    # In real code, this would query a database
    # For now, return some fake invoice IDs
    return []  # TODO: Return list of InvoiceId
