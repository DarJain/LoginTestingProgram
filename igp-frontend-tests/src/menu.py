from config import portals
from login import portal_login, instance_login
from response import info, testing, error


def menu():
    menu_options = []
    portal_options = [[]]
    instance_keys = list(portals.keys())

    try:

        # Instance selection menu options
        instance_selection = "Choose the Platform:\n\n    A. ALL\n"

        for i, instance_key in enumerate(instance_keys):
            instance_selection += f"    {i + 1}. {instance_key}\n"

        instance_selection += "    X. EXIT\n\nChoose the platform for portals testing or 'x' to exit: "

        menu_options.append(instance_selection)

        # Portal selection menu options
        for i, instance_key in enumerate(instance_keys):
            instance = portals[instance_key]
            portal_keys = list(instance.keys())
            portals_selection = f"{instance_key} portals for testing:\n\n    A. Test all {instance_key} portals\n"

            for j, portal_key in enumerate(portal_keys):
                portal = instance[portal_key]
                portal_options[0].append(portal)  # ALL portals

                if len(portal_options) <= i + 1:
                    portal_options.append([])

                portal_options[i + 1].append(portal)  # ALL Instance portals
                portals_selection += f"    {j + 1}. {portal['name']} ({portal['version']})\n"

            portals_selection += "    X. BACK\n\nInsert the number of the portal you want to test or 'x' to go back: "
            menu_options.append(portals_selection)

        while True:
            instance_choice = input(menu_options[0])
            info("---------------------------------------------------------------------")

            if instance_choice.upper() == "X":
                break

            elif instance_choice.upper() == "A":
                testing("All portals login.")
                info("---------------------------------------------------------------------")
                instance_login(portal_options[0])

            elif instance_choice.isdigit():
                instance_choice_int = int(instance_choice)

                if 0 < instance_choice_int < len(menu_options):

                    while True:
                        portal_choice = input(menu_options[instance_choice_int])
                        info("---------------------------------------------------------------------")

                        if portal_choice.upper() == "X":
                            break

                        elif portal_choice.upper() == "A":
                            testing(f"All {instance_keys[instance_choice_int - 1]} portals login.")
                            info("---------------------------------------------------------------------")
                            instance_login(portal_options[instance_choice_int])

                        elif portal_choice.isdigit():
                            portal_choice_int = int(portal_choice)

                            if 0 < portal_choice_int <= len(portal_options[instance_choice_int]):
                                portal_login(portal_options[instance_choice_int][portal_choice_int - 1])

                            else:
                                info(f"Invalid input '{portal_choice}'! Try one of the options listed below.")

                        else:
                            info(f"Invalid input '{portal_choice}'! Try one of the options listed below.")

                else:
                    info(f"Invalid input '{instance_choice}'! Try one of the options listed below.")

            else:
                info(f"Invalid input '{instance_choice}'! Try one of the options listed below.")

    except KeyError as e:
        error(f"Invalid configuration for {e}. Check config details and restart to try again.")
