

from kivy.app import App
from kivy.core.window import Window
import os
import mimetypes


mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


global image_formats
images_formats = tuple(get_extensions_for_type('image'))


class WindowFileDropExampleApp(App):
        global items
        items = []

        def build(self):
            i = Window.bind(on_dropfile=self._on_file_drop)
            print(i)
            return

        def recursive(self, path):
                result = []
                for subdir, dirs, files in os.walk(path):
                        for file in files:
                                result.append(os.path.join(subdir, file))
                return result

        def _on_file_drop(self, window, file_path):
            global items
            files = []
            file_path = bytes.decode(file_path)
            if os.path.isdir(str(file_path)):
                files.extend(self.recursive(file_path))
            items = [file for file in files if file.lower().endswith(images_formats)]
            return

if __name__ == '__main__':
        WindowFileDropExampleApp().run()

