import re
import datetime

today = datetime.date.today()
today_format = today.strftime("%d-%m-%Y")

email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,6}$")
phone_regex = re.compile(r"^01[0-2]{1}[0-9]{8}$")

date_regex = re.compile(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-([12]\d{3})$")


def logged_in_menu(email):
    # projects: title, details, total target, start date, end date, owner:email
    while True:
        choice = input("To view current projects type: 'view'\n"
                       "To create a project type: 'create'\n"
                       "To edit a project you own type: 'edit'\n"
                       "To delete a project you own type: 'delete'\n"
                       "to logout type: 'logout'\n").strip()

        if choice.lower() == 'logout':
            print("-----------------------\n"
                  "Successfully logged out\n"
                  "-----------------------")
            return

        # create a new project
        elif choice.lower() == 'create':
            title = input("Enter the project title: ").strip()
            if not title or title.isdigit():
                print("Error: title must have an alphabetical value")
                continue

            unique_title = True
            f = open("projects.txt", "r")
            contents = f.read()
            lines = contents.splitlines()
            for line in lines:
                info_list = line.split(';')
                for i in info_list:
                    if i:
                        key, value = i.split(':')
                        if key == 'title' and value == title:
                            print("Error: can not use this title, it has been used before")
                            unique_title = False
            f.close()

            if not unique_title:
                continue

            description = input("Enter the project description: ").strip()
            if not description or description.isdigit():
                print("Error: Description must have an alphabetical value")
                continue

            total_target = input("Enter the project total target: ").strip()
            if not total_target or not total_target.isdigit():
                print("Error: Total target must be a number")
                continue

            start_date = input("Enter the start date in the format day-month-year e.g.'01-01-2000': ").strip()
            if not date_regex.match(start_date):
                print("Error: date must match DD-MM-YYYY")
                continue
            elif datetime.datetime.strptime(start_date, "%d-%m-%Y") < datetime.datetime.strptime(today_format, "%d-%m-%Y"):
                print("Error: start date must be after today: ", today_format)
                continue

            end_date = input("Enter the end date in the format day-month-year e.g.'01-01-2000': ").strip()
            if not date_regex.match(end_date):
                print("Error: date must match DD-MM-YYYY")
                continue
            elif datetime.datetime.strptime(end_date, "%d-%m-%Y") < datetime.datetime.strptime(start_date, "%d-%m-%Y"):
                print("Error: end date must be after start date: ", start_date)
                continue

            project_info = {
                'title': title,
                'description': description,
                'total target': total_target,
                'start date': start_date,
                'end date': end_date,
                'owner': email
            }

            f = open('projects.txt', 'a')
            for key, value in project_info.items():
                f.write('{}:{};'.format(key, value))
            f.write('\n')
            f.close()

        # view projects
        elif choice.lower() == 'view':
            f = open("projects.txt", "r")
            contents = f.read()
            lines = contents.splitlines()
            projects_list = []
            for line in lines:
                info_list = line.split(';')
                info_dict = {}
                for i in info_list:
                    if i:
                        key, value = i.split(':')
                        info_dict[key] = value
                projects_list.append(info_dict)
            f.close()

            for i in projects_list:
                for key, value in i.items():
                    print(f"{key} : {value}  ;  ", end='')
                print("")
            # print(projects_list)

        # edit projects owned by the user
        elif choice.lower() == "edit":

            # read all projects
            f = open("projects.txt", "r")
            contents = f.read()
            lines = contents.splitlines()
            projects_dict = {}
            for line in lines:
                info_list = line.split(';')
                info_dict = {}
                for i in info_list:
                    if i:
                        key, value = i.split(':')
                        info_dict[key] = value

                    # if info_dict['owner'] == email:
                    projects_dict[info_dict['title']] = info_dict
            f.close()

            projects_found = False
            print("Your projects is: ")
            for key, value in projects_dict.items():
                if value['owner'] == email:
                    projects_found = True
                    print(key)

            if not projects_found:
                print("No projects found for this account")
                continue

            project_name = input("Pick a project name to edit: ").strip()
            try:
                if not projects_dict[project_name]['owner'] == email:
                    print("Error: the project is not in your projects' list")
                    continue
            except:
                print("Error: project name not found")
                continue

            fields = ['title', 'details', 'total target', 'start date', 'end date']

            field = input(
                "Enter only one field to edit: 'title','Details','Total target','start date', 'end date': ").strip()

            if field.lower() in fields:
                new_value = input(f"Enter the new value for {field}: ").strip()

                if field.lower() == 'start_date' or field.lower() == 'end_date':
                    if not date_regex.match(new_value):
                        print("Error: date must match DD-MM-YYYY")
                        continue

                elif field.lower() == 'total target' and not new_value.isdigit():
                    print("Error: total target must be a number")
                    continue

                elif field.lower() == 'title' and new_value in projects_dict:
                    print("Error: can not use this title, it has been used before")
                    continue
                    pass

                projects_dict[project_name][field] = new_value
                print(projects_dict[project_name][field])

                try:
                    f = open('projects.txt', 'w')
                    for key, value in projects_dict.items():
                        for k, v in value.items():
                            f.write('{}:{};'.format(k, v))
                        f.write("\n")
                    f.close()
                except:
                    print("Error: file does not exist")
                else:
                    print("The project has been successfully updated")

            else:
                print("Error: field name not correct")
                continue

        # delete projects owned by the user
        elif choice.lower() == 'delete':
            f = open("projects.txt", "r")
            contents = f.read()
            lines = contents.splitlines()
            projects_dict = {}
            for line in lines:
                info_list = line.split(';')
                info_dict = {}
                for i in info_list:
                    if i:
                        key, value = i.split(':')
                        info_dict[key] = value

                    # if info_dict['owner'] == email:
                    projects_dict[info_dict['title']] = info_dict
            f.close()

            projects_found = False
            print("Your projects is: ")
            for key, value in projects_dict.items():
                if value['owner'] == email:
                    projects_found = True
                    print(key)

            if not projects_found:
                print("No projects found for this account")
                continue

            project_name = input("Pick a project name to delete: ").strip()
            try:
                if not projects_dict[project_name]['owner'] == email:
                    print("Error: the project is not in your projects' list")
                    continue
            except:
                print("Error: project name not found")
                continue

            prompt = input(f"Do you really want to delete project {project_name}: 'yes/no ")
            if prompt.lower() == 'yes':
                del projects_dict[project_name]
                try:
                    f = open('projects.txt', 'w')
                    for key, value in projects_dict.items():
                        for k, v in value.items():
                            f.write('{}:{};'.format(k, v))
                        f.write("\n")
                    f.close()
                except:
                    print("Error: file does not exist")
                else:
                    print("The project has been successfully deleted")


while True:
    print("Today date: \033[4m"+ today.strftime('%d %B %Y') + '\033[0m')

    # Get input from user (register, login, exit)
    c = input("To register a new account type: 'register'\n"
              "To login to your existing account type: 'login'\n"
              "To exit the application type: 'exit'\n").strip()

    # Register a new account
    if c.lower() == 'register':
        first_name = input("Please enter your first name: ").strip()
        if not first_name or first_name.isdigit():
            print("Error: first name must be alphabet and not empty")
            continue

        last_name = input("Please enter your last name: ").strip()
        if not last_name or last_name.isdigit():
            print("Error: last name must be alphabet and not empty")
            continue

        email = input("Please enter your email: ").strip()
        if not email_regex.match(email):
            print("Error: email is not valid")
            continue

        password = input("Enter your password: ").strip()
        if not password:
            print("Error: password can not be left blank")
            continue

        confirm_password = input("Re enter your password: ")
        if not confirm_password:
            print("Error: password can not be left blank")
            continue
        if not password == confirm_password:
            print("Error: passwords does not match")
            continue

        mobile_phone = input("Please enter your phone number: ").strip()
        if not phone_regex.match(mobile_phone):
            print("Error: phone number is not valid")
            continue

        info = {"first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "mobile_phone": mobile_phone
                }

        f = open('credentials.txt', 'a')
        for key, value in info.items():
            f.write('{}:{};'.format(key, value))
        f.write('\n')
        f.close()


    # Login using credentials
    elif c.lower() == 'login':
        f = open("credentials.txt", "r")
        contents = f.read()
        lines = contents.splitlines()
        credentials_list = []
        for line in lines:
            info_list = line.split(';')
            info_dict = {}
            for i in info_list:
                if i:
                    key, value = i.split(':')
                    info_dict[key] = value
            credentials_list.append(info_dict)

        f.close()

        email = input("Enter your email address: ").strip()
        password = input("Enter your password: ").strip()

        logged_in = False
        for i in credentials_list:
            if i['email'] == email and i['password'] == password:
                print("Login successfully!")
                logged_in = True
                break

        if not logged_in:
            print("Error: email or password is incorrect")
            continue

        logged_in_menu(email)

    elif c.lower() == 'exit':
        exit()

    else:
        print("Wrong choice!!")
