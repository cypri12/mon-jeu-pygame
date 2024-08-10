import minecraft_launcher_lib
import subprocess


def launch(email, mdp):
    try:
        latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]

        minecraft_directory = "./minecraft"

        print("telechargement ...")
        minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory)

        login_data = minecraft_launcher_lib.account.login_user(email, mdp)

        options = {
            "username": login_data["selectedProfile"]["name"],
            "uuid": login_data["selectedProfile"]["id"],
            "token": login_data["accessToken"]
        }
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)

        print("lancement ...")
        subprocess.call(minecraft_command)
        return "ok"
    except KeyError :