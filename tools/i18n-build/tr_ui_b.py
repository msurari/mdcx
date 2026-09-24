# -*- coding: utf-8 -*-
"""UI translations, batch B (canonical idx 139-260). Keys are canon.json indices."""

T = {
    139: "<p style='line-height:20px'>\u26a0\ufe0f Files to keep: set what to keep or update under "
         "Settings > Download > Keep old files or<br>\n"
         "Download.<br>\n"
         "\u26a0\ufe0f Skipped files: create an empty file named skip in a video directory to skip that "
         "directory and its subdirectories automatically (works in every mode)<br>\n"
         "\u26a0\ufe0f Moving files: nothing is moved on failure; on success the update mode rules apply<br>\n"
         "\u26a0\ufe0f Renaming files: set whether to rename under \"Rename files after a successful scrape\"; "
         "the naming rules are the same as [Naming] - [Video filename]</p>",
    140: "Rename files after a successful scrape",
    141: "On success, rename the file following [Naming] - [Video naming rules] - [Video filename]",
    142: "On success, keep using the original filename",
    143: "Multi-threaded scraping",
    144: "javdb delay (seconds)",
    145: "A javdb delay lowers the chance of being blocked by javdb; a random value between delay/2 and delay is used.",
    146: "Number of threads",
    147: "Thread interval (seconds)",
    148: "Create a symlink or hardlink in the output directory after a successful scrape",
    149: "Create symlink",
    150: "<span>For NAS and hard-drive users. Local users can organise files freely.<br>Note: only with this "
         "option do the \"Move files after success\" / \"Move files after failure\" settings below apply</span>",
    151: "Create hardlink",
    152: "<span>For cloud drive users. Scraped data stays local, Emby loads fast and the cloud drive is barely "
         "touched.<br>Note: on Windows the success output directory must be on a local disk (system limit)</span>",
    153: "<span>For PT users. Scraped data is stored separately on the same disk and does not affect your ratio."
         "<br>Note: on Mac choose symlinks and keep the output directory on the same disk (hardlinks have "
         "permission issues)</span>",
    154: "Note: symlinks and hardlinks do not move or rename the original video file; only the link file is moved and renamed",
    155: " Scrape sites ",
    156: "Sites scraped by code type",
    157: "Uncensored code:",
    158: "Anime / hentai:",
    159: "<span>When [Site preference] - [Specific site] is set to mdtv or hdouban, or the file path contains "
         "\u300c\u56fd\u4ea7\u300d or \u300c\u9ebb\u8c46\u300d, the sites above are used automatically to scrape "
         "Chinese domestic codes</span>",
    160: "Example: 259LUXU-1111",
    161: "Example: FC2-111111",
    162: "Example: sexart.11.11.11",
    163: "Western code:",
    164: "Example: 111111-111, 111111_111, n1111, HEYZO-1111, SMD-111",
    165: "<p>When [Site preference] - [Specific site] is set to getchu, dmm or getchu_dmm, or the file path "
         "contains \u300c\u91cc\u756a\u300d or \u300c\u52a8\u6f2b\u300d, getchu_dmm (combined) is used "
         "automatically</p>",
    166: "<p>When [Site preference] - [Specific site] is set to mywife, or the file path contains mywife, mywife "
         "is used automatically (Mywife code format: Mywife No.1230)</p>",
    167: "Example: MIDE-111, and any code not matching the types below",
    168: "Amateur code:",
    169: "Censored code:",
    170: "FC2 code:",
    171: "Chinese domestic code:",
    172: "When selected, automatic type detection is skipped and every code is scraped with the site list of the "
         "chosen type. Select \"Auto detect\" to restore the default behaviour.",
    173: "Auto detect",
    174: "Censored",
    175: "Uncensored",
    176: "Amateur",
    177: "Western",
    178: "Chinese domestic",
    179: "Lock scrape type:",
    180: "When selected, automatic type detection is skipped and every code is scraped with the site list of the chosen type.",
    181: "Per-field scrape sites",
    182: "Release date:",
    183: "Original title:",
    184: "Cover (large):",
    185: "Score:",
    186: "Studio:",
    187: "Stills:",
    188: "Wanted count:",
    189: "Publisher:",
    190: "Original plot:",
    191: "Cover (small):",
    192: "Actresses:",
    193: "Trailer:",
    194: "All actors:",
    195: "<p>Note: for a given field, leaving the scrape site empty means data from any site already fetched is "
         "used; otherwise the intersection of the field's sites and the sites of that code type is used in order."
         "</p><p>For example, if the title is set to theporndb,dmm,javdb,fc2ppvdb, censored to dmm,javdb,javbus "
         "and FC2 to fc2,fc2ppvdb</p><p>then for a censored title the title data of dmm and then javdb is used; "
         "for an FC2 title the title data of fc2ppvdb is used</p>",
    196: "Site preference",
    197: "Specific site",
    198: "Scrapes with the site set for each field; the fields come from several sites. More complete fields.",
    199: "With a specific site, every code is scraped from that site only!",
    200: "Fields first",
    201: "Scrapes with the sites set for the code type; the fields come from a single site. A bit faster.",
    202: "Speed first",
    203: "\u26a0\ufe0f To download stills and trailers choose \"Fields first\" or \"Specific site\"! "
         "\"Speed first\" gives incomplete information!",
    204: "Try all images",
    205: "When a fields-first image download fails, keep trying the other image candidates",
    206: "Nothing scraped? Look here!",
    207: "\u26a0\ufe0f Note!!! These settings only apply with \"Fields first\" selected!!!",
    208: " Download ",
    209: "Download",
    210: "Fanart",
    211: "Stills",
    212: "Trailer",
    213: "An image download failure is not treated as a scrape failure",
    214: " Sometimes the image has been deleted from the source site, in which case the download fails",
    215: "Do not crop censored covers, copy the thumbnail as is",
    216: " Censored covers can be cropped; tick this if you do not want cropping",
    217: "For censored poster (portrait) images, pick the best automatically by size",
    218: " Censored only: direct download / image search / right-side crop, best one wins",
    219: "Do not crop uncensored covers, copy the thumbnail as is",
    220: " On uncensored covers the face position varies; cropping by hand or copying as is is recommended",
    221: "Do not crop western covers, copy the thumbnail as is",
    222: " On western covers the face position varies; cropping by hand or copying as is is recommended",
    223: "Do not crop FC2 covers, copy the thumbnail as is",
    224: " On FC2 covers the face position varies; cropping by hand or copying as is is recommended",
    225: "Do not crop Chinese domestic covers, copy the thumbnail as is",
    226: " On Chinese domestic covers the face position varies; cropping by hand or copying as is is recommended",
    227: "Do not verify the file size when downloading trailers",
    228: " Sometimes a site returns something unexpected and the check makes the trailer download fail",
    229: "<p style='line-height:20px'>Cover: poster — when the Emby view is set to cover, the list page shows "
         "poster (portrait);<br>\n"
         "                                Thumbnail: thumb — when the Emby view is set to thumbnail, the list "
         "page shows Thumb (landscape);<br>\n"
         "                                Fanart: fanart — shown as the background image on the Emby detail page "
         "(copying the thumbnail produces the fanart);<br>\n"
         "                                Stills: extrafanart — shown as a background slideshow on the Emby detail "
         "page (it starts rotating after about 50s);<br>\n"
         "                                Trailer: trailer — the trailer can be played from the Emby detail "
         "page;<br>\n"
         "                                nfo: holds the title, plot, tags and so on, shown on the Emby detail "
         "page.</p>",
    230: "Keep old files",
    231: "Stills copy",
    232: "Theme video",
    233: "<p style='line-height:20px'>When checked, local files are used (if present) and not downloaded "
         "again.<br>\n"
         "                          \u26a0\ufe0f Note: when unchecked the local old files are DELETED and "
         "downloaded again according to the download items set above!</p>",
    234: "Create theme video",
    235: "<p style='line-height:20px'>Copies the trailer into the backdrops folder under the video; when you "
         "browse that title in Emby<br>\n"
         "                          the trailer plays as a background video.<br>\n"
         "                          Turn theme videos on: Emby Settings - Display - Theme videos - On (fine on "
         "desktop, not recommended on phones where it plays full screen...)</p>",
    236: "Use the trailer as theme video",
    237: "Add all theme videos",
    238: "Delete all theme videos",
    239: "Create stills copy",
    240: "Copy an extra set of still images into a folder",
    241: "<p style='line-height:20px'>In Emby, still images are shown as background and cannot be browsed "
         "manually.<br>\n"
         "                          To browse stills by hand in Emby, copy them into a separate folder and set "
         "the library type to \"Home videos and photos\"<br>\n"
         "                          Use a name other than \"extrafanart\". When the folder name is empty or "
         "\"extrafanart\", no copy folder is created.<br>\n"
         "                          Note: enter the folder name only, not a full path!</p>",
    242: "Add all stills copies",
    243: "Delete all stills copies",
    244: "Download high-resolution images",
    245: "Searches the Amazon Japan site for high-resolution cover images; strict verification compares every "
         "Amazon result by similarity, which can lower the search success rate.",
    246: "Use Amazon to find high-resolution cover images",
    247: "Affects only the Amazon high-resolution cover search, not ordinary image downloads",
    248: "Strictly verify Amazon images",
    249: "Compare every Amazon result by image similarity",
    250: "Skip the preliminary poster size check",
    251: "Do not skip Amazon because the current poster is >=400KB",
    252: "Show stills",
    253: "<p style='line-height:20px'>Copies the stills into the behind the scenes folder under the video; while "
         "browsing in Emby\n"
         "                          the stills are shown as extras below the detail page.<br></p>",
    254: "Show stills as extras",
    255: "Copy stills for all videos",
    256: "Delete all copied stills",
    257: " Naming ",
    258: "Video naming rules",
    259: "<p\n"
         "                                style='line-height:20px'>When a scrape succeeds, a video directory is "
         "created for that video and moved to the success output directory.<br>\n"
         "                                The naming template uses standard Jinja2 syntax: a field is written "
         "{{ field name }} and a condition {% if field name %}...{% endif %}.<br>\n"
         "                                Example: {{ number }}{% if studio %} [{{ studio }}]{% endif %} "
         "{{ originaltitle }} {{ definition }}<br>\n"
         "                                Symbols in the template are not removed when a field is empty; wrap a "
         "whole section in a Jinja2 if to avoid empty [] or stray separators.<br>\n"
         "                                Common fields: {{ number }} code, {{ title }} title, "
         "{{ originaltitle }} original title, {{ actor }} actors, {{ studio }} studio, {{ series }} series, "
         "{{ release }} release date, {{ definition }} definition, {{ filename }} original filename.<br>\n"
         "                                Other fields: all_actor (all actors), first_actor (first actor), "
         "letters (code prefix), first_letter (first character of the code), outline (plot), director, publisher, "
         "year, runtime, mosaic (censored/uncensored), cnword (subtitle marker), moword (version marker), "
         "wanted (wanted count), score, four_k (4K/8K/UHD marker).<br>\n"
         "                                Notes:<br>\n"
         "                                1. A / in the template creates a subdirectory; a / inside a field "
         "value is turned into -; Jinja2 only produces text;<br>\n"
         "                                2. An empty video directory name means no video directory is "
         "created;<br>\n"
         "                                3. When the name is too long, long fields such as plot and title are "
         "shortened first and key fields such as the code are kept.</p>",
    260: "Video filename:",
}
