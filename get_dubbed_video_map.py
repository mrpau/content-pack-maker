#!/usr/bin/env python
"""
Get a video map based on the language argument from the Khan Academy spreadsheet and output it as a json file.

Usage:
  get_dubbed_video_map <lang> [options]
  get_dubbed_video_map -h | --help

Options:
-h --help                       Show this screen
--lang=lang                     The language to download dubbed videos for.
--videolang=lang                The language of dubbed videos, i.e. what dubbed video mapping language to use.
--out=outdir                    The path to place the final content pack. 

"""
import logging
import sys

from docopt import docopt


DUBBED_VIDEO_MAP_RAW = None
DUBBED_VIDEO_MAP = None
def get_dubbed_video_map(lang_code=None, reload=None, force=False):
    """
    Stores a key per language.  Value is a dictionary between video_id and (dubbed) youtube_id
    """
    global DUBBED_VIDEO_MAP, DUBBED_VIDEO_MAP_RAW, DUBBED_VIDEOS_MAPPING_FILEPATH

    reload = (reload is None and force) or reload  # default of reload is force

    if DUBBED_VIDEO_MAP is None or reload:
        try:
            if not os.path.exists(DUBBED_VIDEOS_MAPPING_FILEPATH) or force:
                try:
                    # Generate from the spreadsheet
                    logging.debug("Generating dubbed video mappings.")
                    call_command("generate_dubbed_video_mappings", force=force)
                except Exception as e:
                    logging.debug("Error generating dubbed video mappings: %s" % e)
                    if not os.path.exists(DUBBED_VIDEOS_MAPPING_FILEPATH):
                        # Unrecoverable error, so raise
                        raise
                    elif DUBBED_VIDEO_MAP:
                        # No need to recover--allow the downstream dude to catch the error.
                        raise
                    else:
                        # We can recover by NOT forcing reload.
                        logging.warn("%s" % e)

            DUBBED_VIDEO_MAP_RAW = softload_json(DUBBED_VIDEOS_MAPPING_FILEPATH, raises=True)
        except Exception as e:
            logging.info("Failed to get dubbed video mappings (%s); defaulting to empty.")
            DUBBED_VIDEO_MAP_RAW = {}  # setting this will avoid triggering reload on every call

        # Remove any empty items, as they break things
        if "" in DUBBED_VIDEO_MAP_RAW:
            del DUBBED_VIDEO_MAP_RAW[""]

        DUBBED_VIDEO_MAP = {}
        for lang_name, video_map in DUBBED_VIDEO_MAP_RAW.iteritems():
            if lang_name:
                logging.debug("Adding dubbed video map entry for %s (name=%s)" % (get_langcode_map(lang_name), lang_name))
                DUBBED_VIDEO_MAP[get_langcode_map(lang_name)] = video_map

    return DUBBED_VIDEO_MAP.get(lang_code, {}) if lang_code else DUBBED_VIDEO_MAP


def main(argv):
    args = docopt(__doc__)
    
    lang = args["<lang>"]
#    out = Path(args["--out"]) if args['--out'] else Path.cwd() / "{lang}.zip".format(lang=lang)

    logging.basicConfig(level=logging.INFO)
    logging.debug("==> main lang=%s" % lang)


if __name__ == "__main__":
    logging.warn("==> args %s" % sys.argv[1])
    main(sys.argv[1:])
