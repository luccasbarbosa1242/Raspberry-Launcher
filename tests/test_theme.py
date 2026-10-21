"""Light/dark palette legibility regression without requiring Tk or a display."""

import unittest

from frontend import theme


def relative_luminance(value):
    channels = (int(value[pos:pos + 2], 16) / 255 for pos in (1, 3, 5))
    corrected = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return sum(weight * channel for weight, channel in
               zip((0.2126, 0.7152, 0.0722), corrected))


def contrast(foreground, background):
    light, dark = sorted(
        (relative_luminance(foreground), relative_luminance(background)),
        reverse=True,
    )
    return (light + 0.05) / (dark + 0.05)


class PaletteTests(unittest.TestCase):
    def test_page_sidebar_and_cards_have_distinct_light_and_dark_colors(self):
        for name in ("BG", "PAGE", "CARD", "SIDEBAR", "FOOTER", "POPUP", "HOVER",
            "BORDER"):
            colors = getattr(theme, name)
            with self.subTest(token=name):
                self.assertEqual(len(colors), 2)
                self.assertNotEqual(colors[0], colors[1])

    def test_text_and_status_have_at_least_45_to_1_contrast(self):
        for background in ("PAGE", "SIDEBAR", "CARD"):
            for foreground in (
                "TEXT", "MUTED", "STATUS_ROM", "STATUS_INSTALLED", "STATUS_MISSING"
            ):
                for mode_index in (0, 1):
                    with self.subTest(background=background, foreground=foreground,
                                      mode=mode_index):
                        ratio = contrast(
                            getattr(theme, foreground)[mode_index],
                            getattr(theme, background)[mode_index],
                        )
                        self.assertGreaterEqual(ratio, 4.5)
