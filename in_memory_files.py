import io

class InMemoryFile:
    """Creates file in memory buffer as object with filename and file content."""
    def __init__(self, filename, content):
        self.filename = filename
        self.content = io.BytesIO(content) if content else io.BytesIO()
    
    def read(self):
        self.content.seek(0)
        return self.content.read()

    def write(self, data=None):
        if data is None:
            self.content.seek(0)
            data = self.content.read()
        self.content.seek(0)
        self.content.write(data)
        self.content.truncate()

    def buffer(self):
        self.content.seek(0)
        return self.content

class InMemoryFolder:
    def __init__(self):
        self.files = {}

    def add_file(self, filename, content):
        self.files[filename] = InMemoryFile(filename, content)

    def open(self, filename):
        if filename in self.ls():
            return self.files.get(filename)
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{filename}'")

    def ls(self):
        return sorted(self.files)

# Creation folder and files in memory
folder = InMemoryFolder()
folder.add_file(filename='test_file_1.txt', content=b'Some Binary content of file 1.')
folder.add_file(filename='test_file_2.txt', content=b'Some Binary content of another file 2.')

# List files in the folder
print(f"Files in folder: {folder.ls()}")

# Read content of the first file: 'test_file_1.txt'
file_1 = folder.open('test_file_1.txt')
if file_1:
    print(f"Content of '{file_1.filename}': {file_1.read().decode('utf-8')}")

# Ovwerwrite content for second file: 'test_file_2.txt'
file_2 = folder.open('test_file_2.txt')
if file_2:
    file_2.write(b'Updated Binary content of file 2....')
    print(f"New content of '{file_2.filename}': {file_2.read().decode('utf-8')}")


# Override the content with a new DataFrame
import pandas as pd

df = pd.DataFrame({
    'Column1': [4, 5, 6],
    'Column2': ['D', 'E', 'F']
})

# Saving DataFrame to memory buffer
df.to_excel(file_2.buffer(), index=False)

new_df = pd.read_excel(file_2.content)
print(f"new_df: {new_df}")
    
# Reading missing file from filesystem - checking Exception
# a = open('test_file_3.txt')

# Reading missing file from buffer - checking Exception
file_3 = folder.open('test_file_3.txt')
