from nicegui import ui
import database
import calculator
import sqlite3

# =========================================================
# PAGE STYLE
# =========================================================
ui.query('body').style(
    'margin: 0;'
    'background-color: #202020;'
    'overflow: hidden;'
    'touch-action: none;'
)

# =========================================================
# APPLICATION DATA
# =========================================================
gyms = database.get_gyms()

if gyms:
    gym_names = [gym["name"] for gym in gyms]
    selected_gym_name = gym_names[0]
else:
    gym_names = []
    selected_gym_name = None

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def get_selected_gym():
    if not selected_gym_name:
        return None
    for gym in gyms:
        if gym["name"] == selected_gym_name:
            return gym
    return None

def refresh_page():
    ui.run_javascript(
        'location.reload()'
    )

# =========================================================
# CALCULATOR
# =========================================================
def calculate_result():
    result_area.clear()
    gym = get_selected_gym()

    if gym is None:
        with result_area:
            ui.label(
                'No gym selected.'
            ).classes(
                'text-red-400 text-lg'
            )
        return

    goal = goal_weight.value
    input_unit = unit_select.value

    if goal is None:
        with result_area:
            ui.label(
                'Enter a goal weight.'
            ).classes(
                'text-red-400 text-lg'
            )
        return

    gym_plates = database.get_plates(
        gym["id"]
    )

    if not gym_plates:
        with result_area:
            ui.label(
                'The selected gym has no plates.'
            ).classes(
                'text-red-400 text-lg'
            )
        return

    bar_weight = gym["bar_weight"]

    result = calculator.calculate(
        goal_weight=goal,
        input_unit=input_unit,
        gym_plates=gym_plates,
        bar_weight=bar_weight
    )

    if not result["success"]:
        with result_area:
            ui.label(
                result["error"]
            ).classes(
                'text-red-400 text-lg'
            )
        return

    with result_area:
        with ui.card().classes(
            'w-full'
        ):
            ui.label(
                'Result'
            ).classes(
                'text-xl font-bold'
            )

            ui.label(
                f'{result["input_weight"]:.2f} '
                f'{result["input_unit"]} '
                f'('
                f'{result["gym_weight"]:.2f} '
                f'{result["gym_unit"]}'
                f')'
            ).classes(
                'text-2xl font-bold'
            )

            ui.label(
                f'Target Per Side: '
                f'{result["target_per_side"]:.2f} '
                f'{result["gym_unit"]}'
            )

            ui.separator()

            ui.label(
                'Recommended Setup'
            ).classes(
                'text-lg font-bold'
            )

            with ui.column().classes(
                'w-full gap-2'
            ):
                for plate in result["plates"]:
                    weight = plate["weight"]
                    unit = plate["unit"]
                    color = plate["color"]

                    if color and color != "none":
                        text = (
                            f'{weight:.2f} {unit} '
                            f'({color})'
                        )
                    else:
                        text = (
                            f'{weight:.2f} {unit}'
                        )

                    ui.label(
                        text
                    ).classes(
                        'text-lg'
                    )

            ui.separator()

            ui.label(
                f'Actual Per Side: '
                f'{result["actual_per_side"]:.2f} '
                f'{result["gym_unit"]}'
            )

            ui.label(
                f'Actual Total: '
                f'{result["actual_total"]:.2f} '
                f'{result["gym_unit"]}'
            )

            ui.label(
                f'Actual Total: '
                f'{result["actual_total_input"]:.2f} '
                f'{result["input_unit"]}'
            )

            if result["difference"] > 0:
                difference_text = (
                    f'Over by '
                    f'{result["difference_input"]:.2f} '
                    f'{result["input_unit"]}'
                )
            elif result["difference"] < 0:
                difference_text = (
                    f'Under by '
                    f'{result["difference_input"]:.2f} '
                    f'{result["input_unit"]}'
                )
            else:
                difference_text = 'Exact weight'

            ui.label(
                difference_text
            ).classes(
                'text-lg font-bold'
            )

            ui.label(
                f'Plate Count: '
                f'{result["plate_count"]}'
            )

def gym_changed(event):
    global selected_gym_name
    selected_gym_name = event.value
    result_area.clear()

