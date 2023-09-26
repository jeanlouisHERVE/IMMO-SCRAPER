from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['your_script.py', '--onefile', '--name', 'your_app_name']
    run(opts)