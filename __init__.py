from pyvod import Collection
from os.path import join, dirname, basename
from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename
from ovos_workshop.frameworks.playback import CommonPlayMediaType, CommonPlayPlaybackType, \
    CommonPlayMatchConfidence
from ovos_workshop.skills.video_collection import VideoCollectionSkill
from ovos_workshop.skills.common_play import common_play_search


class SovietWaveSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("SovietWave")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.default_image = join(dirname(__file__), "ui", "sovietwave_logo.png")
        self.skill_logo = join(dirname(__file__), "ui", "sovietwave_icon.png")
        self.skill_icon = join(dirname(__file__), "ui", "sovietwave_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "sovietwave_logo.png")
        self.supported_media = [CommonPlayMediaType.GENERIC,
                                CommonPlayMediaType.VIDEO,
                                CommonPlayMediaType.RADIO,
                                CommonPlayMediaType.MUSIC]
        self.settings["max_duration"] = -1
        path = join(dirname(__file__), "res", "NewSovietWave.jsondb")
        # load video catalog
        self.media_collection = Collection("NewSovietWave",
                                           logo=self.skill_logo,
                                           db_path=path)

    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # common play - video catalog template skill methods
    def match_media_type(self, phrase, media_type):
        score = 0

        if self.voc_match(phrase,
                          "video") or media_type == CommonPlayMediaType.VIDEO:
            score += 5

        if self.voc_match(phrase,
                          "radio") or media_type == CommonPlayMediaType.RADIO:
            score += 10

        if self.voc_match(phrase,
                          "music") or media_type == CommonPlayMediaType.MUSIC:
            score += 10

        if self.voc_match(phrase, "sovietwave"):
            score += 30

        return score

    # NOTE: video collection catalog search is handled in CPS_search method
    # use the decorator to add extra search functions
    @common_play_search()
    def search_sovietwave(self, phrase, media_type):
        if self.voc_match(phrase, "sovietwave"):
            score = 80
            if media_type == CommonPlayMediaType.RADIO or \
                    self.voc_match(phrase, "radio"):
                score = 100
            yield {
                "match_confidence": score,
                "media_type": CommonPlayMediaType.RADIO,
                "playback": CommonPlayPlaybackType.AUDIO,
                "skill_icon": self.skill_icon,
                "skill_logo": self.skill_logo,
                "bg_image": self.default_bg,
                "image": self.default_image,
                "author": self.name,
                "title": "SovietWave Radio",
                "url": "https://listen5.myradio24.com/sovietwave"
            }


def create_skill():
    return SovietWaveSkill()
