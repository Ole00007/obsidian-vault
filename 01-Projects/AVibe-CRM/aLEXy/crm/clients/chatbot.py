"""HTTP REST client for chatbot microservice integration.

Implements exponential backoff retry logic with graceful failure handling.
"""
import requests
import logging
import time
from typing import Dict, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class ChatbotClient:
    """HTTP REST client for chatbot microservice.
    
    Features:
    - Exponential backoff retry logic (max 3 retries)
    - Connection timeout: 5 seconds
    - Read timeout: 10 seconds
    - Graceful failure handling
    """

    def __init__(
        self,
        base_url: str = "http://localhost:5001",
        timeout: tuple = (5, 10),
        max_retries: int = 3,
        backoff_factor: float = 0.5
    ):
        """Initialize chatbot client.
        
        Args:
            base_url: Base URL for chatbot service
            timeout: (connect_timeout, read_timeout) in seconds
            max_retries: Maximum retry attempts
            backoff_factor: Exponential backoff factor
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = self._create_session(max_retries, backoff_factor)

    def _create_session(self, max_retries: int, backoff_factor: float) -> requests.Session:
        """Create requests session with retry strategy."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[500, 502, 503, 504],
            backoff_factor=backoff_factor,
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def send_message(
        self,
        user_id: int,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        case_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send message to chatbot service."""
        endpoint = f"{self.base_url}/api/messages"
        payload = {
            "user_id": user_id,
            "message": message,
            "context": context or {},
            "case_id": case_id
        }
        
        try:
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json(),
                "error": None,
                "status_code": response.status_code
            }
        
        except requests.exceptions.Timeout as e:
            logger.error(f"Chatbot timeout: {endpoint} after {self.timeout[1]}s")
            return {
                "success": False,
                "data": None,
                "error": f"Service timeout: {str(e)}",
                "status_code": 504
            }
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Chatbot connection error: {endpoint} - {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Connection failed: {str(e)}",
                "status_code": 503
            }
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"Chatbot HTTP error: {endpoint} - {response.status_code}")
            try:
                error_data = response.json()
                error_msg = error_data.get("error", str(e))
            except:
                error_msg = str(e)
            
            return {
                "success": False,
                "data": None,
                "error": error_msg,
                "status_code": response.status_code
            }
        
        except Exception as e:
            logger.exception(f"Unexpected error in send_message: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Unexpected error: {str(e)}",
                "status_code": 500
            }

    def get_conversation_history(
        self,
        user_id: int,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Fetch conversation history for a user."""
        endpoint = f"{self.base_url}/api/conversations/{user_id}"
        params = {"limit": limit}
        
        try:
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json(),
                "error": None,
                "status_code": response.status_code
            }
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching conversation history for user {user_id}")
            return {
                "success": False,
                "data": None,
                "error": "Service timeout",
                "status_code": 504
            }
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error fetching conversation: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": "Connection failed",
                "status_code": 503
            }
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching conversation: {response.status_code}")
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "status_code": response.status_code
            }
        
        except Exception as e:
            logger.exception(f"Unexpected error in get_conversation_history: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": f"Unexpected error: {str(e)}",
                "status_code": 500
            }

    def health_check(self) -> Dict[str, Any]:
        """Health check for chatbot service."""
        endpoint = f"{self.base_url}/health"
        
        try:
            response = self.session.get(
                endpoint,
                timeout=(3, 5)
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json(),
                "error": None,
                "status_code": response.status_code
            }
        
        except Exception as e:
            logger.warning(f"Chatbot health check failed: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "status_code": 503
            }

    def close(self):
        """Close the session and cleanup resources."""
        if self.session:
            self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
