import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL
from services.gemini_service import GeminiService

class STTManager(GeminiService):
    def __init__(self):
        super().__init__()

    def transcribe(self, audio_file_path):
        """
        Transcribe audio file to text using Gemini 2.0 Flash (Multimodal).
        """
        if not self.is_available():
            print("STT: Gemini client not available.")
            return None
            
        try:
            # New SDK way to upload/process audio
            with open(audio_file_path, "rb") as f:
                audio_data = f.read()
                
            # We can pass raw bytes to Gemini
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    "Hãy chuyển đoạn âm thanh này thành văn bản chính xác nhất. Chỉ trả về văn bản.",
                    types.Part.from_bytes(data=audio_data, mime_type="audio/wav")
                ]
            )
            return response.text.strip() if response.text else None
        except Exception as e:
            print(f"Error in Gemini STT transcribe: {e}")
            return None

    def listen_and_transcribe(self):
        """
        Nghe từ Microphone và chuyển thành văn bản.
        Ưu tiên Google Web Speech (miễn phí, ổn định) trước, sau đó mới dùng Gemini.
        """
        try:
            import speech_recognition as sr
        except ImportError:
            print("Lỗi: Chưa cài đặt thư viện 'SpeechRecognition'. Vui lòng chạy: pip install SpeechRecognition")
            return input("Bạn (nhập văn bản dự phòng): ")

        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Đang nghe... (Mời bạn nói hoặc gõ lệnh trực tiếp)")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    # If timeout, allow manual input instead of failing
                    return input("Không nghe thấy gì. Bạn muốn nhập văn bản không?: ")

                print("Đang xử lý giọng nói...")
                
                # Try Google Web Speech first (free, reliable, no quota issues)
                text = None
                try:
                    text = recognizer.recognize_google(audio, language="vi-VN")
                    print(f"✓ Google Web Speech nhận diện: {text}")
                except sr.UnknownValueError:
                    print("Google Web Speech không hiểu được âm thanh")
                except sr.RequestError as e:
                    print(f"Google Web Speech lỗi kết nối: {e}")
                except Exception as ge:
                    print(f"Google Web Speech lỗi: {ge}")
                
                # If Google fails, try Gemini as backup
                if not text:
                    print("Thử dùng Gemini STT...")
                    temp_file = "temp_record.wav"
                    try:
                        with open(temp_file, "wb") as f:
                            f.write(audio.get_wav_data())
                        
                        text = self.transcribe(temp_file)
                        if text:
                            print(f"✓ Gemini STT nhận diện: {text}")
                    except Exception as e:
                        print(f"Gemini STT lỗi: {e}")
                    finally:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)

                return text if text else input("Không nhận diện được. Bạn nhập văn bản: ")
        except Exception as e:
            if "pyaudio" in str(e).lower() or "portaudio" in str(e).lower():
                print("Lỗi Micro: Thiếu thư viện 'pyaudio' (Yêu cầu: brew install portaudio && pip install pyaudio)")
            else:
                print(f"Lỗi thu âm: {e}")
            return input("Bạn (nhập văn bản dự phòng): ")