# =========================================================
# CREATE GYM
# =========================================================
def create_new_gym():
    name = create_gym_name.value
    unit = create_gym_unit.value
    bar_weight = create_gym_bar.value

    if not name:
        ui.notify(
            'Enter a gym name.',
            type='negative'
        )
        return

    if bar_weight is None or bar_weight <= 0:
        ui.notify(
            'Enter a valid bar weight.',
            type='negative'
        )
        return

    try:
        gym_id = database.add_gym(
            name,
            unit,
            bar_weight
        )

        if create_standard_set.value:
            if unit == 'LB':
                standard_plates = (
                    database.STANDARD_LB_PLATES
                )
            else:
                standard_plates = (
                    database.STANDARD_KG_PLATES
                )

            for weight, quantity in standard_plates:
                database.add_plate(
                    gym_id,
                    weight,
                    unit,
                    'none',
                    quantity
                )

        ui.notify(
            'Gym created!',
            type='positive'
        )

        create_gym_dialog.close()
        refresh_page()

    except sqlite3.IntegrityError:
        ui.notify(
            'A gym with that name already exists.',
            type='negative'
        )

# =========================================================
# MODIFY GYM
# =========================================================
def modify_gym():
    gym = get_selected_gym()

    if gym is None:
        return

    name = modify_gym_name.value
    unit = modify_gym_unit.value
    bar_weight = modify_gym_bar.value

    if not name:
        ui.notify(
            'Enter a gym name.',
            type='negative'
        )
        return

    if bar_weight is None or bar_weight <= 0:
        ui.notify(
            'Enter a valid bar weight.',
            type='negative'
        )
        return

    try:
        database.update_gym(
            gym["id"],
            name,
            unit,
            bar_weight
        )

        ui.notify(
            'Gym modified!',
            type='positive'
        )

        modify_gym_dialog.close()
        refresh_page()

    except sqlite3.IntegrityError:
        ui.notify(
            'A gym with that name already exists.',
            type='negative'
        )

# =========================================================
# DELETE GYM
# =========================================================
def delete_selected_gym():
    gym = get_selected_gym()

    if gym is None:
        return

    database.delete_gym(
        gym["id"]
    )

    ui.notify(
        'Gym deleted!',
        type='positive'
    )

    delete_gym_dialog.close()
    refresh_page()

# =========================================================
# ADD PLATE
# =========================================================
def add_plate_to_gym():
    gym = get_selected_gym()

    if gym is None:
        return

    weight = add_weight.value
    quantity = add_quantity.value
    unit = add_unit.value
    color = add_color.value

    if weight is None or weight <= 0:
        ui.notify(
            'Enter a valid plate weight.',
            type='negative'
        )
        return

    if quantity is None or quantity < 1:
        ui.notify(
            'Enter a valid quantity.',
            type='negative'
        )
        return

    database.add_plate(
        gym["id"],
        weight,
        unit,
        color,
        quantity
    )

    ui.notify(
        'Plate added!',
        type='positive'
    )

    add_plate_dialog.close()
    refresh_page()

# =========================================================
# MODIFY PLATE
# =========================================================
def modify_plate():
    plate_id = modify_plate_select.value

    if plate_id is None:
        ui.notify(
            'Select a plate.',
            type='negative'
        )
        return

    weight = modify_weight.value
    quantity = modify_quantity.value
    unit = modify_unit.value
    color = modify_color.value

    if weight is None or weight <= 0:
        ui.notify(
            'Enter a valid plate weight.',
            type='negative'
        )
        return

    if quantity is None or quantity < 1:
        ui.notify(
            'Enter a valid quantity.',
            type='negative'
        )
        return

    database.update_plate(
        plate_id,
        weight,
        unit,
        color,
        quantity
    )

    ui.notify(
        'Plate modified!',
        type='positive'
    )

    modify_plate_dialog.close()
    refresh_page()

# =========================================================
# DELETE PLATE
# =========================================================
def delete_selected_plate():
    plate_id = delete_plate_select.value

    if plate_id is None:
        ui.notify(
            'Select a plate.',
            type='negative'
        )
        return

    database.delete_plate(
        plate_id
    )

    ui.notify(
        'Plate deleted!',
        type='positive'
    )

    delete_plate_dialog.close()
    refresh_page()

