#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 Groq API Key Setup - First Time Configuration
"""

import json
import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

class APIKeySetup:
    def __init__(self):
        self.api_key = None
        self.setup_window = None
        
    def check_api_key(self):
        """Check if valid API key exists in config.json"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    key = config.get('groq_api_key', '')
                    
                    # Check if key is valid (not placeholder)
                    if key and key != "YOUR_GROQ_API_KEY_HERE" and key.startswith('gsk_'):
                        return True
            return False
        except:
            return False
    
    def save_api_key(self, key):
        """Save API key to config.json"""
        try:
            config = {"groq_api_key": key}
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API key: {e}")
            return False
    
    def open_groq_console(self):
        """Open Groq Console in browser"""
        webbrowser.open("https://console.groq.com/")
    
    def validate_and_save(self):
        """Validate and save the API key"""
        key = self.api_key_entry.get().strip()
        
        if not key:
            messagebox.showwarning("Empty Key", "Please enter your Groq API key")
            return
        
        if not key.startswith('gsk_'):
            result = messagebox.askyesno(
                "Key Format Warning",
                "API key should start with 'gsk_'\n\nContinue anyway?",
                icon='warning'
            )
            if not result:
                return
        
        if len(key) < 20:
            messagebox.showwarning("Invalid Key", "API key seems too short. Please check and try again.")
            return
        
        # Save the key
        if self.save_api_key(key):
            self.api_key = key
            messagebox.showinfo(
                "Success! 🎉",
                "API key saved successfully!\n\nThe application will now start.",
                parent=self.setup_window
            )
            self.setup_window.destroy()
    
    def show_setup_dialog(self):
        """Show API key setup dialog"""
        ctk.set_appearance_mode("dark")
        
        self.setup_window = ctk.CTk()
        self.setup_window.title("🔑 Groq API Key Setup - First Time Configuration")
        self.setup_window.geometry("700x700")
        self.setup_window.resizable(True, True)
        
        # Make window always on top
        self.setup_window.attributes('-topmost', True)
        self.setup_window.after(100, lambda: self.setup_window.attributes('-topmost', False))
        
        # Center window
        self.setup_window.update_idletasks()
        x = (self.setup_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.setup_window.winfo_screenheight() // 2) - (700 // 2)
        self.setup_window.geometry(f"700x700+{x}+{y}")
        
        # Main scrollable container
        main_frame = ctk.CTkScrollableFrame(self.setup_window, fg_color="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🔑 Groq API Key Required",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00ffff"
        )
        title.pack(pady=(20, 10))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="First Time Setup - Get Your FREE API Key",
            font=ctk.CTkFont(size=14),
            text_color="#00ff88"
        )
        subtitle.pack(pady=(0, 20))
        
        # Instructions frame
        instructions_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=10)
        instructions_frame.pack(fill="x", padx=10, pady=10)
        
        instructions_title = ctk.CTkLabel(
            instructions_frame,
            text="📋 How to Get Your FREE Groq API Key:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffff00",
            anchor="w"
        )
        instructions_title.pack(pady=(15, 10), padx=15, anchor="w")
        
        steps = [
            "1️⃣  Click 'Open Groq Console' button below",
            "2️⃣  Create a FREE account (no credit card required)",
            "3️⃣  Log in to your account",
            "4️⃣  Find 'API Keys' section in the left sidebar",
            "5️⃣  Click 'Create API Key' button",
            "6️⃣  Copy the generated key (starts with 'gsk_')",
            "7️⃣  Paste it in the box below and click 'Save & Continue'"
        ]
        
        for step in steps:
            step_label = ctk.CTkLabel(
                instructions_frame,
                text=step,
                font=ctk.CTkFont(size=13),
                text_color="#ffffff",
                anchor="w"
            )
            step_label.pack(pady=3, padx=30, anchor="w")
        
        # Note
        note = ctk.CTkLabel(
            instructions_frame,
            text="⚠️  Note: This is a ONE-TIME setup. Your key will be saved securely.",
            font=ctk.CTkFont(size=11),
            text_color="#ff9900",
            anchor="w"
        )
        note.pack(pady=(10, 15), padx=15, anchor="w")
        
        # Open Console Button
        open_btn = ctk.CTkButton(
            main_frame,
            text="🌐 Open Groq Console (Get API Key)",
            command=self.open_groq_console,
            fg_color="#0088ff",
            text_color="#ffffff",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        open_btn.pack(pady=15, padx=10, fill="x")
        
        # API Key Input Section
        input_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="🔑 Paste Your Groq API Key Here:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ffff",
            anchor="w"
        )
        input_label.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.api_key_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="gsk_YOUR_API_KEY_HERE",
            height=45,
            font=ctk.CTkFont(size=13),
            fg_color="#0a0a0a",
            border_color="#00ff88",
            border_width=2
        )
        self.api_key_entry.pack(pady=(0, 15), padx=15, fill="x")
        
        # Bind Enter key
        self.api_key_entry.bind('<Return>', lambda e: self.validate_and_save())
        
        # Save button
        save_btn = ctk.CTkButton(
            main_frame,
            text="✅ Save & Continue to Application",
            command=self.validate_and_save,
            fg_color="#00ff88",
            text_color="#000000",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8
        )
        save_btn.pack(pady=15, padx=10, fill="x")
        
        # Footer
        footer = ctk.CTkLabel(
            main_frame,
            text="🛡️ Fake News Detection System | Created by Muzammil Abbas",
            font=ctk.CTkFont(size=10),
            text_color="#888888"
        )
        footer.pack(pady=(10, 10))
        
        # Focus on entry
        self.api_key_entry.focus()
        
        self.setup_window.mainloop()
        
        return self.api_key
    
    def run(self):
        """Main entry point - check and setup API key if needed"""
        if self.check_api_key():
            # API key already configured
            return True
        else:
            # Show setup dialog
            print("\n" + "="*60)
            print("⚠️  GROQ API KEY NOT FOUND")
            print("="*60)
            print("Opening setup dialog...")
            print()
            
            result = self.show_setup_dialog()
            
            if result:
                print("✅ API Key configured successfully!")
                return True
            else:
                print("❌ API Key setup cancelled. Application will exit.")
                return False

def main():
    """Run API key setup"""
    setup = APIKeySetup()
    return setup.run()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
