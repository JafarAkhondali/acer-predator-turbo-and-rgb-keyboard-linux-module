import os
from time import sleep as sleep

(
    mode_choice,
    zone_list,
    speed_choice,
    bright_choice,
    direction_choice,
    color_choice,
    final_command,
) = ([], [], [], [], [], [], [])
choice = 0


def setup():
    if not (".keyboard_cache" in [f for f in os.listdir(".") if f.startswith(".")]):
        os.system("touch .keyboard_cache")


def prep():
    global mode_choice, zone_list, speed_choice, bright_choice, direction_choice, color_choice, final_command
    command = "./facer_rgb.py "
    if mode_choice:
        command += f"-m {mode_choice[0]} "
    if speed_choice:
        command += f"-s {speed_choice[0]} "
    if bright_choice:
        command += f"-b {bright_choice[0]} "
    if direction_choice:
        command += f"-d {direction_choice[0]} "
    if color_choice:
        command += f"-cR {color_choice[0]} -cB {color_choice[1]} -cG {color_choice[2]} "
    if zone_list:
        zone = list(map(lambda x: f"-z {x} ", zone_list))
        for i in zone:
            final_command.append(command + i)
        pass
    else:
        final_command.append(command)


def speed():
    global speed_choice, choice
    try:
        choice = int(
            input(
                "Enter the Value of Speed [0-9] \n0 -> Static\n1 -> Slowest\n9 -> Fastest\nJust Press Enter to use the Default Value:"
            )
        )
    except ValueError:
        os.system("clear")
        return None
    if choice < 0 or choice > 9:
        print("Invlid Choice. Try again")
        sleep(1.5)
        os.system("clear")
        speed()
    else:
        speed_choice.append(choice)
        os.system("clear")


def bright():
    global choice, bright_choice
    try:
        choice = int(
            input(
                "Enter the Value of Brightness [0-100]\n0 -> Switched Off\n100 -> Brightest\nJust Press Enter to use the Default Value:"
            )
        )
    except ValueError:
        os.system("clear")
        return None
    if choice < 0 or choice > 100:
        print("Invlid Choice. Try again")
        sleep(1.5)
        os.system("clear")
        bright()
    else:
        bright_choice.append(choice)
        os.system("clear")


def direction():
    global direction_choice, choice
    try:
        choice = int(
            input(
                "Enter the Driection of Animation [1/2]\n1 -> Right to Left\n2 -> Left to Right\nJusr Press Enter to use the Default Vlaue:"
            )
        )
    except ValueError:
        os.system("clear")
        return None
    if choice not in [1, 2]:
        print("Invlid Choice. Try again")
        sleep(1.5)
        os.system("clear")
        direction()
    else:
        direction_choice.append(choice)
        os.system("clear")


def zone():
    global zone_list
    zones = input(
        "Enter the Zone ID(s) you want to select (1-4) seperated by space\nIf you want to select all the zones just press Enter:"
    )
    if len(zones) == 0:
        os.system("clear")
        zone_list = [1, 2, 3, 4]
        return None
    z_list = list(map(lambda x: int(x), zones.split()))
    if len(z_list) < 5 and set(z_list).issubset({1, 2, 3, 4}):
        zone_list = list(map(lambda x: int(x), zones.split()))
        os.system("clear")
    else:
        print("Invalid Selection, Choose Again")
        sleep(1.5)
        os.system("clear")
        zone()


def color():
    global color_choice
    raw = input(
        "Enter a Valid RGB code with all the channels seperated by space\nExample: 255 255 255\nJust Press Enter to use the Default Color (White):"
    )
    if len(raw) == 0:
        color_choice = [255, 255, 255]
        os.system("clear")
        return None
    inter = raw.split(" ")
    values = []
    try:
        for i in inter:
            if i == "":
                continue
            elif i != "" and (int(i) < 0 or int(i) > 255):
                print("RGB values should be between 0 - 255")
                sleep(1.5)
                os.system("clear")
                color()
            else:
                values.append(int(i))
    except ValueError:
        print("Invalid Values. Try Again!")
        sleep(1.5)
        os.system("clear")
        color()
    if len(values) != 3:
        print("There are 3 channels")
        sleep(1.5)
        os.system("clear")
        color()
    color_choice = values
    os.system("clear")


def rerun():
    # This is different than the refresh.sh and should not be considered redundant
    # If we are using the Zones Function, then the current script will run multiple commands to match
    # all the zones the user has specifies but in this case the refresh will only run the last command.
    global final_command
    with open(".keyboard_cache", "r") as file:
        data = file.read()
    final_command.append(data.split(","))
    exit()


def run():
    global final_command
    for i in final_command:
        os.system(i)
    with open(".keyboard_cache", "w") as file:
        file.write(",".join(final_command))


def mode():
    global mode_choice, choice
    print("Choose the RGB Mode")
    print("1. Static")
    print("2. Breathing")
    print("3. Neon")
    print("4. Wave")
    print("5. Shifting")
    print("6. Zoom")
    print("7. Re-Run the Last Command")
    print("0. Exit")
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            os.system("clear")
            mode_choice.append(0)
            zone()
            color()
        elif choice == 2:
            os.system("clear")
            mode_choice.append(1)
            speed()
            bright()
            color()
        elif choice == 3:
            os.system("clear")
            mode_choice.append(2)
            speed()
            bright()
        elif choice == 4:
            os.system("clear")
            mode_choice.append(3)
            speed()
            bright()
            direction()
        elif choice == 5:
            os.system("clear")
            mode_choice.append(4)
            speed()
            bright()
            color()
            direction()
        elif choice == 6:
            os.system("clear")
            mode_choice.append(5)
            speed()
            bright()
            color()
        elif choice == 7:
            os.system("clear")
            rerun()
        elif choice == 0:
            os.system("clear")
            exit()
        else:
            print("Invalid Choice")
            sleep(2)
            os.system("clear")
            mode()
    except ValueError:
        print("Invalid Values. Try Again")
        sleep(1.5)
        os.system("clear")
        mode()


def start():
    try:
        os.system("clear")
        setup()
        mode()
        prep()
        run()
    except KeyboardInterrupt:
        print("\nExiting the Program")
        exit()


if __name__ == "__main__":
    start()
