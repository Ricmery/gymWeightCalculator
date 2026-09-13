from nicegui import ui

# =========================================================
# PLATE CALCULATOR - GUI MOCKUP
# =========================================================

ui.query('body').style(
    'margin: 0;'
    'background-color: #202020;'
    'overflow: hidden;'
    'touch-action: none;'
)

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
            ui.label('PLATE CALCULATOR').classes(
                'text-2xl sm:text-3xl font-bold text-white'
            )

            ui.label('●').classes(
                'text-green-500 text-xl'
            )

        ui.separator().classes('my-2')

        # =================================================
        # Main Horizontal Swipe Navigation
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
                        'text-xl sm:text-2xl font-bold text-white'
                    )

                    ui.select(
                        ['GymTest LB', 'GymTest KG'],
                        value='GymTest LB',
                        label='Gym'
                    ).classes(
                        'w-full'
                    )

                    with ui.row().classes(
                        'w-full gap-2'
                    ):
                        ui.select(
                            ['LB', 'KG'],
                            value='LB',
                            label='Unit'
                        ).classes(
                            'flex-1'
                        )

                        ui.number(
                            label='Goal Weight',
                            value=180,
                            format='%.2f'
                        ).classes(
                            'flex-[2]'
                        )

                    ui.button(
                        'CALCULATE'
                    ).classes(
                        'w-full'
                    )

                    # -------------------------------------
                    # Mock Result
                    # -------------------------------------

                    with ui.card().classes(
                        'w-full'
                    ):
                        ui.label(
                            '180.00 LB (81.65 KG)'
                        ).classes(
                            'text-xl font-bold'
                        )

                        ui.label(
                            'Per Side: 67.50 LB'
                        )

                        ui.separator()

                        ui.label(
                            'Recommended Setup'
                        ).classes(
                            'font-bold'
                        )

                        with ui.row().classes(
                            'w-full flex-wrap gap-2'
                        ):
                            for plate in [
                                '45 LB',
                                '10 LB',
                                '10 LB',
                                '2.5 LB'
                            ]:
                                ui.badge(
                                    plate
                                ).classes(
                                    'text-lg p-3'
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
                        'text-xl sm:text-2xl font-bold text-white'
                    )

                    ui.input(
                        label='Gym Name',
                        value='GymTest LB'
                    ).classes(
                        'w-full'
                    )

                    ui.select(
                        ['LB', 'KG'],
                        value='LB',
                        label='Default Unit'
                    ).classes(
                        'w-full'
                    )

                    ui.button(
                        'SAVE GYM'
                    ).classes(
                        'w-full'
                    )

                    ui.separator()

                    ui.label(
                        'Plate Inventory'
                    ).classes(
                        'text-lg font-bold'
                    )

                    plates = [
                        ('2.5 LB', 2),
                        ('5 LB', 4),
                        ('10 LB', 2),
                        ('25 LB', 2),
                        ('35 LB', 2),
                        ('45 LB', 2),
                    ]

                    for weight, quantity in plates:
                        with ui.row().classes(
                            'w-full items-center justify-between'
                        ):
                            ui.label(
                                weight
                            ).classes(
                                'text-lg'
                            )

                            ui.label(
                                f'× {quantity}'
                            ).classes(
                                'text-lg'
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
                        'text-xl sm:text-2xl font-bold text-white'
                    )

                    ui.number(
                        label='Weight',
                        value=45
                    ).classes(
                        'w-full'
                    )

                    ui.select(
                        ['LB', 'KG'],
                        value='LB',
                        label='Unit'
                    ).classes(
                        'w-full'
                    )

                    ui.select(
                        [
                            'None',
                            'White',
                            'Green',
                            'Yellow',
                            'Blue',
                            'Red'
                        ],
                        value='None',
                        label='Color'
                    ).classes(
                        'w-full'
                    )

                    ui.number(
                        label='Quantity',
                        value=2,
                        min=1
                    ).classes(
                        'w-full'
                    )

                    ui.button(
                        'ADD TO INVENTORY'
                    ).classes(
                        'w-full'
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

    // -------------------------------------------------
    // Swipe DOWN = Open Settings
    // -------------------------------------------------

    if (!settingsOpen && difference > swipeDistance) {
        settingsPanel.classList.remove(
            '-translate-y-full'
        );

        settingsPanel.classList.add(
            'translate-y-0'
        );

        settingsOpen = true;
    }

    // -------------------------------------------------
    // Swipe UP = Close Settings
    // -------------------------------------------------

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
