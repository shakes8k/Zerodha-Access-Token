
"""
Zerodha Access Token Generator
Helps generate valid access tokens for various Algo Trading applications
and scripts.
"""

import webbrowser
import urllib.parse
from kiteconnect import KiteConnect

class ZerodhaTokenGenerator:
    def __init__(self):
        self.api_key = ""
        self.api_secret = ""
        self.kite = None
    
    def setup_credentials(self):
        print("="*60)
        print("ZERODHA ACCESS TOKEN GENERATOR")
        print("="*60)
        print()
        
        print("Step 1: Get your API credentials from https://kite.trade/")
        print("- Login to Kite")
        print("- Go to 'API' section")
        print("- Create a new app if you haven't")
        print()
        
        self.api_key = input("Enter your API Key: ").strip()
        self.api_secret = input("Enter your API Secret: ").strip()
        
        if not self.api_key or not self.api_secret:
            print("❌ Error: Both API Key and API Secret are required!")
            return False
        
        self.kite = KiteConnect(api_key=self.api_key)
        return True
    
    def generate_login_url(self):
        """Generate login URL for getting request token"""
        login_url = self.kite.login_url()
        
        print("\n" + "="*60)
        print("STEP 2: COMPLETE LOGIN FLOW")
        print("="*60)
        print()
        print("1. Opening browser automatically...")
        print("2. Complete the login process")
        print("3. After login, you'll be redirected to a URL")
        print("4. Copy the ENTIRE redirect URL and paste it below")
        print()
        print(f"Login URL: {login_url}")
        print()
        
        # Try to open browser automatically
        try:
            webbrowser.open(login_url)
            print("✅ Browser opened automatically")
        except:
            print("⚠️  Could not open browser automatically")
            print("Please copy and paste the URL above into your browser")
        
        print("\n" + "-"*60)
        
        return login_url
    
    def get_access_token(self):
        """Get access token from redirect URL"""
        print("After completing login, paste the full redirect URL here:")
        print("(It will look like: http://your-domain.com/?request_token=...&action=login&status=success)")
        print()
        
        redirect_url = input("Paste redirect URL: ").strip()
        
        if not redirect_url:
            print("❌ Error: Redirect URL is required!")
            return None
        
        try:
            # Parse the URL to extract request_token
            parsed_url = urllib.parse.urlparse(redirect_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            if 'request_token' not in query_params:
                print("❌ Error: request_token not found in URL!")
                print("Make sure you copied the complete redirect URL")
                return None
            
            request_token = query_params['request_token'][0]
            print(f"\n✅ Request token extracted: {request_token}")
            
            # Generate access token
            data = self.kite.generate_session(request_token, api_secret=self.api_secret)
            access_token = data["access_token"]
            
            print(f"\n🎉 SUCCESS! Access token generated: {access_token}")
            
            return access_token
            
        except Exception as e:
            print(f"❌ Error generating access token: {e}")
            return None
    
    def test_connection(self, access_token):
        """Test the connection with generated token"""
        try:
            self.kite.set_access_token(access_token)
            profile = self.kite.profile()
            
            print("\n" + "="*60)
            print("CONNECTION TEST")
            print("="*60)
            print(f"✅ Connection successful!")
            print(f"User: {profile['user_name']}")
            print(f"Broker: {profile['broker']}")
            print(f"Email: {profile['email']}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Connection test failed: {e}")
            return False
    
    def save_credentials(self, access_token):
        try:
            with open("zerodha_credentials.txt", "w") as f:
                f.write(f"API_KEY={self.api_key}\n")
                f.write(f"ACCESS_TOKEN={access_token}\n")
                f.write(f"# Generated on: {__import__('datetime').datetime.now()}\n")
                f.write(f"# Valid for: Current trading session only\n")
            
            print(f"\n💾 Credentials saved to: zerodha_credentials.txt")
            print("You can use these in your options tracker!")
            
        except Exception as e:
            print(f"⚠️  Could not save credentials: {e}")
    
    def run(self):
        # Main execution flow
        print("\n🚀 Starting Zerodha token generation process...\n")
        
        if not self.setup_credentials():
            return
        
        self.generate_login_url()
        
        access_token = self.get_access_token()
        if not access_token:
            return
        
        if self.test_connection(access_token):
            self.save_credentials(access_token)
            
            print("\n" + "="*60)
            print("NEXT STEPS")
            print("="*60)
            print("1. Use these credentials in your Options Tracker:")
            print(f"   API Key: {self.api_key}")
            print(f"   Access Token: {access_token}")
            print()
            print("2. Remember: Access tokens expire daily!")
            print("3. Run this script again tomorrow for fresh tokens")
            print("="*60)

def main():
    """Main function"""
    generator = ZerodhaTokenGenerator()
    
    try:
        generator.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

# Alternative: Quick credential checker
def check_existing_credentials():
    """Check if saved credentials exist and are valid"""
    try:
        with open("zerodha_credentials.txt", "r") as f:
            lines = f.readlines()
        
        api_key = None
        access_token = None
        
        for line in lines:
            if line.startswith("API_KEY="):
                api_key = line.split("=")[1].strip()
            elif line.startswith("ACCESS_TOKEN="):
                access_token = line.split("=")[1].strip()
        
        if api_key and access_token:
            print("Found saved credentials. Testing...")
            
            kite = KiteConnect(api_key=api_key)
            kite.set_access_token(access_token)
            profile = kite.profile()
            
            print(f"✅ Existing credentials are valid!")
            print(f"User: {profile['user_name']}")
            print(f"API Key: {api_key}")
            print(f"Access Token: {access_token}")
            
            return api_key, access_token
        
    except FileNotFoundError:
        print("No saved credentials found.")
    except Exception as e:
        print(f"❌ Saved credentials are invalid: {e}")
        print("Generating new tokens...")
    
    return None, None

if __name__ == "__main__":
    print("Zerodha Access Token Generator")
    print("=" * 40)
    
    api_key, access_token = check_existing_credentials()
    
    if not api_key or not access_token:
        main()
    else:
        print("\n✅ You can use the existing credentials in your Options Tracker!")

# Quick troubleshooting guide
def troubleshooting_guide():
    """Print troubleshooting steps"""
    print("""
TROUBLESHOOTING ZERODHA API CONNECTION:
=====================================

❌ Common Error: "Incorrect api_key or access_token"

🔧 Solutions:

1. ACCESS TOKEN EXPIRED:
   - Access tokens expire daily at market close
   - Generate new token each trading day
   - Run this script to get fresh token

2. WRONG API KEY:
   - Check your API key from https://kite.trade/
   - Make sure it's copied correctly (no extra spaces)
   - API key should be alphanumeric

3. WRONG API SECRET:
   - API secret is different from access token
   - Get it from your Kite app settings
   - Don't confuse with access token

4. APP NOT ACTIVATED:
   - Make sure your Kite app is active
   - Check app status in Kite developer console
   - Ensure you have proper subscriptions

5. IP RESTRICTIONS:
   - Some accounts have IP restrictions
   - Check if your IP is whitelisted
   - Contact Zerodha if needed

6. SUBSCRIPTION ISSUES:
   - Ensure you have live data subscription
   - Check if historical data is enabled
   - Verify options data access

📞 Still having issues?
   - Contact Zerodha support
   - Check their API documentation
   - Verify your account permissions
""")

# Usage instructions
"""
USAGE:
======

1. Run this script first:
   python token_generator.py

2. Follow the steps to get valid credentials

3. Use the credentials in your Options Tracker

4. If you get connection errors, run troubleshooting_guide()

DAILY WORKFLOW:
==============
- Run token generator each morning
- Get fresh access token
- Use in Options Tracker
- Tokens expire at market close
"""