#!/usr/bin/env python3
"""Generate all four Poimandres Zed themes (Poimandres & Storm — unbordered & bordered) in themes/poimandres.json.

Usage: python3 scripts/build.py

Faithful to drcmda/poimandres-theme (using alpha-composited official colors over #1b1e28 / #252b37),
with harmonized Poimandres git colors + 65%-blended gutter bars, clean file selector highlight,
and a pure white (#ffffff) primary cursor.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "themes"
SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"
AUTHOR = "Dallas Gere"
TRANSPARENT = "#00000000"
GIT_DIM = 0.92


def blend(fg, alpha, bg):
    """Straight sRGB mix: alpha of fg over bg."""
    a = [int(fg[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * alpha + y * (1 - alpha)):02x}" for x, y in zip(a, b))


def tok(color, style="normal", weight=400):
    return {"color": color, "font_style": style, "font_weight": weight}


# Official Poimandres palette (drcmda/poimandres-theme).
POI = {
    "mint": "#5de4c7",
    "teal": "#5fb3a1",
    "light_blue": "#add7ff",
    "cyan": "#89ddff",
    "steel": "#91b4d5",
    "blue_gray": "#a6accd",
    "pink": "#d0679d",
    "yellow": "#e6dfa4",       # #fffac2 eased slightly
    "white": "#d4e0ec",        # #e4f0fb eased slightly so white doesn't glare
    "comment": "#767c9d",
}

GIT = {
    "added": "#5de4c7",
    "modified": "#e6dfa4",
    "deleted": "#d0679d",
    "conflict": "#e08e79",
    "ignored": "#767c9d",
    "gutter_added": "#5de4c7",
    "gutter_modified": "#89ddff",
    "gutter_deleted": "#d0679d",
}

BASES = {
    "default": {
        "label": "Poimandres",
        "editor": "#1b1e28",
        "shell_bordered": "#161922",
        "elevated": "#232736",
        "line": "#232737",
        "selection": "#30364d",
        "border": "#2a2f40",
        "border_variant": "#222634",
        "wrap": "#252938",
        "wrap_active": "#343a4f",
        "invisible": "#383e54",
        "indent": "#242836",
        "indent_active": "#363c52",
    },
    "storm": {
        "label": "Poimandres Storm",
        "editor": "#252b37",
        "shell_bordered": "#1f2530",
        "elevated": "#2e3545",
        "line": "#2e3546",
        "selection": "#3a4259",
        "border": "#363e50",
        "border_variant": "#2c3342",
        "wrap": "#2f3747",
        "wrap_active": "#3f495e",
        "invisible": "#424c63",
        "indent": "#2e3645",
        "indent_active": "#424c63",
    },
}


def build_syntax(editor_bg):
    # Official Poimandres alpha-composited token colors over the variant's editor bg.
    comment = blend(POI["comment"], 0xb0 / 255, editor_bg)
    mint_flow = blend(POI["mint"], 0xc0 / 255, editor_bg)
    type_col = blend(POI["blue_gray"], 0xc0 / 255, editor_bg)
    call_col = blend("#e4f0fb", 0xd0 / 255, editor_bg)

    groups = [
        (tok(comment, "italic", 400), ("comment", "comment.doc")),
        (tok(comment, "normal", 400), ("hint", "predictive")),
        # Mint: strings, numbers, booleans, `this`, diff plus
        (tok(POI["mint"]), (
            "string", "string.doc", "string.special", "text.literal", "link_text",
            "number", "boolean", "variable.special", "diff.plus",
        )),
        # Alpha-composited mint (#5de4c7c0): control-flow keywords (return, await, import, export, async)
        (tok(mint_flow), (
            "keyword.return", "keyword.coroutine", "keyword.import",
            "keyword.export", "keyword.modifier", "keyword.control",
        )),
        # Teal-mint: attributes, regex, escapes
        (tok(POI["teal"]), (
            "attribute", "string.regex", "string.escape", "selector", "selector.pseudo",
        )),
        # Light sky blue: function definitions, constants, tags, JSON keys
        (tok(POI["light_blue"]), (
            "function", "function.definition", "function.method", "function.builtin",
            "constant", "property.json_key", "tag", "tag.doctype", "title", "link_uri",
        )),
        # Alpha-composited #e4f0fbd0: function & method calls
        (tok(call_col), ("function.call", "function.method.call")),
        # Steel blue: storage/type keywords, operators, constructors, namespaces
        (tok(POI["steel"]), (
            "keyword.storage", "keyword.type", "keyword.function", "keyword.operator",
            "keyword.directive", "preproc", "operator", "constructor", "namespace",
            "enum", "string.special.symbol",
        )),
        # Alpha-composited #a6accdc0: types
        (tok(type_col), ("type", "type.builtin", "type.interface", "type.parameter")),
        # Muted blue-gray: general keywords & punctuation
        (tok(POI["blue_gray"]), (
            "keyword", "keyword.conditional", "keyword.repeat",
            "punctuation", "punctuation.bracket", "punctuation.delimiter",
            "punctuation.list_marker", "punctuation.markup", "punctuation.special",
        )),
        # Berry pink: exceptions (try/catch/throw), null/undefined, diff minus
        (tok(POI["pink"]), (
            "keyword.exception", "constant.builtin", "function.special",
            "diff.minus", "variant",
        )),
        # Soft ice white: variables, parameters, properties
        (tok(POI["white"]), (
            "variable", "variable.parameter", "variable.member", "property",
            "label", "embedded", "emphasis", "emphasis.strong", "primary",
        )),
    ]
    syntax = {}
    for entry, keys in groups:
        for key in keys:
            syntax[key] = dict(entry)
    return dict(sorted(syntax.items()))


def build_style(base, bordered):
    editor_bg = base["editor"]
    shell_bg = base["shell_bordered"] if bordered else editor_bg
    elevated = base["elevated"]
    border = base["border"] if bordered else TRANSPARENT
    border_variant = base["border_variant"] if bordered else TRANSPARENT

    hover = blend(POI["white"], 0.06, shell_bg)
    selected = blend(POI["white"], 0.11, shell_bg)

    g_add = blend(GIT["gutter_added"], GIT_DIM, editor_bg)
    g_mod = blend(GIT["gutter_modified"], GIT_DIM, editor_bg)
    g_del = blend(GIT["gutter_deleted"], GIT_DIM, editor_bg)
    g_con = blend(GIT["conflict"], GIT_DIM, editor_bg)

    return {
        "background.appearance": "opaque",
        "background": shell_bg,
        "border": border,
        "border.variant": border_variant,
        "border.focused": TRANSPARENT,
        "border.selected": TRANSPARENT,
        "border.transparent": TRANSPARENT,
        "border.disabled": border,
        "elevated_surface.background": elevated,
        "surface.background": shell_bg,
        "element.background": elevated,
        "element.hover": hover,
        "element.active": selected,
        "element.selected": selected,
        "element.disabled": elevated,
        "drop_target.background": POI["mint"] + "2b",
        "ghost_element.background": TRANSPARENT,
        "ghost_element.hover": hover,
        "ghost_element.active": selected,
        "ghost_element.selected": selected,
        "ghost_element.disabled": TRANSPARENT,
        "text": POI["blue_gray"],
        "text.muted": POI["comment"],
        "text.placeholder": POI["comment"],
        "text.disabled": "#505670",
        "text.accent": POI["mint"],
        "icon": POI["blue_gray"],
        "icon.muted": POI["comment"],
        "icon.disabled": "#505670",
        "icon.placeholder": POI["comment"],
        "icon.accent": POI["mint"],
        "status_bar.background": shell_bg,
        "title_bar.background": shell_bg,
        "title_bar.inactive_background": shell_bg,
        "toolbar.background": editor_bg,
        "tab_bar.background": shell_bg,
        "tab.inactive_background": shell_bg,
        "tab.active_background": editor_bg if bordered else elevated,
        "search.match_background": "#5de4c726",
        "search.active_match_background": "#5de4c74d",
        "panel.background": shell_bg,
        "panel.focused_border": border if bordered else TRANSPARENT,
        "panel.indent_guide": base["indent"],
        "panel.indent_guide_active": base["indent_active"],
        "panel.indent_guide_hover": base["indent_active"],
        "pane.focused_border": TRANSPARENT,
        "pane_group.border": border,
        "scrollbar.thumb.background": "#767c9d38",
        "scrollbar.thumb.hover_background": "#767c9d5c",
        "scrollbar.thumb.active_background": "#767c9d80",
        "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": TRANSPARENT,
        "minimap.thumb.background": "#767c9d30",
        "minimap.thumb.hover_background": "#767c9d50",
        "minimap.thumb.active_background": "#767c9d75",
        "minimap.thumb.border": TRANSPARENT,
        "editor.foreground": POI["blue_gray"],
        "editor.background": editor_bg,
        "editor.gutter.background": editor_bg,
        "editor.subheader.background": elevated,
        "editor.active_line.background": base["line"],
        "editor.highlighted_line.background": base["line"],
        "editor.line_number": "#565d78",
        "editor.active_line_number": POI["white"],
        "editor.hover_line_number": POI["white"],
        "editor.invisible": base["invisible"],
        "editor.wrap_guide": base["wrap"],
        "editor.active_wrap_guide": base["wrap_active"],
        "editor.indent_guide": base["indent"],
        "editor.indent_guide_active": base["indent_active"],
        "editor.document_highlight.read_background": "#717cb428",
        "editor.document_highlight.write_background": "#717cb43d",
        "editor.document_highlight.bracket_background": "#5de4c722",
        "link_text.hover": POI["cyan"],
        "terminal.background": editor_bg,
        "terminal.foreground": POI["white"],
        "terminal.ansi.background": editor_bg,
        "terminal.bright_foreground": "#e4f0fb",
        "terminal.dim_foreground": POI["comment"],
        "terminal.ansi.black": "#1b1e28",
        "terminal.ansi.bright_black": "#767c9d",
        "terminal.ansi.red": POI["pink"],
        "terminal.ansi.bright_red": "#e37cb0",
        "terminal.ansi.green": POI["mint"],
        "terminal.ansi.bright_green": "#7ef0d8",
        "terminal.ansi.yellow": POI["yellow"],
        "terminal.ansi.bright_yellow": "#fffac2",
        "terminal.ansi.blue": POI["cyan"],
        "terminal.ansi.bright_blue": POI["light_blue"],
        "terminal.ansi.magenta": "#fcc5e9",
        "terminal.ansi.bright_magenta": "#ffd9f2",
        "terminal.ansi.cyan": POI["cyan"],
        "terminal.ansi.bright_cyan": POI["light_blue"],
        "terminal.ansi.white": POI["white"],
        "terminal.ansi.bright_white": "#e4f0fb",
        **{
            f"{name}{suffix}": c + (a or "")
            for name, c in {
                "error": POI["pink"],
                "warning": POI["yellow"],
                "info": POI["cyan"],
                "hint": POI["comment"],
                "success": GIT["added"],
                "created": GIT["added"],
                "modified": GIT["modified"],
                "deleted": GIT["deleted"],
                "renamed": GIT["added"],
                "conflict": GIT["conflict"],
                "ignored": GIT["ignored"],
                "hidden": "#505670",
                "unreachable": POI["comment"],
                "predictive": POI["comment"],
            }.items()
            for suffix, a in (("", None), (".background", "2e"), (".border", "66"))
        },
        "hint.background": elevated,
        "version_control.added": g_add,
        "version_control.modified": g_mod,
        "version_control.deleted": g_del,
        "version_control.renamed": g_mod,
        "version_control.conflict": g_con,
        "version_control.ignored": GIT["ignored"],
        "version_control.word_added": g_add + "5c",
        "version_control.word_deleted": g_del + "5c",
        "players": [
            {"cursor": "#ffffff", "background": POI["mint"], "selection": base["selection"]},
            {"cursor": POI["cyan"], "background": POI["cyan"], "selection": POI["cyan"] + "3d"},
            {"cursor": POI["light_blue"], "background": POI["light_blue"], "selection": POI["light_blue"] + "3d"},
            {"cursor": POI["yellow"], "background": POI["yellow"], "selection": POI["yellow"] + "3d"},
            {"cursor": POI["pink"], "background": POI["pink"], "selection": POI["pink"] + "3d"},
        ],
        "accents": [POI["mint"], POI["cyan"], POI["light_blue"], POI["yellow"], POI["pink"], POI["steel"]],
        "syntax": build_syntax(editor_bg),
    }


def main():
    OUT.mkdir(exist_ok=True)
    themes = []
    for key in ("default", "storm"):
        base = BASES[key]
        for bordered in (False, True):
            name = f"{base['label']} Bordered" if bordered else base["label"]
            themes.append({
                "name": name,
                "appearance": "dark",
                "style": build_style(base, bordered),
            })

    family = {
        "$schema": SCHEMA,
        "name": "Poimandres",
        "author": AUTHOR,
        "themes": themes,
    }
    target = OUT / "poimandres.json"
    target.write_text(json.dumps(family, indent=2, ensure_ascii=False) + "\n")
    for t in themes:
        print(f"themes/poimandres.json: {t['name']}")


if __name__ == "__main__":
    main()
