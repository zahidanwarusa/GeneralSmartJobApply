"""
Supabase Authentication Service
Handles all authentication operations using Supabase
"""

from typing import Optional, Dict, Any
from supabase_client import get_supabase_client
from gotrue.errors import AuthApiError

class AuthService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def sign_up_with_email(self, email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sign up a new user with email and password

        Args:
            email: User's email
            password: User's password
            user_metadata: Additional user metadata (name, etc.)

        Returns:
            Dict containing user data and session
        """
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_metadata or {}
                }
            })
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "message": "Registration successful! Please check your email to verify your account."
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Registration failed. Please try again."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "An unexpected error occurred."
            }

    def sign_in_with_email(self, email: str, password: str) -> Dict[str, Any]:
        """
        Sign in a user with email and password

        Args:
            email: User's email
            password: User's password

        Returns:
            Dict containing user data and session
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "message": "Login successful!"
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Invalid email or password."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "An unexpected error occurred."
            }

    def sign_in_with_oauth(self, provider: str, redirect_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Sign in with OAuth provider (Google, GitHub, etc.)

        Args:
            provider: OAuth provider name (google, github, etc.)
            redirect_to: URL to redirect after authentication

        Returns:
            Dict containing auth URL
        """
        try:
            response = self.supabase.auth.sign_in_with_oauth({
                "provider": provider,
                "options": {
                    "redirect_to": redirect_to or "http://localhost:5000/auth/callback"
                }
            })
            return {
                "success": True,
                "url": response.url,
                "message": f"Redirecting to {provider} authentication..."
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to authenticate with {provider}."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "An unexpected error occurred."
            }

    def sign_out(self) -> Dict[str, Any]:
        """
        Sign out the current user

        Returns:
            Dict containing success status
        """
        try:
            self.supabase.auth.sign_out()
            return {
                "success": True,
                "message": "Signed out successfully."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to sign out."
            }

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Get the current authenticated user

        Returns:
            User data if authenticated, None otherwise
        """
        try:
            response = self.supabase.auth.get_user()
            return response.user if response else None
        except Exception:
            return None

    def get_session(self) -> Optional[Dict[str, Any]]:
        """
        Get the current session

        Returns:
            Session data if authenticated, None otherwise
        """
        try:
            response = self.supabase.auth.get_session()
            return response
        except Exception:
            return None

    def reset_password_for_email(self, email: str) -> Dict[str, Any]:
        """
        Send password reset email

        Args:
            email: User's email

        Returns:
            Dict containing success status
        """
        try:
            self.supabase.auth.reset_password_for_email(email, {
                "redirect_to": "http://localhost:5000/auth/reset-password"
            })
            return {
                "success": True,
                "message": "Password reset email sent. Please check your inbox."
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send password reset email."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "An unexpected error occurred."
            }

    def update_password(self, new_password: str) -> Dict[str, Any]:
        """
        Update user's password

        Args:
            new_password: New password

        Returns:
            Dict containing success status
        """
        try:
            self.supabase.auth.update_user({
                "password": new_password
            })
            return {
                "success": True,
                "message": "Password updated successfully."
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update password."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "An unexpected error occurred."
            }

    def verify_otp(self, email: str, token: str, type: str = "email") -> Dict[str, Any]:
        """
        Verify OTP token

        Args:
            email: User's email
            token: OTP token
            type: Token type (email, sms, etc.)

        Returns:
            Dict containing success status
        """
        try:
            response = self.supabase.auth.verify_otp({
                "email": email,
                "token": token,
                "type": type
            })
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "message": "Verification successful!"
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Invalid verification code."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "An unexpected error occurred."
            }

    def exchange_code_for_session(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for session (OAuth callback)

        Args:
            code: Authorization code from OAuth provider

        Returns:
            Dict containing session data
        """
        try:
            # The exchange_code_for_session expects a dictionary with 'auth_code'
            response = self.supabase.auth.exchange_code_for_session({"auth_code": code})
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "message": "Authentication successful!"
            }
        except AuthApiError as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to authenticate: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"An unexpected error occurred: {str(e)}"
            }
