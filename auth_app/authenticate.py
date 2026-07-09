from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extends simplejwt's JWTAuthentication to support retrieving the access 
    token from HTTP-only cookies in addition to the standard Authorization header.
    """
    def authenticate(self, request):
        """
        Authenticates the user by first attempting to retrieve the JWT from 
        the 'access_token' cookie, falling back to the 'Authorization' 
        header if the cookie is not present.

        Args:
            request (Request): The incoming Django REST framework request object.

        Returns:
            tuple: A (user, validated_token) tuple if authentication succeeds, 
                   otherwise None.
        """
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return super().authenticate(request)
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token