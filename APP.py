import webbrowser
import boto3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation


class WelcomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[50, 100])
        self.add_widget(layout)

        # Load and display the image
        image_path = "C:\\Users\\moham\\Desktop\\WhatsApp Image 2024-02-13 at 3.00.32 PM.jpeg"
        welcome_image = KivyImage(source=image_path, size_hint=(1, 0.5))
        layout.add_widget(welcome_image)

        # Label for welcome message
        welcome_label = Label(text='Welcome to CitySight', size_hint=(1, None), height=100, font_size='20sp', halign='center')
        layout.add_widget(welcome_label)

        # Additional text
        additional_text = (
            "Discover Saudi Arabia's landmarks effortlessly with our app.\n"
            "Just point your camera and uncover the stories behind each site\n"
            "From ancient ruins to modern marvels, explore the wonders of Saudi\n"
            "Arabia with us Start exploring....."
        )
        additional_label = Label(text=additional_text, size_hint=(1, None), height=200, font_size='16sp', halign='center')
        layout.add_widget(additional_label)

        # Button to navigate to the main page
        start_button = Button(text='Start', size_hint_y=None, height=50)
        start_button.bind(on_press=self.switch_to_main_page)
        layout.add_widget(start_button)

    def switch_to_main_page(self, instance):
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=lambda *args: self.change_screen('main_page'))
        anim.start(self)

    def change_screen(self, screen_name):
        self.manager.current = screen_name


class MainPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[50])
        self.add_widget(layout)

        # Add a back button to the top left
        back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.switch_to_welcome_page)
        layout.add_widget(back_button)

        # Label for title
        title_label = Label(text='Discover unknown landmarks', size_hint_y=0.1, font_size='30sp', halign='center')
        layout.add_widget(title_label)

        # Image display widget
        self.image_display = KivyImage(size_hint_y=0.3)
        layout.add_widget(self.image_display)

        # BoxLayout to hold upload button and analyze button
        button_layout = BoxLayout(size_hint_y=0.1)
        layout.add_widget(button_layout)

        # Button for uploading image
        upload_button = Button(text='Upload Image')
        upload_button.bind(on_press=self.upload_image)
        button_layout.add_widget(upload_button)

        # Button to analyze and call detected labels
        analyze_button = Button(text='Analyze')
        analyze_button.bind(on_press=self.analyze_image)
        button_layout.add_widget(analyze_button)

        # ScrollView for displaying detected labels
        self.scroll_view = ScrollView(size_hint=(1, 0.4))
        layout.add_widget(self.scroll_view)

        # Layout for detected labels
        self.label_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=[10], spacing=10)
        self.scroll_view.add_widget(self.label_layout)

    def switch_to_welcome_page(self, instance):
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=lambda *args: self.change_screen('welcome_page'))
        anim.start(self)

    def upload_image(self, instance):
        # Open file browser for selecting an image
        from tkinter import Tk, filedialog
        Tk().withdraw()  # Hide the main window
        filename = filedialog.askopenfilename()  # Show the file dialog

        # Display selected image
        self.image_display.source = filename
        self.image_display.reload()

    def analyze_image(self, instance):
        if self.image_display.source:
            # Analyze the image and update label output
            labels = self.detect_labels(self.image_display.source)
            self.update_label_output(labels)
        else:
            # Display an error message if no image is uploaded
            self.label_layout.clear_widgets()
            error_label = Label(text="Please upload an image first.", size_hint=(1, None), height=50)
            self.label_layout.add_widget(error_label)

    def detect_labels(self, filename):
        # Read image file
        with open(filename, 'rb') as image_file:
            image_bytes = image_file.read()

        # Call DetectCustomLabels
        response = self.show_custom_labels(image_bytes)

        # Process response
        labels = [label['Name'] for label in response['CustomLabels']]
        return labels

    def show_custom_labels(self, image_bytes):
        # Replace these values with your own
        model = 'arn:aws:rekognition:us-east-1:905418420890:project/Tuwaiq_LandMarks_KSA/version/Tuwaiq_LandMarks_KSA.2024-02-10T17.08.49/1707574130097'
        min_confidence = 90
        client = boto3.client('rekognition')

        # Call DetectCustomLabels
        response = client.detect_custom_labels(
            Image={'Bytes': image_bytes},
            MinConfidence=min_confidence,
            ProjectVersionArn=model
        )

        return response

    def update_label_output(self, labels):
        self.label_layout.clear_widgets()  # Clear previous labels

        for label in labels:
            label_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

            # Label for the detected label
            label_label = Label(text=label, size_hint_x=0.8)
            label_box.add_widget(label_label)

            # Button to learn more about the label
            learn_more_button = Button(text='Learn More', size_hint_x=0.2, on_press=lambda x: self.more_info(label))
            label_box.add_widget(learn_more_button)

            self.label_layout.add_widget(label_box)

    def more_info(self, label_name):
        query = label_name.replace(' ', '+')
        url = f'https://www.google.com/search?q={query}'
        webbrowser.open(url)


class CustomLabelApp(App):
    def build(self):
        # Create ScreenManager
        self.screen_manager = ScreenManager()

        # Create screens
        welcome_page = WelcomePage(name='welcome_page')
        main_page = MainPage(name='main_page')

        # Add screens to ScreenManager
        self.screen_manager.add_widget(welcome_page)
        self.screen_manager.add_widget(main_page)

        return self.screen_manager


if __name__ == '__main__':
    CustomLabelApp().run()
