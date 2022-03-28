def edit_lists(item_list,code_list, item_string):
    for x in range(len(item_list)):
        current_item = item_list[x]
        print(f"Currently working on item {current_item}")
        current_code = code_list[x]
        if current_code not in current_item:
            print(f"Updating current item: {current_item}.")
            item_string = item_string.replace(current_item, f"{current_item}_{current_code}")

            for y in range(len(item_list)):
                item_list[y] = item_list[y].replace(current_item, f"{current_item}_{current_code}")

    return item_string


def main():
    item_list = ["item1", "item1", "item2", "item1", "item3"]
    code_list = ["code1", "code1", "code2", "code1", "code3"]
    item_string = ", ".join(item_list)
    print(f"Initial Item String: {item_string}")
    new_item_string = edit_lists(item_list, code_list, item_string)
    print(f"New Item String: {new_item_string}")

if __name__ == "__main__":
    main()