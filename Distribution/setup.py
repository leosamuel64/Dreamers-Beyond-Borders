from cx_Freeze import setup, Executable


target = Executable(
    script="DB2_Game.py",
	base = "Win32GUI",
    icon="logo.ico"
    )


# On appelle la fonction setup
setup(
    name = "Dreamers Beyond Borders - The Game",
    version = "1.0",
    description = "Erasmus+ project -- 2018-2021",
    executables = [target],
)