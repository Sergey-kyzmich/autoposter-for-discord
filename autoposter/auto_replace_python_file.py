import os
import json
derictori = os.getcwd().replace("\\", "/")
print(os.getcwd().replace("\\", "/"))
root = derictori+"/baze"
list = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
print(list)
for i in list:
    print(f"replace {i}")
    for g in range(1,9):
        # data = {"id_chanal": "", "text": "", "image": "", "time": "", "next_time": 0}
        with open(f"{root}/{i}/{g}.py" ,"w") as write_file:
            with open(derictori+"/authoposter_text.txt", "r", encoding="UTF-8") as read_file:
                write_file.write(f"id = {str(i)}\nk = {str(g)+str(read_file.read())[1:].replace('п»ї', '')}")
                # print(f"id = {str(i)}\nk = {str(g)+str(read_file.read()).replace('п»ї', '')}")
        # with open(f"{root}/{i}/{g}.json", "w") as write_file:
        #     json.dump(data, write_file)
    data_name_button = {'1': 'Транспорт', '2': 'Недвижимость', '3': 'Бизнес', '4': 'Оказание Услуг',
                        '5': 'Барахолка', '6': 'Одежда', '7': 'Custom', '8': 'Черный Рынок'}
    with open(derictori+f"/baze/{str(i)}/name_button.json", "w") as write_json:
        json.dump(data_name_button, write_json)
    with open(derictori+f"/baze/{str(i)}/pay_to.txt" , "w") as write_file:
        write_file.write("2024,2,15,23,59")
    with open(f"baze/{str(i)}/main.py", "w") as f:
        with open("main_text.txt", "r") as read_file:
            f.write(f"id = {i}{str(read_file.read()).replace('п»ї', '')}")