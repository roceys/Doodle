# -*- coding: utf-8 -*-

from tornado.web import HTTPError

from doodle.core.models.article import ArticleHitCount
from doodle.core.models.tag import Tag, TagArticle
from doodle.core.models.comment import ArticleComments

from ..base_handler import UserHandler


class TagArticlesHandler(UserHandler):
    def get(self, tag_name):
        cursor = self.get_cursor()

        if not Tag.exists(tag_name):
            raise HTTPError(404)

        articles, next_cursor = TagArticle.get_articles(tag_name, cursor)
        if articles:
            article_ids = [article.id for article in articles]
            hit_counts = ArticleHitCount.get_by_ids(article_ids)
            replies_dict = ArticleComments.get_comment_count_of_articles(article_ids)
        else:
            hit_counts = replies_dict = {}
            next_cursor = None

        self.render('web/tag_articles.html', {
            'title': u'标签《%s》' % tag_name,
            'page': 'tag_articles',
            'cursor': cursor,
            'next_cursor': next_cursor,
            'tag_name': tag_name,
            'articles': articles,
            'hit_counts': hit_counts,
            'replies_dict': replies_dict
        })

    def compute_etag(self):
        return