import PySimpleGUI as sg
import os.path
import json

# Define the theme
sg.theme('DarkGrey14')
fontarial = ('Arial', 14)
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
    anchor_x, anchor_y = table.winfo_x() + x + 5, table.winfo_y() + y + 195

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
          [sg.FileBrowse('Select File', font=('Arial', 14)),
           sg.Text('No file selected', key='-FILE-', font=('Arial', 14))],
          [sg.Button('Show JSON', font=fontarial)],
          [sg.Text('Party Guests:', font=fontarial)],
          [sg.Table(values=[], headings=['id', 'name', 'startposition'],
                    max_col_width=25,
                    auto_size_columns=True,
                    # display_row_numbers=True,
                    justification='right',
                    num_rows=20,
                    alternating_row_color='#5f5f5f',
                    background_color='#7e7e7e',
                    key='-TABLE-',
                    # selected_row_colors='red on yellow',
                    # enable_events=True,
                    # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,  # Comment out to not enable header and other clicks
                    font=('Arial', 14))],
          [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')],
          [sg.HorizontalSeparator(color='black')],
          [sg.Button('Start with this data', font=fontarial)],
          [sg.Text('This is a simple test Partyplanera', font=('Arial', 12), justification='center')]
          ]

# Create the window
window = sg.Window('My Application', layout, size=(1000, 800))

# Event loop
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
    elif event == 'Show JSON':
        filename = values['Select File']
        if os.path.isfile(filename):
            with open(filename) as f:
                data = json.load(f)
                headings = ['id', 'name', 'startposition']
                values = [[p['id'], p['name'], str(p['startposition'])] for p in data['Personen']]
                window['-TABLE-'].update(values=values)
        else:
            sg.popup_error('Please select a file first')
    elif isinstance(event, tuple):
        cell = row, col = event[2]
        window['-CLICKED-'].update(cell)
        try:
            edit_cell(window, '-TABLE-', row + 1, col, justify='right')
        except Exception as e:
            print(e)
            pass
    elif event == 'Start with this data':
        data = []
        num_rows = len(values['-TABLE-'])
        print(window['-TABLE-'].widget.item(1, 'values'))
        for row in window['-TABLE-'].get():
            data.append({
                'id': row[0],
                'name': row[1],
                'startposition': [int(x.strip('[').strip(']')) for x in row[2].split(',')]
            })
        with open('data.json', 'w') as f:
            json.dump({'Personen': data}, f)
        sg.popup(f"JSON file generated successfully!: {json.dumps({'Personen': data})}", title='Success')

# Close the window
window.close()
