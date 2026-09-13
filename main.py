
from nicegui import ui
import database
import calculator

# =========================================================
# PLATE CALCULATOR - MAIN GUI
# =========================================================
ui.query('body').style(
    'margin: 0;'
    'background-color: #202020;'
    'overflow: hidden;'
    'touch-action: none;'
)

# =========================================================
# Application Data
# =========================================================
gyms = database.get_gyms()
if gyms:
    gym_names = [gym["name"] for gym in gyms]
    selected_gym_name = gym_names[0]
else:
    gym_names = []
    selected_gym_name = None

# =========================================================
# Helper Functions
# =========================================================
def get_selected_gym():
    if not selected_gym_name:
        return None
    for gym in gyms:
        if gym["name"] == selected_gym_name:
            return gym
    return None

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
    gym_plates = database.get_plates(gym["id"])
    if not gym_plates:
        with result_area:
            ui.label(
                'The selected gym has no plates.'
            ).classes(
                'text-red-400 text-lg'
            )
        return
    if gym["default_unit"].upper() == "KG":
        bar_weight = 20
    else:
        bar_weight = 45
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
# Main Application
# =========================================================
with ui.column().classes(
    'w-full h-screen items-center justify-center p-4'
):
    with ui.column().classes(
        'w-full max-w-2xl h-full'
    ):
        # -------------------------------------------------
        # Header
        # -------------------------------------------------
        with ui.row().classes(
            'w-full items-center justify-between'
        ):
            ui.label(
                'PLATE CALCULATOR'
            ).classes(
                'text-2xl sm:text-3xl font-bold text-white'
            )
            ui.label(
                '●'
            ).classes(
                'text-green-500 text-xl'
            )
        ui.separator().classes('my-2')

        # =================================================
        # Horizontal Swipe Navigation
        # =================================================
        with ui.carousel(
            value='calculator'
        ).props(
            'animated swipeable infinite'
        ).classes(
            'w-full flex-1'
        ):

            # =============================================
            # CALCULATOR
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

                    # -------------------------------------
                    # Selected Gym
                    # -------------------------------------
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
                            'No gyms found. Create a gym first.'
                        ).classes(
                            'text-yellow-400'
                        )

                    # -------------------------------------
                    # Unit + Goal Weight
                    # -------------------------------------
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

                    # -------------------------------------
                    # Calculate
                    # -------------------------------------
                    ui.button(
                        'CALCULATE',
                        on_click=calculate_result
                    ).classes(
                        'w-full'
                    )

                    # -------------------------------------
                    # Results
                    # -------------------------------------
                    result_area = ui.column().classes(
                        'w-full gap-4'
                    )

            # =============================================
            # GYM
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
                    ui.label(
                        'Gym management will go here.'
                    ).classes(
                        'text-gray-400'
                    )
                    ui.label(
                        'The database is the source '
                        'of the plate inventory.'
                    ).classes(
                        'text-gray-400'
                    )

            # =============================================
            # ADD PLATE
            # =============================================
            with ui.carousel_slide(
                name='add'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):
                    ui.label(
                        'Add Plate'
                    ).classes(
                        'text-xl sm:text-2xl '
                        'font-bold text-white'
                    )
                    ui.label(
                        'Plate management will go here.'
                    ).classes(
                        'text-gray-400'
                    )
                    ui.label(
                        'New plates will eventually '
                        'be saved directly to SQLite.'
                    ).classes(
                        'text-gray-400'
                    )

# =========================================================
# Settings Panel
# =========================================================
with ui.element('div').classes(
    'fixed left-0 top-0'
    ' w-full'
    ' bg-gray-900'
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
        # -------------------------------------------------
        # Drag Handle
        # -------------------------------------------------
        with ui.element('div').classes(
            'w-full flex justify-center'
        ):
            ui.element('div').classes(
                'w-14 h-1.5 bg-gray-500 rounded-full'
            )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------
        ui.label(
            'Settings'
        ).classes(
            'text-2xl font-bold text-white text-center'
        )

        # -------------------------------------------------
        # Settings
        # -------------------------------------------------
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
# Swipe JavaScript
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

    // Swipe DOWN = Open Settings
    if (!settingsOpen && difference > swipeDistance) {
        settingsPanel.classList.remove(
            '-translate-y-full'
        );
        settingsPanel.classList.add(
            'translate-y-0'
        );
        settingsOpen = true;
    }

    // Swipe UP = Close Settings
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
# Run Application
# =========================================================
ui.run(
    title='Plate Calculator',
    host='0.0.0.0',
    port=8080
)