# =========================================================
# MAIN APPLICATION
# =========================================================
with ui.column().classes(
    'w-full h-screen items-center justify-center p-4'
):
    with ui.column().classes(
        'w-full max-w-2xl h-full'
    ):

        # =================================================
        # HEADER
        # =================================================
        with ui.row().classes(
            'w-full items-center justify-between'
        ):
            ui.label(
                'PLATE CALCULATOR'
            ).classes(
                'text-2xl sm:text-3xl '
                'font-bold text-white'
            )

            ui.label(
                '●'
            ).classes(
                'text-green-500 text-xl'
            )

        ui.separator().classes(
            'my-2'
        )

        # =================================================
        # CAROUSEL
        # =================================================
        with ui.carousel(
            value='calculator'
        ).props(
            'animated swipeable infinite'
        ).classes(
            'w-full flex-1'
        ):

            # =============================================
            # CALCULATOR PAGE
            # =============================================
            with ui.carousel_slide(
                name='calculator'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):
                    ui.label(
                        'Calculator'
                    ).classes(
                        'text-xl sm:text-2xl '
                        'font-bold text-white'
                    )

                    if gym_names:
                        gym_select = ui.select(
                            gym_names,
                            value=selected_gym_name,
                            label='Gym',
                            on_change=gym_changed
                        ).classes(
                            'w-full'
                        )
                    else:
                        gym_select = ui.select(
                            [],
                            label='Gym'
                        ).classes(
                            'w-full'
                        )

                        ui.label(
                            'No gyms found. '
                            'Create a gym first.'
                        ).classes(
                            'text-yellow-400'
                        )

                    with ui.row().classes(
                        'w-full gap-2'
                    ):
                        unit_select = ui.select(
                            ['LB', 'KG'],
                            value='LB',
                            label='Unit'
                        ).classes(
                            'flex-1'
                        )

                        goal_weight = ui.number(
                            label='Goal Weight',
                            value=180,
                            format='%.2f'
                        ).classes(
                            'flex-[2]'
                        )

                    ui.button(
                        'CALCULATE',
                        on_click=calculate_result
                    ).classes(
                        'w-full'
                    )

                    result_area = ui.column().classes(
                        'w-full gap-4'
                    )

            # =============================================
            # GYM PAGE
            # =============================================
            with ui.carousel_slide(
                name='gym'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):

                    ui.label(
                        'My Gym'
                    ).classes(
                        'text-xl sm:text-2xl '
                        'font-bold text-white'
                    )

                    # -------------------------------------
                    # NO GYMS
                    # -------------------------------------
                    if not gyms:

                        ui.label(
                            'No gyms created yet.'
                        ).classes(
                            'text-gray-300'
                        )

                        ui.button(
                            'ADD GYM',
                            on_click=lambda:
                            create_gym_dialog.open()
                        ).classes(
                            'w-full'
                        )

                    # -------------------------------------
                    # EXISTING GYM
                    # -------------------------------------
                    else:

                        gym = get_selected_gym()

                        # ---------------------------------
                        # GYM SELECTOR
                        # ---------------------------------
                        ui.select(
                            gym_names,
                            value=selected_gym_name,
                            label='Selected Gym',
                            on_change=gym_changed
                        ).classes(
                            'w-full'
                        )

                        if gym:

                            ui.label(
                                gym['name']
                            ).classes(
                                'text-2xl font-bold text-white'
                            )

                            ui.label(
                                f'Unit: '
                                f'{gym["default_unit"].upper()}'
                            ).classes(
                                'text-gray-300'
                            )

                            ui.label(
                                f'Bar: '
                                f'{gym["bar_weight"]:.2f} '
                                f'{gym["default_unit"].upper()}'
                            ).classes(
                                'text-gray-300'
                            )

                            ui.separator()

                            ui.label(
                                'Plate Inventory'
                            ).classes(
                                'text-lg font-bold text-white'
                            )

                            gym_plates = database.get_plates(
                                gym['id']
                            )

                            if gym_plates:

                                for plate in gym_plates:

                                    with ui.row().classes(
                                        'w-full '
                                        'items-center '
                                        'justify-between'
                                    ):

                                        ui.label(
                                            f'{plate["weight"]:.2f} '
                                            f'{plate["unit"]}'
                                        ).classes(
                                            'text-white'
                                        )

                                        ui.label(
                                            f'x {plate["quantity"]}'
                                        ).classes(
                                            'text-gray-300'
                                        )

                                        if (
                                            plate["color"]
                                            and
                                            plate["color"] != "none"
                                        ):
                                            ui.label(
                                                plate["color"]
                                            ).classes(
                                                'text-gray-400'
                                            )

                            else:

                                ui.label(
                                    'No plates added.'
                                ).classes(
                                    'text-gray-400'
                                )

                            ui.separator()

                            # ---------------------------------
                            # GYM MANAGEMENT
                            # ---------------------------------
                            ui.label(
                                'Manage Gym'
                            ).classes(
                                'text-lg font-bold text-white'
                            )

                            with ui.row().classes(
                                'w-full gap-2'
                            ):

                                ui.button(
                                    'ADD GYM',
                                    on_click=lambda:
                                    create_gym_dialog.open()
                                ).classes(
                                    'flex-1'
                                )

                                ui.button(
                                    'MODIFY GYM',
                                    on_click=lambda:
                                    open_modify_gym()
                                ).classes(
                                    'flex-1'
                                )

                                ui.button(
                                    'DELETE GYM',
                                    on_click=lambda:
                                    delete_gym_dialog.open()
                                ).classes(
                                    'flex-1'
                                )

                            ui.separator()

                            # ---------------------------------
                            # PLATE MANAGEMENT
                            # ---------------------------------
                            ui.label(
                                'Manage Plates'
                            ).classes(
                                'text-lg font-bold text-white'
                            )

                            with ui.row().classes(
                                'w-full gap-2'
                            ):

                                ui.button(
                                    'ADD',
                                    on_click=lambda:
                                    add_plate_dialog.open()
                                ).classes(
                                    'flex-1'
                                )

                                ui.button(
                                    'MODIFY',
                                    on_click=lambda:
                                    open_modify_plate()
                                ).classes(
                                    'flex-1'
                                )

                                ui.button(
                                    'DELETE',
                                    on_click=lambda:
                                    open_delete_plate()
                                ).classes(
                                    'flex-1'
                                )

            # =============================================
            # ADD PAGE
            # =============================================
            with ui.carousel_slide(
                name='add'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):

                    ui.label(
                        'Add'
                    ).classes(
                        'text-xl sm:text-2xl '
                        'font-bold text-white'
                    )

                    ui.label(
                        'Additional features can go here.'
                    ).classes(
                        'text-gray-400'
                    )

