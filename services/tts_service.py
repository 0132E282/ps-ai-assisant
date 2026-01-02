import os
import pygame
from gtts import gTTS
import tempfile

class TTSManager:
    """
    Enhanced TTS Manager với điều chỉnh giọng nói tự nhiên hơn
    """
    def __init__(self, slow_mode=True, lang='vi'):
        """
        Args:
            slow_mode (bool): True = giọng nói chậm, rõ ràng hơn (khuyến nghị)
            lang (str): Ngôn ngữ ('vi', 'en', 'ja', etc.)
        """
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.slow_mode = slow_mode
            self.lang = lang
            self.temp_dir = tempfile.gettempdir()
            print(f"✓ TTS initialized: slow_mode={slow_mode}, lang={lang}")
        except Exception as e:
            print(f"Warning: Could not initialize pygame mixer: {e}")

    def speak(self, text):
        """
        Convert text to speech với giọng nói tự nhiên hơn
        """
        if not text or text.strip() == "":
            return
            
        print(f"🔊 Assistant: {text}")
        
        # Tạo file tạm với timestamp để tránh conflict
        import time
        timestamp = int(time.time() * 1000)
        output_file = os.path.join(self.temp_dir, f"tts_{timestamp}.mp3")
        
        try:
            # Cải thiện phát âm tiếng Việt
            text = self._improve_pronunciation(text)
            
            # Tạo TTS với slow mode cho chân thực hơn
            tts = gTTS(
                text=text, 
                lang=self.lang,
                slow=self.slow_mode,  # Giọng chậm, rõ ràng
                tld='com.vn'  # Vietnamese TLD for better accent
            )
            
            tts.save(output_file)
            
            if os.path.exists(output_file):
                self._play_audio(output_file)
                print("✓ TTS playback completed")
            else:
                print("✗ gTTS failed to save file.")
                
        except Exception as ge:
            print(f"✗ TTS Error: {ge}")
            # Fallback: in ra text nếu TTS thất bại
            print(f"[TEXT ONLY] {text}")

    def _improve_pronunciation(self, text):
        """
        Cải thiện phát âm tiếng Việt
        """
        # Thêm dấu ngắt câu để giọng tự nhiên hơn
        replacements = {
            ' PS-Assistant': ' Pi És - A-xi-sơ-tơn',
            'PS-Assistant': 'Pi És - A-xi-sơ-tơn',
            'AI': 'Ây Ai',
            'ChatGPT': 'Chát Giê Pê Tê',
            'LLaMA': 'La-ma',
            'Gemini': 'Giê-mi-nai',
            'robot': 'rô-bốt',
            'app': 'áp',
            'PC': 'Pê Xê',
            '...': '.',  # Bớt dấu 3 chấm
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Thêm pause ngắn sau dấu câu
        text = text.replace('. ', '... ')
        text = text.replace('! ', '! ... ')
        text = text.replace('? ', '? ... ')
        
        return text

    def _play_audio(self, file_path):
        """
        Play audio với cleanup tốt hơn
        """
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Cleanup
            pygame.mixer.music.unload()
            
            # Xóa file tạm
            try:
                os.remove(file_path)
            except:
                pass
                
        except Exception as pe:
            print(f"✗ Audio Playback Error: {pe}")
            # Cleanup on error
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass

    def set_slow_mode(self, enabled=True):
        """
        Bật/tắt slow mode
        """
        self.slow_mode = enabled
        print(f"TTS slow mode: {'ON' if enabled else 'OFF'}")

    def set_language(self, lang='vi'):
        """
        Đổi ngôn ngữ
        """
        self.lang = lang
        print(f"TTS language: {lang}")
