
from nicegui import ui

# =========================================================
# PLATE CALCULATOR - GUI MOCKUP
# =========================================================

ui.query('body').style(
    'margin: 0;'
    'background-color: #202020;'
)

# ---------------------------------------------------------
# Main container
# ---------------------------------------------------------

with ui.column().classes(
    'w-full min-h-screen items-center justify-center p-4'
):
    with ui.column().classes(
        'w-full max-w-2xl'
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

        # -------------------------------------------------
        # Swipeable pages
        # -------------------------------------------------

        with ui.carousel(
            value='calculator'
        ).props(
            'animated swipeable infinite'
        ).classes(
            'w-full'
        ) as carousel:

            # =================================================
            # CALCULATOR PAGE
            # =================================================

            with ui.carousel_slide(
                name='calculator'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):
                    ui.label('Calculator').classes(
                        'text-xl sm:text-2xl font-bold text-white'
                    )

                    ui.select(
                        ['GymTest LB', 'GymTest KG'],
                        value='GymTest LB',
                        label='Gym'
                    ).classes('w-full')

                    with ui.row().classes(
                        'w-full gap-2'
                    ):
                        ui.select(
                            ['LB', 'KG'],
                            value='LB',
                            label='Unit'
                        ).classes('flex-1')

                        ui.number(
                            label='Goal Weight',
                            value=180,
                            format='%.2f'
                        ).classes('flex-[2]')

                    ui.button(
                        'CALCULATE'
                    ).classes(
                        'w-full'
                    )

                    # -----------------------------------------
                    # Mock result
                    # -----------------------------------------

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

            # =================================================
            # GYM PAGE
            # =================================================

            with ui.carousel_slide(
                name='gym'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):
                    ui.label('My Gym').classes(
                        'text-xl sm:text-2xl font-bold text-white'
                    )

                    ui.input(
                        label='Gym Name',
                        value='GymTest LB'
                    ).classes('w-full')

                    ui.select(
                        ['LB', 'KG'],
                        value='LB',
                        label='Default Unit'
                    ).classes('w-full')

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

                    # -----------------------------------------
                    # Inventory
                    # -----------------------------------------

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
                            ui.label(weight).classes(
                                'text-lg'
                            )

                            ui.label(
                                f'× {quantity}'
                            ).classes(
                                'text-lg'
                            )

            # =================================================
            # ADD PLATE PAGE
            # =================================================

            with ui.carousel_slide(
                name='add'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):
                    ui.label('Add Plate').classes(
                        'text-xl sm:text-2xl font-bold text-white'
                    )

                    ui.number(
                        label='Weight',
                        value=45
                    ).classes('w-full')

                    ui.select(
                        ['LB', 'KG'],
                        value='LB',
                        label='Unit'
                    ).classes('w-full')

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
                    ).classes('w-full')

                    ui.number(
                        label='Quantity',
                        value=2,
                        min=1
                    ).classes('w-full')

                    ui.button(
                        'ADD TO INVENTORY'
                    ).classes(
                        'w-full'
                    )

            # =================================================
            # SETTINGS PAGE
            # =================================================

            with ui.carousel_slide(
                name='settings'
            ):
                with ui.column().classes(
                    'w-full gap-4'
                ):
                    ui.label('Settings').classes(
                        'text-xl sm:text-2xl font-bold text-white'
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

        # -------------------------------------------------
        # Bottom Navigation
        # -------------------------------------------------

        ui.separator().classes('my-2')

        with ui.row().classes(
            'w-full justify-around'
        ):
            ui.button(
                'Calculator',
                on_click=lambda: carousel.set_value('calculator')
            ).props('flat')

            ui.button(
                'Gym',
                on_click=lambda: carousel.set_value('gym')
            ).props('flat')

            ui.button(
                'Add Plate',
                on_click=lambda: carousel.set_value('add')
            ).props('flat')

            ui.button(
                'Settings',
                on_click=lambda: carousel.set_value('settings')
            ).props('flat')


# =========================================================
# Run Application
# =========================================================

ui.run(
    title='Plate Calculator',
    host='0.0.0.0',
    port=8080
)