# =========================================================
# CREATE GYM DIALOG
# =========================================================
with ui.dialog() as create_gym_dialog:
    with ui.card().classes(
        'w-full max-w-md'
    ):

        ui.label(
            'Create Gym'
        ).classes(
            'text-xl font-bold'
        )

        create_gym_name = ui.input(
            label='Gym Name',
            placeholder='Example: Home Gym'
        ).classes(
            'w-full'
        )

        create_gym_unit = ui.select(
            ['LB', 'KG'],
            value='LB',
            label='Unit'
        ).classes(
            'w-full'
        )

        create_gym_bar = ui.number(
            label='Bar Weight',
            value=45,
            format='%.2f'
        ).classes(
            'w-full'
        )

        create_standard_set = ui.checkbox(
            'Create standard plate set',
            value=True
        )

        with ui.row().classes(
            'w-full justify-end'
        ):
            ui.button(
                'CANCEL',
                on_click=create_gym_dialog.close
            )

            ui.button(
                'CREATE GYM',
                on_click=create_new_gym
            )

# =========================================================
# MODIFY GYM DIALOG
# =========================================================
def open_modify_gym():
    gym = get_selected_gym()

    if gym is None:
        return

    modify_gym_name.value = gym["name"]
    modify_gym_unit.value = gym["default_unit"]
    modify_gym_bar.value = gym["bar_weight"]

    modify_gym_dialog.open()

with ui.dialog() as modify_gym_dialog:
    with ui.card().classes(
        'w-full max-w-md'
    ):

        ui.label(
            'Modify Gym'
        ).classes(
            'text-xl font-bold'
        )

        modify_gym_name = ui.input(
            label='Gym Name'
        ).classes(
            'w-full'
        )

        modify_gym_unit = ui.select(
            ['LB', 'KG'],
            label='Unit'
        ).classes(
            'w-full'
        )

        modify_gym_bar = ui.number(
            label='Bar Weight',
            format='%.2f'
        ).classes(
            'w-full'
        )

        with ui.row().classes(
            'w-full justify-end'
        ):
            ui.button(
                'CANCEL',
                on_click=modify_gym_dialog.close
            )

            ui.button(
                'SAVE CHANGES',
                on_click=modify_gym
            )

