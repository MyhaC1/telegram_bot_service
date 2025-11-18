class APIGatewayError(Exception):
    """Raised when API Gateway request fails"""
    pass


class ManagerNotFoundError(Exception):
    """Raised when manager is not found"""
    pass


class ValidationError(Exception):
    """Raised when validation fails"""
    pass
