"""
Email Notification Service
Handles email notifications for donations, requests, and alerts
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587, email=None, password=None):
        """
        Initialize email service
        For Gmail: Enable 2FA and use App Password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.enabled = email is not None and password is not None
    
    def send_email(self, to_email, subject, body, html=False):
        """
        Send email to recipient
        """
        if not self.enabled:
            print(f"Email service disabled. Would send to {to_email}: {subject}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    def send_welcome_email(self, to_email, name, role):
        """
        Send welcome email to new user
        """
        subject = "Welcome to Smart Food Donation System"
        
        body = f"""
        Dear {name},
        
        Welcome to Smart Food Donation System!
        
        Your account has been successfully created as a {role}.
        
        {"As a donor, you can now start posting food donations and make a difference in your community." if role == 'donor' else 'As an NGO, please complete your profile to start receiving donation requests.'}
        
        Together, we can reduce food waste and feed those in need.
        
        Best regards,
        Smart Food Donation Team
        """
        
        return self.send_email(to_email, subject, body)
    
    def send_donation_posted_alert(self, ngo_emails, donation_details):
        """
        Alert nearby NGOs about new donation
        """
        subject = f"New Food Donation Available: {donation_details['food_name']}"
        
        body = f"""
        A new food donation has been posted in your area!
        
        Food Item: {donation_details['food_name']}
        Quantity: {donation_details['quantity']}
        Location: {donation_details['location']}
        Best Before: {donation_details['expiry_time']}
        
        Log in to the platform to request pickup.
        
        Act fast before the food expires!
        
        Best regards,
        Smart Food Donation Team
        """
        
        success_count = 0
        for email in ngo_emails:
            if self.send_email(email, subject, body):
                success_count += 1
        
        return success_count
    
    def send_request_received_notification(self, donor_email, ngo_name, donation_name):
        """
        Notify donor about pickup request
        """
        subject = f"Pickup Request Received for {donation_name}"
        
        body = f"""
        Good news! Your donation has received a pickup request.
        
        NGO: {ngo_name}
        Donation: {donation_name}
        
        Please log in to accept or reject the request.
        
        Thank you for making a difference!
        
        Best regards,
        Smart Food Donation Team
        """
        
        return self.send_email(donor_email, subject, body)
    
    def send_request_accepted_notification(self, ngo_email, donation_details, donor_contact):
        """
        Notify NGO that their request was accepted
        """
        subject = f"Your Pickup Request Accepted: {donation_details['food_name']}"
        
        body = f"""
        Your pickup request has been accepted!
        
        Donation Details:
        - Food Item: {donation_details['food_name']}
        - Quantity: {donation_details['quantity']}
        - Location: {donation_details['location']}
        - Best Before: {donation_details['expiry_time']}
        
        Donor Contact: {donor_contact}
        
        Please coordinate with the donor for pickup.
        
        Best regards,
        Smart Food Donation Team
        """
        
        return self.send_email(ngo_email, subject, body)
    
    def send_expiry_warning(self, donor_email, donation_name, hours_left):
        """
        Warn donor about expiring donation
        """
        subject = f"⚠️ Donation Expiring Soon: {donation_name}"
        
        body = f"""
        Your donation is expiring soon!
        
        Donation: {donation_name}
        Time Left: {hours_left} hours
        
        If no NGO has claimed it yet, consider:
        1. Extending the expiry time
        2. Sharing directly with local organizations
        3. Reducing the quantity if partially consumed
        
        Log in to manage your donation.
        
        Best regards,
        Smart Food Donation Team
        """
        
        return self.send_email(donor_email, subject, body)
    
    def send_completion_notification(self, donor_email, ngo_email, donation_name):
        """
        Notify both parties about successful completion
        """
        # Email to donor
        donor_subject = f"✅ Donation Completed: {donation_name}"
        donor_body = f"""
        Great news! Your donation has been successfully collected.
        
        Donation: {donation_name}
        
        Thank you for making a difference in someone's life!
        Your contribution helps reduce food waste and feed those in need.
        
        Keep up the amazing work!
        
        Best regards,
        Smart Food Donation Team
        """
        
        # Email to NGO
        ngo_subject = f"✅ Pickup Completed: {donation_name}"
        ngo_body = f"""
        Thank you for completing the pickup!
        
        Donation: {donation_name}
        
        Your dedication helps us fight hunger and reduce food waste.
        
        Please ensure the food is distributed to those in need.
        
        Best regards,
        Smart Food Donation Team
        """
        
        self.send_email(donor_email, donor_subject, donor_body)
        self.send_email(ngo_email, ngo_subject, ngo_body)
    
    def send_ngo_verification_notification(self, ngo_email, organization_name, approved=True):
        """
        Notify NGO about verification status
        """
        if approved:
            subject = f"✅ NGO Verified: {organization_name}"
            body = f"""
            Congratulations! Your NGO has been verified.
            
            Organization: {organization_name}
            
            You can now:
            - Browse available food donations
            - Request pickups
            - Track your impact
            
            Start making a difference today!
            
            Best regards,
            Smart Food Donation Team
            """
        else:
            subject = f"NGO Verification Update: {organization_name}"
            body = f"""
            Thank you for registering with Smart Food Donation System.
            
            Your NGO verification is currently under review.
            We may contact you for additional information.
            
            You will be notified once the verification is complete.
            
            Best regards,
            Smart Food Donation Team
            """
        
        return self.send_email(ngo_email, subject, body)
    
    def send_monthly_impact_report(self, email, name, stats):
        """
        Send monthly impact report to users
        """
        subject = f"Your Monthly Impact Report - {datetime.now().strftime('%B %Y')}"
        
        body = f"""
        Dear {name},
        
        Here's your impact summary for {datetime.now().strftime('%B %Y')}:
        
        📊 Your Statistics:
        - Total Donations: {stats.get('total_donations', 0)}
        - Completed Pickups: {stats.get('completed', 0)}
        - Estimated Meals Served: {stats.get('meals_served', 0)}
        - Food Saved: {stats.get('food_saved_kg', 0)} kg
        
        🌟 Community Impact:
        - Active Donors: {stats.get('community_donors', 0)}
        - Active NGOs: {stats.get('community_ngos', 0)}
        - Total Community Meals: {stats.get('community_meals', 0)}
        
        Thank you for being part of our mission to reduce food waste!
        
        Together, we're making a difference.
        
        Best regards,
        Smart Food Donation Team
        """
        
        return self.send_email(email, subject, body)

# Example usage
if __name__ == "__main__":
    # Initialize service (credentials would come from config)
    email_service = EmailService(
        email="your_email@gmail.com",
        password="your_app_password"
    )
    
    # Test welcome email
    email_service.send_welcome_email(
        "user@example.com",
        "John Doe",
        "donor"
    )