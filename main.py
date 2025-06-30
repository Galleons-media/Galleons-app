from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.utils import platform
from kivy.clock import Clock
import requests
import json
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

# AdMob Configuration
ADMOB_APP_ID = 'ca-app-pub-6179277409535855~6192143253'
ADMOB_BANNER_ID = 'ca-app-pub-6179277409535855/7423681486'
ADMOB_INTERSTITIAL_ID = 'ca-app-pub-6179277409535855/7423681486'

# BitLab API Configuration
BITLAB_API_KEY = '42bf26b9-1ee6-43e1-a27b-eb89a5bb8f0f'
BITLAB_API_URL = 'https://api.bitlab.com/v1/'  # Update with actual API URL

# AdGem Configuration
ADGEM_APP_ID = '30684'
ADGEM_API_URL = 'https://api.adgem.com/v1/wall'

# UPI Configuration
UPI_HANDLER_API = 'https://your-upi-handler-api.com/withdraw'  # Replace with your actual UPI handler

Builder.load_string('''
<MainScreen>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    
    BoxLayout:
        size_hint_y: None
        height: '60dp'
        Label:
            text: 'Galleons App'
            font_size: '24sp'
            bold: True
            halign: 'center'
    
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        
        Button:
            text: 'Show Banner Ad'
            size_hint_y: None
            height: '50dp'
            on_press: root.show_banner_ad()
            
        Button:
            text: 'Show Fullscreen Ad'
            size_hint_y: None
            height: '50dp'
            on_press: root.show_interstitial_ad()
            
        Button:
            text: 'Load AdGem Offers'
            size_hint_y: None
            height: '50dp'
            on_press: root.load_adgem_offers()
            
        Button:
            text: 'Call BitLab API'
            size_hint_y: None
            height: '50dp'
            on_press: root.call_bitlab_api()
            
        Button:
            text: 'Withdraw via UPI'
            size_hint_y: None
            height: '50dp'
            on_press: root.show_upi_withdrawal_popup()
    
    ScrollView:
        Label:
            id: status_label
            text: root.status_text
            size_hint_y: None
            height: self.texture_size[1]
            padding: 10, 10
            text_size: self.width, None
            halign: 'left'
            valign: 'top'

<UPIWithdrawalPopup>:
    size_hint: 0.9, 0.6
    title: 'UPI Withdrawal'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        Label:
            text: 'Enter UPI ID:'
            size_hint_y: None
            height: '30dp'
            
        TextInput:
            id: upi_id
            hint_text: 'e.g. name@upi'
            size_hint_y: None
            height: '50dp'
            
        Label:
            text: 'Enter Amount:'
            size_hint_y: None
            height: '30dp'
            
        TextInput:
            id: amount
            hint_text: 'Minimum ₹10'
            input_filter: 'int'
            size_hint_y: None
            height: '50dp'
            
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: 10
            
            Button:
                text: 'Cancel'
                on_press: root.dismiss()
                
            Button:
                text: 'Withdraw'
                on_press: root.process_withdrawal()
''')

class UPIWithdrawalPopup(Popup):
    def process_withdrawal(self):
        upi_id = self.ids.upi_id.text.strip()
        amount = self.ids.amount.text.strip()
        
        if not upi_id or '@' not in upi_id:
            self.show_message('Invalid UPI ID', 'Please enter a valid UPI ID (e.g. name@upi)')
            return
            
        if not amount or int(amount) < 10:
            self.show_message('Invalid Amount', 'Minimum withdrawal amount is ₹10')
            return
            
        # Process withdrawal
        app = App.get_running_app()
        app.root.process_upi_withdrawal(upi_id, amount)
        self.dismiss()
    
    def show_message(self, title, message):
        popup = Popup(title=title,
                     content=Label(text=message),
                     size_hint=(0.8, 0.4))
        popup.open()

class MainScreen(BoxLayout):
    status_text = StringProperty('Ready to start...')
    player_id = StringProperty('12345')  # You'll need to implement proper player ID system
    user_balance = NumericProperty(0)  # Track user's balance
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.interstitial_ad = None
        
        if platform == 'android':
            self.initialize_admob()
        
        # Initialize with some dummy balance (replace with actual balance logic)
        self.user_balance = 100
        self.update_status(f'Current balance: ₹{self.user_balance}')
    
    def show_upi_withdrawal_popup(self):
        popup = UPIWithdrawalPopup()
        popup.open()
    
    def process_upi_withdrawal(self, upi_id, amount):
        amount = int(amount)
        
        if amount > self.user_balance:
            self.update_status(f'Withdrawal failed: Insufficient balance (₹{self.user_balance})')
            return
            
        # Show processing message
        self.update_status(f'Processing UPI withdrawal of ₹{amount} to {upi_id}...')
        
        # In a real app, you would call your backend API here
        try:
            payload = {
                'upi_id': upi_id,
                'amount': amount,
                'user_id': self.player_id,
                'timestamp': str(datetime.now())
            }
            
            headers = {
                'Authorization': f'Bearer {BITLAB_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            # This is where you would call your actual UPI handler API
            # response = requests.post(UPI_HANDLER_API, json=payload, headers=headers)
            
            # Simulate API response for demonstration
            success = True  # In real app, check response.status_code == 200
            
            if success:
                self.user_balance -= amount
                self.update_status(f'Success! ₹{amount} sent to {upi_id}\nNew balance: ₹{self.user_balance}')
                
                # Show success popup
                self.show_message('Withdrawal Successful', 
                                f'₹{amount} will be credited to {upi_id} within 24 hours')
            else:
                self.update_status('Withdrawal failed: Server error')
                
        except Exception as e:
            self.update_status(f'Withdrawal error: {str(e)}')
    
    def show_message(self, title, message):
        popup = Popup(title=title,
                     content=Label(text=message),
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def update_status(self, message):
        self.status_text = message
    
    # ... [Keep all the existing AdMob, AdGem, BitLab methods from previous implementation] ...

class GalleonsApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    GalleonsApp().run()