# =========================================================
# DELETE GYM DIALOG
# =========================================================
with ui.dialog() as delete_gym_dialog:
    with ui.card().classes(
        'w-full max-w-md'
    ):

        ui.label(
            'Delete Gym'
        ).classes(
            'text-xl font-bold'
        )

        ui.label(
            'This will permanently delete the gym '
            'and all of its plates.'
        ).classes(
            'text-red-500'
        )

        with ui.row().classes(
            'w-full justify-end'
        ):
            ui.button(
                'CANCEL',
                on_click=delete_gym_dialog.close
            )

            ui.button(
                'DELETE GYM',
                on_click=delete_selected_gym
            )

# =========================================================
# ADD PLATE DIALOG
# =========================================================
with ui.dialog() as add_plate_dialog:
    with ui.card().classes(
        'w-full max-w-md'
    ):

        ui.label(
            'Add Plate'
        ).classes(
            'text-xl font-bold'
        )

        add_weight = ui.number(
            label='Weight',
            format='%.2f'
        ).classes(
            'w-full'
        )

        add_unit = ui.select(
            ['LB', 'KG'],
            value='LB',
            label='Unit'
        ).classes(
            'w-full'
        )

        add_quantity = ui.number(
            label='Quantity',
            value=2,
            format='%.0f'
        ).classes(
            'w-full'
        )

        add_color = ui.select(
            [
                'none',
                'white',
                'green',
                'yellow',
                'blue',
                'red'
            ],
            value='none',
            label='Color'
        ).classes(
            'w-full'
        )

        with ui.row().classes(
            'w-full justify-end'
        ):
            ui.button(
                'CANCEL',
                on_click=add_plate_dialog.close
            )

            ui.button(
                'ADD PLATE',
                on_click=add_plate_to_gym
            )

# =========================================================
# MODIFY PLATE DIALOG
# =========================================================
def open_modify_plate():
    gym = get_selected_gym()

    if gym is None:
        return

    plates = database.get_plates(
        gym["id"]
    )

    options = {}

    for plate in plates:
        label = (
            f'{plate["weight"]:.2f} '
            f'{plate["unit"]} '
            f'x {plate["quantity"]}'
        )

        options[plate["id"]] = label

    modify_plate_select.options = options
    modify_plate_select.update()

    if plates:
        first_plate = plates[0]

        modify_plate_select.value = first_plate["id"]
        modify_weight.value = first_plate["weight"]
        modify_unit.value = first_plate["unit"]
        modify_quantity.value = first_plate["quantity"]
        modify_color.value = first_plate["color"]

    modify_plate_dialog.open()

def modify_plate_selected(event):
    gym = get_selected_gym()

    if gym is None:
        return

    plate_id = event.value

    plates = database.get_plates(
        gym["id"]
    )

    for plate in plates:
        if plate["id"] == plate_id:

            modify_weight.value = plate["weight"]
            modify_unit.value = plate["unit"]
            modify_quantity.value = plate["quantity"]
            modify_color.value = plate["color"]

            break

with ui.dialog() as modify_plate_dialog:
    with ui.card().classes(
        'w-full max-w-md'
    ):

        ui.label(
            'Modify Plate'
        ).classes(
            'text-xl font-bold'
        )

        modify_plate_select = ui.select(
            options={},
            label='Plate',
            on_change=modify_plate_selected
        ).classes(
            'w-full'
        )

        modify_weight = ui.number(
            label='Weight',
            format='%.2f'
        ).classes(
            'w-full'
        )

        modify_unit = ui.select(
            ['LB', 'KG'],
            value='LB',
            label='Unit'
        ).classes(
            'w-full'
        )

        modify_quantity = ui.number(
            label='Quantity',
            value=2,
            format='%.0f'
        ).classes(
            'w-full'
        )

        modify_color = ui.select(
            [
                'none',
                'white',
                'green',
                'yellow',
                'blue',
                'red'
            ],
            value='none',
            label='Color'
        ).classes(
            'w-full'
        )

        with ui.row().classes(
            'w-full justify-end'
        ):
            ui.button(
                'CANCEL',
                on_click=modify_plate_dialog.close
            )

            ui.button(
                'SAVE CHANGES',
                on_click=modify_plate
            )

