from ovos_utils.log import LOG
from json_database import JsonStorageXDG
from ovos_skills_manager.appstores.andlo import AndloSkillList
from ovos_skills_manager.appstores.mycroft_marketplace import \
    MycroftMarketplace
from ovos_skills_manager.appstores.pling import Pling
from ovos_skills_manager.appstores.ovos import OVOSstore
from ovos_skills_manager.exceptions import UnknownAppstore


class OVOSSkillsManager:
    def __init__(self):
        self.config = JsonStorageXDG("OVOS-SkillsManager")
        if "appstores" not in self.config:
            self.config["appstores"] = {
                "ovos": {
                    "active": True,
                    "url": "https://github.com/OpenVoiceOS/OVOS-appstore",
                    "parse_github": False,
                    "priority": 1},
                "mycroft_marketplace": {
                    "active": False,
                    "url": "https://market.mycroft.ai/",
                    "parse_github": False,
                    "priority": 5},
                "pling": {
                    "active": False,
                    "url": "https://apps.plasma-bigscreen.org/",
                    "parse_github": False,
                    "priority": 10},
                "andlo_skill_list": {
                    "active": False,
                    "url": "https://andlo.gitbook.io/mycroft-skills-list/",
                    "parse_github": False,
                    "priority": 100}
            }
            self.save_config()
        self._threads = []

    def get_active_appstores(self):
        stores = {}
        for appstore_name in self.config["appstores"]:
            if self.config["appstores"][appstore_name]["active"]:
                stores[appstore_name] = self.get_appstore(appstore_name)
        return stores

    def get_appstore(self, name):
        if self.config["appstores"][name]["active"]:
            parse_github = self.config["appstores"][name]["parse_github"]
            store = self.name_to_appstore(name)
            return store(parse_github=parse_github)
        return None

    @staticmethod
    def name_to_appstore(name):
        if name in ["pling", "bigscreen"]:
            return Pling
        elif name in ["mycroft", "mycroft_marketplace"]:
            return MycroftMarketplace
        elif name in ["andlo", "andlo_skill_list"]:
            return AndloSkillList
        elif name in ["ovos", "ovos_appstore", "ovos_marketplace"]:
            return OVOSstore
        else:
            raise UnknownAppstore

    def save_config(self):
        self.config.store()

    def clear_cache(self, appstore_name=None):
        if appstore_name:
            self.get_appstore(appstore_name).clear_cache()
        else:
            for appstore in self.appstores:
                appstore.clear_cache()

    def validate_appstore_name(self, appstore):
        if appstore in ["pling", "bigscreen"]:
            appstore = "pling"
        elif appstore in ["mycroft", "mycroft_marketplace"]:
            appstore = "mycroft_marketplace"
        elif appstore in ["andlo", "andlo_skill_list"]:
            appstore = "andlo_skill_list"
        elif appstore in ["ovos", "ovos_appstore", "ovos_marketplace"]:
            appstore = "ovos"
        elif appstore not in self.config["appstores"]:
            raise UnknownAppstore
        return appstore

    def enable_appstore(self, appstore):
        appstore = self.validate_appstore_name(appstore)
        self.config["appstores"][appstore]["active"] = True

    def set_appstore_priority(self, appstore, priority):
        appstore = self.validate_appstore_name(appstore)
        self.config["appstores"][appstore]["priority"] = priority

    def disable_appstore(self, appstore):
        appstore = self.validate_appstore_name(appstore)
        self.config["appstores"][appstore]["active"] = False

    def sync_appstores(self, merge=False, new_only=True, threaded=False):
        stores = self.get_active_appstores()
        for appstore_name in stores:
            LOG.info("Syncing skills from " + appstore_name)
            store = stores[appstore_name]
            if threaded:
                t = store.sync_skills_list_threaded(merge, new_only)
                self._threads.append(t)
            else:
                store.sync_skills_list(merge, new_only)

    @property
    def total_skills(self):
        return sum([s.total_skills() for s in self.appstores])

    @property
    def appstores(self):
        stores = []
        for s in self.config["appstores"]:
            store = self.get_appstore(s)
            if not store:
                continue
            priority = self.config["appstores"][s]["priority"]
            stores.append((store, priority))
        return [s[0] for s in sorted(stores, key=lambda k: k[1])]

    def search_skills(self, name, as_json=False, fuzzy=True, thresh=0.85,
                      ignore_case=True):
        for store in self.appstores:
            for skill in store.search_skills(name, as_json, fuzzy,  thresh,
                                             ignore_case):
                yield skill

    def search_skills_by_name(self, name, as_json=False,
                              fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            for skill in store.search_skills_by_name(name, as_json, fuzzy,
                                                     thresh, ignore_case):
                yield skill

    def search_skills_by_url(self, url, as_json=False):
        for store in self.appstores:
            for skill in store.search_skills_by_url(url, as_json):
                yield skill

    def search_skills_by_category(self, category, as_json=False,
                                  fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            for skill in store.search_skills_by_category(category, as_json,
                                                         fuzzy, thresh,
                                                         ignore_case):
                yield skill

    def search_skills_by_author(self, authorname, as_json=False,
                                fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            for skill in store.search_skills_by_author(authorname, as_json,
                                                       fuzzy, thresh,
                                                       ignore_case):
                yield skill

    def search_skills_by_tag(self, tag, as_json=False,
                             fuzzy=True, thresh=0.85, ignore_case=True):
        for store in self.appstores:
            for skill in store.search_skills_by_tag(tag, as_json, fuzzy,
                                                    thresh, ignore_case):
                yield skill

    def search_skills_by_description(self, value, as_json=False,
                                     fuzzy=True, thresh=0.85,
                                     ignore_case=True):
        for store in self.appstores:
            for skill in store.search_skills_by_description(value, as_json,
                                                            fuzzy, thresh,
                                                            ignore_case):
                yield skill

    def __iter__(self):
        for store in self.appstores:
            for skill in store:
                yield skill
