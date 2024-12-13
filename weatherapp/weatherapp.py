import sys
import requests
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("", self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

        self.current_color = QColor(255, 255, 255)
        self.target_color = QColor(255, 255, 255)
        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.update_background_color)

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout(self)

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
        QLabel{
            font-family: calibri;
        }
        QLabel#city_label{
            font-size:40px;
            font-style:italic;
        }        
        QLineEdit#city_input{
            font-size:40px;
        }
        QPushButton#get_weather_button{
            font-size:30px;
            font-weight:bold;
        }
        QLabel#temperature_label{
            font-size:75px;
        } 
        QLabel#emoji_label{
            font-size:150px;
            font-family: 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif;
        }
        QLabel#description_label{
            font-size:50px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "25781bfb4c308470927afbb647e4dd6b"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.RequestException as e:
            self.display_error(f"Error: {e}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temperature_k = data["main"]["temp"]
        temp_c = int(temperature_k - 273.15)
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.description_label.setText(weather_description)
        self.set_weather_picture(self.weather_emoji(weather_id))
        self.temperature_label.setText(f"{temp_c}°C")
        self.start_background_transition(self.get_weather_color(weather_id))

    def set_weather_picture(self, filename):
        try:
            pixmap = QPixmap(filename)
            scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
            self.emoji_label.setPixmap(scaled_pixmap)
        except Exception as e:
            self.display_error(f"Image load error: {e}")

    def weather_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            return "pic/voltage.png"
        if 300 <= weather_id <= 321:
            return "pic/drizzle.png"
        if 500 <= weather_id <= 531:
            return "pic/drizzle.png"
        if 600 <= weather_id <= 622:
            return "pic/snow.png"
        if 701 <= weather_id <= 781:
            return "pic/voltage.png"
        if weather_id == 800:
            return "pic/sunny.png"
        if 801 <= weather_id <= 804:
            return "pic/cloud.png"
        return ""

    def get_weather_color(self, weather_id):
        if 200 <= weather_id <= 232:  #
            return QColor(128, 0, 128)
        if 300 <= weather_id <= 531:
            return QColor(0, 0, 255)
        if 600 <= weather_id <= 622:
            return QColor(255, 255, 255)
        if 701 <= weather_id <= 781:
            return QColor(192, 192, 192)
        if weather_id == 800:
            return QColor(255, 255, 0)
        if 801 <= weather_id <= 804:
            return QColor(128, 128, 128)
        return QColor(255, 255, 255)

    def start_background_transition(self, target_color):

        self.target_color = target_color
        self.color_timer.start(50)

    def update_background_color(self):

        r = self.current_color.red() + (self.target_color.red() - self.current_color.red()) // 10
        g = self.current_color.green() + (self.target_color.green() - self.current_color.green()) // 10
        b = self.current_color.blue() + (self.target_color.blue() - self.current_color.blue()) // 10

        self.current_color = QColor(r, g, b)

        palette = self.palette()
        palette.setColor(QPalette.Window, self.current_color)
        self.setPalette(palette)

        if self.current_color == self.target_color:
            self.color_timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherApp = WeatherApp()
    weatherApp.show()
    sys.exit(app.exec_())