# =========================================================
# DELETE PLATE DIALOG
# =========================================================
def open_delete_plate():
    gym = get_selected_gym()

    if gym is None:
        return

    plates = database.get_plates(
        gym["id"]
    )

    options = {}

    for plate in plates:
        options[plate["id"]] = (
            f'{plate["weight"]:.2f} '
            f'{plate["unit"]} '
            f'x {plate["quantity"]}'
        )

    delete_plate_select.options = options
    delete_plate_select.update()

    if plates:
        delete_plate_select.value = plates[0]["id"]

    delete_plate_dialog.open()

with ui.dialog() as delete_plate_dialog:
    with ui.card().classes(
        'w-full max-w-md'
    ):

        ui.label(
            'Delete Plate'
        ).classes(
            'text-xl font-bold'
        )

        delete_plate_select = ui.select(
            options={},
            label='Plate'
        ).classes(
            'w-full'
        )

        ui.label(
            'This will permanently remove '
            'the selected plate.'
        ).classes(
            'text-red-500'
        )

        with ui.row().classes(
            'w-full justify-end'
        ):
            ui.button(
                'CANCEL',
                on_click=delete_plate_dialog.close
            )

            ui.button(
                'DELETE',
                on_click=delete_selected_plate
            )

# =========================================================
# SETTINGS PANEL
# =========================================================
with ui.element('div').classes(
    'fixed left-0 top-0'
    ' w-full'
    ' bg-gray-800'
    ' rounded-b-3xl'
    ' shadow-2xl'
    ' p-5'
    ' z-50'
    ' -translate-y-full'
    ' transition-transform'
    ' duration-300'
    ' select-none'
):
    with ui.column().classes(
        'w-full max-w-2xl mx-auto gap-4'
    ):

        with ui.element('div').classes(
            'w-full flex justify-center'
        ):
            ui.element('div').classes(
                'w-14 h-1.5 bg-gray-500 rounded-full'
            )

        ui.label(
            'Settings'
        ).classes(
            'text-2xl font-bold text-white text-center'
        )

        ui.switch(
            'Show opposite unit',
            value=True
        )

        ui.switch(
            'Show colors',
            value=True
        )

        ui.switch(
            'Show plate count',
            value=True
        )

        ui.switch(
            'Show weight difference',
            value=True
        )

        ui.separator()

        ui.label(
            'Swipe up to close'
        ).classes(
            'text-sm text-gray-400 text-center'
        )

# =========================================================
# SWITCH TEXT COLOR
# =========================================================
ui.add_body_html('''
<style>
.q-toggle__label {
    color: white !important;
}
</style>
''')

# =========================================================
# SETTINGS SWIPE
# =========================================================
ui.add_body_html('''
<script>
let startY = 0;
let currentY = 0;
let settingsOpen = false;

document.addEventListener('touchstart', function(event) {
    startY = event.touches[0].clientY;
    currentY = startY;
}, { passive: true });

document.addEventListener('touchmove', function(event) {
    currentY = event.touches[0].clientY;
}, { passive: true });

document.addEventListener('touchend', function(event) {
    const settingsPanel = document.querySelector(
        '.fixed.left-0.top-0'
    );

    if (!settingsPanel) {
        return;
    }

    const difference = currentY - startY;
    const swipeDistance = 70;

    if (!settingsOpen && difference > swipeDistance) {
        settingsPanel.classList.remove(
            '-translate-y-full'
        );

        settingsPanel.classList.add(
            'translate-y-0'
        );

        settingsOpen = true;
    }

    if (settingsOpen && difference < -swipeDistance) {
        settingsPanel.classList.remove(
            'translate-y-0'
        );

        settingsPanel.classList.add(
            '-translate-y-full'
        );

        settingsOpen = false;
    }

    startY = 0;
    currentY = 0;
}, { passive: true });
</script>
''')

# =========================================================
# RUN APPLICATION
# =========================================================
ui.run(
    title='Plate Calculator',
    host='0.0.0.0',
    port=8080
)