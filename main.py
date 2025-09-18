import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import io
import random
import pygame


class WildWestPosterGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Wild West Poster Generator")
        self.root.geometry("800x600")
        self.root.configure(bg='#3A160E')
        
        #Vars
        self.name_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.template_var = tk.StringVar(value="wanted")
        self.random_var = tk.BooleanVar(value=False)
        self.uploaded_image_path = None
        self.generated_poster = None

        pygame.init()
        pygame.mixer.init()
        sound_effect = pygame.mixer.Sound(r"C:\Users\lanel\Documents\GitHub\hsd-pilot-night-2025-lane-and-simeon\wildWest.mp3")
        sound_effect.set_volume(0.5)
        sound_effect.play()
        
        self.setup_gui()
    
    def setup_gui(self):
        # Method to setup the GUI components
        # Formating + styling

        main_frame = tk.Frame(self.root, bg='#3A160E', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="🤠 WILD WEST POSTER GENERATOR 🤠", 
                              font=("Courier New", 20, "bold"), 
                              fg='#C3976A', bg='#3A160E')
        title_label.pack(pady=(0, 20))
        
        # Input fields
        input_frame = tk.Frame(main_frame, bg='#3A160E')
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Name input
        tk.Label(input_frame, text="Name:", font=("Courier New", 12, "bold"), 
                fg='#C3976A', bg='#3A160E').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(input_frame, textvariable=self.name_var, 
                             font=("Courier New", 12), width=30)
        name_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Location input
        tk.Label(input_frame, text="Location:", font=("Courier New", 12, "bold"), 
                fg='#C3976A', bg='#3A160E').grid(row=1, column=0, sticky='w', pady=5)
        location_entry = tk.Entry(input_frame, textvariable=self.location_var, 
                                 font=("Courier New", 12), width=30)
        location_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Template selection
        tk.Label(input_frame, text="Template:", font=("Courier New", 12, "bold"), 
                fg='#C3976A', bg='#3A160E').grid(row=2, column=0, sticky='w', pady=5)
        # Make the template combobox an instance attribute so we can enable/disable it
        self.template_combo = ttk.Combobox(input_frame, textvariable=self.template_var, 
                                     values=["wanted", "sheriff", "bounty"], 
                                     state="readonly", font=("Courier New", 12))
        self.template_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')

        # Random toggle (checkbox) - when enabled, template selection is randomized on generate
        random_check = tk.Checkbutton(input_frame, text="Random Template", 
                                      variable=self.random_var, onvalue=True, offvalue=False,
                                      command=self.toggle_random,
                                      font=("Courier New", 10, "bold"),
                                      fg='#C3976A', bg='#3A160E', selectcolor='#3A160E')
        random_check.grid(row=2, column=2, padx=(10, 0), pady=5, sticky='w')
        
        # Image upload section
        image_frame = tk.Frame(main_frame, bg='#3A160E')
        image_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(image_frame, text="Photo:", font=("Courier New", 12, "bold"), 
                fg='#C3976A', bg='#3A160E').pack(side=tk.LEFT)
        
        upload_btn = tk.Button(image_frame, text="Upload Photo", 
                              command=self.upload_image, 
                              font=("Courier New", 10, "bold"),
                              bg='#AC714A', fg='#3A160E',
                              relief=tk.RAISED, borderwidth=2)
        upload_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        self.image_label = tk.Label(image_frame, text="No image selected", 
                                   font=("Courier New", 10), 
                                   fg='#C3976A', bg='#3A160E')
        self.image_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Generate button
        generate_btn = tk.Button(main_frame, text="🎯 GENERATE POSTER 🎯", 
                               command=self.generate_poster,
                               font=("Courier New", 16, "bold"),
                               bg='#C3976A', fg='#3A160E',
                               relief=tk.RAISED, borderwidth=3,
                               padx=20, pady=10)
        generate_btn.pack(pady=20)
        
        # Preview section
        self.preview_frame = tk.Frame(main_frame, bg='#3A160E')
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_label = tk.Label(self.preview_frame, 
                                     text="Generated poster will appear here", 
                                     font=("Courier New", 12), 
                                     fg='#C3976A', bg='#3A160E')
        self.preview_label.pack(expand=True)
        
        # Save button (initially hidden)
        self.save_btn = tk.Button(main_frame, text="💾 SAVE POSTER", 
                                 command=self.save_poster,
                                 font=("Courier New", 12, "bold"),
                                 bg='#CD853F', fg='#3A160E',
                                 relief=tk.RAISED, borderwidth=2)
    
    def upload_image(self):
        #Method to handle image upload

        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            self.uploaded_image_path = file_path
            filename = os.path.basename(file_path)
            self.image_label.config(text=f"Selected: {filename}")
    
    def toggle_random(self):
        """Enable or disable the template combobox depending on the random toggle."""
        if self.random_var.get():
            # disable combobox when random is on
            try:
                self.template_combo.configure(state='disabled')
            except Exception:
                pass
        else:
            try:
                self.template_combo.configure(state='readonly')
            except Exception:
                pass
    
    def create_sepia_filter(self, image):
        # Apply sepia filter to the image

        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create sepia effect
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                
                # Sepia formula
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                
                # Clamp values
                pixels[i, j] = (min(255, tr), min(255, tg), min(255, tb))
        
        return image
    
    def generate_poster(self):
        # Method to generate the poster based on inputs

        name = self.name_var.get().strip()
        location = self.location_var.get().strip()
        # If random toggle is active, pick a random template and set template_var so user can see it
        if self.random_var.get():
            values = list(self.template_combo['values']) if hasattr(self, 'template_combo') else ["wanted", "sheriff", "bounty"]
            template = random.choice(values)
            # reflect chosen template in the UI
            self.template_var.set(template)
        else:
            template = self.template_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a name!")
            return
        
        if not location:
            messagebox.showerror("Error", "Please enter a location!")
            return
        
        if not self.uploaded_image_path:
            messagebox.showerror("Error", "Please upload a photo!")
            return
        
        try:
            # Create poster
            poster = self.create_poster(name, location, template, self.uploaded_image_path)
            self.generated_poster = poster
            
            # Display preview
            self.display_preview(poster)
            
            # Show save button
            self.save_btn.pack(pady=(10, 0))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate poster: {str(e)}")
    
    def create_poster(self, name, location, template, image_path):
        # Method to create the poster image

        # Load and process the uploaded image
        try:
            user_image = Image.open(image_path)
        except Exception as e:
            raise Exception(f"Could not load image: {str(e)}")
        
        # Create poster canvas
        poster_width, poster_height = 600, 800
        poster = Image.new('RGB', (poster_width, poster_height), '#F5E6D3')  # Parchment color
        draw = ImageDraw.Draw(poster)
        
        # Template-specific styling
        if template == "wanted":
            title_text = "WANTED"
            subtitle_text = "DEAD OR ALIVE"
            reward_text = "$5000 REWARD"
            border_color = '#8B0000' 
        elif template == "sheriff":
            title_text = "SHERIFF"
            subtitle_text = "BADGE OF HONOR"
            reward_text = f"PROTECTOR OF {location.upper()}"
            border_color = '#DAA520'
        else:
            title_text = "BOUNTY HUNTER"
            subtitle_text = "FOR HIRE"
            reward_text = "JUSTICE SERVED"
            border_color = '#2F4F4F'
        
        # Draw border
        border_width = 20
        for i in range(border_width):
            draw.rectangle([i, i, poster_width-1-i, poster_height-1-i], 
                          outline=border_color, width=2)
        
        # Draw corner stars
        star_size = 30
        corners = [(50, 50), (poster_width-50, 50), (50, poster_height-50), (poster_width-50, poster_height-50)]
        for x, y in corners:
            self.draw_star(draw, x, y, star_size, border_color)
        
        # Try to use a bold font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
            name_font = ImageFont.truetype("arial.ttf", 36)
            text_font = ImageFont.truetype("arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Draw title
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (poster_width - title_width) // 2
        draw.text((title_x, 80), title_text, fill='#8B0000', font=title_font)
        
        # Draw subtitle
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (poster_width - subtitle_width) // 2
        draw.text((subtitle_x, 140), subtitle_text, fill='#3A160E', font=subtitle_font)
        
        # Process and place user image
        # Resize image to fit in poster
        img_width, img_height = 300, 300
        user_image = user_image.resize((img_width, img_height), Image.Resampling.LANCZOS)
        
        # Apply sepia filter 
        user_image = self.create_sepia_filter(user_image)
        
        # Add slight blur
        user_image = user_image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Paste image onto poster
        img_x = (poster_width - img_width) // 2
        img_y = 200
        poster.paste(user_image, (img_x, img_y))
        
        # Draw frame around image
        frame_padding = 10
        draw.rectangle([img_x-frame_padding, img_y-frame_padding, 
                       img_x+img_width+frame_padding, img_y+img_height+frame_padding], 
                      outline=border_color, width=3)
        
        # Draw name
        name_bbox = draw.textbbox((0, 0), name.upper(), font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (poster_width - name_width) // 2
        draw.text((name_x, 530), name.upper(), fill='#8B0000', font=name_font)
        
        # Draw location
        location_text = f"LAST SEEN IN {location.upper()}"
        location_bbox = draw.textbbox((0, 0), location_text, font=text_font)
        location_width = location_bbox[2] - location_bbox[0]
        location_x = (poster_width - location_width) // 2
        draw.text((location_x, 580), location_text, fill='#3A160E', font=text_font)
        
        # Draw reward text
        reward_bbox = draw.textbbox((0, 0), reward_text, font=subtitle_font)
        reward_width = reward_bbox[2] - reward_bbox[0]
        reward_x = (poster_width - reward_width) // 2
        draw.text((reward_x, 630), reward_text, fill='#8B0000', font=subtitle_font)
        
        # Draw footer text
        footer_text = "PAID FOR BY YOUR LOCAL SHERIFF"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=text_font)
        footer_width = footer_bbox[2] - footer_bbox[0]
        footer_x = (poster_width - footer_width) // 2
        draw.text((footer_x, 700), footer_text, fill='#3A160E', font=text_font)
        
        # Add aging effects
        poster = self.add_aging_effects(poster)
        
        return poster
    
    def draw_star(self, draw, cx, cy, size, color):
        import math
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.4
            x = cx + radius * math.cos(angle - math.pi/2)
            y = cy + radius * math.sin(angle - math.pi/2)
            points.extend([x, y])
        draw.polygon(points, fill=color)
    
    def add_aging_effects(self, image):
        # Slightly reduce contrast and brightness
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.9)
        
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.95)
        
        return image
    
    def display_preview(self, poster):
        # Clear previous preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        # Resize for display
        display_size = (300, 400)
        display_poster = poster.resize(display_size, Image.Resampling.LANCZOS)
        
        # Convert PIL image to PhotoImage
        bio = io.BytesIO()
        display_poster.save(bio, format='PNG')
        bio.seek(0)
        
        # Display 
        self.poster_photo = tk.PhotoImage(data=bio.read())
        preview_label = tk.Label(self.preview_frame, image=self.poster_photo, bg='#3A160E')
        preview_label.pack(expand=True)
        
        # Add success message
        success_label = tk.Label(self.preview_frame, 
                               text="🎉 Poster generated successfully! 🎉", 
                               font=("Courier New", 12, "bold"), 
                               fg='#C3976A', bg='#3A160E')
        success_label.pack(pady=(10, 0))
    
    def save_poster(self):
        if self.generated_poster:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
                title="Save Poster As"
            )
            if file_path:
                try:
                    self.generated_poster.save(file_path)
                    messagebox.showinfo("Success", f"Poster saved as {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save poster: {str(e)}")

def main():
    root = tk.Tk()
    app = WildWestPosterGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()