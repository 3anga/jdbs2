import json

def generatePreviewData(bpm, duration, mapname):
    beat = 60000 / bpm
    beats = []
    for INDEX in range(int(duration / bpm) + 1):
        beats.append(int((beat * INDEX) * 48))
    RESPONSE = {
        "__class": "Actor_Template",
        "WIP": 0,
        "LOWUPDATE": 0,
        "UPDATE_LAYER": 0,
        "PROCEDURAL": 0,
        "STARTPAUSED": 0,
        "FORCEISENVIRONMENT": 0,
        "COMPONENTS": [{
                "__class": "MusicTrackComponent_Template",
                "trackData": {
                    "__class": "MusicTrackData",
                    "structure": {
                        "__class": "MusicTrackStructure",
                        "markers": beats,
                        "signatures": [{
                                "__class": "MusicSignature",
                                "marker": 4,
                                "beats": 4
                            }, {
                                "__class": "MusicSignature",
                                "marker": 12,
                                "beats": 4
                            }
                        ],
                        "sections": [{
                                "__class": "MusicSection",
                                "marker": 8,
                                "sectionType": 0,
                                "comment": ""
                            }, {
                                "__class": "MusicSection",
                                "marker": 16,
                                "sectionType": 0,
                                "comment": ""
                            }
                        ],
                        "startBeat": 0,
                        "endBeat": len(beats),
                        "fadeStartBeat": 0,
                        "useFadeStartBeat": False,
                        "fadeEndBeat": 0,
                        "useFadeEndBeat": False,
                        "videoStartTime": 0,
                        "previewEntry": 0,
                        "previewLoopStart": 0,
                        "previewLoopEnd": len(beats),
                        "volume": 0,
                        "fadeInDuration": 0,
                        "fadeInType": 0,
                        "fadeOutDuration": 0,
                        "fadeOutType": 0
                    },
                    "path": "",
                    "url": f"jmcs://jd-contents/{mapname}/{mapname}_AudioPreview.ogg"
                }
            }
        ]
    }
    return json.dumps(RESPONSE)
