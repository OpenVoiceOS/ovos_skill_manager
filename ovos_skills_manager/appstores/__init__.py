from json_database import JsonDatabaseXDG
from json_database.search import Query
from ovos_utils import create_daemon
from ovos_utils.log import LOG
from os.path import join, dirname, isfile
from ovos_skills_manager import SkillEntry
import shutil
from os import remove


class AbstractAppstore:
    def __init__(self, name, parse_github=False):
        self.name = name
        self.db = JsonDatabaseXDG(name)
        self.parse_github = parse_github
        self.bootstrap()

    def bootstrap(self):
        base_db = join(dirname(dirname(__file__)), "res", "bootstrap_o",
                       self.db.name + ".jsondb")
        if not len(self.db):
            LOG.info("Bootstrapping {database}, this might take a "
                     "while!".format(database=self.name))
            if isfile(base_db):
                LOG.debug("Bootstrapping from bundled skill list")
                shutil.copyfile(base_db, self.db.path)
                self.db.reset()
            else:
                LOG.debug("Downloading skill list")
                self.sync_skills_list()

    def clear_cache(self):
        if isfile(self.db.path):
            LOG.debug("Removing appstore cache " + self.db.path)
            remove(self.db.path)
            self.db.reset()

    def get_skills_list(self, skiplist=None):
        return []

    def sync_skills_list(self, merge=False, new_only=False):
        skiplist = None
        if new_only:
            skiplist = [s["url"] for s in self.db if s.get("url")]

        for skill in self.get_skills_list(skiplist=skiplist):
            LOG.info("Synced skill: " + skill.url)

            for old_skill in self.search_skills_by_url(skill.url,
                                                       as_json=True):
                item_id = self.db.get_item_id(old_skill)
                if merge:
                    LOG.debug("Merging skill data")
                    self.db.merge_item(skill.json, item_id)
                else:
                    LOG.debug("Removing old skill from db")
                    self.db.remove_item(item_id)
            if not merge:
                LOG.debug("Adding new skill to db")
                self.db.add_item(skill.json)
            self.db.commit()

    def sync_skills_list_threaded(self, merge=False, new_only=False):
        return create_daemon(self.sync_skills_list, (merge, new_only))

    def total_skills(self):
        return len(self.db)

    def search_skills_by_name(self, name, as_json=False,
                              fuzzy=True, thresh=0.85, ignore_case=True):
        query = Query(self.db)
        query.contains_value('skillname', name, fuzzy, thresh, ignore_case)
        results = query.result
        for idx in range(0, len(results)):
            if "appstore" not in results[idx]:
                results[idx]["appstore"] = self.name
        if as_json:
            return query.result
        return [SkillEntry.from_json(s, False) for s in results]

    def search_skills_by_url(self, url, as_json=False):
        query = Query(self.db)
        query.equal("url", url)
        results = query.result
        for idx in range(0, len(results)):
            if "appstore" not in results[idx]:
                results[idx]["appstore"] = self.name
        if as_json:
            return query.result
        return [SkillEntry.from_json(s, False) for s in results]

    def search_skills_by_category(self, category, as_json=False,
                                  fuzzy=True, thresh=0.85, ignore_case=True):
        query = Query(self.db)
        query.contains_value('category', category, fuzzy, thresh)
        results = query.result
        for idx in range(0, len(results)):
            if "appstore" not in results[idx]:
                results[idx]["appstore"] = self.name
        if as_json:
            return query.result
        return [SkillEntry.from_json(s, False) for s in results]

    def search_skills_by_author(self, authorname, as_json=False,
                                fuzzy=True, thresh=0.85, ignore_case=True):
        query = Query(self.db)
        query.value_contains_token('authorname', authorname,
                                   fuzzy, thresh, ignore_case)
        results = query.result
        for idx in range(0, len(results)):
            if "appstore" not in results[idx]:
                results[idx]["appstore"] = self.name
        if as_json:
            return query.result
        return [SkillEntry.from_json(s, False) for s in results]

    def search_skills_by_tag(self, tag, as_json=False,
                             fuzzy=True, thresh=0.85, ignore_case=True):
        query = Query(self.db)
        query.contains_value('tags', tag, fuzzy, thresh, ignore_case)
        results = query.result
        for idx in range(0, len(results)):
            if "appstore" not in results[idx]:
                results[idx]["appstore"] = self.name
        if as_json:
            return query.result
        return [SkillEntry.from_json(s, False) for s in results]

    def search_skills_by_description(self, value, as_json=False,
                                     fuzzy=True, thresh=0.85,
                                     ignore_case=True):
        query = Query(self.db)
        query.value_contains_token('description', value,
                                   fuzzy, thresh, ignore_case)
        results = query.result
        for idx in range(0, len(results)):
            if "appstore" not in results[idx]:
                results[idx]["appstore"] = self.name
        if as_json:
            return query.result
        return [SkillEntry.from_json(s, False) for s in results]

    def search_skills(self, query, as_json=False, fuzzy=True, thresh=0.85,
                      ignore_case=True):
        # check for exact url matches
        url_skills = self.search_skills_by_url(query, as_json)
        if url_skills:
            return url_skills

        # check for query in name
        name_skills = self.search_skills_by_name(query, as_json, fuzzy,
                                                 thresh, ignore_case)
        if name_skills:
            return name_skills

        # check for author
        author_skills = self.search_skills_by_author(query, as_json, fuzzy,
                                                     thresh, ignore_case)
        if author_skills:
            return author_skills

        # check in tags and description
        tag_skills = self.search_skills_by_tag(query, as_json, fuzzy,
                                               thresh, ignore_case)
        desc_skills = self.search_skills_by_description(query, as_json, fuzzy,
                                                        thresh, ignore_case)
        res = desc_skills + tag_skills
        if res:
            return res

        # last chance... very generic search
        author_skills = self.search_skills_by_author(query, as_json, fuzzy,
                                                     thresh - 0.25,
                                                     ignore_case)
        cat_skills = self.search_skills_by_category(query, as_json, fuzzy,
                                                    thresh, ignore_case)
        return author_skills + cat_skills

    def print(self):
        self.db.print()

    def __iter__(self):
        for s in self.db:
            yield SkillEntry.from_json(s, parse_github=False)
