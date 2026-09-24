"""Short descriptions shown when hovering a control.

Zak's request (2026-09-24): the app has far more functions than he knew about,
mostly because the labels were Chinese. A one-line description on hover makes
every function discoverable without changing any behaviour.

Design notes
------------
* Keyed on **objectName**. NOTE the widget names have no ``_clicked`` suffix --
  that suffix belongs to the handler method, not the widget (``pushButton_about``
  is the button; ``pushButton_about_clicked`` is the slot).
* Applied **after** the window is built (``apply_tooltips(window)``). It only
  calls ``setToolTip``, so layout, geometry, signals and config values are
  untouched. Purely additive.
* **The six ``pushButton_tips_*`` buttons are deliberately absent.** Their
  tooltip IS the help body -- ``_show_tips(self.Ui.pushButton_tips_X.toolTip())``
  renders it in a popup. A one-line description there would destroy real help
  text. Their long HTML bodies are translated separately.
* The entries that also appear in ``controllers/main_window/init.py`` replace
  short **Chinese** tooltips with English, which is part of the interface
  translation. Everything else is a new description where none existed.
* Text must stay SHORT -- it renders as a hover bubble, not a paragraph.
"""

from typing import Dict

#: objectName -> one-line description of what the control does.
TOOLTIPS: Dict[str, str] = {
    # --- main page: scrape control -------------------------------------------------
    "pushButton_start_cap":
        "Start scraping every video in the scrape folder. Becomes Stop while running.",
    "pushButton_start_cap2":
        "Start scraping every video in the scrape folder. Becomes Stop while running.",
    "pushButton_scraper_failed_list":
        "Re-scrape only the videos in the failed list.",
    "pushButton_view_failed_list":
        "Show or hide the list of failed tasks.",
    "pushButton_success_list_clear":
        "Clear the success list. No files are touched.",
    "pushButton_success_list_save":
        "Save the success list to a text file.",
    "pushButton_view_success_file":
        "Open the folder of the selected video.",
    "pushButton_show_pic_actor":
        "Open the selected actor's photo.",
    "pushButton_save_failed_list":
        "Save the failed list to a text file.",
    "pushButton_show_hide_logs":
        "Show or hide the log panel.",
    "pushButton_tree_clear":
        "Clear the results list.",

    # --- main page: single-file scrape ---------------------------------------------
    "pushButton_select_file":
        "Choose one video file to scrape on its own.",
    "pushButton_select_file_clear_info":
        "Clear the single-file form.",
    "pushButton_start_single_file":
        "Scrape the single file entered above.",

    # --- left navigation -----------------------------------------------------------
    "pushButton_main":
        "Main page: scrape control, progress and results.",
    "pushButton_log":
        "Log page: live scrape, web, source and data logs.",
    "pushButton_net":
        "Network page: test whether each scraping site is reachable.",
    "pushButton_tool":
        "Tools page: one-off utilities that do not scrape.",
    "pushButton_setting":
        "Settings page.",
    "pushButton_about":
        "Built-in manual.",

    # --- window controls -----------------------------------------------------------
    "pushButton_min":
        "Minimise the window.",
    "pushButton_close":
        "Close the window.",

    # --- main page: small icons ----------------------------------------------------
    "pushButton_right_menu":
        "Open the right-click menu.",
    "pushButton_play":
        "Play the video.",
    "pushButton_open_folder":
        "Open the folder.",
    "pushButton_open_nfo":
        "Edit the NFO file.",
    "pushButton_open_pic":
        "Open the image.",

    # --- network page --------------------------------------------------------------
    "pushButton_check_net":
        "Test every configured site and report which ones respond.",
    "pushButton_check_javbus_cookie":
        "Check whether the JavBus cookie is still valid.",
    "pushButton_check_javdb_cookie":
        "Check whether the JavDb cookie is still valid.",
    "pushButton_check_fc2ppvdb_cookie":
        "Check whether the FC2PPVDB cookie is still valid.",

    # --- tools page: file housekeeping ---------------------------------------------
    "pushButton_check_and_clean_files":
        "Scan the scrape folder and clean out files that are not videos.",
    "pushButton_move_mp4":
        "Move videos and subtitles out of subfolders into the scrape folder.",
    "pushButton_creat_symlink":
        "Create softlinks for everything on the mounted cloud drive.",

    # --- tools page: subtitles -----------------------------------------------------
    "pushButton_add_sub_for_all_video":
        "Check every video for subtitles and add the missing ones.",

    # --- tools page: theme videos --------------------------------------------------
    "pushButton_add_all_theme_videos":
        "Add a theme video to every folder that lacks one.",
    "pushButton_del_all_theme_videos":
        "Remove theme videos from all folders.",

    # --- tools page: stills --------------------------------------------------------
    "pushButton_add_all_extrafanart_copy":
        "Copy stills into an extrafanart folder for every video.",
    "pushButton_del_all_extrafanart_copy":
        "Remove the extrafanart copies.",
    "pushButton_add_all_extras":
        "Copy each video's stills next to it.",
    "pushButton_del_all_extras":
        "Remove the copied stills.",

    # --- tools page: media-server actor metadata -----------------------------------
    "pushButton_add_actor_pic":
        "Fill in missing actor photos in Emby / Jellyfin.",
    "pushButton_add_actor_info":
        "Fill in missing actor information in Emby / Jellyfin.",
    "pushButton_add_actor_pic_kodi":
        "Fill in missing actor photos for Kodi / Plex / Jvedio.",
    "pushButton_del_actor_folder":
        "Delete every .actors folder.",

    # --- tools page: library checks ------------------------------------------------
    "pushButton_find_missing_number":
        "Compare an actor's full code list against your library and list what is missing.",

    # --- folder pickers ------------------------------------------------------------
    "pushButton_select_media_folder":
        "Choose the folder to work on.",
    "pushButton_select_media_folder_setting_page":
        "Choose the main scrape folder.",
    "pushButton_select_subtitle_folder":
        "Choose the folder holding your subtitle files.",
    "pushButton_select_softlink_folder":
        "Choose the softlink destination folder.",
    "pushButton_select_netdisk_path":
        "Choose the mounted cloud-drive path.",
    "pushButton_select_localdisk_path":
        "Choose the local disk path.",
    "pushButton_select_actor_photo_folder":
        "Choose the folder holding actor photos.",
    "pushButton_select_actor_info_db":
        "Choose the actor information database file.",
    "pushButton_select_thumb":
        "Choose the image to crop.",
    "pushButton_select_config_folder":
        "Choose where config files are kept.",
    "pushButton_select_failed_folder":
        "Choose the folder for failed videos.",
    "pushButton_select_sucess_folder":
        "Choose the folder for successful videos.",
    "pushButton_select_local_library":
        "Choose the local library folder.",

    # --- settings page -------------------------------------------------------------
    "pushButton_save_config":
        "Save settings to the current config file.",
    "pushButton_save_new_config":
        "Save settings to a new config file.",
    "pushButton_init_config":
        "Reset every setting to its default.",

    # --- NFO editor -----------------------------------------------------------------
    "pushButton_field_tips_nfo":
        "Explain what each NFO field means.",
    "pushButton_nfo_save":
        "Save the edited NFO.",
    "pushButton_nfo_close":
        "Close without saving.",

    # --- crop window ----------------------------------------------------------------
    "pushButton_cut":
        "Crop the image.",
    "pushButton_cut_close":
        "Crop the image and close.",
    "pushButton_to_cut_2":
        "Confirm the crop.",
    "pushButton_select_cutrange":
        "Drag to select the crop area.",

    # --- help dialogs --------------------------------------------------------------
    "pushButton_scrape_note":
        "What to do when a video will not scrape.",
    "pushButton_show_tips_close":
        "Close.",
    "pushButton_success_list_close":
        "Close.",
}


#: The six buttons whose tooltip is the help body itself. Listed so a test can
#: assert we never overwrite them with a one-liner.
HELP_BODY_BUTTONS = (
    "pushButton_tips_normal_mode",
    "pushButton_tips_sort_mode",
    "pushButton_tips_update_mode",
    "pushButton_tips_read_mode",
    "pushButton_tips_soft",
    "pushButton_tips_hard",
)


def apply_tooltips(window) -> int:
    """Set the hover description on every control we have text for.

    Walks ``window``'s widgets and matches on objectName. Returns how many
    tooltips were set, so a test can assert none were silently lost to a
    renamed control.
    """
    from PyQt6.QtWidgets import QWidget

    applied = 0
    for widget in window.findChildren(QWidget):
        name = widget.objectName()
        if not name or name not in TOOLTIPS:
            continue
        if name in HELP_BODY_BUTTONS:
            continue
        widget.setToolTip(TOOLTIPS[name])
        applied += 1
    return applied
