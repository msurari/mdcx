# -*- coding: utf-8 -*-
"""UI translations, batch C (canonical idx 261-420). Keys are canon.json indices."""

T = {
    261: "Test",
    262: "Video directory name:",
    263: "Anti-blocking character:",
    264: "The title format written into the nfo file; it is shown as the video title in Emby. "
         "Full Jinja2 syntax is supported",
    265: "Emby video title:",
    266: "The filename format for local video files; the naming fields are the same as above, "
         "{{ number }} is recommended",
    267: "When naming a video file, the anti-blocking character can be inserted between every character of the name",
    268: "Template preview:",
    269: "After entering a Jinja2 naming template, a sample rendering and the syntax status are shown here.",
    270: "Part naming rules",
    271: "Uppercase, -CD1, -CD2",
    272: "Lowercase, -cd1, -cd2",
    273: "Numeric, -1, -2",
    274: "Parts recognised by default: -CD1｜-PART1｜-HD1｜-1.mp4 "
         "(a filename containing these characters is read for part information)",
    275: "-A.mp4｜.A.mp4｜12A.mp4 (parts ending in a letter, the letter C excluded)",
    276: "Parts allowed:",
    277: "-01.mp4 (parts ending in two digits)",
    278: "-1 abc.mp4 (parts where the number is not at the end)",
    279: "Separators allowed:",
    280: " Space",
    281: "_ Underscore",
    282: ". Dot",
    283: "Separator recognised by default: - hyphen",
    284: "-C.mp4｜.C.mp4｜12C.mp4 (parts ending in the letter C, read as CD3)",
    285: "When checked, -C and .C are read as CD3 and no longer as subtitles",
    286: "Length rules",
    287: "Maximum directory name length:",
    288: "Maximum number of actor names:",
    289: "<p style='line-height:20px'>The maximum number of characters in a directory name (100 is "
         "recommended; Windows may complain about longer ones)<br>\n"
         "                          When the maximum is exceeded the title field is truncated to shorten "
         "the name</p>",
    290: "Maximum filename length:",
    291: "<p style='line-height:20px'>The maximum number of characters in a filename (100 is recommended; "
         "Windows may complain about longer ones)<br>\n"
         "                          When the maximum is exceeded the title field is truncated to shorten "
         "the name</p>",
    292: "When several actors are credited, the maximum number shown in the name. Extra actors are replaced "
         "with the characters below:",
    293: "Mosaic naming rules",
    294: "Adds a version marker after the code when naming. You can also use the moword field to control where "
         "it is added",
    295: "Uncensored:",
    296: "\n"
         "                          <p\n"
         "                          style='line-height:20px'>The leaked-uncensored version: when the video "
         "file path contains \u300c\u6d41\u51fa\u300d or \u300cLEAKED\u300d the file is treated as leaked "
         "uncensored. This character is added after the code in file and directory names to mark it</p>",
    297: "Leaked uncensored:",
    298: "Censored:",
    299: "\n"
         "                          <p\n"
         "                          style='line-height:20px'>The uncensored version: when the video file path "
         "contains \u300c\u65e0\u7801\u300d, \u300c\u7121\u78bc\u300d, \u300c\u7121\u4fee\u6b63\u300d or "
         "\u300cuncensored\u300d the file is treated as uncensored.<br>This character is added after the code "
         "in file and directory names to mark it</p>",
    300: "<p\n"
         "                          style='line-height:20px'>The lossy mosaic-removal version: when the video "
         "file path contains \u300c-uncensored.\u300d, \u300c.restored\u300d, \u300c\u7834\u89e3\u300d, "
         "\u300c\u514b\u7834\u300d or \u300cUMR.\u300d the file is treated as uncensored-restored.<br>\n"
         "                          This character is added after the code in file and directory names to mark "
         "it</p>",
    301: "Uncensored (restored):",
    302: "<p>The censored version: when the video file path contains \u300c\u6709\u7801\u300d or "
         "\u300c\u6709\u78bc\u300d the file is treated as\n"
         "                          censored; this character is added after the code in file and directory names "
         "to mark it</p>",
    303: "Add mosaic naming character:",
    304: "Video directory name",
    305: "Video filename",
    306: "Image naming rules",
    307: "video filename-poster.jpg ",
    308: "video filename-thumb.jpg, video filename-fanart.jpg",
    309: "Trailer naming rules",
    310: "video filename-trailer.mp4 ",
    311: "One \"video name-trailer.mp4\" per video; several are created for multi-part videos",
    312: "Create a \"trailers\" folder in the video directory; multi-part videos share one \"trailer.mp4\"",
    313: "Field naming rules",
    314: "<p>For example moword (a custom uncensored marker) and cnword (subtitle) are shown as: "
         "code-leaked-C<br>\n"
         "                                This only controls the order; the marker must be ticked in its own "
         "place (such as \"Add the 4K character\") to be shown at all</p>",
    315: "Strip the numeric prefix from amateur codes (e.g. 259LUXU-1488 becomes LUXU-1488; keeping it is "
         "recommended)",
    316: "Strip the name in brackets from actor names (e.g. Rio\uff08\u67da\u6728\u30c6\u30a3\u30ca\uff09 "
         "becomes Rio)",
    317: "Code suffix order:",
    318: "Strip the actor name appended to the title (some sites add the actor name at the end of the title; "
         "removing it is recommended)",
    319: "Release date:",
    320: "year: YYYY or YY, month: MM, day: DD; e.g. YY.MM.DD renders as 22.03.20",
    321: "When no actor name exists, these characters are used in place of the actor naming field",
    322: "Unknown actor:",
    323: "For FC2 without an actor, use the seller name as the actor name",
    324: "Quality naming rules",
    325: "Name each quality by the height value of the video resolution",
    326: "Name each quality by the English definition abbreviation",
    327: "<p>Note: qHD=540P, HD=720P/960P, FHD=1080P, QHD=1440P(2K), UHD=4K/8K. Below 540P the height value "
         "is used by default</p>",
    328: "Read the video frame height",
    329: "Use the quality information contained in the path",
    330: "Do not read the resolution",
    331: "How the resolution is obtained:",
    332: "Add the 4K character:",
    333: "Adds 4K after the code when naming (4K only). You can also use the 4K field to control where it "
         "is added",
    334: "Other notes",
    335: "1. Multi-version display:",
    336: "<p>1) Emby supports multi-version display (similar to episodes); this needs:</p><p>The beginning of the "
         "video filename must contain the video directory name. (e.g. SSIS-111/SSIS-111-4K.mp4)\n"
         "                          </p><p>See the rules: <a\n"
         "                          href=\"https://support.emby.media/support/solutions/articles/44001159102-movie-naming\">"
         "<span\n"
         "                          style=\" text-decoration: underline;\n"
         "                          color:#094fd1;\">"
         "https://support.emby.media/support/solutions/articles/44001159102-movie-naming</span></a></p>"
         "<p>2) Part videos are shown as extras by default; to show them as multiple versions the part naming "
         "rule must also be set to \"-1\"</p>",
    337: "Emby part covers need an image for every part, so the image naming rule must be set to "
         "\"video filename-poster.jpg\"",
    338: "2. Part cover display:",
    339: " Translate ",
    340: "Translation engines",
    341: "Translation engines:",
    342: "DeepL and DeepLX are independent options; fill in the matching settings to use them.",
    343: "When several are ticked, one of the ticked engines is picked at random, which lowers the chance of "
         "being blocked",
    344: "LLM translation",
    345: "Example: https://api.openai.com/v1",
    346: "Title prompt:",
    347: "Plot prompt:",
    348: "Prompt template. Available variables: {content} source text, {lang} target language",
    349: "Maximum request rate (/s):",
    350: "Set it according to the limits of the API provider you use",
    351: "Maximum attempts:",
    352: "An API request can fail simply because of temporary rate limiting, so a few retries are fine",
    353: "Title",
    354: "Translate the title with a translation engine",
    355: "Title language:",
    356: "The Chinese translation from the scraped site is preferred; the methods below are used only when the "
         "scraped page has no Chinese.",
    357: "Chinese (simplified)",
    358: "Chinese (traditional)",
    359: "Japanese",
    360: "Translation method:",
    361: "Plot",
    362: "Plot language:",
    363: "When the field language is set to Chinese but only Japanese was scraped, a translation engine can "
         "translate it",
    364: "Translate the plot with a translation engine",
    365: "Show translation source",
    366: "Chinese + Japanese",
    367: "Japanese + Chinese",
    368: "Off",
    369: "Bilingual display:",
    370: "Actors",
    371: "<p style='line-height:20px'>\n"
         "                                Actors for amateur and FC2 codes may be fake names such as "
         "\u300c\u7d20\u4eba\u300d. Ticking \"Use AV-wiki to get actors' real names\" asks AV-wiki\n"
         "                                for the actor's real Japanese name, which can then be translated "
         "with the mapping table!<br>\n"
         "                                Actor names are complicated and cannot simply be run through a "
         "translation engine. The main problems: inaccurate translation, several names per actor, "
         "inconsistent actor names for the same actor across codes, different sites using different "
         "names.<br>\n"
         "                                An actor-name mapping table solves these and keeps scraped actor "
         "names consistent.<br>\n"
         "                                How it works: after a scraped site returns the actor name, the "
         "matching keyword in the mapping table is looked up to map it to an output word.\n"
         "                                <br>\n"
         "                                The actor-name mapping table file is: mapping_actor.xml<br>\n"
         "                                \u00b7\n"
         "                                Windows path: \\config dir\\userdata\\mapping_actor.xml (the "
         "config directory is set in [Settings] - [Other])<br>\n"
         "                                \u00b7 Mac path: /config dir/userdata/mapping_actor.xml<br>\n"
         "                                You can open the file in a text editor and edit it yourself. The "
         "fields in the mapping table mean:<br>\n"
         "                                1. keyword: the match word (a comma before and after each name). "
         "After a site returns an actor name it is matched against the keyword names.<br>\n"
         "                                2. zh_cn/zh_tw/jp: the output words. When a keyword matches an "
         "actor name, the name in the matching language is output.</p>",
    372: "Use AV-wiki to get actors' real names",
    373: "Translate actor names with the actor mapping table",
    374: "Actor language:",
    375: "Tags",
    376: "Mapping table filename: mapping_info.xml. It works like the actor mapping table; see the actor "
         "mapping table for an explanation.",
    377: "Translate tags with the info mapping table",
    378: "Tag language:",
    379: "Series",
    380: "Series language:",
    381: "Translate the series with the info mapping table",
    382: "Studio",
    383: "Studio language:",
    384: "Translate the studio with the info mapping table",
    385: "Publisher",
    386: "Publisher language:",
    387: "Translate the publisher with the info mapping table",
    388: "Director",
    389: "Translate the director with the info mapping table",
    390: " Subtitles ",
    391: "Chinese subtitle character rules",
    392: "Chinese subtitle detection characters:",
    393: "When a video has Chinese subtitles this character is added after the code in file and directory "
         "names to mark it",
    394: "<p\n"
         "                                style='line-height:20px'>When the video file path contains the "
         "characters above the file is treated as having Chinese subtitles; separate several with commas<br>\n"
         "                                In addition, a subtitle file with the same name in the same "
         "directory is looked for, and the nfo tags are checked for a Chinese-subtitle marker</p>",
    395: "Chinese subtitle naming character:",
    396: "Adds the Chinese subtitle naming character after the code. You can also use the cnword field to "
         "control where it is added",
    397: "Add the Chinese subtitle character:",
    398: "Add external subtitles",
    399: "While scraping, if a video has no embedded subtitles and no subtitle file in its directory, a "
         "subtitle is looked up in the subtitle directory and copied",
    400: "Download and unzip the subtitle pack, then enter the path of the subtitle directory",
    401: "Click to download the subtitle pack",
    402: "Subtitle directory:",
    403: "Add subtitles automatically while scraping:",
    404: "Click to check the subtitle status of every video and add subtitles to videos that have none",
    405: "<p\n"
         "                          style='line-height:20px'>When the subtitle directory is empty only the "
         "list of videos without subtitles is checked and counted<br>\n"
         "                          A video already marked as having subtitles (subtitles present, or "
         "Chinese subtitle characters in the name) is not given another subtitle<br>\n"
         "                          After a new external subtitle is added, re-scraping starts automatically "
         "when the re-scrape option is ticked<br>\n"
         "                          A video that already got an external subtitle but has not been re-scraped "
         "yet is also re-scraped automatically<br>\n"
         "                          When the .chs suffix option is ticked, subtitle files are named "
         "video filename.chs.srt</p>",
    406: "Add the .chs suffix to subtitle filenames",
    407: "Re-scrape videos that received a new subtitle when finished",
    408: " Watermark ",
    409: "Custom watermark style",
    410: "<p\n"
         "                          style='line-height:20px'>1. Download and unzip the watermark image pack "
         "(you may also use your own images). The watermark images live at:<br>\n"
         "                          \u00b7 Windows: (the config directory is set in [Settings] - "
         "[Advanced])<br>\n"
         "                          Subtitle watermark: \\config dir\\userdata\\watermark\\sub.png<br>\n"
         "                          Censored watermark: \\config dir\\userdata\\watermark\\youma.png<br>\n"
         "                          Restored watermark: \\config dir\\userdata\\watermark\\umr.png<br>\n"
         "                          Leaked watermark: \\config dir\\userdata\\watermark\\leak.png<br>\n"
         "                          Uncensored watermark: \\config dir\\userdata\\watermark\\wuma.png<br>\n"
         "                          4K watermark: \\config dir\\userdata\\watermark\\4k.png<br>\n"
         "                          8K watermark: \\config dir\\userdata\\watermark\\8k.png<br>\n"
         "                          \u00b7 Mac: (the config directory is set in [Settings] - [Advanced])<br>\n"
         "                          Subtitle watermark: /config dir/userdata/watermark/sub.png<br>\n"
         "                          Censored watermark: /config dir/userdata/watermark/youma.png<br>\n"
         "                          Restored watermark: /config dir/userdata/watermark/umr.png<br>\n"
         "                          Leaked watermark: /config dir/userdata/watermark/leak.png<br>\n"
         "                          Uncensored watermark: /config dir/userdata/watermark/wuma.png<br>\n"
         "                          4K watermark: /config dir/userdata/watermark/4k.png<br>\n"
         "                          8K watermark: /config dir/userdata/watermark/8k.png<br>\n"
         "                          <br>\n"
         "                          2. How watermark images are displayed:<br>\n"
         "                          \u00b7 First the display height of the watermark is computed = cover "
         "height * watermark size setting / 40<br>\n"
         "                          For example with a watermark size of 5 the watermark image is scaled to "
         "5/40 of the cover height<br>\n"
         "                          \u00b7 Then the display width is computed from that height and the "
         "watermark image's aspect ratio<br>\n"
         "                          \u00b7 Finally, according to the watermark types and the first watermark "
         "position set, they are drawn clockwise on the four corners of the cover</p>",
    411: "Click to download the watermark image pack",
    412: "Watermark settings",
    413: "Floating position",
    414: "Fixed single position",
    415: "Fixed separate positions",
    416: "<p\n"
         "                                style='line-height:20px'>Watermarks come in three kinds: subtitle, "
         "mosaic and 4K/8K.<br>\n"
         "                                There are four mosaic watermarks: censored, restored, leaked and "
         "uncensored; one of them is shown according to priority<br>\n"
         "                                Mosaic watermark priority: censored > restored > leaked > "
         "uncensored<br>\n"
         "                                Example: if the video is a leaked version<br>\n"
         "                                \u00b7 when both leaked and uncensored are ticked, the leaked "
         "watermark is shown<br>\n"
         "                                \u00b7 when leaked is not ticked and uncensored is, the uncensored "
         "watermark is shown<br>\n"
         "                                \u00b7 when neither leaked nor uncensored is ticked, no watermark is "
         "shown</p>",
    417: "Watermark types:",
    418: "Images to watermark:",
    419: "Subtitle",
    420: "Restored",
}
