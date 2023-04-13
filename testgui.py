import PySimpleGUI as sg
import os.path
import json

# Define the theme
sg.theme('DarkGrey14')
fontarial = ('Arial', 12)
edit = False


def edit_cell(window, key, row, col, justify='left'):
    global textvariable, edit

    def callback(event, row, col, text, key):
        global edit
        widget = event.widget
        if key == 'Return':
            text = widget.get()
            print(text)
        widget.destroy()
        widget.master.destroy()
        values = list(table.item(row, 'values'))
        values[col] = text
        table.item(row, values=values)
        edit = False

    if edit or row <= 0:
        return

    edit = True
    root = window.TKroot
    table = window[key].Widget

    text = table.item(row, "values")[col]
    x, y, width, height = table.bbox(row, col)

    frame = sg.tk.Frame(root)
    # set anchor point to top-left corner of cell
    anchor_x, anchor_y = table.winfo_x() + x + 5, table.winfo_rooty() + row * height - 115
    print("table.winfo_y():", table.winfo_y())
    print("table.bbox(row, col) y value:", y)
    print("table.winfo_rooty():", table.winfo_rooty())

    frame.place(x=anchor_x, y=anchor_y, anchor="nw", width=width, height=height)
    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    entry.pack()
    entry.select_range(0, sg.tk.END)
    entry.icursor(sg.tk.END)
    entry.focus_force()
    entry.bind("<Return>", lambda e, r=row, c=col, t=text, k='Return': callback(e, r, c, t, k))
    entry.bind("<Escape>", lambda e, r=row, c=col, t=text, k='Escape': callback(e, r, c, t, k))
    entry.bind("<FocusOut>", lambda e, r=row, c=col, t=text, k='Escape': callback(e, r, c, t, k))


# Define the layout
# noinspection DuplicatedCode
layout = [[sg.Text('Welcome to the PartyPlaner', font=('Arial', 20), justification='center', size=(30, 2))],
          [sg.FileBrowse('Select File', font=fontarial),
           sg.Text('No file selected', key='-FILE-', font=fontarial)],
          [sg.Button('Load config file', font=fontarial)],
          [sg.Text('Party Guests:', font=fontarial)],
          [sg.Table(values=[], headings=['id', 'name', 'startposition'],
                    max_col_width=25,
                    auto_size_columns=True,
                    # display_row_numbers=True,
                    justification='center',
                    num_rows=5,
                    alternating_row_color='#5f5f5f',
                    background_color='#7e7e7e',
                    key='-TABLE-',
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,  # Comment out to not enable header and other clicks
                    font=('Arial', 12))],
          [sg.Text('Wunschabstaende:', font=fontarial)],
          [sg.Table(values=[], headings=['person1_id', 'person2_id', 'wunschabstand'],

                    auto_size_columns=True,
                    # display_row_numbers=True,
                    justification='cente',
                    num_rows=5,
                    alternating_row_color='#5f5f5f',
                    background_color='#7e7e7e',
                    key='-DISTANCE-',
                    # selected_row_colors='red on yellow',
                    # enable_events=True,
                    # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,  # Comment out to not enable header and other clicks
                    font=('Arial', 12))],
          [sg.Text('Generell:', font=fontarial)],
          [sg.Table(values=[], headings=['Einstellung', 'Wert'],
                    max_col_width=25,
                    auto_size_columns=True,
                    # display_row_numbers=True,
                    justification='center',
                    num_rows=5,
                    alternating_row_color='#5f5f5f',
                    background_color='#7e7e7e',
                    key='-SETTING-',
                    # selected_row_colors='red on yellow',
                    # enable_events=True,
                    # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,  # Comment out to not enable header and other clicks
                    font=('Arial', 12))],
          [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')],
          [sg.HorizontalSeparator(color='black')],
          [sg.Button('Start with this data', font=fontarial)],
          ]

# Create the window
window = sg.Window('My Application', layout, size=(1000, 700))

# Event loop
def load_config_file(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            data = json.load(f)
            headings = ['id', 'name', 'startposition']
            values = [[p['id'], p['name'], str(p['startposition'])] for p in data['Personen']]
            window['-TABLE-'].update(values=values)
            window['-DISTANCE-'].update(
                values=[[p['person1_id'], p['person2_id'], p['wunschabstand']] for p in data['Wunschabstaende']])
            window['-SETTING-'].update(values=[[key, value] for key, value in data['Spielfeld'].items()])
    else:
        sg.popup_error('Please select a file first')


def put_into_json():
    personen = []
    num_rows = num_rows = len(window['-TABLE-'].widget.get_children())
    # print("Number of rows :", num_rows)
    for i in range(1, num_rows + 1):
        row = list(window['-TABLE-'].widget.item(i, 'values'))
        print(row)
        personen.append({
            'id': row[0],
            'name': row[1],
            'startposition': [int(x.strip('[').strip(']')) for x in row[2].split(',')]
        })

    Wunschabstaende = []
    num_rows = num_rows = len(window['-DISTANCE-'].widget.get_children())
    for i in range(1, num_rows + 1):
        row = list(window['-DISTANCE-'].widget.item(i, 'values'))
        print(row)
        Wunschabstaende.append({
            'person1_id': int(row[0]),
            'person2_id': int(row[1]),
            'wunschabstand': float(row[2])
        })

    Einstellungen = {}
    num_rows = num_rows = len(window['-SETTING-'].widget.get_children())
    print("Number of rows :", num_rows)
    for i in range(1, num_rows + 1):
        row = list(window['-SETTING-'].widget.item(i, 'values'))
        print(row)
        Einstellungen[row[0]] = int(row[1])
    try:
        sg.popup(
            f"JSON file generated successfully!: {json.dumps({'Personen': personen, 'Wunschabstaende': Wunschabstaende, 'Spielfeld': Einstellungen})}",
            title='Success')
    except Exception as e:
        sg.popup_error('Try again! Some obvious error with the config provided: ' + str(e), title='Error')


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Select File':
        try:
            filename = values['Select File']
            if os.path.isfile(filename):
                window['-FILE-'].update(filename)
            else:
                window['-FILE-'].update('No file selected')
        except:
            window['-FILE-'].update('No file selected')
    elif event == 'Load config file':
        filename = values['Select File']
        load_config_file(filename)

    elif event[1] == '+CLICKED+':
        cell = row, col = event[2]
        table = event[0]
        window['-CLICKED-'].update(cell)
        try:
            edit_cell(window, table, row + 1, col, justify='center')
        except Exception as e:
            print(e)
            pass
    elif event == 'Start with this data':
        put_into_json()
# Close the window
window.close()
